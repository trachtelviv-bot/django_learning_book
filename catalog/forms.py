from django import forms
from datetime import date
from django.forms import ModelForm
from .models import Book


# ------------------------------------------- клас редагує дані авторів
class AuthorsForm(forms.Form):

    first_name = forms.CharField(label="Ім'я автора")
    last_name = forms.CharField(label="Прізвище")
    date_of_birth = forms.DateField(label="дата народження",
        initial=format(date.today()),
        widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    date_of_death = forms.DateField(label="дата смерті",
        initial=format(date.today()),
        widget=forms.widgets.DateInput(attrs={'type': 'date'}))

# ------------------- Форма створена на основі моделі, редагування книг
class BookModelForm(ModelForm):
    class Meta:

        model = Book
        fields = ['title', 'genre', 'language', 'author', 'summary', 'isbn']










