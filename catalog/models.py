from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date


# Create your models here.
# ---------------------------------- Модель для жанрів книг class Genre
class Genre(models.Model):

    name = models.CharField(max_length=200,
        help_text = "Введіть жанр книги",
        verbose_name = "Жанр книги")

    def __str__(self):

        return self.name

#----------------------------------- Модель для мов книг class Language
class Language(models.Model):

    name = models.CharField(max_length=20,
        help_text="Введіть мову книги",
        verbose_name="Мова книги")

    def __str__(self):

        return self.name

# -------------------------------- Модель для автора книги class Author
class Author(models.Model):

    first_name = models.CharField(max_length=100,
        help_text="Введіть ім'я автора",
        verbose_name="Ім'я автора")

    last_name = models.CharField(max_length=100,
        help_text="Введіть призвіще автора",
        verbose_name="Прізвище автора")

    date_of_birth = models.DateField(
        help_text="Введіть дату народження",
        verbose_name="Дата народження",
        null=True, blank=True)

    date_of_death = models.DateField(
        help_text="Введіть дату смерті",
        verbose_name="Дата смерті",
        null=True, blank=True)

    def __str__(self):

        return self.last_name

# ------------------------------------------ Модель для книг class Book
class Book(models.Model):

    title = models.CharField(max_length=200,
        help_text="Введіть назву книги",
        verbose_name="Назва книги")

    genre = models.ForeignKey('Genre', on_delete=models.CASCADE,
        help_text="Виберіть жанр книги",
        verbose_name="Жанр книги", null=True)

    language = models.ForeignKey('Language', on_delete=models.CASCADE,
        help_text="Виберіть мову книги",
        verbose_name="Мова книги", null=True)

    author = models.ManyToManyField('Author',
        help_text="Виберіть автора книги",
        verbose_name="Автор книги")

    summary = models.TextField(max_length=1000,
        help_text="Введіть короткий опис книги",
        verbose_name="Аннотація до книги")

    isbn = models.CharField(max_length=13,
        help_text="Має містити 13 символів",
        verbose_name="isbn книги")

    def __str__(self):

        return self.title

    def get_absolute_url(self):

        return reverse('book-detail', args=[str(self.id)])

    def display_author(self):

        return ', '.join([author.last_name for author in self.author.all()])

    display_author.short_description = 'Автори'

# --------------------- Модель екземплярів classes Status, BookInstance
class Status(models.Model):

    name = models.CharField(max_length=20,
        help_text="Введіть статус екземпляру книги",
        verbose_name="Статус екземпляру")

    def __str__(self):

        return self.name

class BookInstance(models.Model):

    book = models.ForeignKey('Book', on_delete=models.CASCADE,
        null=True)

    inv_num = models.CharField(max_length=20, null=True,
        help_text="Введіть інвентарний номер",
        verbose_name="Інвентарний номер")

    imprint = models.CharField(max_length=200,
        help_text="Введіть видавництво і рік випуску",
        verbose_name="Видавництво")

    status = models.ForeignKey('Status', on_delete=models.CASCADE,
        help_text="Змінити статус екземпляру",
        verbose_name='Статус', null=True)

    due_back = models.DateField(null=True, blank=True,
        help_text='Введіть кінець строку статусу',
        verbose_name='Дата закінчення статусу')

    borrower = models.ForeignKey(User, on_delete=models.SET_NULL,
        null=True, blank=True, verbose_name='Замовник',
        help_text='Виберіть замовника книги')

    def __str__(self):

        return '%s %s %s' % (self.inv_num, self.book, self.status)

    @property
    def is_overdue(self):

        if self.due_back and date.today() > self.due_back:

            return True
            
        return False












































































