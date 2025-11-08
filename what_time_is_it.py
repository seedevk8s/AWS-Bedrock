import boto3
from functions import get_current_time, tool_config


client = boto3.client("bedrock-runtime", region_name="us-east-1")
model_id = "amazon.nova-micro-v1:0"
system_prompt = "당신은 친절한 AI 비서로, 모든 질문에 대해 한국어로 답변합니다."


messages = []


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


    response = client.converse(
        modelId=model_id,
        system=[{"text": system_prompt}],
        messages=messages,
        toolConfig=tool_config,
    )
    print(response)
    print()


