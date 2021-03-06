from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Watchlist, Messages
from django.urls import reverse
from django.contrib import messages
from users.models import Profile
from django.core.paginator import Paginator
from django.db.models import Q
import json

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

    def get_context_data(self, *args, **kwargs):
        context = super(PostListView, self).get_context_data(*args, **kwargs)
        if(self.request.user.is_authenticated):
            curr_user = User.objects.filter(username=self.request.user).get()  # utilisateur actuel
            context['watchlist_list'] = curr_user.watchlist_list.all()
        else:
            context['watchlist_list'] = ''
        return context

class UserPostListView(ListView): #affichage de tous les posts (home.html)
    model = Post
    template_name = 'blog/user_posts.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        #si l'utilisateur existe, il sera enregistré dans la variable user, sinon erreur 404
        return Post.objects.filter(author=user).order_by('-date_posted') #tous les posts de l'autheur concerné (filter), du plus récént au plus ancien


class PostDetailView(DetailView): #quand on clique sur un post, le post va être afficher de manière bcp + détaillée
    model = Post

    def get_context_data(self, **kwargs):
        data = super(PostDetailView, self).get_context_data(**kwargs)
        self.object.number_views = self.object.number_views + 1 #j'incrémente le nombre de vues par 1 à chaque visite de la page
        self.object.save()
        return data

class PostCreateView(LoginRequiredMixin, CreateView): #création d'un post
    model = Post
    fields = ['title', 'sell_rent', 'price', 'localisation','address', 'category', 'room_number', 'surface', 'content', 'image', 'image2', 'image3']

    def form_valid(self, form):
        form.instance.author = self.request.user #auteur du poste = l'utilisateur actuellement connecté
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):  # création d'un post
    model = Post
    fields = ['title', 'sell_rent', 'price', 'localisation','address', 'category', 'room_number', 'surface', 'content', 'image', 'image2', 'image3']

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

class UserPreferencesPost(ListView):
    model = Post
    template_name = 'blog/user_mypreferences.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

def place_search(request):# inspired by the video https://www.youtube.com/watch?v=AGtae4L5BbI&list=WL&index=33&t=913s
    if request.method == 'POST':
        search = request.POST['search']
        posts= Post.objects.filter(localisation__contains = search)
        if posts.exists():
            return render(request, 'blog/place_search.html', {'search' : search, 'posts':posts.order_by('-date_posted')})
        else:
            return render(request, 'blog/place_search2.html', {})
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
                search_if_already_in_watchlist.delete()
                messages.warning(request, 'Post deleted from your watchlist...')

            return HttpResponseRedirect(reverse('blog-home')) #afin d'aller sur la page home
    else:
        return render(request, 'blog/home.html')


def watchlist(request):
    curr_user = User.objects.filter(username=request.user.username).get() #utilisateur actuel
    user_watchlist = curr_user.watchlist_list.all() #permet d'obtenir la watchlist de l'utilisateur en cours
    return render(request, 'blog/user_watchlist.html',{'user_watchlist' : user_watchlist.order_by('-id'), 'title' : 'My watchlist'})

def filter(request): #inspired by https://www.youtube.com/watch?v=vU0VeFN-abU
    post = Post.objects.all()

    localisation = request.GET.get('localisation')
    priceMin = request.GET.get('priceMin')
    priceMax = request.GET.get('priceMax')
    sellOrRent = request.GET.get('sellOrRent')
    category = request.GET.get('category')
    surfaceMin = request.GET.get('surfaceMin')
    surfaceMax = request.GET.get('surfaceMax')

    if localisation != '' and localisation is not None:
        post = post.filter(localisation__icontains=localisation)

    if priceMin != '' and priceMin is not None:
        post = post.filter(price__gte=priceMin)

    if priceMax != '' and priceMax is not None:
        post = post.filter(price__lt=priceMax)

    if sellOrRent != '' and sellOrRent is not None and sellOrRent != 'Choose an option':
        post = post.filter(sell_rent__icontains=sellOrRent)

    if category != '' and category is not None and category != 'Choose an option':
        post = post.filter(category__icontains=category)

    if surfaceMin != '' and surfaceMin is not None:
        post = post.filter(surface__gte=surfaceMin)

    if surfaceMax != '' and surfaceMax is not None:
        post = post.filter(surface__lt=surfaceMax)

    context = {
        'posts': post.order_by('-date_posted'),
    }
    if post.exists():
        return render(request, 'blog/filter.html', context)
    else:
        return render(request, 'blog/place_search2.html', {})



