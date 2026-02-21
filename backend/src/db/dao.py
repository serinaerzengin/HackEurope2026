from src.types.cases import (
    CaseType,
    ExtractDSASchema,
    ExtractDesignSchema,
    ProblemDifficulty,
    ProblemComplexity,
    CaseDSAProblem,
    CaseSoftwareDesignProblem,
)


def fetch_cases_from_db(
    case_type: CaseType,
) -> list[ExtractDSASchema | ExtractDesignSchema]:
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
                ExtractDSASchema(
                    company_name="Google",
                    interview_questions=[
                        CaseDSAProblem(
                            title="Two Sum",
                            description="Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
                            difficulty=ProblemDifficulty.EASY,
                            examples=[
                                "Input: nums = [2,7,11,15], target = 9\nOutput: [0,1]\nExplanation: Because nums[0] + nums[1] == 9, we return [0, 1].",
                            ],
                        ),
                        CaseDSAProblem(
                            title="Valid Parentheses",
                            description="Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.",
                            difficulty=ProblemDifficulty.EASY,
                            examples=[
                                "Input: s = \"()\"\nOutput: true",
                                "Input: s = \"()[]{}\"\nOutput: true",
                                "Input: s = \"(]\"\nOutput: false",
                            ],
                        ),
                        CaseDSAProblem(
                            title="LRU Cache",
                            description="Design a data structure that follows the constraints of a Least Recently Used (LRU) cache.",
                            difficulty=ProblemDifficulty.MEDIUM,
                            examples=[
                                "Input\n[\"LRUCache\", \"put\", \"put\", \"get\", \"put\", \"get\", \"put\", \"get\", \"get\", \"get\"]\n[[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]]\nOutput\n[null, null, null, 1, null, -1, null, -1, 3, 4]",
                            ],
                        ),
                    ],
                )
            ]
        case CaseType.SYSTEM_DESIGN:
            # Fetch software design cases from the database and return them as a list of ExtractDesignSchema
            return [
                ExtractDesignSchema(
                    company_name="Google",
                    interview_questions=[
                        CaseSoftwareDesignProblem(
                            name="Design a URL Shortener",
                            description="Design a URL shortening service like bit.ly. The service should take a long URL and return a shortened version of it. The shortened URL should redirect to the original long URL when accessed.",
                            complexity=ProblemComplexity.MEDIUM,
                            role=["SWE", "SDE", "Backend"],
                            resources=[
                                "https://www.youtube.com/watch?v=QjYq5uYbY8w",
                                "https://www.youtube.com/watch?v=HqP9rJQZt3k",
                                "https://www.youtube.com/watch?v=0sTQeXoXKjE",
                            ],
                        ),
                        CaseSoftwareDesignProblem(
                            name="Design a Pastebin",
                            description="Design a Pastebin like service where users can paste text and get a unique URL to share it. The service should support expiration times, syntax highlighting, and custom URLs.",
                            complexity=ProblemComplexity.MEDIUM,
                            role=["SWE", "SDE", "Backend"],
                            resources=[
                                "https://www.youtube.com/watch?v=joDQuyGWueE",
                                "https://www.youtube.com/watch?v=Ks9fS2_uI6M",
                            ],
                        ),
                    ],
                )
            ]
        case _:
            raise ValueError(f"Invalid case type: {case_type}")
