import os
from dotenv import load_dotenv # need to install

from llama_hub.tools.gmail import GmailToolSpec
from llama_index.agent import OpenAIAgent

if __name__ == '__main__':
    load_dotenv()
    print("Hello world - Llama Index")
    print(f"OPENAI_API_KEY is: {os.environ['OPENAI_API_KEY']}")

    google_api_key = os.getenv('GOOGLE_API_KEY')
    tool_spec = GmailToolSpec()

    agent = OpenAIAgent.from_tools(tool_spec.to_tool_list(), verbose=True)

    # result = GmailToolSpec.search_messages(query="Who are the last 4 people who sent me an email?")
    response = agent.chat("Send an email to ananyaa.kaushik7@gmail.com saying 'Wohooooooooo' ")
    response = agent.chat('Send the email')
    print(response)


