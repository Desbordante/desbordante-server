# References, thanks max-pfeiffer:
# https://github.com/max-pfeiffer/python-poetry/blob/main/build/Dockerfile
# https://github.com/max-pfeiffer/uvicorn-poetry/blob/main/build/Dockerfile
# https://github.com/max-pfeiffer/uvicorn-poetry/blob/main/examples/fast_api_multistage_build/Dockerfile

# References: using official Python images
# https://hub.docker.com/_/python
ARG OFFICIAL_PYTHON_IMAGE=python:3.11.5-slim-bullseye
FROM ${OFFICIAL_PYTHON_IMAGE} as poetry-install-build-stage
ARG POETRY_VERSION=1.6.1

# References:
# https://pip.pypa.io/en/stable/topics/caching/#avoiding-caching
# https://pip.pypa.io/en/stable/cli/pip/?highlight=PIP_NO_CACHE_DIR#cmdoption-no-cache-dir
# https://pip.pypa.io/en/stable/cli/pip/?highlight=PIP_DISABLE_PIP_VERSION_CHECK#cmdoption-disable-pip-version-check
# https://pip.pypa.io/en/stable/cli/pip/?highlight=PIP_DEFAULT_TIMEOUT#cmdoption-timeout
# https://pip.pypa.io/en/stable/topics/configuration/#environment-variables
# https://python-poetry.org/docs/#installation
# https://refspecs.linuxfoundation.org/FHS_2.3/fhs-2.3.html#OPTADDONAPPLICATIONSOFTWAREPACKAGES

ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=${POETRY_VERSION} \
    POETRY_HOME="/opt/poetry"

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        build-essential

# https://python-poetry.org/docs/#installing-manually
RUN python -m venv ${POETRY_HOME}
RUN ${POETRY_HOME}/bin/pip install -U pip setuptools
RUN ${POETRY_HOME}/bin/pip install "poetry==${POETRY_VERSION}"

FROM ${OFFICIAL_PYTHON_IMAGE} as server-setup-build-stage

ENV PATH="/opt/poetry/bin:$PATH"

COPY --from=poetry-install-build-stage /opt/poetry /opt/poetry/
ARG APPLICATION_SERVER_PORT=8000

    # https://docs.python.org/3/using/cmdline.html#envvar-PYTHONUNBUFFERED
ENV PYTHONUNBUFFERED=1 \
    # https://docs.python.org/3/using/cmdline.html#envvar-PYTHONDONTWRITEBYTECODE
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/application_root \
    # https://python-poetry.org/docs/configuration/#virtualenvsin-project
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_CACHE_DIR="/application_root/.cache" \
    VIRTUAL_ENVIRONMENT_PATH="/application_root/.venv" \
    APPLICATION_SERVER_PORT=$APPLICATION_SERVER_PORT

# Adding the virtual environment to PATH in order to "activate" it.
# https://docs.python.org/3/library/venv.html#how-venvs-work
ENV PATH="$VIRTUAL_ENVIRONMENT_PATH/bin:$PATH"

# Principle of least privilege: create a new user for running the application
RUN groupadd -g 1001 python_application && \
    useradd -r -u 1001 -g python_application python_application

# Set the WORKDIR to the application root.
# https://www.uvicorn.org/settings/#development
# https://docs.docker.com/engine/reference/builder/#workdir
WORKDIR ${PYTHONPATH}
RUN chown python_application:python_application ${PYTHONPATH}

# Create cache directory and set permissions because user 1001 has no home
# and poetry cache directory.
# https://python-poetry.org/docs/configuration/#cache-directory
RUN mkdir ${POETRY_CACHE_DIR} && chown python_application:python_application ${POETRY_CACHE_DIR}

# Document the exposed port
# https://docs.docker.com/engine/reference/builder/#expose
EXPOSE ${APPLICATION_SERVER_PORT}

# Use the unpriveledged user to run the application
USER 1001

# Run the uvicorn application server.
CMD exec uvicorn --workers 1 --host 0.0.0.0 --port $APPLICATION_SERVER_PORT app.main:app

FROM server-setup-build-stage as install-dependencies-build-stage
# install [tool.poetry.dependencies]
# this will install virtual environment into /.venv because of POETRY_VIRTUALENVS_IN_PROJECT=true
# see: https://python-poetry.org/docs/configuration/#virtualenvsin-project
COPY ./poetry.lock ./pyproject.toml /application_root/
RUN poetry install --no-interaction --no-root --without dev

FROM server-setup-build-stage as production-image

# Copy virtual environment
COPY --chown=python_application:python_application --from=install-dependencies-build-stage /application_root/.venv /application_root/.venv

# Copy application files
COPY --chown=python_application:python_application /app /application_root/app/
