from pydantic_ai import Agent
from models import *
from config import model

    
def recognize_symptom(problem, appliance):
    refrigerator_symptoms = [
            "Noisy",
            "Leaking",
            "Will-not-start",
            "Ice-maker-not-making-ice",
            "Fridge-too-warm",
            "Not-dispensing-water",
            "Fridge-and-freezer-are-too-warm",
            "Door-sweating",
            "Light-not-working",
            "Fridge-too-cold",
            "Fridge-runs-too-long",
            "Freezer-too-cold"
        ]
    
    symptoms = {
        'refrigerator': refrigerator_symptoms,
        'dish': "NA"
    }

    agent = Agent(
        model=model,
        output_type=Symptom
        )
    symptom = agent.run_sync(f"Match the problem to the closest matching symptom. Problem = {problem}. Symptom options = {symptoms[appliance]}").output.symptom

    return symptom

