import os
from typing import Any, Dict, List, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
KNOWLEDGE_BASE_ID = os.getenv("BEDROCK_KNOWLEDGE_BASE_ID", "")
MODEL_ARN = os.getenv("BEDROCK_MODEL_ARN", "")
NUMBER_OF_RESULTS = int(os.getenv("BEDROCK_NUMBER_OF_RESULTS", "5"))


class ConfigurationError(RuntimeError):
    pass


def validate_config() -> None:
    missing = []
    if not KNOWLEDGE_BASE_ID:
        missing.append("BEDROCK_KNOWLEDGE_BASE_ID")
    if not MODEL_ARN:
        missing.append("BEDROCK_MODEL_ARN")
    if missing:
        raise ConfigurationError("Missing required configuration: " + ", ".join(missing))


def get_client():
    return boto3.client("bedrock-agent-runtime", region_name=AWS_REGION)


def _extract_sources(response: Dict[str, Any]) -> List[Dict[str, str]]:
    sources: List[Dict[str, str]] = []
    seen = set()
    for citation in response.get("citations", []):
        for reference in citation.get("retrievedReferences", []):
            location = reference.get("location", {})
            label = "Unknown source"
            uri = ""
            if "s3Location" in location:
                uri = location["s3Location"].get("uri", "")
                label = uri or "S3 source"
            elif "webLocation" in location:
                uri = location["webLocation"].get("url", "")
                label = uri or "Web source"
            elif "confluenceLocation" in location:
                uri = location["confluenceLocation"].get("url", "")
                label = uri or "Confluence source"
            elif "salesforceLocation" in location:
                uri = location["salesforceLocation"].get("url", "")
                label = uri or "Salesforce source"
            elif "sharePointLocation" in location:
                uri = location["sharePointLocation"].get("url", "")
                label = uri or "SharePoint source"
            key = (label, uri)
            if key not in seen:
                seen.add(key)
                sources.append({"label": label, "uri": uri})
    return sources


def ask(question: str, session_id: Optional[str] = None) -> Dict[str, Any]:
    validate_config()
    if not question or not question.strip():
        raise ValueError("Question must not be empty.")
    client = get_client()
    request: Dict[str, Any] = {
        "input": {"text": question.strip()},
        "retrieveAndGenerateConfiguration": {
            "type": "KNOWLEDGE_BASE",
            "knowledgeBaseConfiguration": {
                "knowledgeBaseId": KNOWLEDGE_BASE_ID,
                "modelArn": MODEL_ARN,
                "retrievalConfiguration": {
                    "vectorSearchConfiguration": {"numberOfResults": NUMBER_OF_RESULTS}
                },
            },
        },
    }
    if session_id:
        request["sessionId"] = session_id
    try:
        response = client.retrieve_and_generate(**request)
    except (ClientError, BotoCoreError) as exc:
        raise RuntimeError(f"Bedrock request failed: {exc}") from exc
    return {
        "answer": response.get("output", {}).get("text", ""),
        "session_id": response.get("sessionId"),
        "sources": _extract_sources(response),
        "raw_citations": response.get("citations", []),
    }


def main() -> None:
    print("Amazon Bedrock RAG Assistant")
    print("Type 'exit' to quit.\n")
    session_id: Optional[str] = None
    while True:
        question = input("You: ").strip()
        if question.lower() in {"exit", "quit"}:
            break
        if not question:
            continue
        try:
            result = ask(question, session_id=session_id)
            session_id = result["session_id"] or session_id
            print(f"\nAssistant: {result['answer']}\n")
            if result["sources"]:
                print("Sources:")
                for index, source in enumerate(result["sources"], start=1):
                    print(f"  {index}. {source['label']}")
                print()
        except Exception as exc:
            print(f"\nError: {exc}\n")


if __name__ == "__main__":
    main()
