def get_subscriptions():
    with open('subscriptions.txt', 'r') as filehandle:
        subscriptions = [sub_id.rstrip() for sub_id in filehandle.readlines()]
    return subscriptions

def write_subscriptions(subs=[]):
    with open('subscriptions.txt', 'w') as filehandle:
        filehandle.writelines(sub_id + '\n' for sub_id in subs)
    filehandle.close()

def subscribe(channel_id=str):
    subs = get_subscriptions()
    if str(channel_id) in subs:
        return 'Channel already subscribed'
    else:
        subs.append(str(channel_id))
        write_subscriptions(subs)
        return ":first_quarter_moon: **Channel subscribed!** Every 30 minutes the bot will check for tough missions, and post them here (if there are any)."


def unsubscribe(channel_id=str):
    subs = get_subscriptions()
    if str(channel_id) not in subs:
        return "This channel is not subscribed"
    else:
        subs.remove(str(channel_id))
        write_subscriptions(subs)
        return ":new_moon: **Channel unsubscribed**"

