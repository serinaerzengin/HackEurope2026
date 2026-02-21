from enum import StrEnum, auto
from pydantic import BaseModel


class CaseType(StrEnum):
    DSA = auto()
    SYSTEM_DESIGN = auto()
    BEHAVIORAL = auto()


class ProblemDifficulty(StrEnum):
    EASY = auto()
    MEDIUM = auto()
    HARD = auto()


class ProblemComplexity(StrEnum):
    EASY = auto()
    MEDIUM = auto()
    HIGH = auto()
    VERY_HIGH = auto()


class CaseDSAProblem(BaseModel):
    title: str
    description: str
    difficulty: ProblemDifficulty
    examples: list[str] = []
    constraints: list[str] = []
    url: str | None = None
    difficulty: ProblemDifficulty
    time_complexity: str | None = None
    space_complexity: str | None = None


class CaseSoftwareDesignProblem(BaseModel):
    name: str
    description: str | None = None
    """Generate a detailed description of the software design problem, including the system requirements, constraints, and any specific components or features that need to be designed."""
    complexity: ProblemComplexity = ProblemComplexity.MEDIUM
    role: list[str] = []  # SWE, SDE, Backend, Frontend, Fullstack, etc.
    resources: list[str] = []  # URLs or references for further reading


class ExtractDSASchema(BaseModel):
    company_name: str
    interview_questions: list[CaseDSAProblem]


class ExtractDesignSchema(BaseModel):
    company_name: str
    interview_questions: list[CaseSoftwareDesignProblem]
