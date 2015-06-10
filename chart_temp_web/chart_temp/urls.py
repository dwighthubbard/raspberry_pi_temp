from . import views
from django.conf.urls import url

urlpatterns = []
        
# Added by django_easy_app
from django_easy_app.urlmanager import view_urlpatterns
urlpatterns += view_urlpatterns(views)
