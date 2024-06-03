from django.db import models

# Create your models here.
class StoryMap(models.Model):
    RowNumber = models.TextField()
    REF_WP = models.TextField()
    CAT1 = models.TextField()
    CAT2 = models.TextField()
    MEMO_TIME = models.TextField()
    SERIAL_NO = models.TextField()
    stitle = models.TextField()
    xbody = models.TextField()
    xurl = models.TextField()
    idpt = models.TextField()
    address = models.TextField()
    fileurl = models.TextField()
    info = models.TextField()
    longitude = models.FloatField()
    latitude = models.FloatField()
    MRT = models.TextField()

    class Meta:
        db_table = "storymap"