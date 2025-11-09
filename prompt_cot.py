import boto3
from botocore.exceptions import ClientError




def query_to_ai(prompt_type, question):
    print(f"{prompt_type}\n{'=' * 50}")


    client = boto3.client("bedrock-runtime", region_name="us-east-1")
    model_id = "amazon.nova-micro-v1:0"
    conversation = [
        {
            "role": "user",
            "content": [{"text": question}],
        }
    ]


    try:
        response = client.converse(
            modelId=model_id,
            messages=conversation,
            inferenceConfig={"maxTokens": 1000, "temperature": 0.5},
        )
        response_text = response["output"]["message"]["content"][0]["text"]


        print(f"User >>>\n{question.strip()}\n")
        print(f"<<< AI\n{response_text.strip()}\n")
    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")




if __name__ == "__main__":
    prompt_type = "Zero-shot prompting"
    prompt = "우주와 신"
    query_to_ai(prompt_type, prompt)


    prompt_type = "Few-shot prompting"
    prompt = """### 예시 ###
Q. 사과
A. 사과 색은 RED 입니다.
Q. 바나나
A. 바나나 색은 YELLOW 입니다.


Q. 무지개"""
    query_to_ai(prompt_type, prompt)


    # 언어 모델이 발전함에 따라 CoT 기법이 기본적으로 적용되어 있는 경우가 많음
    prompt_type = "CoT(Chain of Thought) prompting"
    prompt = """다음 문제를 풀어 보세요:
한 가게에서 사과 3개에 1,500원, 배 2개에 2,000원을 받습니다.
사과 5개와 배 3개를 사려면 얼마가 필요할까요?"""
    query_to_ai(prompt_type, prompt)