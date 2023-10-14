"""Create agents."""
import logging

import autogen
from autogen import config_list_from_json

from app.llm.perplexity_functions import get_valid_folder_name
from app.utils import load_string_from_file

llm_config_list_4 = config_list_from_json(
    env_or_file="OAI_CONFIG_LIST",
    filter_dict={
        "model": [
            "gpt-4",
            # "gpt-4-32k",
        ],
    },
)


llm_config_list_35 = config_list_from_json(
    env_or_file="OAI_CONFIG_LIST",
    filter_dict={
        "model": [
            # "gpt-3.5-turbo",
            "gpt-3.5-turbo-16k",
        ],
    },
)


llm_config_planner = {
    "config_list": llm_config_list_4,
}

llm_config_assistant = {
    "temperature": 0,
    "request_timeout": 600,
    "seed": 42,
    "functions": [
        {
            "name": "ask_planner",
            "description": load_string_from_file(
                "app/resources/ask_planner_description.txt"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": load_string_from_file(
                            "app/resources/ask_planner_message.txt"
                        ),
                    },
                },
                "required": ["message"],
            },
        },
        {
            "name": "ask_mermaid_expert",
            "description": load_string_from_file(
                "app/resources/ask_mermaid_expert_description.txt"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": load_string_from_file(
                            "app/resources/ask_mermaid_expert_message.txt"
                        ),
                    },
                },
                "required": ["message"],
            },
        },
    ],
    "config_list": llm_config_list_4,
}


class ChatException(Exception):
    """Chat exception."""


def create_planner_agent():
    """Create planner agent."""

    planner = autogen.AssistantAgent(
        name="planner",
        llm_config=llm_config_planner,
        system_message=load_string_from_file(
            "app/resources/planner_system_message.txt"
        ),
    )
    planner_user = autogen.UserProxyAgent(
        name="planner_user",
        max_consecutive_auto_reply=0,  # terminate without auto-reply
        human_input_mode="NEVER",
    )

    def ask_planner(message):
        """Ask the planner a question."""
        planner_user.initiate_chat(planner, message=message)
        # return the last message received from the planner
        return planner_user.last_message()["content"]

    return ask_planner


def create_agents(foldername: str, command_args):
    """Create agents."""

    # query_engine = RepoQueryEngine(command_args)

    # def ask_mermaid_expert(message):
    #     """Ask the mermaid expert a question."""
    #     answer = query_engine.query_repo(message)
    #     return answer

    ask_planner = create_planner_agent()

    assistant = autogen.AssistantAgent(
        name="assistant",
        llm_config=llm_config_assistant,
    )

    user_proxy = autogen.UserProxyAgent(
        name="user_proxy",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=40,
        code_execution_config={
            "work_dir": f"work_dir/{foldername}",
        },
        # is_termination_msg=lambda x: x.get("content", "")
        # .rstrip()
        # .endswith("TERMINATE"),
        system_message="""Reply TERMINATE if the task has been solved at full satisfaction. Otherwise, reply CONTINUE, or the reason why the task is not solved yet.""",  # noqa: E501 pylint: disable=line-too-long
    )

    user_proxy.register_function(
        function_map={
            "ask_planner": ask_planner,
            # "ask_mermaid_expert": ask_mermaid_expert,
        },
    )

    return assistant, user_proxy


def start_chat(command_args):
    """Start chat."""
    try:
        message = load_string_from_file("app/resources/chat_message.md")
        foldername = get_valid_folder_name(message)

        assistant, user_proxy = create_agents(foldername, command_args)

        user_proxy.initiate_chat(
            assistant,
            message=message,
        )

    except ChatException as e:
        logging.error("logged error %s", e, exc_info=True)
    except Exception as e:  # pylint: disable=broad-except
        logging.error("Unhandled exception %s", e, exc_info=True)
