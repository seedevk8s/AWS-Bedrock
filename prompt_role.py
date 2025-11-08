import boto3
from botocore.exceptions import ClientError




def query_to_ai(role_desc):
    client = boto3.client("bedrock-runtime", region_name="us-east-1")
    model_id = "amazon.nova-micro-v1:0"
    conversation = [
        {
            "role": "user",
            "content": [{"text": "세상에서 누가 제일 이쁘지?"}],
        },
    ]


    try:
        response = client.converse(
            modelId=model_id,
            system=[{"text": role_desc}],
            messages=conversation,
            inferenceConfig={"maxTokens": 1000, "temperature": 0.9},
        )
        response_text = response["output"]["message"]["content"][0]["text"]


        print(f"User >>>\n{role_desc.strip()}\n")
        print(f"<<< AI\n{response_text.strip()}\n")
    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")




if __name__ == "__main__":
    role = "당신은 동화 백설공주에 나오는 마법 거울입니다."
    query_to_ai(role)


    role = "당신은 여대를 다니는 22살 아가씨 입니다."
    query_to_ai(role)