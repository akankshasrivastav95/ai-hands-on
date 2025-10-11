"""
Deep Research Web Interface

This module provides a Gradio-based web interface for the deep research system.
It handles question generation, user interaction, and research execution.
"""

import asyncio
import concurrent.futures
from typing import List, Dict, Any, Optional, Tuple

import gradio as gr
from dotenv import load_dotenv

from research_manager import ResearchManager
from agents import Runner
from product_manager_agent import product_manager_agent

load_dotenv(override=True)

# Configuration constants
MAX_QUESTIONS = 10
DEFAULT_THEME = gr.themes.Default(primary_hue="sky")


class ResearchSession:
    """Manages the state of a research session."""
    
    def __init__(self):
        self.current_questions: List[Any] = []
        self.current_query: str = ""
        self.response_components: List[Dict[str, Any]] = []


# Global session state
session = ResearchSession()

class AsyncHelper:
    """Helper class for handling asyncio operations in Gradio."""
    
    @staticmethod
    def run_async(coro):
        """Run an async coroutine, handling different event loop scenarios."""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If loop is running, we need to run in a thread
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, coro)
                    return future.result()
            else:
                return loop.run_until_complete(coro)
        except RuntimeError:
            # No event loop exists, create a new one
            return asyncio.run(coro)


def generate_questions(query: str) -> Tuple[str, gr.update, List[Dict[str, Any]]]:
    """
    Generate questions using the product manager agent.
    
    Args:
        query: The research query
        
    Returns:
        Tuple of (questions_text, visibility_update, response_components)
    """
    session.current_query = query
    
    try:
        # Generate questions using the product manager agent
        result = AsyncHelper.run_async(
            Runner.run(product_manager_agent, f"Query: {query}")
        )
        
        session.current_questions = result.final_output.searches
        
        # Format questions for display
        questions_text = _format_questions_for_display(session.current_questions)
        
        # Create response components
        session.response_components = _create_response_components(session.current_questions)
        
        return questions_text, gr.update(visible=True), session.response_components
        
    except Exception as e:
        print(f"Error in generate_questions: {e}")
        import traceback
        traceback.print_exc()
        return f"Error generating questions: {str(e)}", gr.update(visible=False), []


def _format_questions_for_display(questions: List[Any]) -> str:
    """Format questions for display in the UI."""
    questions_text = "## Please answer these questions to help with your research:\n\n"
    
    for i, question_item in enumerate(questions, 1):
        questions_text += f"**Question {i}:** {question_item.question}\n\n"
        questions_text += f"*Reason: {question_item.reason}*\n\n"
    
    return questions_text


def _create_response_components(questions: List[Any]) -> List[Dict[str, Any]]:
    """Create response components metadata for dynamic UI generation."""
    response_components = []
    
    for i, question_item in enumerate(questions, 1):
        component_data = {
            'label': f"Question {i}: {question_item.question}",
            'placeholder': _create_placeholder_text(question_item.question),
            'lines': 2
        }
        response_components.append(component_data)
    
    return response_components


def _create_placeholder_text(question: str) -> str:
    """Create placeholder text for question input fields."""
    truncated_question = question[:30] + ('...' if len(question) > 30 else '')
    return f"Your answer to: {truncated_question}"

def run_research(*responses) -> str:
    """
    Run the research with user responses.
    
    Args:
        *responses: Variable number of user responses
        
    Returns:
        Research results or error message
    """
    print(f"Debug: Received {len(responses)} responses")
    print(f"Debug: Current questions count: {len(session.current_questions)}")
    print(f"Debug: Responses: {responses}")
    
    # Validate responses
    validation_result = _validate_responses(responses)
    if validation_result:
        return validation_result
    
    # Format questions and responses
    questions_and_responses = _format_questions_and_responses(responses)
    
    # Execute research
    return _execute_research(questions_and_responses)


def _validate_responses(responses: Tuple[str, ...]) -> Optional[str]:
    """Validate user responses."""
    valid_responses = [resp for resp in responses if resp is not None and str(resp).strip()]
    
    print(f"Debug: Valid responses count: {len(valid_responses)}")
    print(f"Debug: Valid responses: {valid_responses}")
    
    if len(valid_responses) != len(session.current_questions):
        return (f"Please provide answers for all {len(session.current_questions)} questions. "
                f"You provided {len(valid_responses)} answers.")
    
    return None


def _format_questions_and_responses(responses: Tuple[str, ...]) -> str:
    """Format questions and responses for the research manager."""
    valid_responses = [resp for resp in responses if resp is not None and str(resp).strip()]
    questions_and_responses = ""
    
    for i, (question_item, response) in enumerate(zip(session.current_questions, valid_responses), 1):
        questions_and_responses += f"{i}. {question_item.question} - Response: {response}\n"
    
    return questions_and_responses


