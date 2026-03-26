from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AuthorsForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


# Create your views here.
# --------------------------------- Головна сторінка застосунку catalog
def index(request):

    # --------------------------------------- підрахунок кількості книг
    num_books = Book.objects.all().count()    
    # -------------------------------- підрахунок кількості примірників
    num_instaces = BookInstance.objects.all().count()
    # --------------------- кількість доступних книг (статус на складі)
    num_instaces_available = BookInstance.objects.filter(status__exact=2).count()
    # ------------------------------------------ кількість авторів книг
    num_authors = Author.objects.count()
    # ------------------------- кількість відвідувань сторінки/ session
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    
    # ---- відправка даних у HTML-шаблон-------------------------------
    
    return render(request, 'index.html', context=
        {'num_books': num_books, 'num_instances': num_instaces,
        'num_instances_available': num_instaces_available,
        'num_authors': num_authors,
        'num_visits': num_visits },
    )
# -------------------------------- виклик форми для редагування авторів
def authors_add(request):

    author = Author.objects.all()
    authorsform = AuthorsForm()

    return render(request, 'catalog/authors_add.html',
        {'form': authorsform, 'author': author})

# ----------------------------------- збереження даних про авторів у БД
def create(request):

    if request.method == 'POST':

        author = Author()
        author.first_name = request.POST.get('first_name')
        author.last_name = request.POST.get('last_name')
        author.date_of_birth = request.POST.get('date_of_birth')
        author.date_of_death = request.POST.get('date_of_death')
        author.save()

        return HttpResponseRedirect('/authors_add/')

# --------------------------------------------- видалення авторів із БД
def delete(request, id):

    try:
        author = Author.objects.get(id=id)
        author.delete()

        return HttpResponseRedirect('/authors_add/')

    except Author.DoesNotExist:

        return HttpResponseNotFound('<h2>Автора не знайдено</h2>')

# ---------------------------------------------------- зміна даних у БД
def edit1(request, id):

    author = Author.objects.get(id=id)

    if request.method == 'POST':

        author.first_name = request.POST.get('first_name')
        author.last_name = request.POST.get('last_name')
        author.date_of_birth = request.POST.get('date_of_birth')
        author.date_of_death = request.POST.get('date_of_death')

        author.save()

        return HttpResponseRedirect('/authors_add/')

    else:
        return render(request, 'edit1.html', {'author': author})

# ----------------------- сторінка з переліками книг class BookListView
class BookListView(generic.ListView):

    model = Book
    paginate_by = 3

    
class BookDetailView(generic.DetailView):
    model = Book

# -------------------------------- перелік авторів class AuthorListView
class AuthorListView(generic.ListView):

    model = Author
    paginate_by = 4

# ---------------------------------------- клас: список замовлених книг
class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Універсальний клас представлення списку замовлених книг,
    які перебувають у поточного користувача"""

    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):

        return (
        BookInstance.objects.filter(
            borrower=self.request.user)
            .filter(status__exact='2')
            .order_by('due_back')
            )
# -------------------------------------------- клас для створення книги
class BookCreate(CreateView):

    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books')

# ------------------------------------------- клас для редагування книг
class BookUpdate(UpdateView):

    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books')

# --------------------------------------------- клас для видалення книг
class BookDelete(DeleteView):

    model = Book
    success_url = reverse_lazy('books')
    




