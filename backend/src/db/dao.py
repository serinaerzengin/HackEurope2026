from src.types.cases import (
    CaseType,
    ProblemDifficulty,
    ProblemComplexity,
    CaseDSAProblem,
    CaseSoftwareDesignProblem,
)


def fetch_cases_from_db(
    case_type: CaseType,
) -> list[CaseDSAProblem | CaseSoftwareDesignProblem]:
    """
    Fetches interview preparation cases from the database.
    Args:
        case_type (CaseType): The type of cases to fetch.
    Returns:
        list: A list of interview preparation cases.
    """
    match case_type:
        case CaseType.DSA:
            # Fetch DSA cases from the database and return them as a list of ExtractDSASchema
            return [
                CaseDSAProblem(
                    title="Valid Parentheses",
                    description="Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.",
                    difficulty=ProblemDifficulty.EASY,
                    examples=[
                        'Input: s = "()"\nOutput: true',
                        'Input: s = "()[]{}"\nOutput: true',
                        'Input: s = "(]"\nOutput: false',
                    ],
                ),
                CaseDSAProblem(
                    title="LRU Cache",
                    description="Design a data structure that follows the constraints of a Least Recently Used (LRU) cache.",
                    difficulty=ProblemDifficulty.MEDIUM,
                    examples=[
                        'Input\n["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"]\n[[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]]\nOutput\n[null, null, null, 1, null, -1, null, -1, 3, 4]',
                    ],
                ),
            ]
        case CaseType.SYSTEM_DESIGN:
            # Fetch software design cases from the database and return them as a list of ExtractDesignSchema
            return [
                CaseSoftwareDesignProblem(
    name="Design a Todo List Service",
    description="Design a simple Todo List service where users can create tasks, update task details, mark tasks as completed, delete tasks, and view their task list. The service should support basic filtering (all, active, completed) and simple due dates.",
    complexity=ProblemComplexity.EASY,
    role=["SWE", "SDE", "Backend"],
    resources=[
        "https://www.youtube.com/watch?v=7Vf-H9q1uxU",
        "https://www.youtube.com/watch?v=1K0xQGbEAFA",
    ],
),
         CaseSoftwareDesignProblem(
    name="Design a Todo List Service",
    description="Design a simple Todo List service where users can create tasks, update task details, mark tasks as completed, delete tasks, and view their task list. The service should support basic filtering (all, active, completed) and simple due dates.",
    complexity=ProblemComplexity.EASY,
    role=["SWE", "SDE", "Backend"],
    resources=[
        "https://www.youtube.com/watch?v=7Vf-H9q1uxU",
        "https://www.youtube.com/watch?v=1K0xQGbEAFA",
    ],
),
            ]

            
        case _:
            raise ValueError(f"Invalid case type: {case_type}")
