import requests
import json
import time
import os
from dotenv import load_dotenv
from datetime import datetime

# Loading up environment variables, you will have to do this yourself.
load_dotenv()
IP_ENDPOINT = os.getenv("IP_ENDPOINT")
NESSUS_USERNAME = os.getenv("NESSUS_USERNAME")
NESSUS_PASSWORD = os.getenv("NESSUS_PASSWORD")

# Disable warnings for SSL Certificate for testing purposes only
requests.packages.urllib3.disable_warnings()
# print(IP_ENDPOINT)
# First request to get the token
url = f"https://{IP_ENDPOINT}/session"
data = {"username": NESSUS_USERNAME, "password": NESSUS_PASSWORD}

# Note: verify=False is used to bypass SSL verification. This is not recommended for production code.
response = requests.post(url, json=data, verify=False)
token = response.json()["token"]
# print(token)

time.sleep(3)

# Second request to get the scans using the token for authentication.
url = f"https://{IP_ENDPOINT}/scans/"

# Add the token to the request headers for authentication, this is the token we got earlier. This is us interacting with the session we created earlier.
headers = {
    "X-Cookie": f"token={token}"
}

# Note: There's no data to send with GET, so we remove the data parameter
response = requests.get(url, headers=headers, verify=False)

# Check if the response was successful
if response.status_code == 200:
    
    # Pull out the necessary information
    scans = response.json()["scans"][0]
    last_modification_date = scans["last_modification_date"]
    creation_date = scans["creation_date"]
    status = scans["status"]
    owner = scans["owner"]
    rrules = scans["rrules"]
    name = scans["name"]

    parsed_output = f"""
        This is the last modification date: {last_modification_date}
        This is the creation date: {creation_date}
        This is the status of the scan: {status}
        This is the owner of the scan: {owner}
        This is the rules for the scan: {rrules}
        This is the name of the scan: {name}
    """
    
    print(parsed_output)
else:
    print(f"Failed to get scans. Status code: {response.status_code}, Message: {response.text}")