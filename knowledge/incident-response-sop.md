# Cloud Application Incident Response SOP

## Purpose
This sample procedure provides approved support guidance for a RAG demonstration.

## Initial triage
When a cloud application incident is reported:

1. Record the affected application, user impact, start time, and observed symptoms.
2. Determine whether the issue is isolated to one user, one service, one region, or the full application.
3. Review recent deployments, configuration changes, IAM changes, and dependency failures.
4. Check application and infrastructure monitoring for errors, latency, throttling, authorization failures, and resource exhaustion.
5. Preserve relevant logs and evidence before making destructive changes.

## Access-related failures
For an `AccessDenied` or authorization issue:

- Identify the calling principal or workload role.
- Identify the denied action and target resource.
- Confirm the intended access requirement.
- Review identity-based and resource-based policies, permission boundaries, organization policies, and relevant key policies where applicable.
- Do not solve an authorization problem by granting broad administrator access.
- Apply the smallest approved permission change and retest.

## Generative AI / RAG failures
For a RAG application:

- Confirm that the knowledge base is available and synchronized.
- Confirm that the expected document exists in the approved data source.
- Check whether the query should have access to the requested information.
- Review retrieval quality before assuming the foundation model is at fault.
- Verify that the configured model or inference profile is available in the selected region.
- Check for throttling or service errors.
- Validate the answer against the retrieved source content before treating it as authoritative.

## Escalation
Escalate immediately for suspected credential compromise, unauthorized data exposure, persistent production outage, unexplained security-control failure, or any event that meets the organization's incident severity threshold.

## Closure
Document the root cause, corrective action, validation performed, residual risk, and any preventive follow-up. Update approved runbooks or knowledge content if the incident exposed a recurring support gap.
