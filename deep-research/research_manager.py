"""
Research Manager Module

This module provides the ResearchManager class that orchestrates the deep research process,
including question generation, search planning, execution, and report generation.
"""

import asyncio
from typing import AsyncGenerator, List, Optional

from agents import Runner, trace, gen_trace_id
from search_agent import search_agent
from planner_agent import planner_agent, WebSearchItem, WebSearchPlan
from writer_agent import writer_agent, ReportData
from email_agent import email_agent
from product_manager_agent import product_manager_agent


class ResearchManager:
    """
    Orchestrates the deep research process from query to final report.
    
    The research process follows these steps:
    1. Generate clarifying questions (optional)
    2. Plan web searches based on query and responses
    3. Execute searches in parallel
    4. Generate comprehensive report
    5. Send email notification
    """

    def __init__(self):
        """Initialize the ResearchManager."""
        pass

    async def run(self, query: str) -> AsyncGenerator[str, None]:
        """
        Run the complete deep research process with interactive question collection.
        
        Args:
            query: The research topic or question
            
        Yields:
            Status updates and the final report
        """
        trace_id = gen_trace_id()
        with trace("Research trace", trace_id=trace_id):
            yield self._get_trace_url(trace_id)
            
            # Collect user insights through questions
            questions_and_responses = await self._collect_user_insights(query)
            
            # Execute research pipeline
            async for status_update in self._execute_research_pipeline(query, questions_and_responses):
                yield status_update

    async def run_with_responses(self, query: str, questions_and_responses: str) -> AsyncGenerator[str, None]:
        """
        Run the deep research process with pre-collected questions and responses.
        
        Args:
            query: The research topic or question
            questions_and_responses: Pre-collected user responses to clarifying questions
            
        Yields:
            Status updates and the final report
        """
        trace_id = gen_trace_id()
        with trace("Research trace", trace_id=trace_id):
            yield self._get_trace_url(trace_id)
            yield "Starting research with your responses..."
            
            # Execute research pipeline
            async for status_update in self._execute_research_pipeline(query, questions_and_responses):
                yield status_update

    async def _execute_research_pipeline(self, query: str, questions_and_responses: str) -> AsyncGenerator[str, None]:
        """
        Execute the core research pipeline steps.
        
        Args:
            query: The research topic
            questions_and_responses: User responses to clarifying questions
            
        Yields:
            Status updates and final report
        """
        # Plan searches
        search_plan = await self._plan_searches(query, questions_and_responses)
        yield "Searches planned, starting to search..."
        
        # Execute searches
        search_results = await self._perform_searches(search_plan)
        yield "Searches complete, writing report..."
        
        # Generate report
        report = await self._write_report(query, search_results)
        yield "Report written, sending email..."
        
        # Send email
        await self._send_email(report)
        yield "Email sent, research complete"
        yield report.markdown_report

    async def _collect_user_insights(self, query: str) -> str:
        """
        Generate questions and collect user responses interactively.
        
        Args:
            query: The research topic
            
        Returns:
            Formatted string of questions and user responses
        """
        print("Preparing questions...")
        result = await Runner.run(product_manager_agent, f"Query: {query}")
        print(f"Generated questions: {result.final_output}")
        
        return self._interactive_question_collection(result.final_output.searches)

    def _interactive_question_collection(self, questions: List) -> str:
        """
        Collect user responses to questions through interactive prompts.
        
        Args:
            questions: List of question objects from the product manager agent
            
        Returns:
            Formatted string of questions and responses
        """
        questions_and_responses = ""
        
        print("\n" + "="*50)
        print("Please answer the following questions to help with your research:")
        print("="*50)
        
        for i, question_item in enumerate(questions, 1):
            print(f"\nQuestion {i}: {question_item.question}")
            print(f"Reason: {question_item.reason}")
            user_response = input("Your answer: ").strip()
            questions_and_responses += f"{i}. {question_item.question} - Response: {user_response}\n"
        
        print("\n" + "="*50)
        print("Thank you! Proceeding with research...")
        print("="*50)
        
        return questions_and_responses

    async def _plan_searches(self, query: str, questions_and_responses: str) -> WebSearchPlan:
        """
        Plan web searches based on the query and user responses.
        
        Args:
            query: The research topic
            questions_and_responses: User responses to clarifying questions
            
        Returns:
            WebSearchPlan containing the planned searches
        """
        print("Planning searches...")
        input_text = f"Query: {query}\nQuestions and Responses:\n{questions_and_responses}"
        result = await Runner.run(planner_agent, input_text)
        print(f"Will perform {len(result.final_output.searches)} searches")
        return result.final_output

    async def _perform_searches(self, search_plan: WebSearchPlan) -> List[str]:
        """
        Execute web searches in parallel.
        
        Args:
            search_plan: The planned searches to execute
            
        Returns:
            List of search results
        """
        print("Searching...")
        tasks = [asyncio.create_task(self._search(item)) for item in search_plan.searches]
        
        results = []
        num_completed = 0
        
        for task in asyncio.as_completed(tasks):
            result = await task
            if result is not None:
                results.append(result)
            num_completed += 1
            print(f"Searching... {num_completed}/{len(tasks)} completed")
        
        print("Finished searching")
        return results

    async def _search(self, item: WebSearchItem) -> Optional[str]:
        """
        Execute a single web search.
        
        Args:
            item: The search item containing query and reason
            
        Returns:
            Search result or None if search failed
        """
        search_input = f"Search term: {item.query}\nReason for searching: {item.reason}"
        
        try:
            result = await Runner.run(search_agent, search_input)
            return str(result.final_output)
        except Exception as e:
            print(f"Search failed for '{item.query}': {e}")
            return None

    async def _write_report(self, query: str, search_results: List[str]) -> ReportData:
        """
        Generate a comprehensive report from search results.
        
        Args:
            query: The original research query
            search_results: List of search result summaries
            
        Returns:
            ReportData containing the generated report
        """
        print("Thinking about report...")
        report_input = f"Original query: {query}\nSummarized search results: {search_results}"
        
        result = await Runner.run(writer_agent, report_input)
        print("Finished writing report")
        
        return result.final_output_as(ReportData)

    async def _send_email(self, report: ReportData) -> None:
        """
        Send the report via email.
        
        Args:
            report: The generated report data
        """
        print("Writing email...")
        await Runner.run(email_agent, report.markdown_report)
        print("Email sent")

    @staticmethod
    def _get_trace_url(trace_id: str) -> str:
        """
        Generate the trace URL for monitoring.
        
        Args:
            trace_id: The trace identifier
            
        Returns:
            Formatted trace URL
        """
        url = f"https://platform.openai.com/traces/trace?trace_id={trace_id}"
        print(f"View trace: {url}")
        return url