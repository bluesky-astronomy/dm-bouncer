import time
from .message import get_unread_messages, broadcast_new_messages
from astrofeed_lib.client import get_client
from .config import (
    HANDLE,
    PASSWORD,
    DM_CHECK_TIME,
    DM_GROUP,
    ADD_OTHER_MODERATORS,
    MINIMUM_MOD_LEVEL,
    CACHED_MODERATOR_LIST,
)


def run():
    """Runs a single instance of the DM bouncer."""
    client = get_client(HANDLE, PASSWORD)
    dm_client = client.with_bsky_chat_proxy()
    accounts_to_dm = DM_GROUP.copy()
    if ADD_OTHER_MODERATORS and MINIMUM_MOD_LEVEL < 5:
        accounts_to_dm.update(
            CACHED_MODERATOR_LIST.get_accounts_above_level(MINIMUM_MOD_LEVEL)
        )

    updated_convos, new_messages, message_convo_mapping = get_unread_messages(
        dm_client, accounts_to_dm
    )
    broadcast_new_messages(
        dm_client, accounts_to_dm, updated_convos, new_messages, message_convo_mapping
    )


def run_loop():
    """Runs the DM bouncer indefinitely until stopped."""
    while True:
        print("Bouncing DMs...")
        run()
        print("Sleeping...")
        time.sleep(DM_CHECK_TIME)


if __name__ == "__main__":
    run_loop()
