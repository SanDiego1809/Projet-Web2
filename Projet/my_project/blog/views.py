from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post

# Fichier qui va contenir toutes les vues de notre application "blog"

# Ma fonction home prend en paramètre une requête http --> return une réponse http contenant un code html
def home(request):
    # return HttpResponse('<h1>Blog Home</h1>')
    context = {
        'posts' : Post.objects.all()
    }
    return render(request, 'blog/home.html', context) #requête en paramètre, nomDuRepertoire/nomDuTemplate

class UserPostWatchlist(ListView): #consulter les posts dans la watchlist
    model = Post
    template_name = 'blog/user_watchlist.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']  # permet d'afficher les posts du plus récent au plus ancien (grâce au '-' devant date_posted)
    paginate_by = 5  # nombre de posts qui vont être affichés sur une page


class PostListView(ListView): #affichage de tous les posts (home.html)
    model = Post
    template_name = 'blog/home.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted'] #permet d'afficher les posts du plus récent au plus ancien (grâce au '-' devant date_posted)
    paginate_by = 5 #nombre de posts qui vont être affichés sur une page

class UserPostListView(ListView): #affichage de tous les posts (home.html)
    model = Post
    template_name = 'blog/user_posts.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        #si l'utilsateur existe, il sera enregistré dans la variable user, sinon erreur 404
        return Post.objects.filter(author=user).order_by('-date_posted') #tous les posts de l'autheur concerné (filter), du plus récént au plus ancien


class PostDetailView(DetailView): #quand on clique sur un post, le post va être afficher de manière bcp + détaillée
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView): #création d'un post
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user #auteur du poste = l'utilisateur actuellement connecté
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):  # création d'un post
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user  # auteur du poste = l'utilisateur actuellement connecté
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object() #enregistre le post que l'on veut actuellement modifier
        if self.request.user == post.author: #si l'utilsateur connecté correspond à l'auteur du post alors il peut modifier le post (return True)
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView): #quand on clique sur un post, le post va être afficher de manière bcp + détaillée
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object() #enregistre le post que l'on veut actuellement supprimer
        if self.request.user == post.author: #si l'utilsateur connecté correspond à l'auteur du post alors il peut supprimer le post (return True)
            return True
        return False


def about(request):
    # return HttpResponse('<h1>About Home</h1>')
    return render(request, 'blog/about.html', {'title' : 'My About Page'})

