from dataclasses import dataclass

@dataclass(frozen=True)
class Policy:
    issue_age: int
    gender: str
    risk_class: str
    term_duration: int
    face_amount: float