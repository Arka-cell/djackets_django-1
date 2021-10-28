from django.urls import path

from order import views

urlpatterns = [
    path("checkout/", views.checkout),
    path("orders/", views.OrdersList.as_view()),
    path("personal-infos/", views.PersonalInfosView.as_view()),
]
