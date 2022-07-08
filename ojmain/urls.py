from django.urls import path,include
from ojmain.views import login_view, register,to_problems,problems
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', login_view.as_view()),
    path('register', register.as_view()),
    path('problems', views.problems, name='problems'),
    # path('problems/<int:p_no>/', views.to_problems, name='problem_no'),
    path('problems/<int:p_no>/', to_problems.as_view()),
    path('ckeditor/',include('ckeditor_uploader.urls')),
    # path('django_monaco_editor', include('django_monaco_editor.url')),
    path('submissions', views.submissions_view, name='submissions'),
    path('logout', views.logout_view, name='logout')
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)