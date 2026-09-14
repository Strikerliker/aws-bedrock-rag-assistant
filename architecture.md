# Architecture and Security Design

## Logical components

1. **User interface** - CLI for fast testing or Streamlit for a visual demo.
2. **Application layer** - Python code validates configuration, submits the user query, maintains the Bedrock session ID, and renders source references.
3. **Amazon Bedrock Agent Runtime** - executes the Knowledge Base retrieval-and-generation request.
4. **Bedrock Knowledge Base** - retrieves the most relevant chunks from synchronized enterprise content.
5. **Approved data source** - typically an encrypted Amazon S3 bucket containing approved procedures, standards, runbooks, or other enterprise knowledge.
6. **Vector store** - managed or supported vector storage configured for the Knowledge Base.
7. **Foundation model / inference profile** - generates a response from the retrieved context.
8. **IAM** - controls application and service permissions.
9. **Monitoring** - application logs and CloudWatch telemetry appropriate to the workload.

## Production deployment pattern

A production serverless version can use Amazon Cognito, API Gateway, Lambda, Bedrock Knowledge Bases, S3, KMS, CloudWatch, WAF, and Bedrock Guardrails where appropriate.

## Security principles

### Identity and access
- Grant the runtime only the Bedrock actions and specific resources required for the workload.
- Keep administrative permissions separate from application execution permissions.
- Use temporary AWS credentials through standard credential providers or workload roles.
- Never place long-lived AWS credentials in the repository.

### Data authorization
RAG does not replace authorization. A relevant document can still be inappropriate for a given user. In a production design, document-level or tenant-level authorization should be applied before sensitive content reaches the model or user.

### Prompt injection
Retrieved documents must be treated as untrusted input. Mitigations include controlled ingestion, source governance, prompt design, output validation, least-privilege tool access, and guardrails.

### Sensitive information
- Classify data before ingestion.
- Minimize sensitive data in prompts and logs.
- Encrypt source data and application/session data according to organizational requirements.
- Define retention and deletion controls for source content and telemetry.

### Output validation
Generated text should be treated as advisory unless the workflow includes deterministic validation. AI output alone should not approve access, modify production data, change configurations, or initiate high-impact actions.

## Availability and operations
- Handle Bedrock throttling and service errors gracefully.
- Add retries with bounded exponential backoff for production clients where appropriate.
- Monitor request errors and latency.
- Test knowledge-base synchronization and document freshness.
- Maintain versioned, approved source content.

## Interview architecture summary

The core design separates trusted system controls from the probabilistic model. IAM and application logic control access, approved source systems control available knowledge, Bedrock performs retrieval and generation, and the final answer remains subject to validation before privileged action.
