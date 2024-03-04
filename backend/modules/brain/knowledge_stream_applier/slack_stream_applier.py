from modules.brain.knowledge_stream_applier.knowledge_stream_applier import KnowledgeStreamApplier
import requests


def parse_slack_threads_response(content) -> []:
    return []


prompt_summary = "Please summarize the questions and the answers in this conversation."
example_summary = {
    "input": "",
    "output": ""
}

prompt_decision = "Are the problems have been addressed?"


class SlackStreamApplier(KnowledgeStreamApplier):
    def ingest_knowledge(self, knowledge_files):
        for knowledge_file in knowledge_files:
            requests.post(url="", data=knowledge_file)

    def data_processing(self, data) -> []:
        for conversation in data:
            pass
        return []

    def fetch_data(self, source, auth) -> []:
        headers = {
            "Authorization": f"Bearer {auth}"
        }
        response = requests.get(source, headers=headers)
        content = response.text
        return parse_slack_threads_response(content)
