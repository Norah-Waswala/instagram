from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    url(r'^$',views.index,name = 'index'),
     url(r'^search/', views.search_profile, name='search'),
    # path(r'', views.main, name = 'mainpage'),
    # path(r'index/', views.index, name = 'indexpage'),
    # path('createImage/',views.createImage, name='createImage'),
    # path('update/<int:Image_id>',views.update_Image, name='updateImage'),
    # path('delete/<int:Image_id>',views.delete_Image, name='deleteImage'),
    # path('profile/', views.Profile, name='profile')

]
    
    
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)