
import csv
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.db.models import Count
from .models import Variety
from .models import Review
from .models import Wine



def index(request):
    template = loader.get_template('winereviews/index.html')
    context = {
        'a_var': 0,
    }
    return HttpResponse(template.render(context, request))  



def consultancy(request):
    template = loader.get_template('winereviews/consultancy.html')
    varieties = Variety.objects.all().order_by('name')
    context = {
        'varieties': varieties,
    }
    return HttpResponse(template.render(context, request))
    


def variety_options(request):
    response = HttpResponse(content_type='text/csv')
    varieties = Variety.objects.all()
    writer = csv.writer(response)
    writer.writerow(['id','name'])
    for v in varieties:
        writer.writerow([v.id, v.name])
    return response



def variety_reviews(request, variety_id):
    response = HttpResponse(content_type='text/csv')
    sql = '''
        SELECT A.*
        FROM winereviews_review A
        JOIN winereviews_wine B ON A.wine_id = B.id
        JOIN winereviews_variety C ON B.variety_id = C.id
        AND C.id = %s
    '''
    reviews = Review.objects.raw(sql, [variety_id])
    writer = csv.writer(response)
    writer.writerow(['country','description','designation','points','price','taster_name','variety','winery'])
    for r in reviews:
        writer.writerow([r.wine.winery.country, r.comment, r.wine.name, r.rating, r.wine.price, r.user.username, r.wine.variety.name, r.wine.winery.name])
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



def winereviews_review(request):
    template = loader.get_template('winereviews/review.html')
    context = {
        'a_var': 0,
    }
    return HttpResponse(template.render(context, request))
    
    