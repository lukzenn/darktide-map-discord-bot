# Fetches missions from the darkti.de mission board

from urllib.request import urlopen
import json

from base_logger import logger


def get_missions():
    mission_list = {}
    try:
        url = 'https://darkti.de/mission-board?_data'
        response = urlopen(url)
        response_data = json.loads(response.read())
        mission_list = response_data['missions']
        logger.info(f"Successfully fetched missions from darkti.de ({len(mission_list)} current missions)")
    except Exception as e:
        logger.error(f'Failed getting missions... {e}')
    return mission_list
