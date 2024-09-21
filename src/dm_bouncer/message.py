def get_unread_messages(dm_client, accounts: set) -> tuple[dict, list]:
    # Grab valid conversations with unread messages, i.e. those with:
    # - One member
    # - In the broadcast group (the set 'accounts')
    # - Unread messages
    convos_list = dm_client.chat.bsky.convo.list_convos()
    valid_convos = dict()
    for convo in convos_list.convos:
        single_conversation = len(convo.members) == 2
        in_broadcast_group = (
            convo.members[0].did in accounts or convo.members[1].did in accounts
        )
        has_unread_messages = convo.unread_count > 0
        if single_conversation and in_broadcast_group and has_unread_messages:
            valid_convos[convo.id] = convo

    # Fetch all unread messages in these conversations
    unread_messages = []
    for convo_id, convo in valid_convos.items():
        # TODO: need to fetch items recursively if convo.unread_count > 100.
        response = dm_client.chat.bsky.convo.get_messages(
            params=dict(convo_id=convo_id, limit=convo.unread_count)
        )
        unread_messages.extend(response.messages)

    # Sort the messages into sent order
    # Source: https://stackoverflow.com/a/403426
    unread_messages_sorted = sorted(
        unread_messages, key=lambda x: x.sent_at, reverse=False
    )

    return valid_convos, unread_messages_sorted


def broadcast_new_messages(
    dm_client, accounts: set, updated_convos: dict, messages: dict
):
    # Format the text in received messages
    
    pass
