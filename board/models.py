from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f'{self.name}'


class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    header = models.CharField(max_length=128)
    description = models.TextField(max_length=5000)
    date = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='ItemCategory')
    image = models.ImageField(upload_to='images/')
    video = models.FileField(upload_to='videos/', blank=True)

    def __str__(self):
        return f'{self.header}, {self.description}, {self.date}, {self.category}'

    def get_absolute_url(self):
        return reverse('item_detail', args=[str(self.id)])


class ItemCategory(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Reply(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=1024)
    date = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user}, {self.text}, {self.date}'

    # def get_absolute_url(self):
    #     return reverse('reply_list')

    def get_absolute_url(self):
        return reverse('item_detail', args=[str(self.id)])
