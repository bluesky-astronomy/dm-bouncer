import time
import traceback
from .message import get_unread_messages, broadcast_new_messages
from astrofeed_lib.client import get_client
from .config import (
    DM_BOUNCER_HANDLE,
    DM_BOUNCER_PASSWORD,
    DM_BOUNCER_CHECK_TIME,
    DM_BOUNCER_ACCOUNTS,
    ASTROFEED_PRODUCTION,
    DM_BOUNCER_MINIMUM_MOD_LEVEL,
    cached_moderator_list,
)


def run():
    """Runs the DM bouncer once."""
    # Grab & set up our client
    client = get_client(DM_BOUNCER_HANDLE, DM_BOUNCER_PASSWORD)
    dm_client = client.with_bsky_chat_proxy()

    # Work out which accounts we need to DM (which is DM_BOUNCER_ACCOUNTS plus 
    # optionally the moderators)
    accounts_to_dm = DM_BOUNCER_ACCOUNTS.copy()
    if ASTROFEED_PRODUCTION:
        accounts_to_dm.update(
            cached_moderator_list.get_accounts_above_level(DM_BOUNCER_MINIMUM_MOD_LEVEL)
        )

    # Handle receiving & sending messages to the group
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
        time.sleep(DM_BOUNCER_CHECK_TIME)


if __name__ == "__main__":

    while True:
        try:
            run_loop()

        # Todo do we really want to catch all exceptions? Eventually will be better to have a service that auto-restarts
        except Exception as e:
            print(f"EXCEPTION: {e}")
            print(traceback.format_exception(e))
            print("Waiting 60 seconds...")
            time.sleep(60)
            print("Restarting...")
