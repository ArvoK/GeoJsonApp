from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.http import HttpResponse
from MapApp.forms import UploadFileForm
from MapApp.models import GeoData, polygon, line, points
from django.db.models import Count
from django.contrib.gis.geos import GEOSGeometry
from django.contrib import messages
import folium
import json

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
                            GeoData.objects.create(name=name, geom=geom)
                        else:
                            GeoData.objects.create(name='fail')
                #return HttpResponse("The name of the uploaded file is: " + str(file))
                return redirect('map')
            else:
                messages.error(request, 'This Service just takes the .geotiff format')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

def map(request):
    Plist = points.objects.all()
    Llist = line.objects.all()
    Polylist = polygon.objects.all()
    MPolylist = GeoData.objects.all()
    Polygons = polygon.objects.raw\
        ('SELECT id as id , ST_AsGeoJSON(polygons) as gjson, name as lname FROM public."MapApp_polygon"')
    Lines = line.objects.raw\
        ('SELECT id as id , ST_AsGeoJSON(lines) as gjson, name as lname FROM public."MapApp_line"')
    Points = points.objects.raw\
        ('SELECT id as id , ST_AsGeoJSON(point) as gjson, name as lname FROM public."MapApp_points"')
    MultiPolygons = GeoData.objects.raw\
        ('SELECT id as id , ST_AsGeoJSON(geom) as gjson, name as lname FROM public."MapApp_geodata"')


    m = folium.Map(width='100%',
                   height='100%',
                   location=[52.516743, 13.384953],
                   zoom_start=10,
                   tiles='https://server.arcgisonline.com/arcgis/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}',
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

    context = {"my_map": m, "Plist": Plist, "Llist": Llist, "Polylist": Polylist, "Polygons": Polygons, "MPolylist": MPolylist}

    return render(request, 'map.html', context)

def download_point(request, point_id):
    Points = polygon.objects.raw\
        ('''SELECT id as id , ST_AsGeoJSON(point) as gjson, name as lname FROM public."MapApp_points" WHERE id = %s''', [point_id])
    for i in Points:
        response = HttpResponse(i.gjson, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="{}.json"'.format(i.lname)
    return response

def download_line(request, line_id):
    lines = line.objects.raw\
        ('''SELECT id as id , ST_AsGeoJSON(lines) as gjson, name as lname FROM public."MapApp_line" WHERE id = %s''', [line_id])
    for i in lines:
        response = HttpResponse(i.gjson, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="{}.json"'.format(i.lname)
    return response

def download_poly(request, poly_id):
    poly = polygon.objects.raw\
        ('''SELECT id as id , ST_AsGeoJSON(polygons) as gjson, name as lname FROM public."MapApp_polygon" WHERE id = %s''', [poly_id])
    for i in poly:
        response = HttpResponse(i.gjson, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="{}.json"'.format(i.lname)
    return response

def download_multipoly(request, mpoly_id):
    mpoly = polygon.objects.raw\
        ('''SELECT id as id , ST_AsGeoJSON(geom) as gjson, name as lname FROM public."MapApp_polygon" WHERE id = %s''', [mpoly_id])
    for i in mpoly:
        response = HttpResponse(i.gjson, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="{}.json"'.format(i.lname)
    return response