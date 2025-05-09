import os
import sys
from pathlib import Path
from uuid import uuid4

from browser_use.agent.views import ActionResult

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ['BROWSER_USE_LOGGING_LEVEL'] = 'DEBUG'
import asyncio

from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatDeepInfra

from browser_use import Agent, Controller
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext, BrowserContextConfig
import uuid
import json

from langchain.globals import set_verbose

set_verbose(True)


API_KEY = "6nptMuYRgUSexQMWqD9hVMkHkOmHhFMbsIQFm6ZSAQLkOtZ66Q5UNXwXdKUjK7zs"
# from lmnr import Laminar
# Laminar.initialize(project_api_key=API_KEY, base_url="http://localhost", http_port=8000, grpc_port=8001)

initial = [
    {'go_to_url': {'url': 'https://netflix.com/login'}}
]

browser = Browser(
config=BrowserConfig(
		# NOTE: you need to close your chrome browser - so that this can open your browser in debug mode
		chrome_instance_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
	)
)

context = BrowserContext(
     browser=browser,
    #  config=BrowserContextConfig(
    #       trace_path="./examples/agent/traces",
    #       save_recording_path="./examples/agent/traces"
    #  )
)

from typing import (
    Any,
    AsyncIterator,
    Callable,
    Dict,
    Iterator,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
)
from langchain_core.callbacks.manager import (
    AsyncCallbackManagerForLLMRun,
    CallbackManagerForLLMRun,
)
log_id = uuid.uuid4()