def _execute_research(questions_and_responses: str) -> str:
    """Execute the research process."""
    research_manager = ResearchManager()
    
    try:
        async def async_run():
            result = ""
            async for chunk in research_manager.run_with_responses(session.current_query, questions_and_responses):
                result += str(chunk) + "\n\n"
            return result
        
        return AsyncHelper.run_async(async_run())
        
    except Exception as e:
        print(f"Error in run_research: {e}")
        import traceback
        traceback.print_exc()
        return f"Error running research: {str(e)}"

class GradioInterface:
    """Manages the Gradio web interface for the research system."""
    
    def __init__(self):
        self.response_containers = []
        self._setup_interface()
    
    def _setup_interface(self):
        """Set up the Gradio interface components."""
        with gr.Blocks(theme=DEFAULT_THEME) as self.ui:
            gr.Markdown("# Deep Research")
            
            # Query input section
            with gr.Row():
                self.query_textbox = gr.Textbox(
                    label="What topic would you like to research?", 
                    placeholder="Enter your research topic..."
                )
                self.generate_questions_btn = gr.Button("Generate Questions", variant="secondary")
            
            self.questions_display = gr.Markdown(visible=False)
            
            # Questions interface
            with gr.Row(visible=False) as self.questions_section:
                with gr.Column():
                    gr.Markdown("### Answer the questions below:")
                    # Create response containers
                    self.response_containers = []
                    for i in range(MAX_QUESTIONS):
                        self.response_containers.append(gr.Textbox(visible=False, lines=2))
                    self.run_research_btn = gr.Button("Run Research", variant="primary", visible=False)
            
            self.report = gr.Markdown(label="Research Report")
            
            self._setup_event_handlers()
    
    def _setup_event_handlers(self):
        """Set up event handlers for the interface."""
        # Generate questions button and textbox submit
        self.generate_questions_btn.click(
            fn=self.update_questions_interface,
            inputs=self.query_textbox,
            outputs=[self.questions_display, self.questions_section] + 
                    self.response_containers + [self.run_research_btn]
        )
        
        self.query_textbox.submit(
            fn=self.update_questions_interface,
            inputs=self.query_textbox,
            outputs=[self.questions_display, self.questions_section] + 
                    self.response_containers + [self.run_research_btn]
        )
        
        # Run research button
        self.run_research_btn.click(
            fn=self.run_research_with_filtered_inputs,
            inputs=self.response_containers,
            outputs=self.report
        )
    
    def update_questions_interface(self, query: str) -> List[Any]:
        """
        Update the questions interface with dynamic components.
        
        Args:
            query: The research query
            
        Returns:
            List of updates for Gradio components
        """
        try:
            print(f"Generating questions for query: {query}")
            
            # Generate questions
            questions_text, questions_visible, response_components = generate_questions(query)
            
            print(f"Generated {len(response_components)} questions")
            print(f"Questions visible: {questions_visible}")
            
            # Create updates for response containers
            updates = self._create_container_updates(response_components, questions_visible)
            
            print(f"Returning {len(updates)} updates")
            return [questions_text, gr.update(visible=questions_visible)] + updates
            
        except Exception as e:
            print(f"Error in update_questions_interface: {e}")
            import traceback
            traceback.print_exc()
            return [f"Error: {str(e)}", gr.update(visible=False)] + \
                   [gr.update(visible=False)] * (len(self.response_containers) + 1)
    
    def _create_container_updates(self, response_components: List[Dict[str, Any]], 
                                 questions_visible: gr.update) -> List[gr.update]:
        """Create updates for response containers based on generated questions."""
        updates = []
        
        for i, container in enumerate(self.response_containers):
            if i < len(response_components):
                # Update the container with the new component
                updates.append(gr.update(
                    visible=True,
                    label=response_components[i]['label'],
                    placeholder=response_components[i]['placeholder'],
                    lines=response_components[i]['lines']
                ))
            else:
                updates.append(gr.update(visible=False))
        
        # Add update for run research button
        updates.append(gr.update(visible=questions_visible))
        
        return updates
    
    def run_research_with_filtered_inputs(self, *all_responses) -> str:
        """
        Wrapper function that filters responses to only include relevant ones.
        
        Args:
            *all_responses: All response inputs from the interface
            
        Returns:
            Research results
        """
        # Only take the first N responses where N is the number of questions
        relevant_responses = all_responses[:len(session.current_questions)] if session.current_questions else []
        return run_research(*relevant_responses)
    
    def launch(self, inbrowser: bool = True):
        """Launch the Gradio interface."""
        self.ui.launch(inbrowser=inbrowser)


def main():
    """Main function to launch the application."""
    interface = GradioInterface()
    interface.launch()


if __name__ == "__main__":
    main()