from pydantic import BaseModel, Field
from agents import Agent

class CriticFeedback(BaseModel):
    missing_topics: list[str] = Field(
        description="Important topics or perspectives missing from the report"
    )
    weak_sections: list[str] = Field(
        description="Sections that lack depth, clarity, or evidence"
    )
    suggested_searches: list[str] = Field(
        description="Concrete search queries to improve the report"
    )

INSTRUCTIONS = (
    "You are a critical research reviewer. You will be given a detailed research report.\n"
    "Your task is to:\n"
    "1. Identify important missing topics or perspectives\n"
    "2. Point out weak or underdeveloped sections\n"
    "3. Suggest specific follow-up web searches to strengthen the report\n\n"
    "Be concise, analytical, and constructive."
)

critic_agent = Agent(
    name="CriticAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=CriticFeedback,
)
