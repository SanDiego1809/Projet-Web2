from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView, UserMyPostsListView
from . import views # Le "." désigne le fichier courant


# Liste de chemins qui a été importée
urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'), # localhost:8000/blog/
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),  # localhost:8000/blog/
    path('user/profile/add_post_in_watchlist/', views.add_post_in_watchlist, name='add-post-in-watchlist'), #permet d'ajouter une annonce dans la watchlist
    path('user/profile/watchlist/', views.watchlist, name='user-watchlist'), #permet de consulter la watchlist
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'), #affiche les détails d'un post
    #pk = primary key --> exemple : post/1 = post avec l'id 1, le int: sert à dire que le pk est de type int afin d'éviter que qlq mette un string par exemple
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'), #modifier un post
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'), #supprimer un post
    path('post/new/', PostCreateView.as_view(), name='post-create'), #creation d'un post
    path('stats/', views.stats, name='blog-stats'), # localhost:8000/about/
    path('place_search/', views.place_search, name='place-search'),#chercher un endroit
    path('filter/', views.filter, name='blog-filter'),#chercher un filtre
    path('my_posts/', UserMyPostsListView.as_view(), name='user-myposts'), #permet de consulter "My posts"
]