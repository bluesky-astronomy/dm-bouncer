import os
from atproto import IdResolver


# -------------------------
# ENVIRONMENT VARIABLES
# -------------------------
# Whether or not we're in production mode. Production mode will cause all moderators to
# be added to the DM group automatically.
ASTROFEED_PRODUCTION = bool(os.getenv("ASTROFEED_PRODUCTION", False))

# Login details for the bot.
DM_BOUNCER_HANDLE = os.getenv("DM_BOUNCER_HANDLE", None)
DM_BOUNCER_PASSWORD = os.getenv("DM_BOUNCER_PASSWORD", None)

# Comma-separated string of DIDs of users who will always receive DMs.
# Todo validate that all are correct DIDs
DM_BOUNCER_ACCOUNTS = set(os.getenv("DM_BOUNCER_ACCOUNTS", "").split(","))

# How often to check DMs (in seconds)
# (~60 seconds recommended for politeness to Bluesky)
DM_BOUNCER_CHECK_TIME = int(os.getenv("DM_BOUNCER_CHECK_TIME", 60))

# If feed moderators are added, this is the minimum level they need to have
DM_BOUNCER_MINIMUM_MOD_LEVEL = int(os.getenv("DM_BOUNCER_MINIMUM_MOD_LEVEL", 1))


# -------------------------
# ADDING MODS (PRODUCTION ONLY)
# -------------------------
cached_moderator_list = None
if ASTROFEED_PRODUCTION:
    # Avoid this import unless in prod to avoid requiring a database
    from astrofeed_lib.accounts import CachedModeratorList

    cached_moderator_list = CachedModeratorList(query_interval=60)


# -------------------------
# FINAL CHECKS & DEFAULTS
# -------------------------
# Checks
if not DM_BOUNCER_HANDLE:
    raise ValueError("You must set the DM_BOUNCER_HANDLE environment variable")
if not DM_BOUNCER_PASSWORD:
    raise ValueError("You must set the DM_BOUNCER_PASSWORD environment variable")
if not ASTROFEED_PRODUCTION and len(DM_BOUNCER_ACCOUNTS) == 0:
    raise ValueError(
        "DM bouncer does not appear to be in production mode; hence, you must set the"
        "DM_BOUNCER_ACCOUNTS environment variable for the DM bouncer to do anything."
    )

# Other default objects
id_resolver = IdResolver()
