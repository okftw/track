import django_tables2 as tables
from .models import Entries

class EntriesTable(tables.Table):
    class Meta:
        model = Entries
        fields = ('DateTime', 'Username','String_Value') # fields to display

class FoodTable(tables.Table):
    class Meta:
        model = Entries
        fields = ('DateTime', 'String_Value','Additional_Information','Nurtrition_Info__info') # fields to display

class WeightTable(tables.Table):
    class Meta:
        model = Entries
        fields = ('DateTime', 'Numerical_Value') # fields to display

class MedicationTable(tables.Table):
    class Meta:
        model = Entries
        fields = ('DateTime', 'String_Value','Additional_Information') # fields to display

class BmTable(tables.Table):
    class Meta:
        model = Entries
        fields = ('DateTime', 'Numerical_Value','Additional_Information') # fields to display
