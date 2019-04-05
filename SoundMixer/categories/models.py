from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Song(models.Model):
    name = models.CharField(max_length=140)
    link = models.CharField(max_length=50)
    tags = models.ManyToManyField(Category)

    def __str__(self):
        return self.name
