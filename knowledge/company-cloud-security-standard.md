# Company Cloud Security Standard

## Purpose
This sample document represents approved enterprise content that can be ingested into an Amazon Bedrock Knowledge Base for a RAG demonstration.

## Production access
Before an application receives access to production data, the responsible team must verify:

1. The application has a documented business owner and approved purpose.
2. The workload identity uses least-privilege permissions.
3. Production access is separated from development and test access.
4. Sensitive data is classified and handled according to company policy.
5. Encryption is enabled in transit and at rest where required.
6. Security-relevant activity is logged and available for monitoring.
7. Secrets and credentials are stored in approved services rather than source code.
8. The change has completed the applicable testing and approval process.

## IAM guidance
Use workload roles and temporary credentials whenever possible. Avoid long-lived access keys. Permissions should be limited to the actions and resources the workload needs. Administrative permissions should not be assigned to normal application execution roles.

## Generative AI workloads
Generative AI applications must not use model output as an authorization decision. Applications that use retrieval-augmented generation must still enforce user and data authorization outside the language model. Retrieved content should be considered input to the model and should be governed like other enterprise data.

## Logging
Do not log sensitive prompt or retrieved-document content unless there is a documented business and security requirement. Prefer operational metrics, error details, request identifiers, latency, and security events while minimizing sensitive content.

## High-impact actions
AI-generated recommendations may assist users, but high-impact changes to production systems, access, security configuration, or business-critical data require deterministic controls and the appropriate human or workflow approval.
