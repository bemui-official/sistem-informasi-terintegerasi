import datetime
import pprint

import pytz
from django.conf import settings

from .google import create_service, convert_to_RFC_datetime

def create_event(url, judul, jenis_dokumen):
    print(1)

    settings.GCAL_SERVICE

    print(1)
    request_body = {
        'start': {
            'dateTime': (datetime.datetime.now() + datetime.timedelta(minutes=1)).isoformat() ,
            'timeZone': 'Asia/Jakarta'
        },
        'end': {
            'dateTime': (datetime.datetime.now() + datetime.timedelta(minutes=16)).isoformat(),
            'timeZone': 'Asia/Jakarta'
        },
        'summary': judul,
        'description': "Akses pada website: " + url
    }

    send_notification = True

    print((datetime.datetime.now() + datetime.timedelta(minutes=1)).isoformat())

    print(1)
    calendarId= ""
    if jenis_dokumen == "keuangan":
        calendarId = settings.GCAL_CALENDAR_ID_KEUANGAN
    elif jenis_dokumen == "surat":
        calendarId = settings.GCAL_CALENDAR_ID_SURAT

    response = service.events().insert(
        calendarId=calendarId,
        sendNotifications=send_notification,
        body=request_body
    ).execute()