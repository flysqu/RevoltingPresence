# Project: Revolting Presence
## Overview

Revolting Presence is a script that allows you to update your Revolt.chat status based on your current activities. 

The script reads information from a JSON file to determine what game you're playing and listening to music on Spotify works automaticalle. 

It then sends a PATCH request to the Revolt API to update your status on the messaging platform.
JSON Format

The JSON file (revoltingpresence.json) contains a list of objects. The format is very simple and goes as follows::


```json

[
    {
        "applicationname": "Application Display Name",
        "modifier": "Modifier"
    },
        ...
    {
        "priority": "games/spotify"
    }
]
```

### What The Entries Mean
The "applicationname" is what the python script sees the program as to find this name you can run the ```applicationnamefinder.py``` file, this will print all the applications open as the program finds them

The key (second part) of "applicationname" is much simpler, this is what you want others to see in revolt.

Priority is also quite simple. As shown above, here you must write either "games" or "spotify" this will choose wich one has priority if you have a game that is recognized or spotify open

## Adding Entries

To add entries to the JSON file and extend the list of recognized activities, follow these steps:

Open the revoltingpresence.json file in a text editor.
Add a new JSON object to the list, following the format described above. This is my personal setup at the moment:

```json
[
    {
        "java": "Minecraft"
    },
    {
        "BattleBit.exe": "BattleBit"
    },
    {
        "gimp-2.10": "Gimp",
        "modifier": "Painting In"
    },
    {
        "priority": "spotify"
    }
]
```

Save the changes to the revoltingpresence.json file.

## Running the Script

Before running the script, make sure you have installed the required Python packages by running:

```pip install requests pywinctl```

To execute the script, simply run the Python file:

```python revolting_presence.py```

The script will determine your current activity based on the open applications and the information in the JSON file. It will then update your Revolt.chat status accordingly.

Note: Ensure that you have a valid user and token provided in the script to authenticate with the Revolt API. If you don't have one, you can create a Revolt account and generate the token from the user settings.

For this script to be usefull you would have to run this every few seconds. I have not dabled in this yet but you could make a bash script with a while loop that runs forever with a sleep command to delay it a few seconds. You could also use a systemctl service.