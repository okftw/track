from .. import forms
from ..models import Entries
from ..tables import MedicationTable
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
import logging

logging.basicConfig(level=logging.DEBUG)

@login_required(login_url="/users/login/")
def tracker_medication(request):
    if request.method == 'POST':
        form = forms.AddMedication(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.Username = request.user
            logging.debug('+++ instance +++')

            instance.save()
    form = forms.AddMedication()
    form.initial["Tracking"] = "Medication"
    if request.user.is_authenticated:
        entries = Entries.objects.all().filter(Username=request.user,Tracking="Medication").order_by('-DateTime')
        medicationtable = MedicationTable(entries)
        print("Logged in")
        return render(request, 'tracker/tracker_medication.html', {'form': form , 'medicationtable': medicationtable} )
    else:
        print("Not logged in")
        return render(request, 'tracker/tracker_medication.html')
