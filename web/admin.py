from django.contrib import admin

# Register your models here.
from .models import WebFarsl, WebMcust, WebPcust

@admin.register(WebFarsl)
class WebFarslAdmin(admin.ModelAdmin):
    list_display = ('fid', 'fname')
    search_fields = ('fname',)
    list_filter = ('fid',)
    ordering = ('fid',)
    list_per_page = 20
    list_editable = ('fname',)

@admin.register(WebMcust)
class WebMcustAdmin(admin.ModelAdmin):
    list_display = ('fid', 'fname', 'fpassword')
    search_fields = ('fname',)
    list_filter = ('fid',)
    ordering = ('fid',)
    list_per_page = 20
    list_editable = ('fname', 'fpassword')

@admin.register(WebPcust)
class WebPcustAdmin(admin.ModelAdmin):
    list_display = ('fauto', 'fcust', 'fsl', 'fdoc', 'fsdate', 'frem', 'fsdr', 'fscr', 'fsbal')
    search_fields = ('frem',)
    list_filter = ('fcust',)
    ordering = ('fauto',)
    list_per_page = 20
    list_editable = ('fcust', 'fsl', 'fdoc', 'fsdate', 'frem', 'fsdr', 'fscr', 'fsbal')