from pydantic_ai import Agent
from models import *
from config import model, output_types, params



def run_param_detector(tool, conversation_history):
    param_detector = Agent(
        model=model,
        output_type=[output_types[tool] | FailureStatement]
    )

    prompt = f"""
    You are a decision maker.
    Your task is to determine whether you have sufficient information to populate all required parameters.
    The relevant information is contained in <conversation_history />.
    The parameter definitions are contained in <params />.

    If you have values for all parameters:
    - Output an object of type {output_types[tool]}, with each parameter name mapped to its value.

    If you do NOT have values for all parameters:
    - Output a FailureStatement concisely saying what parameters you are missing or need clarification on. You are talking to the user here, so keep that in mind.

    <conversation_history>
    {conversation_history}
    </conversation_history>

    <params>
    {params[tool]}
    </params>
    """
    print(prompt)

    return param_detector.run_sync(prompt).output