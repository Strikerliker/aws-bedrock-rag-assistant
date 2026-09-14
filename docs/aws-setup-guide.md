# AWS Setup Guide

This guide describes one practical way to make the portfolio project runnable in an AWS account. Exact console labels can change over time, so use the current Amazon Bedrock console and documentation when implementing the environment.

## 1. Prepare approved documents

Start with the sample files under `knowledge/` or your own non-sensitive demonstration documents. Create an S3 bucket dedicated to the RAG data source with Block Public Access and encryption enabled, and restrict access to required principals and the Bedrock service role. Upload the approved knowledge documents.

## 2. Select Bedrock model access

Choose a supported foundation model or inference profile available to your account and region. Record its ARN for `BEDROCK_MODEL_ARN`.

## 3. Create a Bedrock Knowledge Base

1. Create a Knowledge Base in Amazon Bedrock.
2. Configure an appropriate Bedrock service role.
3. Select the S3 bucket/prefix containing the approved documents.
4. Configure the embeddings/vector-store options offered for your account and region.
5. Create the data source.
6. Synchronize the data source.
7. Record the Knowledge Base ID.

## 4. Configure the application identity

The local AWS identity or deployed workload role must be permitted to call the Bedrock runtime operation required by the application. `iam-policy-example.json` shows the application actions used by the sample code.

Do not place access keys in `.env` or source code. Use an AWS CLI/SDK profile, IAM Identity Center session, or workload role.

## 5. Configure environment variables

Copy `.env.example` to `.env` and supply your Knowledge Base ID and model/inference-profile ARN.

## 6. Install and run

```bash
python -m venv .venv
pip install -r requirements.txt
python app.py
```

For the UI:

```bash
streamlit run streamlit_app.py
```

## 7. Demo validation

Ask questions directly answerable from the uploaded sample documents. Confirm the generated answer matches source content, source references are returned, unrelated questions do not confidently fabricate company policy, and conversational sessions work when the returned session ID is reused.

## 8. Production hardening discussion

For an interview, discuss Cognito or enterprise federation, document-level authorization, KMS/data-retention requirements, API Gateway/Lambda or containers, WAF/rate limiting, CloudWatch monitoring, prompt-injection testing, model/KB evaluation, Bedrock Guardrails, private networking where required, and formal data-classification and ingestion controls.
