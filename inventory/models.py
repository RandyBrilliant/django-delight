from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=255, unique=True)
    qty = models.DecimalField(max_digits=5, decimal_places=2)
    unit = models.CharField(max_length=20)
    unit_price = models.DecimalField(max_digits=5, decimal_places=2)
    slug = models.SlugField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("ingredient-detail", kwargs={"slug": self.slug})
       
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Ingredient, self).save(*args, **kwargs)


class MenuItem(models.Model):
    name = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to="menu", default="menu/food.jpg")
    slug = models.SlugField()

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("menu-detail", kwargs={"slug": self.slug})
    
    def available(self):
        return all(X.enough() for X in self.reciperequirement_set.all())

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(MenuItem, self).save(*args, **kwargs)


class RecipeRequirement(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    qty = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"List of {self.menu_item}'s Ingredients"
    
    def enough(self):
        return self.qty <= self.ingredient.qty


class Purchase(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.timestamp)
    
    def get_absolute_url(self):
        return reverse('purchase')
