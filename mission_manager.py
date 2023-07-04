from sqlitedict import SqliteDict
import scraper
from datetime import datetime

cache = SqliteDict("cache.sqlite3")

# Extra metadata for modifiers
modifiers = {}
# Easy:
modifiers['Standard'] = {'short':'Standard Damnation','emoji':'','tough':False}
modifiers['Low-Intensity Gauntlet (Hunting Grounds)'] = {'short':'Low-Int Hunting Grounds', 'emoji':':dog2:', 'tough':False}
modifiers['Low-Intensity Gauntlet (Power Supply Interruption)'] = {'short':'Low-Int Power Supply','tough':False}
modifiers['Low-Intensity Engagement Zone'] = {'short':'Low-Int','tough':False}
modifiers['Power Supply Interruption'] = {'short':'Power Supply','tough':False}
# Tough:
modifiers['Hi-Intensity Engagement Zone'] = {'short':'Hi-Int','emoji':':small_red_triangle:','tough':True}
modifiers['Hi-Intensity Shock Troop Gauntlet'] = {'short':'Hi-Int STG', 'emoji':'dog2', 'tough':True}
modifiers['Hi-Intensity Gauntlet (Hunting Grounds)'] = {'short':'Hi-Int Hunting Grounds', 'emoji':':boxing_glove:', 'tough':True}
modifiers['Hi-Intensity Gauntlet (Power Supply Outage)'] = {'short':'Hi-Int Power Supply','emoji':':flashlight:','tough':True}
modifiers['High challenge low intensity'] = {'short':'Elite Resistance','emoji':':woman_lifting_weight:','tough':True}


# Format an individual mission for a discord message. Includes map-id, smart timestamps and emojis for some modifiers
def format_mission_for_discord(mission):
    circumstance = mission['circumstance']['name']
    map = mission.get('name')
    emoji = modifiers.get(mission['circumstance']['name'],{}).get('emoji','')
    return f"<t:{int(mission['start'])}:R>  {emoji}**{circumstance}**  {map}  `/mmtimport {mission['id']}`"

# Return missions that started in the last 30 minutes
def get_current_missions():
    return get_recent_missions(1800)


# Return missions that started in the last X seconds
def get_recent_missions(since_seconds_ago):
    update_missions()

    recent_missions = []
    since_timestamp = datetime.timestamp(datetime.now()) - since_seconds_ago

    cached_missions = [*cache.items()]
    cached_missions.reverse()

    for map_id, data in cached_missions:
        if len(recent_missions) > 13:
            break
        if data['start'] > since_timestamp:
            if modifiers.get(data['circumstance']['name'],{}).get('tough',True):
                recent_missions.append(data)
    return recent_missions

# Scrape darkti.de mission board, discard anything below Damnation, prep data and store into cache as id:Dict
def update_missions():
    print(f"{len(cache)} already in cache. Updating...")
    current_missions = scraper.scrape_missions()
    current_missions = filter_damnations(current_missions)
    print(f"{len(current_missions)} current damnations")
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
    mission['start'] = mission['start'] / 1000
    return mission
