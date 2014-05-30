from django.db import models

class Reginfo(models.Model):
    user_name = models.CharField(max_length = 30)
    token = models.CharField(max_length = 50)

    def __unicode__(self):
        return self.user_name