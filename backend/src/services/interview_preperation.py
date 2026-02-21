from src.types.cases import CaseType
from src.db.dao import fetch_cases_from_db


def generate_system_prompt(company: str, job_description: str, cases: list) -> str:
    """
    Generates a system prompt for the interview preparation tasks based on the company name and job description.
    Args:
        company (str): The name of the company to tailor the system prompt for.
        job_description (str): The job description to analyze for creating the system prompt.
    Returns:
        str: A generated system prompt for the interview preparation tasks.
    """
    # TODO Do some LLM call to generate a more personalized system prompt based on the company name and job description. For now, we are returning a generic system prompt.
    # LLM prompt template

    return f"""
    You are a senior software engineer conducting a technical interview. 
    You are friendly, professional, and encouraging. 
    You ask clarifying questions, give hints when the candidate is stuck, 
    and evaluate their problem-solving approach. 
    The specific interview task will be provided in the conversational context — 
    always refer to that task during the interview. 
    Keep your responses concise and conversational.
    """


def recommend_case(company: str, job_description: str, task_type: str = "dsa") -> list:
    """
    Recommends interview preparation cases based on the company name, job description, and task type (either "dsa" for data structures and algorithms or "design" for software design problems).
    Args:
        company (str): The name of the company to tailor the recommendations for.
        job_description (str): The job description to analyze for creating interview preparation tasks.
        task_type (str): The type of tasks to recommend, either "dsa" for data structures and algorithms or "design" for software design problems. Default is "dsa".
    Returns:
        list: A list of recommended interview preparation cases.
    """

    # Return a list of recommended cases
    case_type = CaseType.DSA
    match task_type.lower():
        case "dsa":
            case_type = CaseType.DSA
        case "design":
            case_type = CaseType.SYSTEM_DESIGN
        case _:
            raise ValueError(f"Unknown task type: {task_type}")
    cases = fetch_cases_from_db(case_type)

    # Flatten the list of cases from the database results
    flattened_cases = []
    for case_schema in cases:
        if hasattr(case_schema, "interview_questions"):
            flattened_cases.extend(case_schema.interview_questions)

    # TODO: Implement the logic to filter and recommend cases based on the company name and job description using the LLM service. For now, we are returning all cases of the specified type from the database.
    return cases
