import requests
import json
import subprocess
import pywinctl
import json

user = "" 
token = ""

# Writing and reading json (This took my last braincells)
def read_json_to_tuples(file_path):
    # Read the JSON data from the file
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

    tuples_list = []
    for item in data:
        if "priority" not in item:
          key, value = list(item.items())[0]  # Extract the first key-value pair
          if "modifier" in item:
              extra = item["modifier"]
              tuples_list.append((key, value, extra))
          else:
              tuples_list.append((key, value))

    return tuples_list

def write_tuples_to_json(tuples_list, file_path):
    # Convert the list of tuples to a list of dictionaries
    try:
        with open(file_path, 'r') as json_file:
            existing_data = json.load(json_file)
    except FileNotFoundError:
        print("JSON not found, making new")

    data = []
    for triplet in tuples_list:
        if len(triplet) == 3:
            key, value, extra = triplet
            data.append({key: value, "modifier": extra})  # Include all three elements
        elif len(triplet) == 2:
            key, value = triplet
            data.append({key: value})
        else:
            raise ValueError("Each tuple should contain either two or three elements.")

    for item in existing_data:
      if "priority" in item:
        data.append(item)

    # Write the data to the JSON file
    with open(file_path, 'w') as json_file:
      json.dump(data, json_file, indent=4)

def getpriorityfromjson(filepath):
  with open(filepath, 'r') as json_file:
    existing_data = json.load(json_file)

  for item in existing_data:
    if "priority" in item:
      return item["priority"]



def getopengames():
  # To config
  gameslist = read_json_to_tuples("revoltingpresence.json")

  for game in gameslist:
    for window in pywinctl.getAllAppsNames():
      if game[0] == window:

        # Now check if it has a modifier
        if len(game) == 3:
          finalstr = (f"{game[2]} {game[1]}")
          return finalstr

        finalstr = (f"Playing {game[1]}")
        return finalstr
  return ""

def sendrequest(presence, token, user):
  url = f"https://api.revolt.chat/users/{user}"

  payload = json.dumps({
    "status": {
      "text": f"{presence}"
    }
  })
  headers = {
    'X-Session-Token': f'{token}',
    'Content-Type': 'application/json'
  }

  requests.request("PATCH", url, headers=headers, data=payload)

def command(command: str):
  comlist = command.split(" ")
  coms = subprocess.check_output(comlist).rsplit()
  com = bytes.decode(coms[0], 'utf-8')
  return com

def getspotify():
  player = command("playerctl --list-all")

  if "spotify" in player:
    song = command("playerctl metadata title")
    artist = command("playerctl metadata artist")

    finalstr = f"Listening to {song} - {artist} on Spotify"
    return finalstr
  else: return ""

# To config (
priority = getpriorityfromjson("/home/lop01/revolt/revoltingpresence.json")
presence = ""

games_presence = getopengames()

# Convert values to True/False
if games_presence != "": games_presence = True
else: games_presence = False

spotify_presence = getspotify()

# Convert values to True/False
if spotify_presence != "": spotify_presence = True
else: spotify_presence = False

if games_presence and spotify_presence:  # Both are active, choose the active one
    if priority == "games":
        presence = getopengames()
    elif priority == "spotify":
        presence = getspotify()
elif games_presence:
  presence = getopengames()
elif spotify_presence:
  presence = getspotify()

# If neither Spotify nor games are active, set presence to "Doing Nothing..."
if not presence:
    presence = "Doing Nothing..."
      

sendrequest(presence, token, user)
