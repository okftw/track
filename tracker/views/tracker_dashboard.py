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

    # entries = Entries.objects.all().filter(Username=request.user).order_by('-DateTime')
    #
    # weight_labels = []
    # weight_data = []
    #
    # for entry in entries:
    #     if entry.Tracking == "Weight" :
    #         weight_labels.append(entry.DateTime.strftime("%d %b"))
    #         weight_data.append(entry.Numerical_Value)

    ## WEIGHT

    weight_entry_queryset = Entries.objects.filter(Username=request.user,Tracking="Weight")\
                                             .values('Date','Numerical_Value')

    df_weight = pd.DataFrame(list(weight_entry_queryset))
    df_weight['Numerical_Value'] = df_weight['Numerical_Value'].astype(float)

    today = (pd.Timestamp("today") - pd.DateOffset(days=13)).strftime("%m-%d-%Y")
    idx = pd.Series(pd.date_range(today,periods=14))
    df_weight.index = df_weight['Date']
    del df_weight['Date']

    df_weight = df_weight.groupby(df_weight.index)\
           .mean()\

    df_weight = df_weight.reindex(idx, fill_value=0)

    print(df_weight)

    weight_labels = df_weight.index.tolist()
    weight_labels = [ weight_label.strftime("%d %b") for weight_label in weight_labels]
    weight_data = df_weight["Numerical_Value"].tolist()

    ## EXERCISE

    exercise_entry_queryset = Entries.objects.filter(Username=request.user,Tracking="Exercise")\
                                             .exclude(Additional_Information="Skipped")\
                                             .values('Date','String_Value')

    df_exercise = pd.DataFrame(list(exercise_entry_queryset))

    today = (pd.Timestamp("today") - pd.DateOffset(days=13)).strftime("%m-%d-%Y")
    #start = pd.Timestamp("today")+pd.offsets.Day(3)
    #idx = pd.date_range(start, today)
    idx = pd.Series(pd.date_range(today,periods=14))
    df_exercise.index = df_exercise['Date']
    del df_exercise['Date']

    df_exercise = df_exercise.groupby(df_exercise.index)\
           .count()\

    df_exercise = df_exercise.reindex(idx, fill_value=0)

    print(df_exercise)

    exercise_labels = df_exercise.index.tolist()
    exercise_labels = [ exercise_label.strftime("%d %b") for exercise_label in exercise_labels]
    exercise_data = df_exercise["String_Value"].tolist()

    ## bm

    bm_entry_queryset = Entries.objects.filter(Username=request.user,Tracking="Stool")\
                                             .values('Date','Numerical_Value')

    df_bm = pd.DataFrame(list(bm_entry_queryset))
    df_bm['Numerical_Value'] = df_bm['Numerical_Value'].astype(float)

    today = (pd.Timestamp("today") - pd.DateOffset(days=13)).strftime("%m-%d-%Y")
    idx = pd.Series(pd.date_range(today,periods=14))
    df_bm.index = df_bm['Date']
    del df_bm['Date']

    df_bm = df_bm.groupby(df_bm.index)\
           .count()\

    df_bm = df_bm.reindex(idx, fill_value=0)

    print(df_bm)

    bm_labels = df_bm.index.tolist()
    bm_labels = [ bm_label.strftime("%d %b") for bm_label in bm_labels]
    bm_data = df_bm["Numerical_Value"].tolist()

    return render(request, 'tracker/tracker_dashboard.html',
                    {

                        'weight_labels' : weight_labels,
                        'weight_data' : weight_data,
                        'exercise_labels' : exercise_labels,
                        'exercise_data' : exercise_data,
                        'bm_labels' : bm_labels,
                        'bm_data' : bm_data
                    } )
