from django.contrib import admin
admin.ModelAdmin.search_fields = ('email',)