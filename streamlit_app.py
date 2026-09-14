import streamlit as st

from app import ConfigurationError, ask

st.set_page_config(page_title="Amazon Bedrock RAG Assistant", page_icon="☁️")
st.title("Amazon Bedrock RAG Assistant")
st.caption("Grounded enterprise answers using Amazon Bedrock Knowledge Bases")

if "session_id" not in st.session_state:
    st.session_state.session_id = None

question = st.text_area(
    "Ask a question about the approved knowledge base",
    placeholder="Example: What controls should be verified before production access is granted?",
    height=110,
)

if st.button("Ask Bedrock", type="primary"):
    if not question.strip():
        st.warning("Enter a question first.")
    else:
        with st.spinner("Retrieving approved context and generating an answer..."):
            try:
                result = ask(question, session_id=st.session_state.session_id)
                st.session_state.session_id = result.get("session_id")
                st.subheader("Grounded answer")
                st.write(result.get("answer") or "No answer returned.")
                sources = result.get("sources", [])
                st.subheader("Sources")
                if not sources:
                    st.info("No source locations were returned for this response.")
                else:
                    for index, source in enumerate(sources, start=1):
                        st.write(f"{index}. {source['label']}")
                with st.expander("Security notes"):
                    st.write(
                        "The application does not embed AWS credentials. Use an approved AWS "
                        "credential provider or workload role and apply least-privilege IAM. "
                        "Generated output should be validated before it drives privileged or "
                        "business-critical actions."
                    )
            except ConfigurationError as exc:
                st.error(str(exc))
            except Exception as exc:
                st.error(f"Request failed: {exc}")
