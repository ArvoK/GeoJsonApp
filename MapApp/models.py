from django.contrib.gis.db import models
# Create your models here.
class maps(models.Model):
    name = models.CharField(max_length=100)
    rast = models.RasterField()

class points(models.Model):
    name = models.CharField(max_length=100)
    point = models.PointField()

class line(models.Model):
    name = models.CharField(max_length=100)
    lines = models.LineStringField()

class polygon(models.Model):
    name = models.CharField(max_length=100)
    polygons = models.PolygonField()

class GeoData(models.Model):
    name = models.CharField(max_length=255)
    geom = models.MultiPolygonField()