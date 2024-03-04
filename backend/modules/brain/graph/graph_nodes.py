from langgraph.prebuilt import ToolInvocation
import json
from langchain_core.messages import FunctionMessage
from langchain.tools.render import format_tool_to_openai_function
from langchain_community.chat_models import ChatLiteLLM
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolExecutor
from typing import TypedDict, Annotated, Sequence
import operator
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]


tools = [TavilySearchResults(max_results=1)]
tool_executor = ToolExecutor(tools)
model = ChatLiteLLM(model="ollama/mistral")
model = model.bind_functions(tools)


def should_continue(state):
    messages = state['message']
    last_message = messages[-1]
    if "function_call" not in last_message.additional_kwargs:
        return "end"
    else:
        return "continue"


def call_model(state):
    messages = state['messages']
    response = model.invoke(messages)
    return {"messages": [response]}


def call_tool(state):
    messages = state['messages']
    last_message = messages[-1]
    action = ToolInvocation(
        tool=last_message.additional_kwargs["function_call"]["name"],
        tool_input=json.loads(last_message.additional_kwargs["function_call"]["arguments"]),
    )
    response = tool_executor.invoke(action)
    function_message = FunctionMessage(content=str(response), name=action.tool)
    return {"messages": [function_message]}


workflow = StateGraph(AgentState)
workflow.add_node("agent", call_model)
workflow.add_node("action", call_tool)

workflow.set_entry_point("agent")

workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "action",
        "end": END
    }
)

workflow.add_edge('action', 'agent')

app = workflow.compile()

inputs = {"messages": [HumanMessage(content="what is the weather in sf")]}
app.invoke()
