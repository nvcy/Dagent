import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.llm_pick import pick_llm

llm = pick_llm("basic")
print(f"Picked LLM: {llm.invoke({'prompt': 'Hello, world!'})}")