from django.db import models


# Logic for the database for the the information app
# index_key attribute is used to control display order on the page
# def __str__ method displays items in the database by the given attribute
# Database items get passed to the app's view context to render them to the page


# Text for the contact page
class ContactText(models.Model):
    objects = None
    header = models.CharField(max_length=100)
    index_key = models.IntegerField()

    def __str__(self):
        return self.header


# Headers for the contact page
class ContactHeader(models.Model):
    objects = None
    header = models.CharField(max_length=100)
    index_key = models.IntegerField()

    def __str__(self):
        return self.header


# Images for the contact page
class ContactImage(models.Model):
    objects = None
    index_key = models.IntegerField()
    name = models.CharField(max_length=100)
    image = models.ImageField(default='default.jpg', upload_to='images')

    def __str__(self):
        return self.name
