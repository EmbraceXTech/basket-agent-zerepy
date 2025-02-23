# loop task
import time,threading
from src.action_handler import register_action
from src.helpers import print_h_bar

@register_action("consider-trade-steps")
def consider_trade(agent, test, **kwargs):
  """
  Consider a trade based on the current market conditions and the agent's strategy.
  """
  agent.logger.info("Considering a trade...")
  print_h_bar()
  
  # get value from kwargs
  # value = kwargs.get('<key>')
  
  # promopt, system_prompt - ZerePy/src/agent.py
  # agent.prompt_llm("<prompt>", "<system_prompt>")
  
  # perform other actions - ZerePy/src/agent.py
  # add other connections (connect with external services) to the agent - ZerePy/src/connection_manager.py and ZerePy/src/connections/...
  # agent.perform_action(connection_name="", action_name="generate-text", params=[])
  return { "success": True, "message": "Trade considered" }
  
  