def map(request):
    map = Post.objects.all()
    context={
        'map': map
    }
    return render(request, 'blog/map.html', context)

def stats(request):
    numPosts = Post.objects.all().count()
    curr_user = User.objects.filter(username=request.user.username).get()  # utilisateur actuel
    numWatchlist = curr_user.watchlist_list.all().count() #permet d'obtenir la watchlist de l'utilisateur en cours
    numPostsUser = Post.objects.filter(author=curr_user).count()
    posts = Post.objects.all()
    numHouse = posts.filter(category__icontains='H').count()
    numApartment= posts.filter(category__icontains='A').count()
    numGarage = posts.filter(category__icontains='G').count()
    numRent = posts.filter(sell_rent__icontains='S').count()
    numSell = posts.filter(sell_rent__icontains='R').count()
    postUser = Post.objects.filter(author=curr_user)

    context = {
        'numPosts': numPosts,
        'numPostsUser' : numPostsUser,
        'numWatchlist': numWatchlist,
        'numHouse': numHouse,
        'numApartment': numApartment,
        'numGarage': numGarage,
        'numRent': numRent,
        'numSell': numSell,
        'postUser':postUser,
    }

    return render(request,  'blog/stats.html', context)

def preferences_posts(request):
    all_posts = Post.objects.all() #je recupère tous les posts

    user_localisation = request.user.profile.localisation_preference #on recupere les critères de l'utilisateur
    user_price = request.user.profile.price_preference
    user_sellrent = request.user.profile.sell_rent_preference

    all_posts = all_posts.filter(price__lte= user_price, localisation= user_localisation, sell_rent= user_sellrent) #prix +petit ou egal au le prix max de l'utilisateur

    preferences = all_posts.order_by('-date_posted')

    if len(all_posts) > 0: #si il y'a des posts pouvant intéresser l'utilisateur
        messages.info(request, 'You have some interesting news !')
    else:
        messages.warning(request, 'There is nothing matching with your preferences for now...')
        return redirect('blog-home')

    context = {
        'preferences': preferences
    }

    return render(request, 'blog/user_mypreferences.html', context)

####################################### MESSAGES ##################################

def message_home(request):

    if(request.user.is_authenticated): #si l'utilisateur est connecté
        users_list = User.objects.all() #je récupère tous les utilisateurs inscrits
        messages_list = {} #liste de messages
        if request.method == 'GET' and 'user' in request.GET:
            messages_list = Messages.objects.filter(Q(sender=request.user.id, receiver=request.GET['user'])
                                                    | Q(sender=request.GET['user'], receiver=request.user.id)) #pour afficher les messages reçus et envoyés
            messages_list = messages_list.order_by('message_datetime')
            message_id = int(request.GET['user'])
        else:
            message_id = 0 #aucun utilisateur sélectionné

        context = {
            'title' : 'Messages',
            'users_list': users_list,
            'messages_list': messages_list,
            'message_id': message_id
        }
        return render(request,'blog/user_messages.html',context)
    else: #si l'utilisateur n'est pas connecté --> redirect vers la page login
        return redirect('login')

def message_sender(request):
    message_information = {}
    if request.method == 'POST':
        sender = User.objects.get(id=request.POST['sender']) #je récupère l'expéditeur
        receiver = User.objects.get(id=request.POST['receiver']) #je récupère le destinataire
        message = Messages(sender=sender, receiver=receiver, message_content=request.POST['message_content'])
        try: #on essaie d'enregistrer les modifications, si OK alors status == success
            message.save()
            message_information['check'] = 'success'
        except Exception as e:
            message_information['check'] = 'failed'
    else:
        message_information['check'] = 'failed'

    return HttpResponse(json.dumps(message_information), content_type="application/json")

####################################################################################
