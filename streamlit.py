import boto3
from botocore.exceptions import ClientError
import streamlit as st


st.title("💬 Chatbot")
st.caption("🚀 A Streamlit chatbot powered by Amazon Bedrock")
if "messages" not in st.session_state:
    st.session_state["conversation"] = []       # 모델에 전달할 대화 내용
    st.session_state["messages"] = []       # 화면에 출력할 대화 내용


for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])



if user_input := st.chat_input():
    client = boto3.client("bedrock-runtime", region_name="us-east-1")
    model_id = "amazon.nova-micro-v1:0"


    st.chat_message("user").write(user_input)
    st.session_state.conversation.append({"role": "user", "content": [{"text": user_input}]})
    st.session_state.messages.append({"role": "user", "content": user_input})


    response = client.converse(
        modelId=model_id,
        system=[{"text": "당신은 친절한 AI 비서입니다."}],
        messages=st.session_state.conversation,
        inferenceConfig={"maxTokens": 1000, "temperature": 0.5},
    )


    response_text = response["output"]["message"]["content"][0]["text"]
    st.chat_message("assistant").write(response_text)
    st.session_state.conversation.append({"role": "assistant", "content": [{"text": response_text}]})
    st.session_state.messages.append({"role": "assistant", "content": response_text})