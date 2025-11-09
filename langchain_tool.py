#1 언어 모델 선언
from langchain_aws import ChatBedrock


llm = ChatBedrock(model_id="amazon.nova-micro-v1:0")




#2 get_current_time 함수를 정의하고 랭체인에 도구로 추가
# 문서화 문자열(docstring)을 이용해 함수의 기능과 입력값, 사용 방법을 랭체인에 알려 줌
import pytz
from datetime import datetime
from langchain_core.tools import tool


@tool
def get_current_time(timezone: str, location: str) -> str:
    """
    현재 시간을 YYYY-MM-DD HH:MI:SS 형식으로 반환하는 함수


    Args:
        timezone (str): 타임존(예: "Asia/Seoul"). 실제 존재해야 함.
        location (str): 지역명. 타임존은 모든 지역에 대응하지 않으며, 이후 llm 답변 생성에 사용됨.
    """
    tz = pytz.timezone(timezone)
    now = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    return f"{timezone} ({location}) 현재시간 {now}"




#3 get_current_time 함수를 랭체인으로 언어 모델(llm)에 연결
# .bind_tools() 메서드를 사용해 기존에 선언한 언어 모델에 도구를 등록
tools = [get_current_time]
tool_dict = {"get_current_time": get_current_time}


# 도구를 모델에 바인딩 => 모델에 도구를 바인딩하면, 도구를 사용해 답변을 생성할 수 있음
llm_with_tools = llm.bind_tools(tools)




#4 도구를 사용해 언어 모델 답변 생성
from langchain_core.messages import HumanMessage, SystemMessage


messages = [
    SystemMessage("당신은 사용자의 질문에 답변을 하기 위해 tools를 사용할 수 있다."),
    HumanMessage("부산은 지금 몇 시야?"),
]


response = llm_with_tools.invoke(messages)
messages.append(response)


print(response)
print("-" * 50)
print(messages)
print("-" * 50)




#5 함수 실행 결과 출력
for tool_call in response.tool_calls:
    selected_tool = tool_dict[tool_call["name"]]
    print(tool_call["args"])
    print("-" * 50)
    tool_msg = selected_tool.invoke(tool_call)
    messages.append(tool_msg)


print(messages)
