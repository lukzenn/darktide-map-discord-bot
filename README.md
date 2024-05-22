# darktide-map-discord-bot
A Discord bot to find the toughest Map IDs for _Warhammer 40,000: Darktide_ even after they disappeared from the mission board.
Best enjoyed alongside the _ManyMoreTries_ mod so you can keep playing these missions for up to 24 hours.

Thanks to [darkti.de](https://darkti.de/) (by raindish) and [Maelstroom](https://maelstroom.net/) (by Grimalackt)   for providing the mission data.

**Use the bot on your discord server:** [Link to Discord invite](https://discord.com/api/oauth2/authorize?client_id=1124539518826074192&permissions=68608&scope=bot%20applications.commands)

**ManyMoreTries mod for Darktide:** [Link to NexusMods](https://www.nexusmods.com/warhammer40kdarktide/mods/175)

Once added to your server, you can use /commands to interact with the bot.

### Available Commands

`/subscribe`  
Subscribes the current discord channel. Every hour, the bot will post any current Damnation Maelstrom maps and their Map IDs to the channel. Admin only.

`/maelstrom_right_now`  
Posts current Damnation Maelstrom maps and their Map IDs.

`/tough_right_now`  
Posts current tough Damnation maps and their Map IDs.

`/tough_and_recent`  
Posts tough Damnation maps from the last 12 hours (maximum 13   missions). Add a number after the command to get missions from the last X hours.

`/unsubscribe`  
Unsubscribes the current channel from receiving regular updates on Maelstrom maps.