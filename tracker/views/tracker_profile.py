from .. import forms
from ..forms import UserProfileForm
from ..models import Entries
from ..models import Exercise
from ..models import UserProfile
from datetime import datetime
from django.db.models import Count
from django.db.models.functions import TruncDay
from django.http import HttpResponse
from django.shortcuts import render
import logging
import urllib.request as urllib2
import json

logging.basicConfig(level=logging.DEBUG)
today = datetime.now().date()

def tracker_profile(request):
    form = UserProfileForm()
    username="Anonymous"
    if request.user.is_authenticated:
        user_exists = UserProfile.objects.all().filter(user=request.user)

        username=request.user
        # Change this to .first() instead of referencing array like [0]
        profile_user = UserProfile.objects.filter(user=request.user)
        #print("facebook ID : {}".format(request.user.social_auth.get(provider='facebook').uid))
        social_user = request.user.social_auth.filter(provider='facebook').first()


    if request.method == "POST":
        form = UserProfileForm(request.POST)
        if form.is_valid():
            # this logic is lame need to fix it up
            if user_exists:
                obj = UserProfile.objects.get(user=request.user)
                if form.cleaned_data['age']:
                    obj.age = form.cleaned_data['age']
                if form.cleaned_data['weight']:
                    obj.weight = form.cleaned_data['weight']
                if form.cleaned_data['height']:
                    obj.height = form.cleaned_data['height']
                obj.weight_tracker = form.cleaned_data['weight_tracker']
                obj.bm_tracker = form.cleaned_data['bm_tracker']
                if form.cleaned_data['countdown_number']:
                    obj.countdown_number = form.cleaned_data['countdown_number']
                obj.save()
            else:
                user_profile = form.save(commit=False)
                user_profile.user = username
                user_profile.age = form.cleaned_data['age']
                user_profile.weight = form.cleaned_data['weight']
                user_profile.height = form.cleaned_data['height']
                user_profile.weight_tracker = form.cleaned_data['weight_tracker']
                user_profile.bm_tracker = form.cleaned_data['bm_tracker']
                user_profile.countdown_number = form.cleaned_data['countdown_number']
                user_profile.save()

    bmi = 0

    if profile_user :
        if profile_user[0].weight and profile_user[0].height :
            bmi = round(profile_user[0].weight/(profile_user[0].height**2)*10000,1)

    return render(request, 'tracker/tracker_profile.html', {
            'form': form ,
            'entries_count': Entries.objects.all()
                                      .filter(Username=username,Tracking="Exercise")
                                      .exclude(Additional_Information="Skipped")
                                      .order_by('-DateTime').count(),

            'exercises_skipped': Entries.objects.all()
                                      .filter(Username=username,Tracking="Exercise",Additional_Information="Skipped")
                                      .count(),

            'exercises_by_day' : Entries.objects.annotate(day=TruncDay('DateTime'))
                                                .filter(Username=username,Tracking="Exercise")
                                                .exclude(Additional_Information="Skipped")
                                                .values('day')
                                                .annotate(total=Count('id')),
            'form' : form,
            'profile_user' : profile_user,
            'bmi' : bmi,
            'social_user' : social_user

        } )
