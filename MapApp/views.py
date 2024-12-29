from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.http import HttpResponse
from MapApp.forms import UploadFileForm
from MapApp.models import multipolygon, polygon, line, points
from django.db.models import Count
from django.contrib.gis.geos import GEOSGeometry
from django.contrib import messages
import folium
import json
from MapApp import download
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        file = request.FILES['file']
        file_content = file.read()
        if file:
            filename = file.name
            if filename.endswith('.geojson'):
                geojson_data = json.loads(file_content)
                for feature in geojson_data['features']:
                    tempname = filename.split(".")
                    name = tempname[0]
                    if name:
                        geom = GEOSGeometry(json.dumps(feature['geometry']))
                        if geom.geom_type == 'Polygon':
                            polygon.objects.create(name=name, polygons=geom)
                        elif geom.geom_type == 'LineString':
                            line.objects.create(name=name, lines=geom)
                        elif geom.geom_type == 'Point':
                            points.objects.create(name=name, point=geom)
                        elif geom.geom_type == 'MultiPolygon':
                            multipolygon.objects.create(name=name, geom=geom)
                        else:
                            multipolygon.objects.create(name='fail')
                #return HttpResponse("The name of the uploaded file is: " + str(file))
                return redirect('map')
            else:
                messages.error(request, 'This Service just takes the .geotiff format')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

def map(request):
    MultiPolyhead = multipolygon.objects.values('name').annotate(total=Count('name'))
    Plist = points.objects.all()
    Llist = line.objects.all()
    Polylist = polygon.objects.all()
    MPolylist = multipolygon.objects.all()
    Polygons = polygon.objects.raw\
        ('SELECT id as id , ST_AsGeoJSON(polygons) as gjson, name as lname FROM public."MapApp_polygon"')
    Lines = line.objects.raw\
        ('SELECT id as id , ST_AsGeoJSON(lines) as gjson, name as lname FROM public."MapApp_line"')
    Points = points.objects.raw\
        ('SELECT id as id , ST_AsGeoJSON(point) as gjson, name as lname FROM public."MapApp_points"')
    MultiPolygons = multipolygon.objects.raw\
        ('SELECT id as id , ST_AsGeoJSON(geom) as gjson, name as lname FROM public."MapApp_multipolygon"')


    m = folium.Map(width='100%',
                   height='100%',
                   location=[52.516743, 13.384953],
                   zoom_start=10,
                   tiles='https://server.arcgisonline.com/arcgis/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}',
                   attr='test'
                   )

    for i in MultiPolygons:
        file = i.gjson
        g = folium.GeoJson(
            file,
            name='file',
            tooltip=i.lname,
            popup=i.gjson
        ).add_to(m)

    for i in Polygons:
        file = i.gjson
        g = folium.GeoJson(
            file,
            name='file',
            style_function=lambda x: {'fillColor': 'green', 'color': 'black', 'weight': 2},
            tooltip=i.lname,
            popup=i.gjson
        ).add_to(m)

    for i in Lines:
        file = i.gjson
        g = folium.GeoJson(
            file,
            name='file',
            style_function=lambda x: {'fillColor': 'green', 'color': 'black', 'weight': 2},
            tooltip=i.lname,
            popup=i.gjson
        ).add_to(m)

    for i in Points:
        file = i.gjson
        g = folium.GeoJson(
            file,
            name='file',
            tooltip=i.lname,
            popup=i.gjson
        ).add_to(m)



    m = m._repr_html_()  # updated

    context = {"my_map": m, "Plist": Plist, "Llist": Llist, "Polylist": Polylist, "Polygons": Polygons, "MPolylist": MPolylist,"MHead": MultiPolyhead}

    return render(request, 'map.html', context)

def download_point(request, point_id):
    data = download.downloaddata(model=points, objectsid=point_id, model_name='points')
    return data

def download_line(request, line_id):
    data = download.downloaddata(model=line, objectsid=line_id, model_name='line')
    return data
def download_poly(request, poly_id):
    data = download.downloaddata(model=polygon, objectsid=poly_id, model_name='polygon')
    return data

def download_multipoly(request, mpoly_id):
    data = download.downloaddata(model=multipolygon, objectsid=mpoly_id, model_name='multipolygon')
    return data