
import csv
import json
import metapy

from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import ListView
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db import connection
from .models import Variety, Review, Wine
from .forms import WineReviewCreateForm, WineReviewSearchForm, WineReviewHiddenSearchForm


def index(request):
    template = loader.get_template('winereviews/index.html')
    context = {
        'a_var': 0,
    }
    return HttpResponse(template.render(context, request))



def winebycountry(request):
    form = WineReviewHiddenSearchForm()
    return render(request, 'winereviews/worldmap-template.html', {'form': form})



def wine_data_viz(request):
    template = loader.get_template('winereviews/wine_data_viz.html')
    context = {
        'form': WineReviewHiddenSearchForm()
    }
    return HttpResponse(template.render(context, request))

    
def word_count_stats_rating_hi(request, number=200):
    response = HttpResponse(content_type='text/plain')

    sql = '''
    SELECT B.word, COUNT(winereviews_review_id) word_count, C.avg_rating
    FROM word_root_review A
    JOIN 
    (
        SELECT Y.root, Y.word 
        FROM (
            SELECT root, MAX(count) AS max_count FROM word_root GROUP BY root
        ) X 
        INNER JOIN word_root Y ON Y.root = X.root 
        AND Y.count = X.max_count GROUP BY Y.root
    ) B ON B.root = A.root
    JOIN word_root_sum C ON C.root = A.root
    WHERE winereviews_review_id IN
        (
            SELECT B.id
            FROM winereviews_review B
            JOIN 
            (
                SELECT A.id, AVG(rating) avg_rating
                FROM winereviews_wine A 
                JOIN winereviews_review B ON B.wine_id = A.id 
                GROUP BY A.id
                ORDER BY avg_rating DESC LIMIT 100
            ) A ON B.wine_id = A.id
        )
    AND A.root NOT IN ('–','—','“','”','$','it','%%','(',')','10')
    AND A.root NOT LIKE '20%%'
    GROUP BY A.root
    ORDER BY word_count DESC, word DESC
    LIMIT %s;
    '''

    # sql = '''
    # SELECT B.word, COUNT(winereviews_review_id) word_count, AVG(C.rating) avg_rating
    # FROM word_root_review A
    # JOIN 
    # (
    #     SELECT Y.root, Y.word 
    #     FROM (
    #         SELECT root, MAX(count) AS max_count FROM word_root GROUP BY root
    #     ) X 
    #     INNER JOIN word_root Y ON Y.root = X.root 
    #     AND Y.count = X.max_count GROUP BY Y.root
    # ) B ON B.root = A.root
    # JOIN winereviews_review C ON C.id = A.winereviews_review_id
    # WHERE winereviews_review_id IN
    #     (
    #         SELECT B.id
    #         FROM winereviews_review B
    #         JOIN 
    #         (
    #             SELECT A.id, AVG(rating) avg_rating
    #             FROM winereviews_wine A 
    #             JOIN winereviews_review B ON B.wine_id = A.id 
    #             GROUP BY A.id
    #             ORDER BY avg_rating DESC LIMIT 100
    #         ) A ON B.wine_id = A.id
    #     )
    # AND A.root NOT IN ('–','—','“','”','$','it','%%','(',')','10')
    # AND A.root NOT LIKE '20%%'
    # GROUP BY A.root
    # ORDER BY word_count DESC, word DESC
    # LIMIT %s;
    # '''
    
    with connection.cursor() as cursor:
        cursor.execute(sql, [number])
        words = cursor.fetchall()

    writer = csv.writer(response)
    writer.writerow(['id','value','avg_rating'])
    for w in words:
        writer.writerow([w[0], w[1], w[2]])
    return response 

def word_count_stats_rating_lo(request, number=200):
    response = HttpResponse(content_type='text/plain')

    sql = '''
    SELECT B.word, COUNT(winereviews_review_id) word_count, C.avg_rating
    FROM word_root_review A
    JOIN 
    (
        SELECT Y.root, Y.word 
        FROM (
            SELECT root, MAX(count) AS max_count FROM word_root GROUP BY root
        ) X 
        INNER JOIN word_root Y ON Y.root = X.root 
        AND Y.count = X.max_count GROUP BY Y.root
    ) B ON B.root = A.root
    JOIN word_root_sum C ON C.root = A.root
    WHERE winereviews_review_id IN
        (
            SELECT B.id
            FROM winereviews_review B
            JOIN 
            (
                SELECT A.id, AVG(rating) avg_rating
                FROM winereviews_wine A 
                JOIN winereviews_review B ON B.wine_id = A.id 
                GROUP BY A.id
                ORDER BY avg_rating ASC LIMIT 100
            ) A ON B.wine_id = A.id
        )
    AND A.root NOT IN ('–','—','“','”','$','it','%%','(',')','10')
    AND A.root NOT LIKE '20%%'
    GROUP BY A.root
    ORDER BY word_count DESC, word DESC
    LIMIT %s;
    '''
    
    with connection.cursor() as cursor:
        cursor.execute(sql, [number])
        words = cursor.fetchall()

    writer = csv.writer(response)
    writer.writerow(['id','value','avg_rating'])
    for w in words:
        writer.writerow([w[0], w[1], w[2]])
    return response
    
    
