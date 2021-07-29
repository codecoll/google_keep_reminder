from __future__ import print_function
import os
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import re
import subprocess
import time

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/tasks.readonly']

def check():
    """Shows basic usage of the Tasks API.
    Prints the title and ID of the first 10 task lists.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('tasks', 'v1', credentials=creds)

    # Call the Tasks API
    results = service.tasklists().list(maxResults=10).execute()
    items = results.get('items', [])

    if not items:
        print('No task lists found.')
    else:
        print ("checking")

        results = service.tasks().list(tasklist = items[0]['id'],
                                       showCompleted = False).execute()
        items = results.get('items', [])

        import datetime
        current_time = datetime.datetime.now().strftime("%H:%M")

        due = []
        
        for item in items:
          m = re.match("(.+) +([0-9]?[0-9]):([0-9]?[0-9]) *$", item['title'])
          if m:
            title = m.group(1)
            time = "%02d:%02d" % (int(m.group(2)), int(m.group(3)))

            if time <= current_time:
              formatted = u'{0} -> {1}'.format(title, time)
              due.append(formatted)

        return due


      
def wait_for_idle():
  while True:
    idle = subprocess.check_output("powershell.exe -File idle.ps1").strip()
    print ("wating for idle %s seconds, currently %s seconds" % (idletime, idle))
    if int(idle) >= idletime:
      break
    
    time.sleep(idletime)



lastnotif = []
lastnotiftime = 0

idletime = 60
checkperiod = 600
notifperiod = 3600

while True:
  due = check()

  if due:
    print (due)

    duediff = list(set(due) - set(lastnotif))
    timediff = int(time.time()) - lastnotiftime
    
    if duediff or timediff > notifperiod:
      print ("notifying user")
      wait_for_idle()

      # origin needed, otherwise we get a 404 error
      subprocess.call(["C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe", "https://tasks.google.com/embed/?origin=https://calendar.google.com&fullWidth=1"])

      lastnotif = due
      lastnotiftime = time.time()

    else:
      print ("not enough time elapsed since last notif: %s" % timediff)


  time.sleep(checkperiod)
