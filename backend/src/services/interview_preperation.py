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
    case_type = CaseType(task_type.upper())
    cases = fetch_cases_from_db(case_type)
    # TODO: Implement the logic to filter and recommend cases based on the company name and job description using the LLM service. For now, we are returning all cases of the specified type from the database.
    return cases
