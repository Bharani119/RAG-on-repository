import requests
import streamlit as st


def get_openai_response(input_text):
    response = requests.post(
        "http://localhost:8000/retrieve", json={"query": input_text}
    )

    return response.json()


## streamlit framework

st.title("Langchain Demo With OPENAI API")
input_text = st.text_input("Write an essay on")

if input_text:
    result = get_openai_response(input_text)
    st.write("### Answer:")
    st.write(result["response"]["answer"])

    with st.expander("Click to view the context behind the answer"):
        st.write(result["response"]["context"])
    st.write()
