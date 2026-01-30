from pydantic import BaseModel, ConfigDict
from pydantic_ai import Agent
from typing import Literal


class ToolChoice(BaseModel):
    tool: Literal["check_compatability()", "get_part_information()", "get_fix_for_problem()"]

class GeneralQuestion(BaseModel):
    is_generalQuestion: bool

class OutOfScope(BaseModel):
    is_outOfScope: bool

class CompatabilityParams(BaseModel):
    machine_ID: str
    part_ID: str

class PartInformationParams(BaseModel):
    appliance: Literal["refrigerator", "dryer"]
    part_ID: str

class GetFixForProblemParams(BaseModel):
    problem: str
    machine_ID: str

class FailureStatement(BaseModel):
    statement: str

class Symptom(BaseModel):
    symptom: str

class Response(BaseModel):
    Text: str
    YoutubeLinks: list[str]
    ImageLinks: list[str]