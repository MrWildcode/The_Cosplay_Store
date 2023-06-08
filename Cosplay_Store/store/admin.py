from django.contrib import admin
from django.contrib.admin import ModelAdmin

from store.models import Products


@admin.register(Products)
class BookAdmin(ModelAdmin):
   pass