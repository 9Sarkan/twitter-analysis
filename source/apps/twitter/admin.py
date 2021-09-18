from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from apps.twitter.models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "tag")
    list_display_links = ("id", "tag")
    search_fields = ("tag",)
