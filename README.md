# DM (direct message) bouncer

A direct message 'bouncing' service for limited group DMs. 

This service is intended for communication for moderators of the Astronomy feed, but can be used by anyone to hack group DMs into Bluesky.

![A screenshot of the moderation chat.](https://github.com/user-attachments/assets/deedf4e0-7f10-4f46-843e-fe2b4dfa939a)


## Developing

### Installing

1. Download the module with

```bash
git clone https://github.com/bluesky-astronomy/dm-bouncer.git
```

2. Ensure that you have uv installed to manage Python (see the [development guide](https://github.com/bluesky-astronomy/development-guide) for help)

3. Set up the environment variables (see below)

4. Start the bot with:

```bash
uv run -m dm_bouncer
```

### Environment variables

To run the DM bouncer, you'll need to set the following environment variables.

**Mandatory:**
* `DM_BOUNCER_HANDLE` - the handle of the account that will bounce DMs (without an @). _Example:_ `"joebloggs.bsky.social"`.
* `DM_BOUNCER_PASSWORD` - an app password for the account. **When creating the app password, make sure it has access to DMs** (there's a checkbox.)

**Mandatory in development:**
* `DM_BOUNCER_ACCOUNTS` - a string with comma-separated DIDs of users to send messages to. At least two are required to do anything! You can look up the DID of an account [with this tool](https://bsky-debug.app/handle?handle=astronomy.blue). _Example:_ `"did:plc:jcoy7v3a2t4rcfdh6i4kza25,did:plc:ko747jc5ma4iarwwfwrlv2ct"` would bounce DMs between @emily.space and @moderation.astronomy.blue.

**Mandatory in production:**
* `ASTROFEED_PRODUCTION` - set to True to automatically DM all moderators of the astronomy feeds, in addition to the accounts specified in `DM_BOUNCER_ACCOUNTS`. Also requires separate database access specified via [astrofeed-lib](https://github.com/bluesky-astronomy/astrofeed-lib).

**Optional:**
* `DM_BOUNCER_CHECK_TIME` - how often to check for new messages (default: 60 seconds)
* `DM_BOUNCER_MINIMUM_MOD_LEVEL` - minimum mod level in production to be included in the DM bouncing circle (default: 1, the lowest)
