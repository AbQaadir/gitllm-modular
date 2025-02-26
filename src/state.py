from typing import List
from typing_extensions import TypedDict

class State(TypedDict):
    task: str
    plan_string: str
    steps: List
    results: dict
    result: str