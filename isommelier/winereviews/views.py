
import csv
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.db.models import Count
from .models import Variety


def index(request):
    template = loader.get_template('winereviews/index.html')
    context = {
        'a_var': 0,
    }
    return HttpResponse(template.render(context, request))  

def consultancy(request):
    template = loader.get_template('winereviews/consultancy.html')
    context = {
        'a_var': 0,
    }
    return HttpResponse(template.render(context, request))  

def pick_a_wine(request):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
    writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])
    return response    

def wine_variety_stats(request):
    response = HttpResponse(content_type='text/csv')
    sql = '''
        SELECT A.id, count(C.id) review_count
        FROM winereviews_variety A
        JOIN winereviews_wine B ON B.variety_id = A.id
        JOIN winereviews_review C ON C.wine_id = B.id
        GROUP BY A.id
        ORDER BY review_count DESC
        LIMIT 100;
    '''
    varieties = Variety.objects.raw(sql)
    writer = csv.writer(response)
    writer.writerow(['id', 'value'])
    for v in varieties:
        writer.writerow([v.name, v.review_count])
    return response
    