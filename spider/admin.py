from django.contrib import admin
from .models import AddMainUrls, AddUrlsInTable


@admin.register(AddMainUrls)
class AddMainUrlsAdmin(admin.ModelAdmin):
    list_display = ["url"]


@admin.register(AddUrlsInTable)
class AddUrlsInTableAdmin(admin.ModelAdmin):
    list_display = ["inn", "out"]
