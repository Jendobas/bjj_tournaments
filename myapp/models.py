from django.db import models


class Quotes(models.Model):
    quote = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.quote
