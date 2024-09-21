import time
from .message import get_unread_messages, broadcast_new_messages
from astrofeed_lib.client import get_client
from .config import HANDLE, PASSWORD, DM_CHECK_TIME, DM_GROUP, ADD_OTHER_MODERATORS, MINIMUM_MOD_LEVEL


def run():
    """Runs a single instance of the DM bouncer."""
    client = get_client(HANDLE, PASSWORD)
    dm_client = client.with_bsky_chat_proxy()
    accounts_to_dm = DM_GROUP.copy()
    if ADD_OTHER_MODERATORS and MINIMUM_MOD_LEVEL < 5:
        raise NotImplementedError("Not currently ")
    
    updated_convos, new_messages = get_unread_messages(dm_client, accounts_to_dm)
    print(new_messages)
    broadcast_new_messages(dm_client, accounts_to_dm, updated_convos, new_messages)


def run_loop():
    """Runs the DM bouncer indefinitely until stopped."""
    while True:
        run()
        time.sleep(DM_CHECK_TIME)


if __name__ == "__main__":
    run()
