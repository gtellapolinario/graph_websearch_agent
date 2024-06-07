import yaml
import os
from models.openai_models import get_open_ai, get_open_ai_json
from prompts.prompts import (
    planner_prompt_template,
    researcher_prompt_template,
    reporter_prompt_template,
    reviewer_prompt_template
)
from utils.helper_functions import get_current_utc_datetime
from states.state import AgentGraphState

model = 'gpt-4o'

def planner_agent(state:AgentGraphState, research_question, prompt=planner_prompt_template, llm=get_open_ai_json(model=model), feedback=None, previous_plans=None):

    planner_prompt = prompt.format(
        feedback=feedback,
        previous_plans=previous_plans,
        datetime=get_current_utc_datetime()
    )

    messages = [
        ("system", planner_prompt),
        ("human", f"research question:{research_question}")
    ]

    ai_msg = llm.invoke(messages)

    state = {**state, "planner_response": ai_msg.content}

    return state

def researcher_agent(state:AgentGraphState, research_question, prompt=researcher_prompt_template, llm=get_open_ai_json(model=model), feedback=None, previous_selections=None, serp=None):

    researcher_prompt = prompt.format(
        feedback=feedback,
        previous_selections=previous_selections,
        serp=serp,
        datetime=get_current_utc_datetime()
    )
    messages = [
        ("system", researcher_prompt),
        ("human", f"research question:{research_question}")
    ]

    ai_msg = llm.invoke(messages)

    state = {**state, "researcher_response": ai_msg.content}

    return state

def reporter_agent(state:AgentGraphState, research_question, prompt=reporter_prompt_template, llm=get_open_ai(model=model), feedback=None, previous_reports=None, research=None):

    reporter_prompt = prompt.format(
        feedback=feedback,
        previous_reports=previous_reports,
        datetime=get_current_utc_datetime(),
        research=research
    )
    messages = [
        ("system", reporter_prompt),
        ("human", f"research question:{research_question}")
    ]

    ai_msg = llm.invoke(messages)

    state = {**state, "reporter_response": ai_msg.content}

    return state

def reviewer_agent(
        state:AgentGraphState,
        research_question,
        prompt=reviewer_prompt_template, 
        llm=get_open_ai_json, 
        planner=None, 
        researcher=None, 
        reporter=None, 
        planner_agent=None, 
        researcher_agent=None, 
        reporter_agent=None,
          feedback=None):

    reviewer_prompt = prompt.format(
        planner = planner,
        researcher=researcher,
        reporter=reporter,
        planner_responsibilities=planner_agent,
        researcher_responsibilities=researcher_agent,
        reporter_responsibilities=reporter_agent,
        feedback=feedback,
        datetime=get_current_utc_datetime()
    )
    messages = [
        ("system", reviewer_prompt),
        ("human", f"research question:{research_question}")  
    ]

    ai_msg = llm.invoke(messages)

    state = {**state, "reviewer_response": ai_msg.content}

    return state


def end_node(state:AgentGraphState):
    state = {**state, "end_chain": "End of the graph"}
    return state


    