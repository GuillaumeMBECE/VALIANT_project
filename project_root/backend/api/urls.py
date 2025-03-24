from django.urls import path
from .views import get_stats, api_home  # 👈 Ajoute api_home si besoin

urlpatterns = [
    path('get_stats/', get_stats,name='get_stats'),  # ✅ API pour les stats
    path('', api_home, name='api_home'),  # ✅ API root
]