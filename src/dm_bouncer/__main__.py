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

        # Reset the exception counter on every successful run
        global exception_count
        exception_count = 0


exception_count = 0


if __name__ == "__main__":
    while True:
        try:
            run_loop()

        except Exception as e:
            traceback.print_exception(e)
            exception_count += 1
            if exception_count > 10:
                print("Max exception count exceeded! Quitting service.")
                raise e

        # Sleep for between 10 to 600 seconds
        sleep_time = 10 * exception_count**2
        if sleep_time > 600:
            sleep_time = 600
        print(
            f"Exception count: {exception_count}\n"
            f"Restarting in {sleep_time} seconds..."
        )
        time.sleep(sleep_time)
        print("Restarting...")
