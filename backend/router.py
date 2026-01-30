from agents.determiner import determine
from agents.param_detector import run_param_detector
from agents.respondent import respond

from toolkit.check_compatability import check_compatability
from toolkit.get_part_info import get_part_information
from toolkit.fix_symptom import get_fix_for_problem
from pydantic_ai import Agent
from models import *
from config import model




def conduct_router(conversation_history):
    determination = determine(conversation_history)

    if getattr(determination, "is_generalQuestion", False): ## General Question?
        response = respond(conversation_history, "No added substance. Respond to this general question however fits.")
    elif getattr(determination, "is_outOfScope", False): ## Out of scope?
        response = respond(conversation_history, "This question was not in scope. Please redirect the conversation.")
    else: ## Tool use required?
        tool = determination.tool
        param_results = run_param_detector(tool, conversation_history)
        if getattr(param_results, "statement", False): ## Insufficient information to fulfill parameters
            substance = param_results.statement
        else: ## Succesful tool calling
            print(param_results)     
            if tool == "check_compatability()":
                substance = check_compatability(param_results.machine_ID, param_results.part_ID)
            elif tool == "get_part_information()":
                substance = get_part_information(param_results.appliance, param_results.part_ID)
            elif tool == "get_fix_for_problem()":
                substance = get_fix_for_problem(param_results.problem, param_results.machine_ID)

        response = respond(conversation_history, substance)
    
    return response


