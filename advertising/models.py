from django.db import models
import uuid
from django.conf import settings


def image_directory(instance, filename):
    return f"{instance.advertisement.user.phone_number}-{instance.advertisement.id}/{filename}"


# Create your models here.
class Property(models.Model):
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    parent = models.ForeignKey('Category', null=True, blank=True, on_delete=models.CASCADE)
    properties = models.ManyToManyField(Property, related_name='categories')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Advertising(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, verbose_name='عنوان آگهی')
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(verbose_name='توضیحات', blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='advertisements')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='categories', verbose_name='دسته بندی')
    property = models.ManyToManyField(Property, related_name='advertisement')

    def __str__(self):
        return f"{self.title} - {self.id}"

    class Meta:
        verbose_name = "Advertisement"
        verbose_name_plural = "Advertisements"


class Image(models.Model):
    advertisement = models.ForeignKey(Advertising, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=image_directory)

    def __str__(self):
        return f'{self.advertisement.user.phone_number}-{self.advertisement.id}'


class PropAd(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='properties')
    advertisement = models.ForeignKey(Advertising, on_delete=models.CASCADE, related_name='advertisement')
    value = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.advertisement.title} - {self.property.title}'
