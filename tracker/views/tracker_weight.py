from .. import forms
from ..models import Entries
from ..tables import WeightTable
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
import logging

logging.basicConfig(level=logging.DEBUG)

@login_required(login_url="/users/login/")
def tracker_weight(request):
    if request.method == 'POST':
        form = forms.CreateWeight(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.Username = request.user
            instance.save()

    form = forms.CreateWeight()
    form.initial["Tracking"] = "Weight"
    entries = Entries.objects.all().filter(Username=request.user,Tracking="Weight").order_by('-DateTime')
    weighttable = WeightTable(entries)

    labels = []
    data = []

    for entry in entries:
        labels.append(entry.DateTime.strftime("%Y-%m-%d"))
        data.append(entry.Numerical_Value)

    print("Logged in")
    return render(request, 'tracker/tracker_weight.html',
                    {'form': form ,
                    'weighttable': weighttable,
                    'entries' : entries,
                    'labels':labels,
                    'data':data } )
