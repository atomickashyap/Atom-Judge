from django.urls import path
from ojmain.views import login_view, register
from . import views

urlpatterns = [
    path('', login_view.as_view()),
    path('register', register.as_view()),
    path('problems', views.problems, name='problems'),
    path('logout', views.logout_view, name='logout')
]