from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Watchlist
from django.urls import reverse
from django.contrib import messages

# Fichier qui va contenir toutes les vues de notre application "blog"

# Ma fonction home prend en paramètre une requête http --> return une réponse http contenant un code html
def home(request):
    # return HttpResponse('<h1>Blog Home</h1>')
    context = {
        'posts' : Post.objects.all()
    }
    return render(request, 'blog/home.html', context) #requête en paramètre, nomDuRepertoire/nomDuTemplate

class UserMyPostsListView(ListView): #affiche les posts dans "My Posts"
    model = Post
    template_name = 'blog/user_myposts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


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
    fields = ['title','sell_rent' ,'price', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user #auteur du poste = l'utilisateur actuellement connecté
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):  # création d'un post
    model = Post
    fields = ['title', 'sell_rent' ,'price','content', 'image']

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

def place_search(request):# inspired by the video https://www.youtube.com/watch?v=AGtae4L5BbI&list=WL&index=33&t=913s
    if request.method == 'POST':
        search = request.POST['search']
        posts= Post.objects.filter(title__contains = search)
        return render(request, 'blog/place_search.html', {'search' : search, 'posts':posts})
    else:
        return render(request, 'blog/place_search.html', {})

def add_post_in_watchlist(request):

    if request.method == 'POST':
        if request.POST['post_id']:
            post_id = request.POST['post_id'] #je récupère l'id du post concerné
            model = Watchlist()
            model.post = Post.objects.filter(id = post_id).get()
            model.user = request.user

            search_if_already_in_watchlist = Watchlist.objects.filter(post = model.post, user=model.user)

            if len(search_if_already_in_watchlist) == 0: #si l'élément n'est pas dans la watchlist (présent 0 fois)
                model.save()
                messages.success(request, 'Post successfully added to your watchlist !')
            else:
                messages.warning(request, 'This post is already in your watchlist...')

            return HttpResponseRedirect(reverse('blog-home')) #afin d'aller sur la page home
    else:
        return render(request, 'blog/home.html')


def watchlist(request):
    curr_user = User.objects.filter(username=request.user.username).get() #utilisateur actuel
    user_watchlist = curr_user.watchlist_list.all() #permet d'obtenir la watchlist de l'utilisateur en cours
    return render(request, 'blog/user_watchlist.html',{'user_watchlist' : user_watchlist, 'title' : 'My watchlist'})

def about(request):
    # return HttpResponse('<h1>About Home</h1>')
    return render(request,  'blog/about.html', {'title' : 'My About Page'})

