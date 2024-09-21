import os
from atproto import IdResolver
from astrofeed_lib.accounts import CachedModeratorList


# Login details for the bot
HANDLE = os.getenv("DM_BOUNCER_HANDLE", None)
PASSWORD = os.getenv("DM_BOUNCER_PASSWORD", None)

# How often to check DMs (in seconds)
# (~60 seconds recommended for politeness to Bluesky)
DM_CHECK_TIME = 60

# Hard-coded users who will always receive DMs
DM_GROUP = {
    "did:plc:jcoy7v3a2t4rcfdh6i4kza25",  # emily.space
    # "did:plc:fe7v6gvpput3klm5wbjqotbi",  # testing.astronomy.blue
    "did:plc:hol3fzmh4guugasdolbpzwtk",  # bot.astronomy.blue
}

# Whether or not to also add feed moderators to the DM group (set to False for testing)
ADD_OTHER_MODERATORS = os.getenv("DM_BOUNCER_ADD_MODERATORS", True)

# If feed moderators are added, this is the minimum level they need to have
MINIMUM_MOD_LEVEL = 1


# Checks
if not HANDLE:
    raise ValueError("You must set the DM_BOUNCER_HANDLE environment variable")
if not PASSWORD:
    raise ValueError("You must set the DM_BOUNCER_PASSWORD environment variable")


# Other default objects
ID_RESOLVER = IdResolver()
CACHED_MODERATOR_LIST = CachedModeratorList(query_interval=60)
