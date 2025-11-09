import boto3
from functions2 import get_current_time, tool_config


client = boto3.client("bedrock-runtime", region_name="us-east-1")
model_id = "amazon.nova-micro-v1:0"
system_prompt = "당신은 친절한 AI 비서로, 모든 질문에 대해 한국어로 답변합니다."


# 대화 내용을 기록할 리스트
messages = []




# 모델에 질의하고 질의 결과를 반환하는 함수
def get_ai_response():
    print("messages >>> ...")
    for i, msg in enumerate(messages):
        print(f"{i}\t{msg}")
    print()


    response = client.converse(
        modelId=model_id,
        system=[{"text": system_prompt}],
        messages=messages,
        toolConfig=tool_config,
    )


    print("... >>> response.output.message")
    print(response["output"]["message"])
    print()


    return response


while True:
    user_input = input("사용자 >>> ")
    if user_input.lower() in ["종료", "exit", "quit"]:
        print("대화를 종료합니다.")
        break


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


        # 모든 도구의 실행 결과를 저장할 리스트
        tool_results_list = []


        tool_requests = response["output"]["message"]["content"]
        for tool_request in tool_requests:
            if "toolUse" in tool_request:
                tool = tool_request["toolUse"]


                if tool["name"] == "get_current_time":
                    timezone = tool["input"].get("timezone", "Asiz/Seoul")
                    tool_result = {
                        "toolUseId": tool["toolUseId"],
                        "content": [{"json": {"current_time": get_current_time(timezone=timezone)}}],
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


    # 최종 응답 출력
    for content in output_message["content"]:
        print(f"AI >>> {content['text']}\n")



