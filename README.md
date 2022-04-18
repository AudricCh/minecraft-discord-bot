# Minecraft Server Discord Bot

## Requirements

You need to give the bot the **manager server role** .
The bot takes Administrator role but doesn't abuse at all (it just rename a channel).

## Configuration

Create a file .env with these values :
  - **DISCORD_TOKEN** = YourBotToken
  
  - **SERVER_IP** = MinecraftServerIP
  
  - **SERVER_PORT** = MinecraftServerPort
  
  - **CHANNEL_ID** = IdOfTheGuild
  
  - **VOCAL_ID** = IdOfTheVocalServerWhichWillBeRenamed

## What is does exactly

It rename the vocal server configured with the number of connected people to your Minecraft Server.
You can create your own branch if you want some translation of the label of connected people. It's only french today.

![image](https://user-images.githubusercontent.com/25503027/163788601-c40277e7-396d-4935-b684-e4cd81572915.png)

*Means "There is 1 connected"*

## Technical information

Discord limit the renaming of a channel to 2 renaming per 10 minutes.
So it can have some delay between the value on Discord and the number of connected people. It shouldn't be more than 5 minutes.
I tried to optimize so it doesn't change the value if there is no difference to keep the possibility to rename the channel when someone connect or disconnect with only 30s of delay. 
