from app.models import db, Message, Chat
from app.functions.openai.utils.remove_whitspace import remove_whitespace


def save_chat(messages, user):  
    # Create Chat object and assign to current user
    chat = Chat(user_id = user.id)    

    # Add Chat to the database
    db.session.add(chat)
    db.session.commit()

    # Create Message objects for all messages in the Chat & assign to the new Chat object
    for message in messages:
        # Don't upload "system messages" to the database (i.e. the header of the prompt)
        # To see any changes to the prompt header over time, check the Github commit history 
        # for the file called "get_openai_prompt_header.py"
        if message["role"] != "system":
            message = Message(
                role = str(message["role"]),
                content = remove_whitespace(str(message.get("content") or None)),
                function_name = str(message.get("function_name") or None),
                function_call = str(message.get("function_call") or None),
                chat_id = chat.id
            )
            db.session.add(message)

    # Add Messages to the database
    db.session.commit()
    