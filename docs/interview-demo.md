# Interview Demo Guide

## 30-second project summary

I built an Amazon Bedrock RAG assistant to demonstrate how generative AI can be grounded in approved enterprise content instead of relying only on general model knowledge. The application uses a Bedrock Knowledge Base, retrieves relevant document chunks, sends that context to a Bedrock foundation model, and returns an answer with source references. I designed the solution with IAM least privilege, controlled source data, no embedded credentials, logging considerations, and output validation.

## 90-second walkthrough

1. **Business problem** — Users need fast answers from approved internal procedures and standards, but a normal chatbot may hallucinate or answer from uncontrolled information.
2. **Architecture** — Approved documents are stored in S3 and synchronized into a Bedrock Knowledge Base. The Python app uses the Bedrock Agent Runtime to retrieve relevant content and generate a grounded response.
3. **Security** — The app uses AWS credential providers instead of hardcoded keys. IAM limits what the runtime can do. RAG is not treated as authorization; sensitive document access still needs deterministic access controls outside the model.
4. **Validation** — The UI shows source references so the user can verify the answer. AI output is advisory and should not directly authorize access or change production systems.
5. **Production path** — Add Cognito, API Gateway/Lambda, KMS, monitoring, guardrails, data classification, and formal document-level authorization based on the use case.

## Suggested live questions

- `What should an engineer verify before granting an application access to production data?`
- `How should an engineer troubleshoot an AccessDenied error without over-permissioning the workload?`
- `What should I check when the RAG assistant gives a poor answer?`

## Strong follow-up answers

**Why Bedrock?**  
It lets me use managed foundation-model services and Knowledge Base retrieval while keeping the surrounding architecture in AWS, where IAM, S3, KMS, CloudWatch, Lambda, API Gateway, and Cognito can be integrated into the same security and operational model.

**Why RAG?**  
Because the answer should come from approved enterprise knowledge, not only from what a model learned during training. RAG gives the model relevant context and makes source verification possible.

**How would you prevent sensitive-data leakage?**  
Start with data classification and approved ingestion, apply deterministic user/document authorization outside the LLM, use least privilege, encrypt data, minimize sensitive prompt logging, and validate outputs. The model is not the security boundary.

**What about prompt injection?**  
I treat retrieved documents as untrusted input. Controls include governed ingestion, least-privilege tool access, application instructions, output validation, monitoring, and guardrails where appropriate. I would not allow retrieved text to bypass IAM or workflow approval.

**What if AI recommends a production change?**  
It remains a recommendation. Production changes still go through deterministic validation, change control, and appropriate human approval.

## Resume connection

This project is a natural extension of an AWS/cloud-security background because the differentiator is not just calling a model. The value is designing a secure enterprise workload around the model: identity, data protection, encryption, authorization, monitoring, governance, and controlled operations.
