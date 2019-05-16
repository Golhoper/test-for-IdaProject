from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from UploadImage.views import MainPage, UploadPage, ShowImage

urlpatterns = [

    path('', MainPage.as_view(), name="main"),
    path('upload/', UploadPage.as_view(), name="upload"),
    re_path(r'^image/(?P<pk>\w+)/$', ShowImage.as_view(), name="image_page"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
