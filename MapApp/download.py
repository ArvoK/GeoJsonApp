from django.http import HttpResponse
from django.contrib.gis.db.models import GeometryField

def downloaddata(model, objectsid, model_name :str):
    model_meta = model._meta
    geometry_field_name = next(
        field.name for field in model_meta.fields if isinstance(field, GeometryField)
    )
    data = model.objects.raw(
        'SELECT id, ST_AsGeoJSON({}) as gjson, name as lname '
        'FROM public."MapApp_{}" WHERE id = %s'.format(geometry_field_name, model_name),
        [objectsid]
    )
    if data is not None:
        for i in data:
            response = HttpResponse(i.gjson, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="{}.json"'.format(i.lname)
            return response
    else:
        return HttpResponse("Fehler beim Herunterladen der Datei.")