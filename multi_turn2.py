import boto3
from botocore.exceptions import ClientError

# 대화 내용을 기록할 리스트
conversation = []

while True:
    user_input = input("사용자 >>> ")
    if user_input.lower() in ["종료", "exit", "quit"]:
        print("대화를 종료합니다.")
        break

    client = boto3.client("bedrock-runtime", region_name="us-east-1")
    model_id = "amazon.nova-micro-v1:0"
    # conversation = [
    #     {
    #         "role": "user",
    #         "content": [{"text": user_input}],
    #     }
    # ]

    # 사용자 입력을 대화 내용에 기록(추가) 
    conversation.append({
        "role": "user",
        "content": [{"text": user_input}],
    })

    try:
        response = client.converse_stream(
            modelId=model_id,
            system=[{"text": "당신은 친절한 AI 비서입니다."}],
            messages=conversation,
            inferenceConfig={"maxTokens": 1000, "temperature": 0.5},
        )
        
        response_text = ""
        print(f"AI비서 >>> ")    
        stream = response.get("stream")
        if stream:
            for event in stream:
                if "contentBlockDelta" in event:
                    response_text += event["contentBlockDelta"]["delta"]["text"]
                    print(event["contentBlockDelta"]["delta"]["text"], end="|", flush=True)
        print("\n")
        
        # 모델 응답을 대화 내용에 추가 
        conversation.append({
            "role": "assistant", 
            "content": [{"text": response_text}],
        })
    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
