# Can be called by main.py (bot) to add new subscribers to the json list
# Can be called by post_current_missions or post_current_maelstroms to get current subscribers, so they can send out mission updates

import json

filename = 'data/subscriptions.json'


def get_subscriptions():
    with open(filename, 'r') as filehandle:
        subscriptions = json.load(filehandle)
    return subscriptions


def write_subscriptions(subs={}):
    with open(filename, 'w') as filehandle:
        json.dump(subs, filehandle, indent=6)


def subscribe(channel_id=str, guild_name=str, owner_id=str):
    subs = get_subscriptions()
    if str(channel_id) in subs:
        return 'Channel already subscribed'
    else:
        subs[channel_id] = {"channel_id": str(channel_id), "guild_name": guild_name, "owner_id": str(owner_id)}
        write_subscriptions(subs)
        return ":first_quarter_moon: **Channel subscribed!** Every hour the bot will post fresh Maelstrom missions here.\n" \
               "Use the mod ManyMoreTries to play any mission less than 24h old."


def unsubscribe(channel_id=str):
    subs = get_subscriptions()
    if str(channel_id) not in subs:
        return "This channel is not subscribed"
    else:
        del subs[str(channel_id)]
        write_subscriptions(subs)
        return ":new_moon: **Channel unsubscribed**"
