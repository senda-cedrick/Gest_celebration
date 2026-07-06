from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def create_default_admin(sender, **kwargs):
    User = get_user_model()
    if sender.name != 'ma_celebration_app':
        return

    username = 'admin'
    password = 'admin'
    email = 'admin@example.com'

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
