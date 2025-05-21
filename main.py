import json
from datetime import datetime, timedelta

import requests
from google_auth_oauthlib.flow import InstalledAppFlow
from icalendar import Calendar
from lxml import etree

SCOPES = ['https://www.googleapis.com/auth/calendar']

flow = InstalledAppFlow.from_client_secrets_file(
    'credentials.json', SCOPES)
creds = flow.run_local_server()

with open('token.json', 'w') as token:
    token.write(creds.to_json())

ACCESS_TOKEN = json.loads(creds.to_json()).get('token')
USER_EMAIL = 'morozvktv@gmail.com'
CALDAV_URL = f'https://apidata.googleusercontent.com/caldav/v2/{USER_EMAIL}/events'

# Date range - last 7 days
now = datetime.utcnow()
seven_days_ago = now - timedelta(days=7)

start_str = seven_days_ago.strftime('%Y%m%dT%H%M%SZ')
end_str = now.strftime('%Y%m%dT%H%M%SZ')

# CalDAV XML REPORT body
xml_body = f'''<?xml version="1.0" encoding="UTF-8"?>
<c:calendar-query xmlns:d="DAV:" xmlns:c="urn:ietf:params:xml:ns:caldav">
  <d:prop>
    <d:getetag/>
    <c:calendar-data/>
  </d:prop>
  <c:filter>
    <c:comp-filter name="VCALENDAR">
      <c:comp-filter name="VEVENT">
        <c:time-range start="{start_str}" end="{end_str}"/>
      </c:comp-filter>
    </c:comp-filter>
  </c:filter>
</c:calendar-query>'''

headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Content-Type': 'application/xml',
    'Depth': '1',
}

response = requests.request('REPORT', CALDAV_URL, headers=headers, data=xml_body)

if response.status_code != 207:
    print("Failed to fetch events")
    print(response.status_code, response.text)
    exit()

# Parse XML multistatus response
tree = etree.fromstring(response.content)
namespaces = {'d': 'DAV:', 'c': 'urn:ietf:params:xml:ns:caldav'}

calendar_data_elements = tree.xpath('//c:calendar-data', namespaces=namespaces)

for element in calendar_data_elements:
    try:
        cal = Calendar.from_ical(element.text)
        for component in cal.walk():
            if component.name == "VEVENT":
                summary = component.get('SUMMARY')
                start = component.get('DTSTART').dt
                print(f"Event: {summary}, Start: {start}")
    except Exception as e:
        print("Failed to parse calendar data:", e)
