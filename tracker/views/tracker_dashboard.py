from .. import forms
from ..models import Entries
from ..tables import WeightTable
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.functions import TruncDay
from django.http import HttpResponse
from django.shortcuts import render
import logging
import pandas as pd
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)

@login_required(login_url="/users/login/")
def tracker_dashboard(request):

    entries = Entries.objects.all().filter(Username=request.user).order_by('-DateTime')

    weight_labels = []
    weight_data = []

    for entry in entries:
        if entry.Tracking == "Weight" :
            weight_labels.append(entry.DateTime.strftime("%d %b"))
            weight_data.append(entry.Numerical_Value)

    #exercise_count_by_day = Entries.objects.annotate(day=TruncDay('DateTime')).filter(Username=request.user,Tracking="Exercise").exclude(Additional_Information="Skipped").values('day').annotate(total=Count('id'))
    exercise_entry_queryset = Entries.objects.filter(Username=request.user,Tracking="Exercise")\
                                             .exclude(Additional_Information="Skipped")\
                                             .values('Date','String_Value')

    df = pd.DataFrame(list(exercise_entry_queryset))

    df = df.groupby('Date')\
           .count()\
           .reset_index()

    print("Date List :")


    exercise_labels = df["Date"].tolist()
    exercise_labels = [ exercise_label.strftime("%d %b") for exercise_label in exercise_labels]
    exercise_data = df["String_Value"].tolist()

    return render(request, 'tracker/tracker_dashboard.html',
                    {

                        'weight_labels' : weight_labels,
                        'weight_data' : weight_data,
                        'exercise_labels' : exercise_labels,
                        'exercise_data' : exercise_data,
                        'df':df
                    } )
