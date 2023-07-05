from urllib import request
from bs4 import BeautifulSoup
import json

#TODO Use _data endpoint instead of scraping html...
def scrape_missions():
    mission_list = {}
    try:
        url = 'https://darkti.de/mission-board'
        html = request.urlopen(url).read()
        soup = BeautifulSoup(html, 'html.parser')
        script_tag = soup.find("script")
        mission_list = json.loads(remove_junk(script_tag.string))["missions"]
        print(f"Scraper: {len(mission_list)} current missions on darkti.de")
    except:
        print('Failed getting missions')
    return mission_list


def remove_junk(content):
    content = content.removeprefix(
        'window.__remixContext = {"state":{"loaderData":{"root":{"user":null},"routes/mission-board":'
    )
    content = content.removesuffix(
        '},"actionData":null,"errors":null},"future":{"unstable_dev":true,"unstable_postcss":false,"unstable_tailwind":true,"v2_errorBoundary":false,"v2_meta":false,"v2_normalizeFormMethod":false,"v2_routeConvention":false}};'
    )
    return content
