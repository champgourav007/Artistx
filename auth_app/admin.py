from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.ArtistsUser)
admin.site.register(models.Language)
admin.site.register(models.Review)
admin.site.register(models.Users)