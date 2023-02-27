from django.contrib.gis.db import models
# Create your models here.
class points(models.Model):
    name = models.CharField(max_length=100)
    point = models.PointField()

class line(models.Model):
    name = models.CharField(max_length=100)
    lines = models.LineStringField()

class polygon(models.Model):
    name = models.CharField(max_length=100)
    polygons = models.PolygonField()

class multipolygon(models.Model):
    name = models.CharField(max_length=255)
    geom = models.MultiPolygonField()