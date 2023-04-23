
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.db.models import Avg, Count
from streaming.models import Movie, UserProfile, Review, SubscriptionPlan
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import logout




def index(request):
    movies = Movie.objects.annotate(
        average_rating=Avg('reviews__rating'), 
        ratings_count=Count('reviews')
    ).order_by('-average_rating')
    return render(request, 'streaming/index.html', {'movies': movies})

def movie(request, movie_id):
    try:
        movie = Movie.objects.get(pk=movie_id)
        return render(request, 'streaming/movie.html', {'movie': movie})
    except ObjectDoesNotExist:
        raise Http404('Movie not found')







def user_reviews(request, user_id):
    user_profile = get_object_or_404(UserProfile, user__id=user_id)
    reviews = Review.objects.filter(user=user_profile)
    return render(request, 'streaming/user_reviews.html', {'reviews': reviews})


def subscription_plan_movies(request, subscription_id):
    subscription_plan = get_object_or_404(SubscriptionPlan, id=subscription_id)
    movies = subscription_plan.movies.all()
    return render(request, 'streaming/subscription_plan.html', {'movies': movies, 'subscription_plan': subscription_plan})
from django.contrib.auth.decorators import login_required
from django.shortcuts import render



@login_required
def user_profile(request):
    user_profile = request.user.userprofile
    subscription_plan = user_profile.subscription_plan
    available_movies = Movie.objects.filter(subscription_plans=subscription_plan)
    return render(request, 'streaming/user_profile.html', {'subscription_plan': subscription_plan, 'available_movies': available_movies})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/streaming/')
        else:
            return render(request, 'streaming/login.html', {'error_message': 'Invalid credentials'})

    return render(request, 'streaming/login.html')