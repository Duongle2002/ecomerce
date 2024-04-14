from django.contrib import admin

from upload.models import Photo

# Register your models here.

class Photos(admin.ModelAdmin):
    list_display = ["id"]
    search_fields = ["id"]
admin.site.register(Photo,Photos)