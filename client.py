import requests
import streamlit as st


def get_openai_response(input_text):
    """
    This function is used to hit the FastAPI emdpoint to get the llm response and return a json reponse.
    """
    response = requests.post(
        "http://localhost:8000/retrieve", json={"query": input_text}
    )

    return response.json()


## streamlit framework

st.title("RAG on repository with Langchain and OpenAI API")
input_text = st.text_input("Type your query")

if input_text:
    result = get_openai_response(input_text)
    st.write("### Answer:")
    st.write(result["response"]["answer"])

    with st.expander("Click to view the context behind the answer"):
        st.write(set(result["github_links"]))
    st.write()
