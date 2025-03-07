# for action connection
import logging
import os
from typing import Dict, Any
from dotenv import load_dotenv
from src.connections.base_connection import BaseConnection, Action, ActionParameter

logger = logging.getLogger("connections.basket_connection")

class BasketConnectionError(Exception):
    """Base exception for Basket connection errors"""
    pass

class BasketConnection(BaseConnection):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self._client = None

    @property
    def is_llm_provider(self) -> bool:
        return False

    def validate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate Basket configuration from JSON"""
        # required_fields = ["model"]
        # missing_fields = [field for field in required_fields if field not in config]
        
        # if missing_fields:
        #     raise ValueError(f"Missing required configuration fields: {', '.join(missing_fields)}")
            
        # # Validate model exists (will be checked in detail during configure)
        # if not isinstance(config["model"], str):
        #     raise ValueError("model must be a string")
            
        return config

    def register_actions(self) -> None:
        """Register available Basket actions"""
        self.actions = {
            "generate-trade-steps": Action(
                name="generate-trade-steps",
                parameters=[],
                description="Consider a trade based on the current market conditions and the agent's strategy.",
            ),
            "test-action": Action(
                name="test-action",
                parameters=[ActionParameter("test", True, str, "Test parameter"), ActionParameter("test1", True, str, "Test parameter")],
                description="Test action",
            )
        }
    def configure(self) -> bool:
        """Sets up OpenAI API authentication"""
        logger.info("\n🤖 OPENAI API SETUP")

        if self.is_configured():
            logger.info("\nOpenAI API is already configured.")
            response = input("Do you want to reconfigure? (y/n): ")
            if response.lower() != 'y':
                return True

        logger.info("\n📝 To get your Basket API credentials:")
        logger.info("1. Go to https://platform.openai.com/account/api-keys")
        logger.info("2. Create a new project or open an existing one.")
        logger.info("3. In your project settings, navigate to the API keys section and create a new API key")
        
        # api_key = input("\nEnter your OpenAI API key: ")

        try:
            if not os.path.exists('.env'):
                with open('.env', 'w') as f:
                    f.write('')

            # set_key('.env', 'OPENAI_API_KEY', api_key)

            logger.info("\n✅ Basket configuration successfully saved!")
            logger.info("Your configuration has been stored in the .env file.")
            return True

        except Exception as e:
            logger.error(f"Configuration failed: {e}")
            return False

    def is_configured(self, verbose = False) -> bool:
        """Check if Basket configuration is configured and valid"""
        try:
            load_dotenv()
            # api_key = os.getenv('BASKET_API_KEY')
            # if not api_key:
            #     return False
            return True
            
        except Exception as e:
            if verbose:
                logger.debug(f"Configuration check failed: {e}")
            return False

    def generate_trade_steps(self, **kwargs) -> str:
        try:
            print(kwargs)
            # call openai connection
            # result = self.perform_action("openai", "generate_text", prompt="Hello, What your name?", system_prompt="My name is John Doe. You are a helpful assistant.")
            # print('result', result)
            return "Consider trade from connection "
            
        except Exception as e:
            raise BasketConnectionError(f"Consider trade failed: {e}")

    def test_action(self, test, test1, **kwargs) -> str:
        # get value from kwargs
        # value = kwargs.get('<key>')
        
        # promopt, system_prompt - ZerePy/src/agent.py
        # agent.prompt_llm("<prompt>", "<system_prompt>")
        
        # perform other actions - ZerePy/src/agent.py
        # add other connections (connect with external services) to the agent - ZerePy/src/connection_manager.py and ZerePy/src/connections/...
        # agent.perform_action(connection_name="", action_name="generate-text", params=[])
        return "Test action from connection " + test + test1

    def perform_action(self, action_name: str, kwargs) -> Any:
        """Execute a Basket action with validation"""
        if action_name not in self.actions:
            raise KeyError(f"Unknown action: {action_name}")

        action: Action = self.actions[action_name]
        errors = action.validate_params(kwargs)
        if errors:
            return f"Error: Invalid parameters: {', '.join(errors)}"
        
        # Call the appropriate method based on action name
        method_name = action_name.replace('-', '_')
        method = getattr(self, method_name)
        return method(**kwargs)