def word_count_stats_expensive(request, number=200):
    response = HttpResponse(content_type='text/plain')

    sql = '''
    SELECT B.word, COUNT(winereviews_review_id) word_count, AVG(D.price)
    FROM word_root_review A
    JOIN 
    (
        SELECT Y.root, Y.word 
        FROM (
            SELECT root, MAX(count) AS max_count FROM word_root GROUP BY root
        ) X 
        INNER JOIN word_root Y ON Y.root = X.root 
        AND Y.count = X.max_count GROUP BY Y.root
    ) B ON B.root = A.root
    JOIN winereviews_review C ON C.id = A.winereviews_review_id
    JOIN winereviews_wine D ON D.id = C.wine_id
    WHERE winereviews_review_id IN
        (
            SELECT B.id
            FROM winereviews_review B
            JOIN 
            (
                SELECT A.id
                FROM winereviews_wine A 
                ORDER BY price DESC LIMIT 100
            ) A ON B.wine_id = A.id
        )
    AND A.root NOT IN ('–','—','“','”','$','it','%%','(',')','10')
    AND A.root NOT LIKE '20%%'
    GROUP BY A.root
    ORDER BY word_count DESC, word DESC
    LIMIT %s;
    '''
    
    with connection.cursor() as cursor:
        cursor.execute(sql, [number])
        words = cursor.fetchall()

    writer = csv.writer(response)
    writer.writerow(['id','value','avg_price'])
    for w in words:
        writer.writerow([w[0], w[1], w[2]])
    return response 

    
