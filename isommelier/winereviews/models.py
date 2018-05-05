from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse

# Create your models here.

class Variety(models.Model):
    class Meta:
        verbose_name_plural = "varieties"
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return '%s' % (self.name)

class Winery(models.Model):
    class Meta:
        verbose_name_plural = "wineries"
    name = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return '%s' % (self.name)
    
class Wine(models.Model):
    name = models.CharField(max_length=255)
    varietal = models.CharField(max_length=255)
    variety = models.ForeignKey(Variety, on_delete=models.CASCADE)
    winery = models.ForeignKey(Winery, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % (self.description)
    def get_absolute_url(self):
        return reverse('wine_detail', kwargs={'pk': self.pk})


class Review(models.Model):
    rating = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ],
        blank=True,
        null=True
    )
    comment = models.TextField()
    wine = models.ForeignKey(Wine, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.IntegerField()
    flag = models.IntegerField()

    def get_absolute_url(self):
        return reverse('review_detail', kwargs={'pk': self.pk})

    class Winery_report(models.Model):
        name = models.TextField()
        province = models.TextField()
        region = models.TextField()
        country = models.TextField()
        wine_Count = models.IntegerField()
        variety_count = models.IntegerField()

        class Meta:
            managed = False
            db_table = 'winery_report'  # your view name
