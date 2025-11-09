import boto3
from functions2 import get_current_time, tool_config
from what_time_is_it5 import get_ai_response, messages
import streamlit as st


# Streamlit 앱 설정
st.title("🗨️ Chatbot")
st.write("나는 당신의 AI 비서입니다. 무엇을 도와드릴까요?")
st.markdown("---")


# 초기 메시지 설정
if "messages" not in st.session_state:
    st.session_state.messages = []


# 대화 내용 출력
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


# 사용자 입력 처리
if user_input := st.chat_input():


    # 질문 출력 및 저장
    st.chat_message("user").write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})


    messages.append(
        {
            "role": "user",
            "content": [{"text": user_input}],
        }
    )
    response = get_ai_response()
    output_message = response["output"]["message"]
    messages.append(output_message)


    # 도구 사용이 요청된 경우 => 도구를 호출하고 결과를 모델에 다시 전송
    if response["stopReason"] == "tool_use":
        # 모든 도구 실행 결과를 저장할 리스트
        tool_results_list = []
        tool_requests = response["output"]["message"]["content"]
        for tool_request in tool_requests:
            if "toolUse" in tool_request:
                tool = tool_request["toolUse"]


                if tool["name"] == "get_current_time":
                    # 함수 호출에 필요한 인자값을 응답에서 추출
                    timezone = tool["input"].get("timezone", "Asia/Seoul")
                    tool_result = {
                        "toolUseId": tool["toolUseId"],
                        "content": [
                            {
                                "json": {
                                    "current_time": get_current_time(timezone=timezone)
                                }
                            }
                        ],
                    }
                    # 도구 실행 결과를 추가
                    tool_results_list.append({"toolResult": tool_result})


        # 모든 도구 실행 결과를 하나의 user 메시지로 묶어서 모델에 전달
        if tool_results_list:
            tool_result_message = {
                "role": "user",
                "content": tool_results_list,
            }
            messages.append(tool_result_message)


            # 함수 호출 결과를 모델에 다시 전송
            response = get_ai_response()
            output_message = response["output"]["message"]
            messages.append(output_message)


    # 답변 출력 및 저장
    for content in output_message["content"]:
        st.chat_message("assistant").write(content["text"])
        st.session_state.messages.append(
            {"role": "assistant", "content": content["text"]}
        )


