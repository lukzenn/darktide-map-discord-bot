# Fetches missions from the mission board via mission_getter
# Stores all missions in SQLiteDict
# Filters them by difficulty
# Can be called to get missions that are formatted for discord messages

from sqlitedict import SqliteDict
import mission_getter
from datetime import datetime
import json
from base_logger import logger
import os

cache_file = "data/mission_cache.sqlite3"

# If cache is >30MB, turns it into a backup so that it can start fresh
if os.path.exists(cache_file) and os.path.getsize(cache_file) > 30000000:
    os.rename(cache_file, f"data/mission_cache_{datetime.today().strftime('%Y-%m-%d')}.sqlite3_bkp")


mission_cache = SqliteDict(cache_file)

# DICTIONARIES
# data/map_names has all the map names
# data/data/circumstances.json has modifier names and knows if they're tough or not
map_dict = json.load(open('data/map_names.json', 'r'))
circumstance_dict = json.load(open('data/circumstances.json', 'r'))
side_missions_dict = {'side_mission_grimoire': ' :blue_book: Grimoires ', 'side_mission_tome': ' :scroll: Scriptures '}

def write_dict(dict, filename='data/map_names.json'):
    with open(filename, 'w') as file:
        json.dump(dict, file, indent=4)


# Format an individual mission for a discord message. Includes map-id, smart timestamps and emojis for some modifiers
def format_mission_for_discord(mission_data):
    circ_id = mission_data.get('circumstance', 'Unkown modifiers')

    if circ_id in circumstance_dict:
        circ_name = circumstance_dict.get(circ_id, {}).get('name', circ_id)
    else:
        circ_name = circ_id

    emoji = circumstance_dict.get(circ_id, {}).get('emoji', '')
    map_name = map_dict.get(mission_data['map'], mission_data['map'])
    side_mission = side_missions_dict.get(mission_data.get('sideMission'), '')
    return f"<t:{int(mission_data['start'])}:R>  {emoji} **{circ_name}**  {map_name} {side_mission} `/mmtimport {mission_data['id']}`"


## MISSION DIFFICULTY FILTERS

def is_maelstrom(mission):
    if mission['challenge'] == 5 and 'flash' in mission['flags']:
        return True
    return False


# A mission is considered not tough if it's not Damnation, or if. True if tough:True or if unknown
def is_tough(mission):
    if is_maelstrom(mission):
        return True
    if mission['challenge'] < 5:
        return False
    if not has_modifiers(mission):
        return False
    if circumstance_dict.get(mission['circumstance'], {}).get('tough', True):
        return True
    return False


def is_damnation(mission):
    return mission["challenge"] == 5


def has_modifiers(mission):
    if mission['circumstance'] == 'default' or mission['circumstance'] == '' or mission['circumstance'] is None:
        return False
    else:
        return True


# GET MISSIONS
# Returns a message formatted for discord of filtered missions that started X seconds ago
def get_recent_missions(since_seconds_ago, *args):
    update_missions()

    since_timestamp = int(datetime.timestamp(datetime.utcnow()) - since_seconds_ago)

    cached_missions = [*mission_cache.items()]
    cached_missions.reverse()

    filtered_missions = []
    for map_id, mission in cached_missions:
        if len(filtered_missions) > 20:
            break  # stop searching when already 20 found (discord character limit)
        if mission['start'] < since_timestamp:
            break  # stop searching once missions are more than X seconds old
        if 'maelstrom_only' in args and is_maelstrom(mission):
            filtered_missions.append(mission)
            continue
        if 'maelstrom_only' not in args and is_tough(mission):
            # If modifier marked as 'tough', include it in the list. Unknown modifiers are always considered "tough".
            filtered_missions.append(mission)
            continue
        if 'interesting' in args and has_modifiers(mission):
            filtered_missions.append(mission)
            continue

    message = ''
    if filtered_missions:
        filtered_missions.reverse()
        for mission in filtered_missions:
            new_line = format_mission_for_discord(mission)
            if len(message) + len(new_line) <= 1998:  # to stay under discord 2000 character limit
                message = message + '\n' + new_line
    return message

def get_current_maelstroms():
    return get_recent_missions(3900, 'maelstrom_only')


# Return missions that started in the last 30 minutes
def get_current_missions():
    return get_recent_missions(1800)

def get_interesting_and_recent(since_seconds_ago):
    return get_recent_missions(1800, 'interesting')


# Fetch current missions, prep data and store into cache as id:Dict
def update_missions(url = mission_getter.maelstroom):
    logger.info(f"{len(mission_cache)} already in cache. Updating...")
    current_missions = mission_getter.get_missions(url)
    for mission in current_missions:
        mission = prep_mission_data(mission)
        map_id = mission["id"]
        mission_cache.update({map_id: mission})
    mission_cache.commit()


def prep_mission_data(mission):
    if mission["circumstance"] is None:
        mission["circumstance"] = {"name": "Standard"}
    mission['start'] = int(int(mission['start']) / 1000)
    return mission


# for troubleshooting
def dump_db_to_json():
    with open("data.json", "w") as outfile:
        cached_missions = [*mission_cache.items()]
        json.dump(cached_missions, outfile)


print(get_recent_missions(3600 * 24))  # for testing
