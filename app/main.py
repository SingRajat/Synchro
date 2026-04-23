from app.orchestrator.pipeline import Msg_History

while True:
    user_input=input("You: ")
    
    if user_input.lower() in ["exit", "quit"]:
        print("Chat is Closing....")
        break

    response=Msg_History.invoke(
        {"input":user_input},
        config={"configurable":{"session_id":"Chat_1"}}
        )
    print("-------------------------")
    print("AI: ", response.content)
    print("-------------------------")

