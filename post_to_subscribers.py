# Posts a message to all subscribers
# When this is invoked directly (as main), then it'll post current missions - to be removed?

import requests
import os
from dotenv import load_dotenv

import mission_manager
import subscription_manager
from base_logger import logger


def get_session():
    load_dotenv()
    token = os.getenv("TOKEN")
    headers = {'Authorization': f'Bot {token}'}
    session = requests.Session()
    session.headers.update(headers)
    return session


def post_to_channel(message=str, channel_id=str, session=get_session()):
    try:
        response = session.post(
            f"https://discord.com/api/v6/channels/{channel_id}/messages",
            headers=session.headers,
            json={"content": message}
        )
        logger.info(f'{response} for channel id {channel_id}')
    except requests.exceptions.HTTPError as errh:
        logger.error(errh)
    except requests.exceptions.ConnectionError as errc:
        logger.error(errc)
    except requests.exceptions.Timeout as errt:
        logger.error(errt)
    except requests.exceptions.RequestException as err:
        logger.error(err)


def post_to_all_subscribers(message=str):
    session = get_session()
    subscribed_channel_list = subscription_manager.get_subscriptions()

    for channel_id in subscribed_channel_list:
        post_to_channel(message, channel_id, session)
    logger.info(f'Messages posted to subscribed channels')


#Run when script is called
if __name__ == '__main__':
    message = mission_manager.get_current_missions()
    if not message:
        logger.info('No tough missions on the board. Aborting auto-post.')
        exit()
    else:
        post_to_all_subscribers(message)
