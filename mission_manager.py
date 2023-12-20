# Fetches missions from the mission board via mission_getter
# Stores all missions in SQLiteDict
# Can be called to get missions, formatted for discord messages

from sqlitedict import SqliteDict
import mission_getter
from datetime import datetime
import json

from base_logger import logger

cache = SqliteDict("data/mission_cache.sqlite3")

# TODO: Turn these dictionaries into editable JSON files
# Extra metadata for modifiers
circumstance_id_dict = {}
circumstance_id_dict['default'] = {'name': 'Standard', 'tough': False}
# Easy:
circumstance_id_dict['Low-Intensity Hunting Grounds'] = {'short': 'Low-Int Hunting Grounds', 'emoji': ':dog2:','tough': False}
circumstance_id_dict['Hunting Grounds'] = {'short': 'Hunting Grounds', 'emoji': ':dog2:', 'tough': False}
circumstance_id_dict['Low-Intensity Gauntlet (Power Supply Interruption)'] = {'short': 'Low-Int Power Supply', 'tough': False}
circumstance_id_dict['less_resistance_01'] = {'name': 'Low-Intensity','short': 'Low-Int', 'tough': False}
circumstance_id_dict['Power Supply Interruption'] = {'short': 'Power Supply Interruption', 'tough': False}
circumstance_id_dict['Hunting Grounds (Power Supply Interruption)'] = {'short': 'Hunting Grounds Power Supply Interruption', 'tough': False}
circumstance_id_dict['waves_of_specials_less_resistance_01'] = {'name': 'Low-Intensity Shock Troop Gauntlet','short': 'Hunting Grounds Power Supply Interruption', 'tough': False}
# Tough:
circumstance_id_dict['more_resistance_01'] = {'name': 'Hi-Intensity', 'short': 'Hi-Int','emoji': '', 'tough': True}
circumstance_id_dict['waves_of_specials_more_resistance_01'] = {'name': 'Hi-Intensity Shock Troop Gauntlet', 'short': 'Hi-Int Shock Troop Gauntlet', 'emoji': ':boxing_glove:', 'tough': True}
circumstance_id_dict['hunting_grounds_more_resistance_01'] = {'name': 'Hi-Intensity Gauntlet (Hunting Grounds)','short': 'Hi-Int Hunting Grounds', 'emoji': ':dog2:','tough': True}
circumstance_id_dict['darkness_more_resistance_01'] = {'name': 'Hi-Intensity Gauntlet (Power Supply Interruption)', 'short': 'Hi-Int Power Supply Interruption','emoji': ':new_moon:', 'tough': True}
circumstance_id_dict['High challenge low intensity'] = {'name': 'Elite Resistance','short': 'Elite Resistance', 'emoji': ':woman_lifting_weight:','tough': True}
circumstance_id_dict['waves_of_specials_01'] = {'name': 'Shock Troop Gauntlet', 'short': 'Shock Troop Gauntlet', 'emoji': ':gloves:', 'tough': True}
circumstance_id_dict['ventilation_purge_with_snipers_more_resistance_01'] = {'name': 'Hi-Intensity Sniper Gauntlet (Ventilation Purge)', 'short': 'Hi-Int Ventilation Purge', 'emoji': ':gloves:', 'tough': True}
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

map_dict = {}
map_dict['dm_stockpile'] = 'Silo Cluster 18-66/a'
map_dict['hm_complex'] = 'Comms-Plex 154/2f'
map_dict['dm_rise'] = 'Ascension Riser 31'
map_dict['lm_rails'] = 'Chasm Logistratum'
map_dict['dm_forge'] = 'Smelter Complex HL-17-36'
map_dict['cm_habs'] = 'Hab Dreyko'
map_dict['fm_resurgence'] = 'Enclavum Baross'
map_dict['dm_propaganda'] = 'Relay Station TRS-150'
map_dict['lm_cooling'] = 'Power Matrix HL-17-36'
map_dict['lm_scavenge'] = 'Excise Vault Spireside-13'
map_dict['fm_armoury'] = 'Mercantile HL-70-04'
map_dict['km_enforcer'] = 'Magistrati Oubliette TM8-707'
map_dict['km_station'] = 'Chasm Station HL-16-11'
map_dict['cm_archives'] = 'Archivum Sycorax'
map_dict['hm_strain'] = 'Refinery Delta-17'
map_dict['fm_cargo'] = 'Consignment Yard HL-17-36'
map_dict['hm_cartel'] = 'Vigil Station Oblivium'

side_missions_dict = {'side_mission_grimoire': ' :blue_book: Grimoires ', 'side_mission_tome': ' :scroll: Scriptures '}


# Format an individual mission for a discord message. Includes map-id, smart timestamps and emojis for some modifiers
def format_mission_for_discord(mission_data):
    circ_id = mission_data.get('circumstance', 'Unkown modifiers')

    if circ_id in circumstance_id_dict:
        circ_name = circumstance_id_dict.get(circ_id, {}).get('name', circ_id)
    else:
        circ_name = circ_id


    emoji = circumstance_id_dict.get(circ_id, {}).get('emoji', '')
    map_name = map_dict.get(mission_data['map'], mission_data['map'])
    sidemission = side_missions_dict.get(mission_data.get('sideMission'), '')
    return f"<t:{int(mission_data['start'])}:R>  {emoji} **{circ_name}**  {map_name} {sidemission} `/mmtimport {mission_data['id']}`"




def is_maelstrom(mission):
    if mission['challenge'] == 5 and 'flash' in mission['flags']:
        return True
    return False


def is_tough(mission):
    # print(circumstance_id_dict.get(mission['circumstance']['name'], {}).get('tough'))
    if mission['challenge'] < 5:
            return False
    if mission['circumstance'] == 'default' or mission['circumstance'] is None:
            return False
    if circumstance_id_dict.get(mission['circumstance'], {}).get('tough', True):
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
        if len(recent_missions) > 20:
            break  # stop searching when already 20 found (discord character limit)
        if mission['start'] < since_timestamp:
            break  # stop searching once missions are more than X seconds old
        if 'maelstrom_only' in args and is_maelstrom(mission):
            recent_missions.append(mission)
            continue
        if 'maelstrom_only' not in args and is_tough(mission):
            # If modifier marked as 'tough', include it in the list. Unknown modifiers are always considered "tough".
            recent_missions.append(mission)

    message = ''
    if recent_missions:
        recent_missions.reverse()
        for mission in recent_missions:
            new_string = format_mission_for_discord(mission)
            if len(message) + len(new_string) <= 1998: # to stay under discord 2000 character limit
                message = message + '\n' + new_string
    return message

def interesting_and_recent(since_seconds_ago):
    return get_recent_missions(1800, tough_only=False)


# Get missions, discard anything below Damnation, prep data and store into cache as id:Dict
def update_missions():
    logger.info(f"{len(cache)} already in cache. Updating...")
    current_missions = mission_getter.get_missions()
    for mission in current_missions:
        mission = prep_mission_data(mission)
        map_id = mission["id"]
        cache.update({map_id: mission})
    cache.commit()


def is_damnation(mission):
    return mission["challenge"] == 5


def prep_mission_data(mission):
    if mission["circumstance"] is None:
        mission["circumstance"] = {"name": "Standard"}
    mission['start'] = int(int(mission['start']) / 1000)
    return mission

# for troubleshooting
def dump_db_to_json():
    with open("data.json", "w") as outfile:
        cached_missions = [*cache.items()]
        json.dump(cached_missions, outfile)


print(get_recent_missions(3600*24)) # for testing