from astrofeed_lib import logger
from atproto import Client

# TODO: refactor code in this module into methods (currently a mess)


def get_unread_messages(dm_client: Client, accounts: set) -> tuple[dict, list]:
    """Fetches all unread messages from accounts in the DM bouncing group."""
    # Grab valid conversations with unread messages, i.e. those with:
    # - One member
    # - In the broadcast group (the set 'accounts')
    # - Unread messages
    logger.debug("Fetching views of all conversations to check")
    convos_list = dm_client.chat.bsky.convo.list_convos()
    valid_convos = dict()
    for convo in convos_list.convos:
        logger.debug("Fetching unread messages")
        single_conversation = len(convo.members) == 2
        in_broadcast_group = (
            convo.members[0].did in accounts or convo.members[1].did in accounts
        )
        has_unread_messages = convo.unread_count > 0
        if single_conversation and in_broadcast_group and has_unread_messages:
            valid_convos[convo.id] = convo

    # Fetch all unread messages in these conversations
    logger.debug(f"Fetching unread messages in {len(valid_convos)} conversations")
    unread_messages = []
    message_convo_mapping = dict()
    for convo_id, convo in valid_convos.items():
        # TODO: need to fetch items recursively if convo.unread_count > 100.
        response = dm_client.chat.bsky.convo.get_messages(
            params=dict(convo_id=convo_id, limit=convo.unread_count)
        )
        unread_messages.extend(response.messages)
        message_convo_mapping.update(
            **{message.id: convo_id for message in response.messages}
        )

    # Sort the messages into sent order
    # Source: https://stackoverflow.com/a/403426
    unread_messages_sorted = sorted(
        unread_messages, key=lambda x: x.sent_at, reverse=False
    )

    return valid_convos, unread_messages_sorted, message_convo_mapping


def broadcast_new_messages(
    dm_client: Client,
    accounts: set,
    updated_convos: dict,
    messages: list,
    message_convo_mapping: dict[str, str],
):
    """Broadcasts all new messages to the DM bouncing group."""
    if len(messages) == 0:
        logger.info("No messages found to broadcast")
        return

    logger.info(f"Broadcasting messages (total unreads = {len(messages)})")
    # Format the text in received messages
    messages_text = format_message_text(updated_convos, messages)

    # Setup the full list of all messages to send out
    # TODO: convo IDs should be cached. This would reduce request load.
    all_convos = [
        dm_client.chat.bsky.convo.get_convo_for_members(
            params=dict(members=[did])
        ).convo
        for did in accounts
    ]

    messages_to_send = []
    for convo in all_convos:
        all_dids_in_convo = {member.did for member in convo.members}

        # For every message, only add it as one to send to this convo if it isn't from
        # it originally! This also prevents sending something multiple times.
        for message, message_formatted in zip(messages, messages_text):
            if message.sender.did not in all_dids_in_convo:
                messages_to_send.append(
                    dict(convo_id=convo.id, message=dict(text=message_formatted))
                )

    if len(messages_to_send) == 0:
        logger.warning("-> no messages are valid to broadcast")
        update_read_status(dm_client, messages, message_convo_mapping)
        return
    
    logger.info(f"-> found {len(messages_to_send)} messages to broadcast")

    # Sort the messages into batches of upto 100 in length (current ATProto limit)
    message_batches = []
    while len(messages_to_send) > 0:
        message_batches.append(messages_to_send[:100])
        messages_to_send = messages_to_send[100:]

    # Send the messages!
    # N.B.: messages with identical text ae usually soft-rejected by the server (seems
    # to be anti-spam)
    for batch in message_batches:
        logger.info("Sending batch of messages...")
        dm_client.chat.bsky.convo.send_message_batch(data=dict(items=batch))

    # Update the read status on the client
    update_read_status(dm_client, messages, message_convo_mapping)


def update_read_status(
    dm_client: Client, messages: list, message_convo_mapping: dict[str, str]
):
    """Updates the read status of conversations in the DM bouncing group to the
    latest point.
    """
    logger.debug("Updating message read status")

    # Get the most recent read message in each convo. This works because it's in
    # ascending time order, so the last message we assign to each convo is hence the
    # last one we saw
    highest_read_status = dict()
    for message in messages:
        highest_read_status[message_convo_mapping[message.id]] = message.id

    # Update the convos on Bluesky
    for convo_id, message_id in highest_read_status.items():
        dm_client.chat.bsky.convo.update_read(
            data=dict(convo_id=convo_id, message_id=message_id)
        )


def format_message_text(updated_convos: dict, messages: list) -> list[str]:
    """Formats text of a message to include the account name, handle, and time sent."""
    logger.debug("Formatting message text")

    # Firstly, make a dict of did: name & handle mappings
    did_name_mappings = {}
    for convo in updated_convos.values():
        for member in convo.members:
            did_name_mappings[member.did] = f"{member.display_name} (@{member.handle})"

    # Then, format the messages!
    messages_formatted = []
    for message in messages:
        name = did_name_mappings[message.sender.did]
        messages_formatted.append(f"{name}:\n{message.text}")

    return messages_formatted
