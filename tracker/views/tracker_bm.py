from .. import forms
from ..models import Entries
from ..tables import BmTable
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
import logging

logging.basicConfig(level=logging.DEBUG)

@login_required(login_url="/users/login/")
def tracker_bm(request):
    if request.method == 'POST':
        form = forms.CreateBm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.Username = request.user
            instance.save()

    form = forms.CreateBm()
    form.initial["Tracking"] = "Stool"
    entries = Entries.objects.all().filter(Username=request.user,Tracking="Stool").order_by('-DateTime')
    bmtable = BmTable(entries)

    labels = []
    data = []

    for entry in entries:
        labels.append(entry.DateTime.strftime("%Y-%m-%d"))
        data.append(entry.Numerical_Value)

    print("Logged in")
    return render(request, 'tracker/tracker_bm.html',
                    {'form': form ,
                    'bmtable': bmtable,
                    'entries' : entries,
                    'labels':labels,
                    'data':data } )
