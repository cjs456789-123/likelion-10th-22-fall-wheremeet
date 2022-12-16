import csv
import os, sys
import django

# id,name,address,lat,lon,location,people,table,outlet,meeting_room,smoking_room,meeting,time


def csv_to_db(django_model):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
    django.setup()
    csv_path = './WMapp/data/csv_meetingplace_final222.csv'
    with open(csv_path, newline="", encoding='UTF-8') as f_csv:
        row_dics = csv.DictReader(f_csv)
        for row in row_dics:
            django_model.objects.create(                        # DB에 저장
                name = row['name'],
                address = row['address'],
                lat = row['lat'],
                lon = row['lon'],
                location = row['location'],
                people = row['people'],
                table = row['table'],
                outlet = row['outlet'],
                meeting_room = row['meeting_room'],
                smoking_room = row['smoking_room'],
                meeting = row['meeting'],
                time = row['time'],
                url = row['url'],
                # open_evening = row['open_evening'],
            )