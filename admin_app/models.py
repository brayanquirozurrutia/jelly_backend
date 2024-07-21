from django.db import models


class BannerPhrase(models.Model):
    phrase = models.CharField(max_length=255, blank=True, null=True, default=None)

    class Meta:
        db_table = 'banner_phrase'
