from django.urls import path, include

from rest_framework import routers

from . import views
from . import views_rest
from . import views_oauth

app_name = 'expenses'


router = routers.DefaultRouter()
router.register('api/accounts', views_rest.BankAccountViewSet)
router.register('api/tickets', views_rest.TicketViewSet)


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('add_account', views.add_account, name='add_account'),
    path('create_account', views.create_account, name='create_account'),
    path('account/<int:account_id>/', views.account_detail, name='detail'),
    path('account/<int:account_id>/add_ticket', views.add_ticket, name='add_ticket'),
    path('account/<int:account_id>/create_ticket', views.create_ticket, name='create_ticket'),
    path('account/<int:account_id>/send_money', views.send_money, name='send_money'),
    path('account/<int:account_id>/send_money/done', views.send_money_done, name='send_money_done'),

    # rest api
    path('', include(router.urls)),

    # oath -- moved to global urls
    # path('accounts/profile/', views_oauth.create_account_oauth, name='create_account_oauth'),
]

