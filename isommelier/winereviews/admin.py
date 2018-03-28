from django.contrib import admin

from .models import Wine, Winery, Variety, Review

admin.site.register(Wine)
admin.site.register(Winery)
admin.site.register(Variety)
admin.site.register(Review)
