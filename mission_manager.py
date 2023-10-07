# Fetches missions from the mission board via mission_getter
# Stores all missions in SQLiteDict
# Can be called to get missions, formatted for discord messages

from sqlitedict import SqliteDict
import mission_getter
from datetime import datetime
import json

from base_logger import logger

cache = SqliteDict("data/mission_cache.sqlite3")

# Extra metadata for modifiers
circumstance_id_dict = {}
circumstance_id_dict['default'] = {'name': ''}
# Easy:
circumstance_id_dict['Standard'] = {'short': 'Standard Damnation', 'emoji': '', 'tough': False}
circumstance_id_dict['Low-Intensity Hunting Grounds'] = {'short': 'Low-Int Hunting Grounds', 'emoji': ':dog2:','tough': False}
circumstance_id_dict['Hunting Grounds'] = {'short': 'Hunting Grounds', 'emoji': ':dog2:', 'tough': False}
circumstance_id_dict['Low-Intensity Gauntlet (Power Supply Interruption)'] = {'short': 'Low-Int Power Supply', 'tough': False}
circumstance_id_dict['Low-Intensity Engagement Zone'] = {'short': 'Low-Int', 'tough': False}
circumstance_id_dict['Power Supply Interruption'] = {'short': 'Power Supply Interruption', 'tough': False}
circumstance_id_dict['Hunting Grounds (Power Supply Interruption)'] = {'short': 'Hunting Grounds Power Supply Interruption', 'tough': False}
# Tough:
circumstance_id_dict['Hi-Intensity Engagement Zone'] = {'short': 'Hi-Intensity', 'emoji': '', 'tough': True}
circumstance_id_dict['Hi-Intensity Shock Troop Gauntlet'] = {'short': 'Hi-Int Shock Troop Gauntlet', 'emoji': ':boxing_glove:', 'tough': True}
circumstance_id_dict['Hi-Intensity Gauntlet (Hunting Grounds)'] = {'short': 'Hi-Int Hunting Grounds', 'emoji': ':dog2:','tough': True}
circumstance_id_dict['Hi-Intensity Gauntlet (Power Supply Interruption)'] = {'short': 'Hi-Int Power Supply Interruption','emoji': ':new_moon:', 'tough': True}
circumstance_id_dict['High challenge low intensity'] = {'short': 'Elite Resistance', 'emoji': ':woman_lifting_weight:','tough': True}
circumstance_id_dict['Shock Troop Gauntlet'] = {'short': 'Shock Troop Gauntlet', 'emoji': ':gloves:', 'tough': True}
# Maelstrom
circumstance_id_dict['flash_mission_01'] = {'name': 'Monstrous Shock Troop Gauntlet (I-II)'}
circumstance_id_dict['flash_mission_02'] = {'name': 'Nurgle-Blessed Shock Troop Gauntlet (I-E)'}
circumstance_id_dict['flash_mission_03'] = {'name': 'Shock Troop Gauntlet (Hunting Grounds) (I-III)'}
circumstance_id_dict['flash_mission_04'] = {'name': 'Nurgle-Blessed Hunting Grounds (Cooldowns Reduced) (I-E-F)'}
circumstance_id_dict['flash_mission_05'] = {'name': 'Monstrous Shock Troop Gauntlet (Power Supply Interruption) (A-I-II)'}
circumstance_id_dict['flash_mission_06'] = {'name': 'Shock Troop & Snipers Gauntlet (Ventilation Purge) (B-I-IV)'}
circumstance_id_dict['flash_mission_07'] = {'name': 'Shock Troop Gauntlet (Melee Scab Enemies Only) (C-I-VI)'}
circumstance_id_dict['flash_mission_08'] = {'name': 'Shock Troop & Mutants Gauntlet (Hunting Grounds) (Cooldowns Reduced) (I-III-VII-F)'}
circumstance_id_dict['flash_mission_09'] = {'name': 'Ventilation Purge (Ranged Scab Enemies Only) (Cooldowns Reduced) (B-VIII-V-F)'}
circumstance_id_dict['flash_mission_10'] = {'name': 'Nurgle-Blessed Monstrous Shock Troop Gauntlet (Scab Enemies Only) (Extra Grenades) (I-II-V-E-G)'}
circumstance_id_dict['flash_mission_11'] = {'name': 'Shock Troop & Poxbursters Gauntlet With Snipers (Extra Grenades & Extra Barrels) (D-I-IV-IX-G)'}
circumstance_id_dict['flash_mission_12'] = {'name': 'Mutants & Poxbursters Gauntlet (Hunting Grounds) (Extra Grenades & Extra Barrels) (D-III-VII-IX-G)'}
circumstance_id_dict['flash_mission_13'] = {'name': 'Nurgle-Blessed Shock Troop & Mutants Gauntlet (Cooldowns Reduced & Extra Barrels) (I-IX-E-F)'}
circumstance_id_dict['flash_mission_14'] = {'name': 'Speedrun Challenge (Cooldowns Reduced)'}
circumstance_id_dict['high_flash_mission_01'] = {'name': 'Hi-Intensity Monstrous Shock Troop Gauntlet (I-II)'}
circumstance_id_dict['high_flash_mission_02'] = {'name': 'Hi-Intensity Nurgle-Blessed Shock Troop Gauntlet (I-E)'}
circumstance_id_dict['high_flash_mission_03'] = {'name': 'Hi-Intensity Shock Troop Gauntlet (Hunting Grounds) (I-III)'}
circumstance_id_dict['high_flash_mission_04'] = {'name': 'Hi-Intensity Nurgle-Blessed Hunting Grounds (Cooldowns Reduced) (I-E-F)'}
circumstance_id_dict['high_flash_mission_05'] = {'name': 'Hi-Intensity Monstrous Shock Troop Gauntlet (Power Supply Interruption) (A-I-II)'}
circumstance_id_dict['high_flash_mission_06'] = {'name': 'Hi-Intensity Shock Troop & Snipers Gauntlet (Ventilation Purge) (B-I-IV)'}
circumstance_id_dict['high_flash_mission_07'] = {'name': 'Hi-Intensity Shock Troop Gauntlet (Melee Scab Enemies Only) (C-I-VI)'}
circumstance_id_dict['high_flash_mission_08'] = {'name': 'Hi-Intensity Shock Troop & Mutants Gauntlet (Hunting Grounds) (Cooldowns Reduced) (I-III-VII-F)'}
circumstance_id_dict['high_flash_mission_09'] = {'name': 'Hi-Intensity Ventilation Purge (Ranged Scab Enemies Only) (Cooldowns Reduced) (B-VIII-V-F)'}
circumstance_id_dict['high_flash_mission_10'] = {'name': 'Hi-Intensity Nurgle-Blessed Monstrous Shock Troop Gauntlet (Scab Enemies Only) (Extra Grenades) (I-II-V-E-G)'}
circumstance_id_dict['high_flash_mission_11'] = {'name': 'Hi-Intensity Shock Troop & Poxbursters Gauntlet With Snipers (Extra Grenades & Extra Barrels) (D-I-IV-IX-G)'}
circumstance_id_dict['high_flash_mission_12'] = {'name': 'Hi-Intensity Mutants & Poxbursters Gauntlet (Hunting Grounds) (Extra Grenades & Extra Barrels) (D-III-VII-IX-G)'}
circumstance_id_dict['high_flash_mission_13'] = {'name': 'Hi-Intensity Nurgle-Blessed Shock Troop & Mutants Gauntlet (Cooldowns Reduced & Extra Barrels) (I-IX-E-F)'}
circumstance_id_dict['high_flash_mission_14'] = {'name': 'Hi-Intensity Speedrun Challenge (Cooldowns Reduced)'}


