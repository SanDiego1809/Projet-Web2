from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView, UserPostWatchlist
from . import views # Le "." désigne le fichier courant


# Liste de chemins qui a été importée
urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'), # localhost:8000/blog/
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),  # localhost:8000/blog/
    path('user/watchlist', UserPostWatchlist.as_view(), name='user-watchlist'), #permet de consulter la watchlist
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'), #affiche les détails d'un post
    #pk = primary key --> exemple : post/1 = post avec l'id 1, le int: sert à dire que le pk est de type int afin d'éviter que qlq mette un string par exemple
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'), #modifier un post
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'), #supprimer un post
    path('post/new/', PostCreateView.as_view(), name='post-create'), #creation d'un post
    path('about/', views.about, name='blog-about'), # localhost:8000/about/
]