def word_count_stats(request, number=200):
    response = HttpResponse(content_type='text/plain')

    sql = ''' 
        SELECT word, sum_count, avg_rating FROM word_root_sum WHERE skip = 0 LIMIT %s;
    '''
    with connection.cursor() as cursor:
        cursor.execute(sql, [number])
        words = cursor.fetchall()

    writer = csv.writer(response)
    writer.writerow(['id','value','rating'])
    for w in words:
        writer.writerow([w[0], w[1], w[2]])
    return response   




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
        LIMIT 100
    '''
    reviews = Review.objects.raw(sql, [variety_id])
    writer = csv.writer(response)
    writer.writerow(['country','description','designation','points','price','taster','variety','winery', 'id', 'likes','flag','vintage'])
    for r in reviews:
        writer.writerow([r.wine.winery.country, r.comment, r.wine.name, r.rating, r.wine.price, r.user.username, r.wine.variety.name, r.wine.winery.name, r.id, r.likes, r.flag, r.wine.vintage])
    return response

def review_create(request):
    if request.method == 'POST':
        form = WineReviewCreateForm(request.POST)
        with connection.cursor() as cursor:
            sql = '''
            INSERT INTO winereviews_review 
            (rating, comment, wine_id, user_id)
            VALUES (%s, %s, %s, %s)
            '''
            if request.POST['user_id'] == "":
                user_id = 21
            else:
                user_id = request.POST['user_id']
            cursor.execute(sql, [request.POST['rating'], request.POST['comment'], request.POST['wine_id'], user_id])
        return HttpResponseRedirect(reverse('reviews'))
    else:
        form = WineReviewCreateForm(initial={'user_id': request.user.id,})
        return render(request, 'winereviews/review_form.html', {'form': form})

    # path('review/<int:pk>/', views.review_update, name='review_update'),
    # path('review/<int:pk>/delete/', views.review_delete_actual, name='review_delete_actual'),

def review_delete_actual(request, pk):
    with connection.cursor() as cursor:
        sql = '''
            DELETE FROM winereviews_review 
            WHERE id = %s
        '''
        cursor.execute(sql, [pk])
        return HttpResponseRedirect(reverse('reviews'))

def review_update(request, pk):
    review = Review.objects.get(id=pk)
    if request.method == 'POST':
        form = WineReviewCreateForm(request.POST)
        with connection.cursor() as cursor:
            sql = '''
                UPDATE winereviews_review SET
                rating=%s, comment=%s, wine_id=%s
                WHERE id = %s;
                '''
            cursor.execute(sql, [request.POST['rating'], request.POST['comment'], request.POST['wine_id'], pk])
        return HttpResponseRedirect(reverse('reviews'))
    else:
        if request.user.id is None:
            user_id = 21
        else:
            user_id = request.user.id
        form = WineReviewCreateForm(initial={'user_id': user_id,'comment': review.comment, 'wine_id': review.wine_id, 'rating':review.rating,})
        return render(request, 'winereviews/review_form.html', {'form': form})



def review_delete(request, review_id):
    flaggedReview = Review.objects.get(id=review_id)
    flaggedReview.flag = flaggedReview.flag + 1
    flaggedReview.save()
    return HttpResponse(1, content_type='text/plain')

def review_like(request, review_id):
    likedReview = Review.objects.get(id =review_id)
    likedReview.likes = likedReview.likes + 1
    likedReview.save()
    return HttpResponse(likedReview.likes,content_type='text/plain')

def wine_variety_stats(request):
    response = HttpResponse(content_type='text/plain')
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
    writer.writerow(['id', 'value', 'varietyId'])
    for v in varieties:
        writer.writerow([v.name, v.review_count, v.id])
    return response

def wine_country_report(request, countryName='France'):
    count = 0
    countryDict = {
        "United States": "US",
    }
    countryName = countryDict.get(countryName, countryName)

    sql = '''
        SELECT country , wine_count
        FROM country_wine_count where country =  %s;
    '''

    with connection.cursor() as cursor:
        cursor.execute(sql, [countryName])
        country = cursor.fetchone()

    if country is not None:
        count = country[1]

    return HttpResponse(count, content_type='text/plain')

# Review CRUD

class ReviewUpdate(UpdateView):
    model = Review
    fields = ['comment', 'user', 'rating']

class ReviewDelete(DeleteView):
    model = Review
    success_url = reverse_lazy('review-list')

class ReviewList(ListView):
    model = Review
    paginate_by = 100

def review_detail(request, pk):
    template = loader.get_template('winereviews/review_detail.html')
    review = Review.objects.get(id=pk)
    context = {
        'review': review,
    }
    return HttpResponse(template.render(context, request))


# Wine CRUD
class WineCreate(CreateView):
    model = Wine
    fields = ['name', 'variety', 'winery', 'price', 'description']
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class WineUpdate(UpdateView):
    model = Wine
    fields = ['name', 'variety', 'winery', 'price', 'description']

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
        form = WineReviewCreateForm(initial={'wine_id': wine.id,'user_id': request.user.id})
    return render(request, 'winereviews/wine_review_create.html', {'form': form})

def wine_type_ahead(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        collection = Wine.objects.filter(name__icontains=q)
        results = []
        for item in collection:
            item_json = {}
            item_json = {'value': item.name, 'id': item.id}
            results.append(item_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


# Wine Review NLP search

def wine_review_search(request):
    if request.method == 'POST':
        form = WineReviewSearchForm(request.POST)
        if form.is_valid():
            template = loader.get_template('winereviews/wine_review_search_results.html')
            
            if request.method == 'POST':
                query = request.POST['search_query']

            against = get_query_nlp(query)

            sql = '''
                SELECT id FROM winereviews_review 
                WHERE MATCH(comment_nlp) AGAINST(%s IN NATURAL LANGUAGE MODE) LIMIT 20
            '''
            
            #return HttpResponse(sql)

            results = Review.objects.raw(sql, [against])

            try:
                results[0]
            except:
                synonym_query = get_synonyms(query)
                if synonym_query[0] is not None:
                    against = get_query_nlp(synonym_query)
                    results = Review.objects.raw(sql, [against])

            context = {
                'results': results,
                'query': query,
            }
            return HttpResponse(template.render(context, request))
    else:
        form = WineReviewSearchForm()

    return render(request, 'winereviews/wine_review_search.html', {'form': form})


def get_query_nlp(query):
    doc = metapy.index.Document()
    doc.content(str(query))
    tok = metapy.analyzers.ICUTokenizer(suppress_tags=True)
    stop_words = settings.BASE_DIR + "/nlp/lemur-stopwords.txt"
    tok = metapy.analyzers.ListFilter(tok, stop_words, metapy.analyzers.ListFilter.Type.Reject)
    tok = metapy.analyzers.Porter2Filter(tok)
    tok.set_content(doc.content())
    tokens = [token for token in tok]
    return " ".join(tokens)

def get_synonyms(query):
    query = ",".join(query.split());
    with connection.cursor() as cursor:
        sql = '''
            SELECT GROUP_CONCAT(synonym SEPARATOR ' ') AS synonyms 
            FROM nlp_variety_synonyms
            WHERE variety IN (%s);
        '''
        cursor.execute(sql, [query])
        synonyms = cursor.fetchone()

    return synonyms

