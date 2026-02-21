"""
This module is responsible for crawling web pages and extracting content using the Firecrawl API.
"""

import requests
from firecrawl import Firecrawl
from src.configuration import FIRECRAWL_API_KEY
from src.types.cases import ExtractDSASchema, ExtractDesignSchema

FIRECRAWL_URL = "https://api.firecrawl.dev/v2/scrape"


def crawl_webpage(url: str) -> dict:
    """
    Crawls the given URL using the Firecrawl API and returns the extracted content as json dictionary.
    Args:
        url (str): The URL of the web page to crawl.
    Returns:
        dict: The extracted content from the web page.
    """
    payload = {
        "url": url,
        "onlyMainContent": False,
        "maxAge": 172800000,
        "parsers": ["pdf"],
        "formats": ["markdown"],
    }

    headers = {
        "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.post(FIRECRAWL_URL, json=payload, headers=headers)

    return response.json()


app = Firecrawl(api_key=FIRECRAWL_API_KEY)


def extract_interview_questions(url: str) -> ExtractDSASchema:
    results = app.agent(
        prompt=f"Extract all interview DSA questions from {url}",
        schema=ExtractDSASchema,
    )
    return results


def extract_software_design_problems(url: str) -> ExtractDesignSchema:
    results = app.agent(
        prompt=f"Extract all software design interview questions from {url}",
        schema=ExtractDesignSchema,
    )
    return results


if __name__ == "__main__":
    DSA_URL = "github.com/ombharatiya/FAANG-Coding-Interview-Questions/tree/main"
    SYSTEM_DESIGN_URL = "https://github.com/ombharatiya/FAANG-Coding-Interview-Questions/blob/main/SYSTEM_DESIGN_INTERVIEW.md"
    response = crawl_webpage(DSA_URL)

    agentic_dsa_extraction = extract_interview_questions(DSA_URL)
    agentic_design_extraction = extract_software_design_problems(SYSTEM_DESIGN_URL)

    # Save the extracted questions to a file or database for further processing
    with open("../data/extracted_dsa_questions.json", "w") as f:
        f.write(agentic_dsa_extraction.model_dump_json(indent=4))

    with open("../data/extracted_design_questions.json", "w") as f:
        f.write(agentic_design_extraction.model_dump_json(indent=4))

    with open("../data/raw_crawled_content.json", "w") as f:
        f.write(str(response))
