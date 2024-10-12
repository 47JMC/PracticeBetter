# This is the README for the Official PracticeBetter Repository

Hello !
Today I am going to tour you to how u can run a instance my bot yourself, you can also customize the bot's name, description, banner, icon as you choose!

What are we waiting for?
Lets Begin!

-------
# Setup
-------

- Step 1: Install [python](https://python.org)
- Step 2: Install the necesary libraries by running `pip install -r requirments.txt`
- Step 3: Create an application in [Discord Developer Portal](https://discord.com/developers/applications)
- Step 4: Go to the bot section and create a bot name it whatever you want
- Step 5: Click the reset token button on the bot section
- Step 6: Copy the bots Token and store it somewhere safe
- Step 7: Scroll down in the bot section untill you find Privileged Gateway Intents and turn PRESENCE INTENT, SERVER MEMBERS INTENT and MESSAGE CONTENT INTENT on

- Step 8: Download the files from the repository
- Step 9: Go to [config.py](config.py) and put the bot token in beetween the double qoutes `Bot_Token = ""`
- Step 10: Open discord and go to Your User Settings and Navigate to `Advanced` and turn Developer Mode on
- Step 11: Right Click the server that you want the suggestion messages to be sent to and click `Copy Server ID` and paste that after  `Server_ID =` Example => `Server_ID = 120092813`

- Step 12: Right Click the channel that you want the suggestion messages to be sent to and click `Copy Channel ID` and paste that after  `Staff_Channel_ID =` Example => `Staff_Channel_ID = 08095480`

- Step 13: Go to the [Discord Developer Portal](https://discord.com/developers/applications) Again and navigate to the bot OAth2 section and scroll to OAth2 URL Generator and select `bot` and `application.commands` and scroll untill you find `Bot Permissions` Select `Administrator` and on the dropdown below select `Guild Install` and copy the generator URL and open a new tab and paste that url and hit enter. Now Select the server you want and click `Authorise`. The Bot will join the server now

- Step 14: In [Discord Developer Portal](https://discord.com/developers/applications) go to installations and select User Install and Guild Install. After that under Install Link Select `Discord Provided Link`. Next Scroll to `Default Install Settings` and under `Guild Install` select `bot` & and `application.commands` now under `PERMISSIONS` Select `Administrator`

- Step 15: Go to the folder in which [PracticeBetter.py](PracticeBetter.py) and select `Copy Path`. Now Open a terminal and type `cd {path}`. Replace `{path}` with the path you just copied and hit enter. now run `python PracticeBetter.py` and your bot is Up and Running untill you close the terminal

-----------------------------------------------------------------------------------------------------------------------------------------------

I Hope you Enjoy the bot!
🚑 Anyway that was the guide! See ya!

# End Of README
