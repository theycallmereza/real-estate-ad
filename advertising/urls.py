from django.urls import path
from .views import HomepageView, create_ad, add_props_to_advertisement, AdDetailView

urlpatterns = [
    path('', HomepageView.as_view(), name='home'),
    path('new/', create_ad, name='new-add'),
    path('new/<int:category_id>/<uuid:ad_id>/', add_props_to_advertisement, name='add-props'),
    path('<uuid:pk>/', AdDetailView.as_view(), name='ad-detail'),
]
