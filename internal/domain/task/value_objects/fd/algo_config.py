from typing import Literal, Annotated, Union
from pydantic import Field
from internal.domain.common import OptionalModel
from internal.domain.task.value_objects.fd.algo_name import FdAlgoName
from internal.domain.task.value_objects.fd.algo_descriptions import descriptions


class BaseFdConfig(OptionalModel):
    __non_optional_fields__ = {
        "algo_name",
    }


class AidConfig(BaseFdConfig):
    algo_name: Literal[FdAlgoName.Aid]

    max_lhs: Annotated[int, Field(ge=1, le=10, description=descriptions["max_lhs"])]


class DFDConfig(BaseFdConfig):
    algo_name: Literal[FdAlgoName.DFD]

    max_lhs: Annotated[int, Field(ge=1, le=10, description=descriptions["max_lhs"])]
    is_null_equal_null: Annotated[
        bool, Field(description=descriptions["is_null_equal_null"])
    ]
    threads: Annotated[int, Field(ge=1, le=8, description=descriptions["threads"])]


class DepminerConfig(BaseFdConfig):
    algo_name: Literal[FdAlgoName.Depminer]

    max_lhs: Annotated[int, Field(ge=1, le=10, description=descriptions["max_lhs"])]
    is_null_equal_null: Annotated[
        bool, Field(description=descriptions["is_null_equal_null"])
    ]


class FDepConfig(BaseFdConfig):
    algo_name: Literal[FdAlgoName.FDep]

    max_lhs: Annotated[int, Field(ge=1, le=10, description=descriptions["max_lhs"])]


class FUNConfig(BaseFdConfig):
    algo_name: Literal[FdAlgoName.FUN]

    max_lhs: Annotated[int, Field(ge=1, le=10, description=descriptions["max_lhs"])]
    is_null_equal_null: Annotated[
        bool, Field(description=descriptions["is_null_equal_null"])
    ]


class FastFDsConfig(BaseFdConfig):
    algo_name: Literal[FdAlgoName.FastFDs]

    max_lhs: Annotated[int, Field(ge=1, le=10, description=descriptions["max_lhs"])]
    is_null_equal_null: Annotated[
        bool, Field(description=descriptions["is_null_equal_null"])
    ]
    threads: Annotated[int, Field(ge=1, le=8, description=descriptions["threads"])]


class FdMineConfig(BaseFdConfig):
    algo_name: Literal[FdAlgoName.FdMine]

    max_lhs: Annotated[int, Field(ge=1, le=10, description=descriptions["max_lhs"])]
    is_null_equal_null: Annotated[
        bool, Field(description=descriptions["is_null_equal_null"])
    ]


class HyFDConfig(BaseFdConfig):
    algo_name: Literal[FdAlgoName.HyFD]

    max_lhs: Annotated[int, Field(ge=1, le=10, description=descriptions["max_lhs"])]
    is_null_equal_null: Annotated[
        bool, Field(description=descriptions["is_null_equal_null"])
    ]


class PFDTaneConfig(BaseFdConfig):
    algo_name: Literal[FdAlgoName.PFDTane]

    max_lhs: Annotated[int, Field(ge=1, le=10, description=descriptions["max_lhs"])]
    is_null_equal_null: Annotated[
        bool, Field(description=descriptions["is_null_equal_null"])
    ]
    error: Annotated[float, Field(ge=0, le=1, description=descriptions["error"])]
    error_measure: Annotated[
        str,
        Literal["per_tuple", "per_value"],
        Field(description=descriptions["error_measure"]),
    ]


class PyroConfig(BaseFdConfig):
    algo_name: Literal[FdAlgoName.Pyro]

    max_lhs: Annotated[int, Field(ge=1, le=10, description=descriptions["max_lhs"])]
    is_null_equal_null: Annotated[
        bool, Field(description=descriptions["is_null_equal_null"])
    ]
    error: Annotated[float, Field(ge=0, le=1, description=descriptions["error"])]
    threads: Annotated[int, Field(ge=1, le=8, description=descriptions["threads"])]
    seed: Annotated[int, Field(description=descriptions["seed"])]


class TaneConfig(BaseFdConfig):
    algo_name: Literal[FdAlgoName.Tane]

    max_lhs: Annotated[int, Field(ge=1, le=10, description=descriptions["max_lhs"])]
    is_null_equal_null: Annotated[
        bool, Field(description=descriptions["is_null_equal_null"])
    ]
    error: Annotated[float, Field(ge=0, le=1, description=descriptions["error"])]


OneOfFdAlgoConfig = Annotated[
    Union[
        AidConfig,
        DFDConfig,
        DepminerConfig,
        FDepConfig,
        FUNConfig,
        FastFDsConfig,
        FdMineConfig,
        HyFDConfig,
        PFDTaneConfig,
        PyroConfig,
        TaneConfig,
    ],
    Field(discriminator="algo_name"),
]
