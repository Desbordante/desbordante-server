import pytest
from pydantic import ValidationError

from internal.domain.common import OptionalModel


class OptionalModelWithoutRequiredFields(OptionalModel):
    implicitly_optional_field: str
    clearly_optional_field: str | None = None


@pytest.mark.parametrize(
    "kwargs, expected_implicitly, expected_clearly",
    [
        ({}, None, None),
        ({"implicitly_optional_field": "value"}, "value", None),
        ({"clearly_optional_field": "value"}, None, "value"),
        (
            {"implicitly_optional_field": "value", "clearly_optional_field": "value"},
            "value",
            "value",
        ),
        (
            {"implicitly_optional_field": "value", "clearly_optional_field": None},
            "value",
            None,
        ),
    ],
)
def test_model_initialization(kwargs, expected_implicitly, expected_clearly):
    model = OptionalModelWithoutRequiredFields(**kwargs)

    assert model.implicitly_optional_field == expected_implicitly
    assert model.clearly_optional_field == expected_clearly


class OptionalModelWithRequiredFields(OptionalModel):
    __non_optional_fields__ = {
        "non_optional_field",
    }

    non_optional_field: str
    optional_field: str


@pytest.mark.parametrize(
    "kwargs, expected_non_optional_field, expected_optional_field, should_fail",
    [
        ({}, None, None, True),
        ({"non_optional_field": "value"}, "value", None, False),
        ({"optional_field": "value"}, None, "value", True),
        (
            {"non_optional_field": "value", "optional_field": "value"},
            "value",
            "value",
            False,
        ),
        ({"non_optional_field": None, "optional_field": None}, None, None, True),
    ],
)
def test_model_with_non_optional_fields_initialization(
    kwargs, expected_non_optional_field, expected_optional_field, should_fail
):
    if should_fail:
        with pytest.raises(ValidationError):
            OptionalModelWithRequiredFields(**kwargs)
    else:
        model = OptionalModelWithRequiredFields(**kwargs)
        assert model.non_optional_field == expected_non_optional_field
        assert model.optional_field == expected_optional_field
