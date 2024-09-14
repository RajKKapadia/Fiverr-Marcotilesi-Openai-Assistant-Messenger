def format_messages(messages: list[dict[str, any]]) -> list[dict[str, str]]:
    formatted_messages = []
    for m in messages:
        formatted_messages.append({
            "role": "user",
            "content": m['query']
        })
        formatted_messages.append({
            "role": "assistant",
            "content": m['response']
        })
    return formatted_messages
