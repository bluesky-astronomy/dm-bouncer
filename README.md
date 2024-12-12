# DM (direct message) bouncer

A direct message 'bouncing' service for limited group DMs. Intended for communication for moderators on the Astronomy feed.


## Developing

### Installing

1. Download the module with

```bash
git clone https://github.com/bluesky-astronomy/dm-bouncer.git
```

2. Ensure that you have uv installed to manage Python (see the [development guide](https://github.com/bluesky-astronomy/development-guide))

3. Set up the environment variables (see below)

4. Start the bot with:

```bash
uv run -m dm_bouncer
```

### Environment variables

To run the DM bouncer, you'll need to set the following environment variables.

**Mandatory:**
* `DM_BOUNCER_HANDLE` - the handle of the account (without an @). E.g.: "joebloggs.bsky.social".
* `DM_BOUNCER_PASSWORD` - an app password for the account.

**Mandatory in development:**
* `DM_BOUNCER_ACCOUNTS` - a string with comma-separated DIDs of users to send messages to.

**Mandatory in production:**
* `ASTROFEED_PRODUCTION` - set to True to automatically DM all moderators.

**Optional:**
* `DM_BOUNCER_CHECK_TIME` - how often to check for new messages (default: 60 seconds)
* `DM_BOUNCER_MINIMUM_MOD_LEVEL` - minimum mod level in production to be included in the DM bouncing circle (default: 1, the lowest)
