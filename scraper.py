from urllib.request import urlopen
import json

from base_logger import logger

def scrape_missions():
    mission_list = {}
    try:
        url = 'https://darkti.de/mission-board?_data'
        response = urlopen(url)
        response_data = json.loads(response.read())
        mission_list = response_data['missions']
        logger.info(f"{len(mission_list)} current missions via darkti.de")
    except Exception as e:
        logger.error(f'Failed getting missions... {e}')
    return mission_list
