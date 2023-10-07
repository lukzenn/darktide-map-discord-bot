# Posts current missions to all subscribed channels via discord http API.
# Invoked every 30 minutes via cronjob

import requests
import os
from dotenv import load_dotenv

import mission_manager
import subscription_manager
from base_logger import logger


# subscribed_channel_list = []
# subscribed_channel_list.append(1124526082566131753) #dorktide
# subscribed_channel_list.append(1117124786238279760) #karks
# subscribed_channel_list.append(1128840198768296008) #jsat
# subscribed_channel_list.append(1127365267715018934) #ABOBUS

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
    message = mission_manager.get_current_missions()
    if not message:
        logger.info('No tough missions on the board. Aborting auto-post.')
        exit()
    else:
        post_to_all_subscribers(message)
