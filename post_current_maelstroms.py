# Posts current maelstrom missions to all subscribed channels via discord http API
# Invoked every 60 minutes via cronjob

import requests
import os
from dotenv import load_dotenv

import mission_manager
import subscription_manager
from base_logger import logger

def post_to_all_subscribers(message=str):
    load_dotenv()
    token = os.getenv("TOKEN")
    headers = {'Authorization': f'Bot {token}'}
    session = requests.Session()
    session.headers.update(headers)

    subscribed_channel_list = subscription_manager.get_subscriptions()

    for channel_id in subscribed_channel_list:
        try:
            response = session.post(
                f"https://discord.com/api/v6/channels/{channel_id}/messages",
                headers=headers,
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
    logger.info(f'Messages posted to subscribed channels')


#Run when script is called
if __name__ == '__main__':
    message = mission_manager.get_current_maelstroms()
    if not message:
        logger.info('No maelstroms on the board. Aborting auto-post.')
        exit()
    else:
        post_to_all_subscribers(message)

# post_to_all_subscribers(":warning:-----Maintenance-----:warning:\nWe're currently experiencing trouble accessing the darkti.de mission board.\nPlease hang tight while we're exploring our options. Reach out to @lukzenn for any questions or feedback. The Emperor protects.")