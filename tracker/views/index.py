from .. import forms
from ..models import Entries
from ..models import Exercise
from ..tables import EntriesTable
from datetime import datetime
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
import logging

logging.basicConfig(level=logging.DEBUG)
today = datetime.now().date()

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = forms.CreateEntry(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.userid = request.user
            instance.save()
            return redirect('tracker:index')
    else:
        form = forms.CreateEntry()

    todays_top_users     = Entries.objects.all()\
                            .filter(Date=today, Tracking="Exercise")\
                            .exclude(Username="Anonymous")\
                            .exclude(Additional_Information="Skipped")\
                            .values('Username')\
                            .annotate(total=Count('Username'))\
                            .order_by('-total')

    top_users            = Entries.objects.all()\
                            .values('Username')\
                            .annotate(total=Count('Username'))\
                            .exclude(Username="Anonymous")\
                            .exclude(Additional_Information="Skipped")\
                            .order_by('-total')

    exercise_count       = Exercise.objects.all().count()

    entries_count        = Entries.objects.all()\
                            .filter(Tracking="Exercise")\
                            .exclude(Additional_Information="Skipped")\
                            .count()

    top_exercises        = Entries.objects.all()\
                            .filter(Tracking="Exercise")\
                            .exclude(Additional_Information="Skipped")\
                            .values('String_Value')\
                            .annotate(total=Count('String_Value'))\
                            .order_by('-total')[:10]

    top_exercise_skipped = Entries.objects.all()\
                            .filter(Tracking="Exercise", Additional_Information="Skipped")\
                            .values('String_Value')\
                            .annotate(total=Count('String_Value'))\
                            .order_by('-total')[:10]

    entries              = Entries.objects.all()\
                            .filter(Tracking="Exercise",Date=today)\
                            .exclude(Additional_Information="Skipped")\
                            .order_by('-DateTime')

    entriestable = EntriesTable(entries)

    return render(
        request, 'tracker/tracker_list.html',
        {
            'entries_count':entries_count,
            'entries': entries,
            'entriestable' : entriestable,
            'exercise_count': exercise_count,
            'form': form ,
            'todays_top_users': todays_top_users,
            'top_exercise_skipped': top_exercise_skipped,
            'top_exercises': top_exercises,
            'top_users': top_users
        }
    )
