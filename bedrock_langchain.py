from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage


# Bedrock 모델 설정
llm = ChatBedrock(model_id="amazon.titan-text-express-v1")


# 프롬프트 메시지 정의
prompt_message = [
    HumanMessage(content="Amazon Bedrock 강의를 듣고 있는 수강생들에게 응원의 말을 한 문장으로 해줘.")
]


# 모델을 호출해 응답 받기
response = llm.invoke(prompt_message)


# 응답 출력
print(response)
print(response.content)