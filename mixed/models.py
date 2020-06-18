from django.db import models

# Create your models here.

PRIORITY = [('H', 'High'), ('M', 'Medium'), ('L', 'Low')]


class Questions(models.Model):
    title = models.CharField(max_length=100)
    question = models.TextField(max_length=500)
    priority = models.CharField(max_length=1, choices=PRIORITY)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'The Question'
        verbose_name_plural = 'All Questions'

