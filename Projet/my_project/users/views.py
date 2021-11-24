from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login') #une fois le compte créer, redirection vers la page de login
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form':form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, request.FILES, instance=request.user) #"instance=request.user" permet d'afficher dans le champ les infos actuelles (username actuel, email actuel)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile) #"instance=request.user.profile" permet de mettre automatiquement l'image actuelle
        if u_form.is_valid() and p_form.is_valid():
            u_form.save() #sauvegarde les mises à jours de user (username et email)
            p_form.save() #sauvegarde les mises à jours de profile (photo de profil)
            messages.success(request, f'Your account has been updated!')
            return redirect('profile') #une fois les updates faites, redirection vers le profil
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form' : u_form,
        'p_form' : p_form
    }

    return render(request, 'users/profile.html', context)