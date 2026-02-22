from typing import Any

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from src.types.cases import CaseType
from src.db.dao import fetch_cases_from_db
from src.configuration import OPENAI_API_KEY

# Lightweight, reusable chain to keep latency low
_llm = ChatOpenAI(
    api_key=OPENAI_API_KEY, model="gpt-4o-mini", temperature=0, timeout=10
)
_prompt = ChatPromptTemplate.from_template(
    """
You are configuring a mock technical interviewer. Craft a concise system prompt (max 150 words) that:
- Sets a friendly, professional, coaching tone.
- References the company {company} and key needs from the job description.
- Highlights up to three focus areas inferred from: {job_description}
- You are going to test the user on the following cases: {cases}.
- Choose one of the cases and describe the task for the user to solve in a clear and engaging way, as you would present it during an interview. Make sure to include any relevant details from the case to set the context for the candidate.

Go through each case and identify the key skills being tested, then weave those into the system prompt to guide the interviewer's questioning style. For example, if a case tests dynamic programming, the prompt might say "Ask questions that probe for dynamic programming insights." If another case tests system design, the prompt might add "Encourage the candidate to think through system design trade-offs."
Respond with only the system prompt text.
    """
)
_system_prompt_chain = _prompt | _llm | StrOutputParser()


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

    system_prompt = _system_prompt_chain.invoke(
        input={
            "company": company,
            "job_description": job_description,
            "cases": cases,
        }
    )
    print(f"Generated system prompt: {system_prompt}")
    return system_prompt.strip()


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
