from urllib.request import urlopen
import json

def scrape_missions():
    mission_list = {}
    try:
        url = 'https://darkti.de/mission-board?_data'
        response = urlopen(url)
        response_data = json.loads(response.read())
        mission_list = response_data['missions']
        print(f"{len(mission_list)} current missions via darkti.de")
    except Exception as e:
        print(f'Failed getting missions... {e}')
    return mission_list