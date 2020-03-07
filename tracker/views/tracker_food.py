from .. import forms
from ..models import Entries, NutritionInfo
from ..tables import FoodTable
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
import logging
from datetime import datetime

today = datetime.now().date()

logging.basicConfig(level=logging.DEBUG)

@login_required(login_url="/users/login/")
def tracker_food(request):
    if request.method == 'POST':
        form = forms.CreateEntry(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.Username = request.user
            try:
                nutrition_info = NutritionInfo.objects.get(name=instance.String_Value)
            except NutritionInfo.DoesNotExist:
                nutrition_info = None
            instance.Nurtrition_Info = nutrition_info
            instance.save()
    form = forms.CreateEntry()
    form.initial["Tracking"] = "Food"

    entries = Entries.objects.all()\
                             .filter(Username=request.user,Tracking="Food",Date=today)\
                             .values('DateTime','String_Value','Additional_Information','Nurtrition_Info__info','Nurtrition_Info__glycemicindex','Nurtrition_Info__glycemicload')\
                             .order_by('-DateTime')
    foodtable = FoodTable(entries)

    return render(request, 'tracker/tracker_food.html', {'form': form , 'foodtable': foodtable, 'entries' : entries} )
