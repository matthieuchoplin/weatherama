from django.db import models


class Weather(models.Model):
    city = models.CharField(max_length=128)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return "{}'s weather between {} and {}".format(
            self.city, self.start_date, self.end_date)
