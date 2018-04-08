
import csv
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import ListView
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db import connection
from .models import Variety, Review, Wine
from .forms import WineReviewCreateForm


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
    


def variety_options(request):
    response = HttpResponse(content_type='text/csv')
    varieties = Variety.objects.all().order_by("name")
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
    writer.writerow(['country','description','designation','points','price','taster','variety','winery'])
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



# Review CRUD
@method_decorator(login_required, name='dispatch')
class ReviewCreate(CreateView):
    model = Review
    fields = ['comment', 'user', 'rating']
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class ReviewUpdate(UpdateView):
    model = Review
    fields = ['comment', 'user', 'rating']

@method_decorator(login_required, name='dispatch')
class ReviewDelete(DeleteView):
    model = Review
    success_url = reverse_lazy('review-list')

class ReviewList(ListView):
    model = Review 
    paginate_by = 100

def review_detail(request, pk):
    template = loader.get_template('winereviews/review_create.html')
    review = Review.objects.get(id=pk)
    context = {
        'review': review,
    }
    return HttpResponse(template.render(context, request))


# Wine CRUD
@method_decorator(login_required, name='dispatch')
class WineCreate(CreateView):
    model = Wine
    fields = ['name', 'variety', 'winery', 'price', 'description']
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class WineUpdate(UpdateView):
    model = Wine
    fields = ['name', 'variety', 'winery', 'price', 'description']

@method_decorator(login_required, name='dispatch')
class WineDelete(DeleteView):
    model = Wine
    success_url = reverse_lazy('wine-list')

class WineList(ListView):
    model = Wine 
    paginate_by = 100

def wine_detail(request, pk):
    template = loader.get_template('winereviews/wine_detail.html')
    wine = Wine.objects.get(id=pk)
    context = {
        'wine': wine,
    }
    return HttpResponse(template.render(context, request))

def wine_review_create(request, pk):
    wine = get_object_or_404(Wine, id=pk)
    if request.method == 'POST':
        form = WineReviewCreateForm(request.POST)
        with connection.cursor() as cursor:
            sql = '''
            INSERT INTO winereviews_review 
            (rating, comment, wine_id, user_id)
            VALUES (%s, %s, %s, %s)
            '''
            cursor.execute(sql, [request.POST['rating'], request.POST['comment'], request.POST['wine_id'], request.POST['user_id']])
        return HttpResponseRedirect(reverse('wine_list'))
    else:
        form = WineReviewCreateForm(initial={'wine_id': wine.id,})
    return render(request, 'winereviews/wine_review_create.html', {'form': form})