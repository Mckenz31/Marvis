import json

import tiktoken
from fastapi import FastAPI, Body, Query
from llama_hub.tools.code_interpreter import CodeInterpreterToolSpec
from llama_hub.tools.gmail import GmailToolSpec
from llama_hub.tools.google_calendar import GoogleCalendarToolSpec
from llama_hub.tools.slack import SlackToolSpec
from llama_hub.tools.wikipedia import WikipediaToolSpec
from llama_index import download_loader, set_global_service_context, ServiceContext, PromptHelper, VectorStoreIndex, \
    SummaryIndex
from llama_index.agent import OpenAIAgent, ReActAgent, OpenAIAgentWorker, AgentRunner
import openai
from llama_index.agent.types import TaskStepOutput
from llama_index.chat_engine.types import StreamingAgentChatResponse, AgentChatResponse
from llama_index.core.llms.types import ChatMessage, MessageRole
from llama_index.llms import OpenAI
from llama_index.node_parser import TextSplitter, SentenceSplitter
from llama_index.tools.tool_spec.load_and_search import LoadAndSearchToolSpec
from starlette.responses import StreamingResponse

from custom_tools import CustomGmailToolSpec, CustomGoogleCalendarToolSpec, date_tool, time_tool, bank_tool, \
    reminder_tool, remember_tool, play_music_tool, set_setting_tool, get_location_tool, get_weather_tool
from get_token_json import authorize_google

dumb = True

def load_api_keys():
    global api_keys
    api_keys = {}
    with open( "api_keys.txt" ) as f:
        for line in f:
            name, value = line.partition( "=" )[ ::2 ]
            api_keys[ name.strip().upper() ] = value.strip()

load_api_keys()
api_keys: dict[str, str]
# noinspection PyUnboundLocalVariable
openai.api_key = api_keys[ "OPENAI_API_KEY" ]

# discord = download_loader( "DiscordReader" )()
# slack = SlackToolSpec( slack_token = api_keys["SLACK_USER_TOKEN"] )
# wikipedia = WikipediaToolSpec()

authorize_google()

# set_global_service_context( ServiceContext.from_defaults(
#     prompt_helper = PromptHelper( context_window = 4097 ),
#     text_splitter = SentenceSplitter( chunk_size = 512, chunk_overlap = 16 ),
# ) )

gmail = CustomGmailToolSpec()
calendar = CustomGoogleCalendarToolSpec()
tools = [ gmail, calendar ]
# tools = [ tool for tool_list in tools for tool in tool_list.to_tool_list() ]
# tools = [ LoadAndSearchToolSpec.from_defaults( tool_list ).to_tool_list() for tool_spec in tools for tool_list in
#           tool_spec.to_tool_list() ]
tools = [ tool for sublist in tools for tool in sublist.to_tool_list() ]
las_tools = [ "search_messages" ]
skip_tools = [ "create_event" ]
new_tools = []
for tool in tools:
    name = tool.metadata.name
    if name in las_tools:
        load, search = LoadAndSearchToolSpec.from_defaults( tool, index_cls = SummaryIndex ).to_tool_list()
        # search.metadata.name = name
        search.metadata.description = f"Once data has been loaded from {load.metadata.name}, the result is stored in a vector database. " \
                                       "This database can be queried using this function. " \
                                       "The natural language query indicates what text should be retrieved."
        new_tools += [ load, search ]
    elif name not in skip_tools:
        new_tools.append( tool )
tools = new_tools
tools += [ date_tool, time_tool, bank_tool, reminder_tool, remember_tool, play_music_tool, set_setting_tool, get_location_tool, get_weather_tool ]

app = FastAPI()

@app.get( "/chat" )
async def chat( message: str = Body(), google_user_file: str = Query(), chat_history: list[str] = Query( [] ) ):
    parsed_file = json.loads( google_user_file )
    gmail.user_file = parsed_file
    calendar.user_file = parsed_file
    parsed_chat_history = []
    user = True
    for entry in chat_history:
        parsed_chat_history.append( ChatMessage( role = MessageRole.USER if user else MessageRole.ASSISTANT, content = entry ) )
        user = not user

    agent = ReActAgent.from_tools(
        tools,
        llm = OpenAI(
            model = "gpt-3.5-turbo" if dumb else "gpt-4-0125-preview",
            system_prompt = "Act as a helpful assistant. You have extensive access to a variety of APIs to securely access personal information and more!"
        ),
        verbose = True
    )
    # worker = OpenAIAgentWorker.from_tools(
    #     tools,
    #     llm = OpenAI(
    #         model = "gpt-3.5-turbo",
    #         system_prompt = "Act as a helpful assistant. You have extensive access to a variety of APIs to securely access personal information and more!",
    #         chat_history = parsed_chat_history
    #     ),
    #     verbose = True
    # )
    # agent = AgentRunner( worker )
    # task = agent.create_task( message )
    # output: TaskStepOutput | None = None
    # while output is None or not output.is_last:
    #     output = agent.run_step( task.task_id )
    # response = agent.finalize_response( task.task_id, output ).response
    response = agent.chat( message, parsed_chat_history ).response
    print( f"Human: {message}\nAssistant: {response}" )
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run( app, port = 8080 )
