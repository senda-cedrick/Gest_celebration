from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from .models import WeddingCelebration


@login_required
def home(request):
    today = timezone.localdate()
    celebrations_count = WeddingCelebration.objects.count()
    marriages_count = celebrations_count
    ongoing_events_count = WeddingCelebration.objects.filter(wedding_date=today).count()
    brides_count = WeddingCelebration.objects.count()
    next_celebration = WeddingCelebration.objects.filter(wedding_date__gte=today).order_by('wedding_date').first()
    User = get_user_model()
    recent_users = User.objects.order_by('-date_joined')[:5]

    return render(request, 'ma_celebration_app/home.html', {
        'celebrations_count': celebrations_count,
        'marriages_count': marriages_count,
        'ongoing_events_count': ongoing_events_count,
        'brides_count': brides_count,
        'next_celebration': next_celebration,
        'recent_users': recent_users,
    })


@login_required
def celebrations_list(request):
    celebrations = WeddingCelebration.objects.order_by('wedding_date')
    return render(request, 'ma_celebration_app/celebrations_list.html', {
        'celebrations': celebrations,
    })


@login_required
def celebration_detail(request, celebration_id):
    celebration = WeddingCelebration.objects.filter(id=celebration_id).first()
    return render(request, 'ma_celebration_app/celebration_detail.html', {
        'celebration': celebration,
    })
