from django.contrib import admin

from django.contrib import admin
from .models import WeddingCelebration


@admin.register(WeddingCelebration)
class WeddingCelebrationAdmin(admin.ModelAdmin):
    list_display = ('groom_name', 'bride_name', 'wedding_date', 'ceremony_time', 'church_name')
    list_filter = ('wedding_date', 'church_name')
    search_fields = ('groom_name', 'bride_name', 'priest_name')
