from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_community.chat_message_histories import ChatMessageHistory


model = ChatBedrock(model_id="amazon.nova-micro-v1:0")


chat_history = ChatMessageHistory()
chat_history.add_message(SystemMessage(content="당신은 사용자를 도와주는 친절한 상담사입니다."))


while True:
    user_input = input("사용자: ")
    if user_input.lower() == "exit":
        break


    chat_history.add_message(HumanMessage(content=user_input))
    ai_message = model.stream(chat_history.messages)
    # chat_history.add_ai_message(ai_message)


    print(f"상담사: ", end="")
    ai_message_all = ""
    for chunk in ai_message:
        #print(chunk)
        print(chunk.text, end="|", flush=True)
        ai_message_all += chunk.text
    print("\n")
    chat_history.add_ai_message(AIMessage(content=ai_message_all))




    print(">" * 50)
    for i, msg in enumerate(chat_history.messages):
        print(f"{i:<3} {msg.__class__.__name__:<15} {msg.content[:50]}")
    print("<" * 50)
    print()