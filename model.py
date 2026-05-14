from dotenv import load_dotenv
import os
from typing import Optional, List

from pydantic import BaseModel, Field
from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import ChatPromptTemplate
from langchain.messages import HumanMessage, SystemMessage

load_dotenv()


# =========================================================
# USER SEARCH REQUEST
# =========================================================

class JobSearchRequest(BaseModel):
    role: str
    description: Optional[str] = None
    experience_level: str
    years_of_experience: Optional[int] = None
    job_type: str
    work_mode: str
    location: Optional[str] = None
    salary_expectation_usd: Optional[int] = None
    preferred_technologies: Optional[List[str]] = None
    visa_sponsorship_required: Optional[bool] = False
    industries: Optional[List[str]] = None


# =========================================================
# JOB RESULT MODEL
# =========================================================

class JobListing(BaseModel):
    title: str = Field(description="Job title")

    company: str = Field(description="Company name")

    location: str = Field(description="Job location")

    work_mode: str = Field(
        description="Remote, Hybrid, Onsite"
    )

    salary_range: Optional[str] = Field(
        default=None,
        description="Salary range if available"
    )

    technologies: List[str] = Field(
        description="Required technologies"
    )

    experience_required: Optional[str] = Field(
        default=None,
        description="Required experience"
    )

    employment_type: str = Field(
        description="Full-time, Contract, etc"
    )

    description: str = Field(
        description="Short job summary"
    )

    apply_url: str = Field(
        description="Application link"
    )

    match_score: float = Field(
        description="AI matching score between 0 and 1"
    )


class JobSearchResponse(BaseModel):
    jobs: List[JobListing]


# =========================================================
# MODEL
# =========================================================

model = ChatOpenRouter(
    model=os.environ["OPENROUTER_MODEL"],
    temperature=0.2,
    max_tokens=2000
)

job_parser_model = model.with_structured_output(
    JobSearchRequest
)

job_result_model = model.with_structured_output(
    JobSearchResponse
)


# =========================================================
# EXTRACT USER REQUIREMENTS
# =========================================================

extract_prompt = ChatPromptTemplate.from_messages([
    (
        SystemMessage(
            """
            You are an AI recruitment assistant.

            Extract structured job requirements
            from the user input.

            Return clean JSON.
            """
        )
    ),
    (
        HumanMessage(
            """
            USER INPUT:
            {user_input}
            """
        )
    )
])


# =========================================================
# GENERATE JOB RESULTS
# =========================================================

jobs_prompt = ChatPromptTemplate.from_messages([
    (
        SystemMessage(
            """
            You are an AI job recommendation engine.

            Generate realistic online job listings
            based on the user's profile.

            Focus on:
            - remote opportunities
            - European and global companies
            - realistic salaries
            - modern tech stacks
            - high relevance matching

            Return structured job results.
            """
        )
    ),
    (
        HumanMessage(
            """
            USER PROFILE:
            {profile}
            """
        )
    )
])


# =========================================================
# FUNCTIONS
# =========================================================

def extract_job_requirements(
    user_input: str
):
    chain = extract_prompt | job_parser_model

    return chain.invoke({
        "user_input": user_input
    })


def generate_job_matches(
    profile: JobSearchRequest
):
    chain = jobs_prompt | job_result_model

    return chain.invoke({
        "profile": profile.model_dump_json(indent=2)
    })
