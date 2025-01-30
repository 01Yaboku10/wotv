# pip install gspread google-auth
# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib


import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

def google_write(player_id, cell, data, dir="h"):
    # Define the scope
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    # Add credentials to the account
    creds = Credentials.from_service_account_file("C:\\Users\\Yaboku\\Pictures\\rpg\\Game\\Python\\wotv-main\\wotv-448920-89d48030bb09.json", scopes=scope)

    # Authorize the client
    client = gspread.authorize(creds)

    # Open the Google Sheet
    sheet = client.open(player_id).worksheet("Code")

    if dir == "v":
        values = [[i] for i in data]

    elif dir == "d":
        values = data
    else:
        values = [[i for i in data]]

    # Write data to cell
    sheet.update(values=values, range_name=cell)

def create_matrix(race_classes: list, race_levels, job_classes, job_levels, inventory_names, inventory_amount, attributes, nicknames):
    max_len = max(len(race_classes), len(job_classes), len(inventory_names), len(attributes), len(nicknames))

    def pad_list(lst, length):
        return lst + [""] * (length - len(lst))
    
    race_classes = pad_list(race_classes, max_len)
    race_levels = pad_list(race_levels, max_len)
    job_classes = pad_list(job_classes, max_len)
    job_levels = pad_list(job_levels, max_len)
    inventory_names = pad_list(inventory_names, max_len)
    inventory_amount = pad_list(inventory_amount, max_len)
    attributes = pad_list(attributes, max_len)
    nicknames = pad_list(nicknames, max_len)

    matrix = []
    for i in range(max_len):
        row = [
            race_classes[i],
            race_levels[i],
            "",
            job_classes[i],
            job_levels[i],
            "",
            inventory_names[i],
            inventory_amount[i],
            attributes[i],
            nicknames[i]
        ]
        matrix.append(row)
    
    return matrix

def google_batch_update(player_id, update_requests):
    # Define the scope
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    # Add credentials to the account
    creds = Credentials.from_service_account_file("C:\\Users\\Yaboku\\Pictures\\rpg\\Game\\Python\\wotv-main\\wotv-448920-89d48030bb09.json", scopes=scope)

    # Authorize the client
    client = gspread.authorize(creds)

    # Open the Google Sheet
    sheet = client.open(player_id).worksheet("Code")

    # Perform the batch update
    sheet.batch_update(update_requests)