from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.BoardView.as_view(), name='main'),
    path('create/', views.boardTextCreateFn, name='create'),
    path('write/', views.BoardTextCreate.as_view(), name='write'),
    path('<int:pk>/view/', views.boardTextViewFn, name='view'),
    path('search/', views.boardTextSearch, name='search'),
    # path('<int:pk>/modify/', views.boardTextModifyFn, name='modify'),
    path('<int:pk>/modify/', views.BoardTextModify.as_view(), name='modify'),
    # path('<int:pk>/delete/', views.BoardTextDelete.as_view(), name='delete'),
    path('<int:pk>/delete/', views.BoardTextDeleteFn, name='delete'),
    path('gotosignin/', views.signinFn, name='gotosignin'),
    path('signin/', views.userSignInFn, name='signin'),
    path('gotologin/', views.logininFn, name='gotologin'),
    path('login/', views.userLogInFn, name='login'),
    path('usernameCheck/<str:name>', views.usernameCheckFn, name='usernameCheck'),
    path('logout/', views.logoutFn, name='logout'),
    path('writeReply/', views.BoardReplyWriteFn, name='writeReply'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)