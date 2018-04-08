from django import forms
from .models import Wine, Review
from django.contrib.auth.models import User
from django.db import connection


class WineReviewCreateForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)
    rating  = forms.IntegerField(min_value=0, max_value=100)
    wine_id = forms.IntegerField(widget=forms.HiddenInput())
    user_id = forms.ModelChoiceField(queryset=User.objects.all())

    def save_review(self):
        with connection.cursor() as cursor:
            sql = '''
            INSERT INTO winereviews_review 
            (rating, comment, wine_id, user_id)
            VALUES (%s, %s, %s, %s)
            '''
            cursor.execute(sql, [self.rating, self.comment, self.wine_id, self.user_id])
        pass