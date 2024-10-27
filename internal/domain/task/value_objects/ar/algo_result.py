from pydantic import BaseModel
from desbordante.ar import ARStrings, ArIDs


class ArModel(BaseModel):
    @classmethod
    def from_ar(cls, ar: ARStrings):
        return cls(confidence=ar.confidence, left=ar.left, right=ar.right)

    @classmethod
    def from_ar_ids(cls, ar_id: ArIDs):
        return cls(confidence=ar_id.confidence, left=ar_id.left, right=ar_id.right)

    confidence: float
    left: list[str]
    right: list[str]


class ArAlgoResult(BaseModel):
    ars: list[ArModel]
    ar_ids: list[ArModel]
