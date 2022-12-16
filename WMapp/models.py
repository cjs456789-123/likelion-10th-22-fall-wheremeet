from django.db import models

# Create your models here.
class Meetingplace(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    lat = models.DecimalField(decimal_places=7, max_digits=10)
    lon = models.DecimalField(decimal_places=7, max_digits=10)
    location = models.CharField(max_length=30)   # 교내라운지/교내카페/교외카페
    class People(models.IntegerChoices):
        ONE = 1
        TWOtoFOUR = 2
        FIVE = 3
    people = models.IntegerField(choices=People.choices)
    class Table(models.IntegerChoices):
        CIRCLE = 1
        RECTANGLE = 2
        WINDOW = 3
        SITTING = 4
    table = models.IntegerField(choices=Table.choices)
    class Outlet(models.IntegerChoices):
        NONE = 0
        ALL = 1
        SOME  = 2
    outlet = models.IntegerField(choices=Outlet.choices)
    meeting_room = models.BooleanField(default=False)
    smoking_room = models.BooleanField(default=False)
    meeting = models.BooleanField(default=False)
    time = models.CharField(max_length=200)
    url = models.CharField(max_length=400)
    # open_evening = models.BooleanField(default=False)


    # 테이블 이름을 'meetingplaces'로 변경 -> makemigrations와 migrate 필수
    class Meta:
        db_table = 'meetingplaces'
        
    def to_json(self):
        return {
            "name": self.name,
            "address": self.address,
            "lat": self.lat,
            "lon": self.lon,
            "location": self.location,
            "people": self.people,
            "table": self.table,
            "outlet": self.outlet,
            "meeting_room": self.meeting_room,
            "smoking_room": self.smoking_room,
            "meeting": self.meeting,
            "time": self.time,
            "url": self.url,
            # "open_evening": self.open_evening,
        }