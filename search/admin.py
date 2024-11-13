from django.contrib import admin
from .models import SearchHistory
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'query', 'timestamp', 'class_id']
    list_filter = ['timestamp']
    search_fields = ['user__username', 'query']

admin.site.register(SearchHistory, SearchHistoryAdmin)  
