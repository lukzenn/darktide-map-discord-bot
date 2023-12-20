# Fetches missions from the darkti.de mission board

from urllib.request import urlopen
import json

from base_logger import logger

maelstroom = 'https://maelstroom.net/DT.json'
darkti_dot_de = 'https://darkti.de/mission-board?_data'


def get_missions(url=maelstroom):
    mission_list = []

    with urlopen(url) as response:
        response_data = json.loads(response.read())
        if url == darkti_dot_de:
            mission_list = response_data['missions']
        if url == maelstroom:
            mission_list = list(response_data.values())
        logger.info(f"Successfully fetched missions from darkti.de ({len(mission_list)} current missions)")
        return mission_list