class GemmaChat(ChatDeepInfra):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    async def acompletion_with_retry(
        self,
        run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> Any:
        """Use tenacity to retry the async completion call."""
        # print('logs/{log_id}.log')
        with open(f'logs/{log_id}.log', 'a') as f:
            json.dump(kwargs, f, indent=4)
        # print(kwargs)
        return await super().acompletion_with_retry(run_manager, **kwargs)
    
    def completion_with_retry(self, run_manager: Optional[CallbackManagerForLLMRun] = None, **kwargs: Any
    ) -> Any:
        with open(f'logs/{log_id}.log', 'a') as f:
            json.dump(kwargs, f, indent=4)
        # print(kwargs)
            res = super().completion_with_retry(run_manager, **kwargs)
            f.write('\nRESPONSE\n')
            json.dump(res.json(), f, indent=4)
            f.write('\n')
            f.flush()
            return res
        
async def main2():
	# Initialize the agent with the task and language model
    # Laminar.set_session(session_id=str(uuid4()))
    # sensitive_data = {'x_email': os.environ.get('AMEX_USER', ''), 'x_password': os.environ.get("AMEX_PW",'')}
    sensitive_data = {'x_email': 'desirejesus@hotmail.com', 'x_password': 'E91HmybW', 
                      'x_PIN_1': '1', 'x_PIN_2': '1', 'x_PIN_3': '8', 'x_PIN_4': '1'}
    agent = Agent(
        task=f"""Sign into American Express and download all transactions for 2025.""",
        llm=ChatOpenAI(model='gpt-4o-mini'),  # Replace with your LLM configuration
        # llm=ChatOpenAI(base_url="http://127.0.0.1:1234/v1"),
        # llm=ChatDeepInfra(model="meta-llama/Meta-Llama-3.1-8B-Instruct"),
        # llm=GemmaChat(model="meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8", max_tokens=1024, temperature=0.2),
        tool_calling_method='auto',
        use_vision=False,
        browser=browser,
        context=context,
        max_failures=5,
        # max_actions_per_step=2,
        generate_gif=True,  # Disable GIF generation,
        sensitive_data=sensitive_data,
        save_conversation_path="examples/agent/logs/log",
        initial_actions=initial
    )

    # Run the agent and get results asynchronously
    result = await agent.run(max_steps=10)

    # Process results token-wise
    for action in result.action_results():
      print(action.extracted_content,end="\r",flush=True)
      print("\n\n")
        # if action.is_done:
        #     print(action.extracted_content)

    # Close the browser after completion
    await browser.close()
	# agent = Agent(
	# 	task='In docs.google.com write my Papa a quick letter',
	# 	llm=ChatOpenAI(model='gpt-4o-mini'),
	# 	browser=browser,
	# )

	# await agent.run()
	# await browser.close()

    # input('Press Enter to close...')
    # Laminar.clear_session()
    agent.save_history()
    print('Finished')        

async def main():
	# Initialize the agent with the task and language model
    # Laminar.set_session(session_id=str(uuid4()))
    sensitive_data = {'x_email': 'desirejesus@hotmail.com', 'x_password': 'E91HmybW', 
                      'x_PIN_1': '1', 'x_PIN_2': '1', 'x_PIN_3': '8', 'x_PIN_4': '1'}
    show = "Triple Frontier"
    agent = Agent(
        task=f"""Play {show}.
        
        Step 1: Sign into Netflix using x_email and x_password.
        Step 2: Select Christopher's profile. 
        Step 3: When a PIN is required. Use x_PIN_1, x_PIN_2, x_PIN_3, and x_PIN_4 in the four PIN inputs.
        Step 4: Click on Search button and enter {show}.
        Step 5: Play or resume {show}r.""",
        llm=ChatOpenAI(model='gpt-4o-mini'),  # Replace with your LLM configuration
        # llm=ChatOpenAI(base_url="http://127.0.0.1:1234/v1"),
        # llm=ChatDeepInfra(model="meta-llama/Meta-Llama-3.1-8B-Instruct"),
        # llm=GemmaChat(model="meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8", max_tokens=1024, temperature=0.2),
        tool_calling_method='auto',
        use_vision=False,
        browser=browser,
        context=context,
        max_failures=10,
        # max_actions_per_step=2,
        generate_gif=True,  # Disable GIF generation,
        sensitive_data=sensitive_data,
        save_conversation_path="examples/agent/logs/log",
        initial_actions=initial
    )

    # Run the agent and get results asynchronously
    result = await agent.run(max_steps=10)

    # Process results token-wise
    for action in result.action_results():
      print(action.extracted_content,end="\r",flush=True)
      print("\n\n")
        # if action.is_done:
        #     print(action.extracted_content)

    # Close the browser after completion
    await browser.close()
	# agent = Agent(
	# 	task='In docs.google.com write my Papa a quick letter',
	# 	llm=ChatOpenAI(model='gpt-4o-mini'),
	# 	browser=browser,
	# )

	# await agent.run()
	# await browser.close()

    # input('Press Enter to close...')
    # Laminar.clear_session()
    agent.save_history()
    print('Finished')

async def replay():
    sensitive_data = {'x_email': 'desirejesus@hotmail.com', 'x_password': 'E91HmybW', 
                      'x_PIN_1': '1', 'x_PIN_2': '1', 'x_PIN_3': '8', 'x_PIN_4': '1'}
    agent = Agent(
        task="""Play Lost.
        
        Step 1: Log into Netflix using x_email and x_password.
        Step 2: Select Christopher's profile. 
        Step 3: When a PIN is required. Use x_PIN_1, x_PIN_2, x_PIN_3, and x_PIN_4 in the four PIN inputs.
        Step 4: Search Netflix.
        Step 5: Play next episode""",
        llm=ChatOpenAI(model='gpt-4o-mini'),  # Replace with your LLM configuration
        # llm=ChatDeepInfra()
        browser=browser,
        context=context,
        generate_gif=True,  # Disable GIF generation,
        sensitive_data=sensitive_data,
        save_conversation_path="examples/agent/logs/log",
        initial_actions=initial
    )
    await agent.load_and_rerun("AgentHistory.json")
    await browser.close()

if __name__ == '__main__':
	asyncio.run(main(), debug=True)
#    asyncio.run(replay(), debug=True)
