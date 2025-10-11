from pydantic import BaseModel, Field
from agents import Agent

INSTRUCTIONS = (
    "You are a product manager who likes to understand the pain point of the users. You will be provided with user query. Based on the query, ask the user 3 clarifying questions to learn more about their pain points and guage what is it that they are really looking for. Ask them exactly 3 questions that you think would provide the most insight."
)

class Question(BaseModel):
    reason: str = Field(description="Reason why this question is important")

    question: str = Field(description="The question to be asked to the user")

class Questions(BaseModel):
    searches: list[Question] = Field(description="A list of questions to guage the users requirement.")


product_manager_agent = Agent(
    name="Product Manager",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=Questions,
)