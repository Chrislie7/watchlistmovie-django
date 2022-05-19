"""watchlistmovie URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from watchlistmovieapp.views import HomePage,signup,addToWatchList,WatchListView,deleteWatchList,updateWatchList,viewNote
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
     
    path('', HomePage),
    path('admin/', admin.site.urls),
    path('homePage/', HomePage,name='homePage'),
    path('masuk/',LoginView.as_view(),name='masuk'),
    path('keluar/',LogoutView.as_view(next_page='masuk'),name='keluar'),
    path('signup/', signup,name='signup'),
    path('account/addtowatchlist/<int:id_film>/<str:title>', addToWatchList,name='addtowatchlist'),
    path('Watchlistpage/', WatchListView,name='WatchListView'),
    path('account/deleteWatchList/<int:id_film>/<str:title>', deleteWatchList,name='deleteWatchList'),
    path('account/updateWatchList/<int:id_filmBefore>', updateWatchList,name='updateWatchList'),
    path('account/viewNote/<int:id_film>', viewNote,name='viewNote'),
]