side_missions_dict = {'side_mission_grimoire': ' :blue_book: Grimoires ', 'side_mission_tome': ' :scroll: Scriptures '}


# Format an individual mission for a discord message. Includes map-id, smart timestamps and emojis for some modifiers
def format_mission_for_discord(mission_data):
    circ_id = mission_data.get('circumstanceId', 'Not found')

    if circ_id in circumstance_id_dict:
        circ_name = circumstance_id_dict.get(circ_id, {}).get('name', circ_id)
    else:
        circ_name = mission_data.get('circumstance', {}).get('name', circ_id)

    emoji = circumstance_id_dict.get(circ_id, {}).get('emoji', '')
    map_name = mission_data.get('name')
    sidemission = side_missions_dict.get(mission_data.get('sideMission'), '')
    return f"<t:{int(mission_data['start'])}:R>  {emoji} **{circ_name}**  {map_name} {sidemission} `/mmtimport {mission_data['id']}`"




def is_maelstrom(mission):
    if mission['challenge'] == 5 and 'flash' in mission['flags']:
        return True
    return False


def is_tough(mission):
    if circumstance_id_dict.get(mission['circumstance']['name'], {}).get('tough', True):
        return True
    return False


def get_current_maelstroms():
    return get_recent_missions(3900, 'maelstrom_only')


# Return missions that started in the last 30 minutes
def get_current_missions():
    return get_recent_missions(1800)


# Return missions that started in the last X seconds
def get_recent_missions(since_seconds_ago, *args):
    update_missions()

    since_timestamp = datetime.timestamp(datetime.now()) - since_seconds_ago

    cached_missions = [*cache.items()]
    cached_missions.reverse()

    recent_missions = []
    for map_id, mission in cached_missions:
        if len(recent_missions) > 13:
            break  # stop searching when already 13 found (discord message limit)
        if mission['start'] < since_timestamp:
            break  # stop searching once missions are more than 1 hour old
        if 'maelstrom_only' in args and is_maelstrom(mission):
            recent_missions.append(mission)
            continue
        if not 'maelstrom_only' in args and is_tough(mission):
            # If modifier marked as 'tough', include it in the list. Unknown modifiers are always considered "tough".
            recent_missions.append(mission)
            continue

    message = ''
    if recent_missions:
        for mission in recent_missions:
            message = message + '\n' + format_mission_for_discord(mission)
    return message

def interesting_and_recent(since_seconds_ago):
    return get_recent_missions(1800, tough_only=False)


# Scrape darkti.de mission board, discard anything below Damnation, prep data and store into cache as id:Dict
def update_missions():
    logger.info(f"{len(cache)} already in cache. Updating...")
    current_missions = mission_getter.get_missions()
    current_missions = filter_damnations(current_missions)
    for mission in current_missions:
        mission = prep_mission_data(mission)
        map_id = mission["id"]
        cache.update({map_id: mission})
    cache.commit()


def filter_damnations(mission_list):
    hard_missions = []
    for mission in mission_list:
        if mission["challenge"] == 5:
            hard_missions.append(mission)
    return hard_missions


def prep_mission_data(mission):
    if mission["circumstance"] is None:
        mission["circumstance"] = {"name": "Standard"}
    mission['start'] = int(mission['start'] / 1000)
    return mission

# for troubleshooting
def dump_db_to_json():
    with open("data.json", "w") as outfile:
        cached_missions = [*cache.items()]
        # json_data refers to the above JSON
        json.dump(cached_missions, outfile)