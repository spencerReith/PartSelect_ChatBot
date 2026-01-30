import os
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.providers.anthropic import AnthropicProvider

from models import *


"""
Title: Setting Model
Description:
Initializes the Anthropic LLM client using the API key from environment variables.
Configures the default model used for all downstream agent calls.
"""
KEY = os.getenv('ANTHROPIC_KEY')
model = AnthropicModel(
    'claude-haiku-4-5',
    provider=AnthropicProvider(api_key=KEY)
)


"""
Title: Setting Toolkit
Description:
Defines the available tools (functions) the agent can call, along with
natural-language descriptions used for tool selection and routing.
"""
toolkit = {
    "check_compatability()": "Check if a part is compatible with an appliance model",
    "get_part_information()": """
    Get information for a given <part_ID> of appliance type <appliance>

    Information includes
    * Name
    * Product Description
    * Installation Instructions
    * Troubleshooting Instructions
    * Relevent instructional youtube videos
    * Price
    """,
    "get_fix_for_problem()": "If the user has a problem with an appliance, this will tell them how to fix it."
}

"""
Title: Tool Parameter Descriptions
Description:
Defines human-readable descriptions for each tool’s input parameters.
These are used by the agent to understand what arguments are required
and how to format them when calling tools.
"""
CompatabilityParams_Description = {
    "machine_ID": "ID for the appliance. Examples are like: 2939139124 or XASDJANEJR23",
    "part_ID": "ID for a part. Examples are like 234123412312"
}
PartInformation_Description = {
    "appliance": "Whether the machine is a refrigerator or a dryer",
    "part_ID": "ID for a part. Examples are like 234123412312"
}
GetFixForProblem_Description = {
    "problem": "What the issue is with the machine. as detailed as you want",
    "machine_ID": "ID for the appliance. Examples are like: 2939139124 or XASDJANEJR23"
}
params = {
    'check_compatability()': CompatabilityParams_Description,
    'get_part_information()': PartInformation_Description,
    'get_fix_for_problem()': GetFixForProblem_Description,
}
output_types = {
    'check_compatability()': CompatabilityParams,
    'get_part_information()': PartInformationParams,
    'get_fix_for_problem()': GetFixForProblemParams,
}