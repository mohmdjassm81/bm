from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.db import transaction
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth import authenticate, login

from post.models import Post, Follow, Stream
from django.contrib.auth.models import User
from authy.models import Profile
from .forms import EditProfileForm, UserRegisterForm
from django.urls import resolve
from comment.models import Comment


def UserProfile(request, username):
    Profile.objects.get_or_create(user=request.user)
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    url_name = resolve(request.path).url_name
    posts = Post.objects.filter(user=user).order_by('-posted')

    if url_name == 'profile':
        posts = Post.objects.filter(user=user).order_by('-posted')
    else:
        posts = profile.favourite.all()

    # Profile Stats
    posts_count = Post.objects.filter(user=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    followers_count = Follow.objects.filter(following=user).count()
    # count_comment = Comment.objects.filter(post=posts).count()
    follow_status = Follow.objects.filter(following=user, follower=request.user).exists()

    # pagination
    paginator = Paginator(posts, 8)
    page_number = request.GET.get('page')
    posts_paginator = paginator.get_page(page_number)

    context = {
        'posts': posts,
        'profile': profile,
        'posts_count': posts_count,
        'following_count': following_count,
        'followers_count': followers_count,
        'posts_paginator': posts_paginator,
        'follow_status': follow_status,
        # 'count_comment':count_comment,
    }
    return render(request, 'profile.html', context)


def EditProfile(request):
    user = request.user.id
    profile = Profile.objects.get(user__id=user)

    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            profile.image = form.cleaned_data.get('image')
            profile.first_name = form.cleaned_data.get('first_name')
            profile.last_name = form.cleaned_data.get('last_name')
            profile.location = form.cleaned_data.get('location')
            profile.locationY = form.cleaned_data.get('locationY')
            profile.locationX = form.cleaned_data.get('locationX')

            profile.url = form.cleaned_data.get('url')
            profile.bio = form.cleaned_data.get('bio')




            profile.im_on = form.cleaned_data.get('im_on')
            profile.castmr_on = form.cleaned_data.get('castmr_on')

            profile.t = form.cleaned_data.get('t')
            profile.w = form.cleaned_data.get('w')

            profile.g = form.cleaned_data.get('g')
            profile.b = form.cleaned_data.get('b')

            profile.a = form.cleaned_data.get('a')

            profile.save()
            return redirect('profile', profile.user.username)
    else:
        form = EditProfileForm(instance=request.user.profile)

    context = {
        'form': form,
    }
    return render(request, 'editprofile.html', context)








def EditProfilee(request):
    user = request.user.id
    profile = Profile.objects.get(user__id=user)

    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            profile.image = form.cleaned_data.get('image')
            profile.first_name = form.cleaned_data.get('first_name')
            profile.last_name = form.cleaned_data.get('last_name')
            profile.location = form.cleaned_data.get('location')
            profile.locationY = form.cleaned_data.get('locationY')
            profile.locationX = form.cleaned_data.get('locationX')

            profile.url = form.cleaned_data.get('url')
            profile.bio = form.cleaned_data.get('bio')




            profile.im_on = form.cleaned_data.get('im_on')
            profile.castmr_on = form.cleaned_data.get('castmr_on')
            profile.serch = form.cleaned_data.get('serch')

            profile.t = form.cleaned_data.get('t')
            profile.w = form.cleaned_data.get('w')

            profile.g = form.cleaned_data.get('g')
            profile.b = form.cleaned_data.get('b')

            profile.a = form.cleaned_data.get('a')








            profile.save()
            return redirect('editprofileeea')

    else:
        form = EditProfileForm(instance=request.user.profile)





    userss = User.objects.all()

    # Paginator
    paginator = Paginator(userss, 68)
    page_number = request.GET.get('page')
    users_paginatorr = paginator.get_page(page_number)
    context = {
        'form': form,
        'userss': users_paginatorr,

    }
    return render(request, 'editprofilee.html', context)










def EditProfileee(request):
    user = request.user.id
    profile = Profile.objects.get(user__id=user)
    userss = User.objects.all()
    castmr_on = profile.castmr_on
    serch = profile.serch

    t = profile.t
    w = profile.w
    g = profile.g
    b = profile.b
    a = profile.a



    context = {

        'userss': userss,

        'castmr_on': castmr_on,
        'serch': serch,

        't': t,

        'w': w,
        'g': g,

        'b': b,
        'a': a,


    }


    return render(request, 'editprofileee.html', context)


























def follow(request, username, option):
    user = request.user
    following = get_object_or_404(User, username=username)

    try:
        f, created = Follow.objects.get_or_create(follower=request.user, following=following)

        if int(option) == 0:
            f.delete()
            Stream.objects.filter(following=following, user=request.user).all().delete()
        else:
            posts = Post.objects.all().filter(user=following)[:25]
            with transaction.atomic():
                for post in posts:
                    stream = Stream(post=post, user=request.user, date=post.posted, following=following)
                    stream.save()
        return HttpResponseRedirect(reverse('profile', args=[username]))

    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('profile', args=[username]))


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            # Profile.get_or_create(user=request.user)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hurray your account was created!!')

            # Automatically Log In The User
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'], )
            login(request, new_user)
            # return redirect('editprofile')
            return redirect('index')



    elif request.user.is_authenticated:
        return redirect('index')
    else:
        form = UserRegisterForm()
    context = {
        'form': form,
    }
    return render(request, 'sign-up.html', context)
