from pydantic_ai import Agent
from models import *
from config import model, toolkit


def determine(conversation_history):
    prompt = f"""
    You are a decision maker.
    You will be given a toolkit of functions <toolkit />.
    You will be given a conversation history between a user and a correspondant for an appliance parts company. The conversation history is tagged <conversation_history />.

    Your job is to determine if there is a function in the toolkit <toolkit /> that is suited to answer the user's most recent query in the conversation history <conversation_history />.
    If there is such a tool, you will report it.
    Otherwise, you must categorize the user's query across a series of possible domains.
    The instructions below (tagged <instructions />) offer detail on your processes and the structure of your output.

    <instructions>
    Follow these steps in order:

    1. Read the <toolkit /> and the <conversation_history />. Focus on the user's most recent query.

    2. Determine whether any tool in the <toolkit /> can directly answer the user's query.
    - If yes, return output type ToolChoice and set ToolChoice.tool to the chosen tool. Stop.
    - If no, continue to step 3.

    3. Classify the user's query into one of the following domains:
    - DOMAIN_A: A general appliance-related question where no tool would add value. Set follow_up_question = true.
    - DOMAIN_B: A question not related to appliances. Set not_in_domain = true.
    </instructions>


    Conversation History:
    <conversation_history>
    {conversation_history}
    </conversation_history>

    Tool Kit:
    <toolkit>
    {str(toolkit)}
    </toolkit>

    """

    determiner = Agent(
        model=model,
        output_type=[ToolChoice | GeneralQuestion | OutOfScope]
    )

    return determiner.run_sync(prompt).output