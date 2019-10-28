from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from posts import views
from django.conf.urls.static import static

from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('blog/', views.blog, name='post-list'),
    path('post/<int:id>/', views.post, name='post-detail'),
    path('search/', views.search, name='search'),
    path('tinymce/', include('tinymce.urls')),
    path('post/<int:id>/update/', views.post_update, name='post-update'),
    path('post/<int:id>/delete/', views.post_delete, name='post-delete'),
    path('post/<int:id>/', views.post, name='post-detail'),
    path('create/', views.post_create, name='post-create'),
    path('frame/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
