import os
from langchain import hub
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import (
    create_react_agent,
    AgentExecutor,
)
from langchain_experimental.tools import PythonREPLTool
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from typing import Any
from langchain_core.tools import Tool

# Load environment variables from the .env file
load_dotenv()

# Access the environment variable
api_key = os.getenv('OPENAI_API_KEY')

def main():
    """Main function to setup and execute LangChain agents."""

    print("code interpreter project using langchain")

    instructions = """You are an agent designed to write and execute python code to answer questions.
    You have access to a python REPL, which you can use to execute python code.
    If you get an error, debug your code and try again.
    Only use the output of your code to answer the question. 
    You might know the answer without running any code, but you should still run the code to get the answer.
    If it does not seem like you can write code to answer the question, just return "I don't know" as the answer.
    """

    base_prompt = hub.pull("langchain-ai/react-agent-template")
    prompt = base_prompt.partial(instructions=instructions)

    tools = [PythonREPLTool()]

    python_agent = create_react_agent(
        prompt=prompt,
        llm=ChatOpenAI(api_key=api_key, temperature=0, model="gpt-4-turbo"),
        tools=tools
    )

    python_agent_executor = AgentExecutor(agent=python_agent, tools=tools, verbose=True)

    csv_agent = create_csv_agent(
                llm=ChatOpenAI(api_key=api_key, temperature=0, model="gpt-4-turbo"),
                path="/Users/iccpd/Desktop/Extra/Udemy/Langchain/code_interpreter/episode_info.csv",
                verbose=True
    )

    def python_agent_executor_wrapper(original_prompt: str) -> dict[str, Any]:
        """Wrapper for the Python agent executor to handle the input prompt."""
        return python_agent_executor.invoke({"input": original_prompt})

    tools = [
        Tool(
            name="Python Agent",
            func=python_agent_executor_wrapper,
            description= """useful when you need to transform natural language to python and execute the python code, 
                            returning the results of the code execution.
                            DOES NOT ACCEPT CODE AS INPUT""",
        ),
        Tool(
            name="CSV Agent",
            func=csv_agent.invoke,
            description= """useful when you need to answer questions over episode_info.csv file, 
                            takes an input the entire question and returns the answer after running pandas calculations""",
        ),
    ]

    prompt = base_prompt.partial(instructions="")

    router_agent = create_react_agent(
        prompt=prompt,
        llm=ChatOpenAI(api_key=api_key, temperature=0, model="gpt-4-turbo"),
        tools=tools
    )

    router_agent_executor = AgentExecutor(agent=router_agent, tools=tools, verbose=True)

    print(
        router_agent_executor.invoke(
            {
                "input" : "which season has the most episodes?"
            }
        )
    )

    print(
        router_agent_executor.invoke(
            {
                "input" : "generate and save in current working directory 15 QR codes that point to https://www.rwth-aachen.de/go/id/a/?lidx=1, you have qrcode package installed already"
            }
        )
    )

if __name__ == '__main__':
    main()
