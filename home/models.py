from django.db import models

# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=25)

def __str__(self):
    return self.name

class Meta:
    verbose_name_plural = 'cities'

class Court(models.Model):
    """Places for people to play pick up games
    
    Attrs:
        latitude - latitude value of coordinates
        longitude - longitude value of coordinates
        name - name of venue
        type_info - info about type of venue
        address - address string
    """
    SPORT_CHOICES = [
        ('Basketball', 'Basketball'),
        ('Soccer', 'Soccer'),
        ('Tennis', 'Tennis'),
        ('Baseball', 'Baseball'),
        ('Other', 'Other')
    ]
    
    latitude = models.DecimalField(max_digits=10, decimal_places=8, default=39.00000000)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, default=-76.70000000)
    name = models.CharField(max_length=30, default='default venue')
    type_info = models.CharField(max_length=20, default='default venue type')
    address = models.CharField(max_length=45, default='default address', unique=True)
    main_sport = models.CharField(max_length=10, choices=SPORT_CHOICES, default='Basketball')
