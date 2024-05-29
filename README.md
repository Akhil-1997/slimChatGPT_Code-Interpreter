"""
LangChain OpenAI Code Interpreter Project
----------------------------------------

This project demonstrates the use of LangChain to create and manage multiple agents with OpenAI's GPT-4 model. The setup includes two specialized agents:
1. Python Agent: Executes Python code to answer questions.
2. CSV Agent: Analyzes data from a CSV file to answer questions.

A Router Agent is also created to dynamically select the appropriate agent based on the input prompt.

Files:
- main.py: The main script that sets up and runs the agents.
- .env: Contains the OpenAI API key required for authentication.

Setup Instructions:
1. Ensure you have a `.env` file with the following content:
   OPENAI_API_KEY=your_openai_api_key_here

2. Install the required Python packages:
   pip install python-dotenv langchain langchain-openai langchain-core langchain-experimental

3. Run the main script:
   python main.py

Functionality:
- The script first sets up two agents: a Python Agent and a CSV Agent.
- It then creates a Router Agent that selects the correct agent based on the user's input.
- The Router Agent is capable of executing Python code or analyzing CSV data based on the provided prompt.

Example Usage:
- The Router Agent can answer questions about the number of episodes in a season or generate QR codes based on the input URL.
"""
