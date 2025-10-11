from pydantic import BaseModel, Field
from agents import Agent

HOW_MANY_SEARCHES = 3

INSTRUCTIONS = f"""You are a helpful research assistant. You will be provided with:
1. A research query
2. A list of 3 clarifying questions that were asked to the user
3. The user's responses to those questions

Based on the original query, the questions, and the user's responses, come up with a set of web searches to perform to best answer the query. 

CRITICAL: You MUST output exactly {HOW_MANY_SEARCHES} search terms. Do not output more or fewer than {HOW_MANY_SEARCHES} searches.

The input will be in this format:
Query: [the original research query]
Questions and Responses:
1. [Question 1] - Response: [User's answer]
2. [Question 2] - Response: [User's answer]  
3. [Question 3] - Response: [User's answer]"""

# Use Pydantic to define the Schema of our response - this is known as "Structured Outputs"
# With massive thanks to student Wes C. for discovering and fixing a nasty bug with this!

class WebSearchItem(BaseModel):
    reason: str = Field(description="Your reasoning for why this search is important to the query.")

    query: str = Field(description="The search term to use for the web search.")


class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem] = Field(description="A list of web searches to perform to best answer the query.")


planner_agent = Agent(
    name="PlannerAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=WebSearchPlan,
)