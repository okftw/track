# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Entries
from .models import UserProfile

admin.site.register(Entries)
admin.site.register(UserProfile)
