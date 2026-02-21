from src.types.cases import CaseType, ExtractDSASchema, ExtractDesignSchema


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
                        {
                            "title": "Two Sum",
                            "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
                            "difficulty": "EASY",
                            "examples": [
                                "Input: nums = [2,7,11,15], target = 9\nOutput: [0,1]\nExplanation: Because nums[0] + nums[1] == 9, we return [0, 1]."
                            ],
                            "constraints": [
                                "2 <= nums.length <= 10^4",
                                "-10^9 <= nums[i] <= 10^9",
                                "-10^9 <= target <= 10^9",
                            ],
                            "url": None,
                            "time_complexity": "O(n)",
                            "space_complexity": "O(n)",
                        }
                    ],
                )
            ]
        case CaseType.SYSTEM_DESIGN:
            # Fetch software design cases from the database and return them as a list of ExtractDesignSchema
            return [
                ExtractDesignSchema(
                    company_name="Google",
                    interview_questions=[
                        {
                            "name": "Design a URL Shortener",
                            "description": "Design a URL shortening service like bit.ly.",
                            "complexity": "MEDIUM",
                            "role": ["SWE", "Backend"],
                            "resources": [
                                "https://en.wikipedia.org/wiki/URL_shortening"
                            ],
                        }
                    ],
                )
            ]
        case _:
            raise ValueError(f"Invalid case type: {case_type}")
