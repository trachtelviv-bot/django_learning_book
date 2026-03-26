from django.contrib import admin
from .models import Author, Book, Genre, Language, Status, BookInstance


# Register your models here.
# ---------------------------------------------------------------------
print("Admin.py is loading...")

#admin.site.register(Author)
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    
    list_display = ('last_name', 'first_name','date_of_birth', 'date_of_death')
    
    
#admin.site.register(Author, AuthorAdmin)

class BooksInstanceInline(admin.TabularInline):

    model = BookInstance

#admin.site.register(Book)
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):

    list_display = ('title', 'genre', 'language', 'display_author')
    #list_filter = ('genre', 'author')
    inlines = [BooksInstanceInline]
    
#admin.site.register(Book, BookAdmin)

admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Status)

#admin.site.register(BookInstance)
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):

    list_display = ('book', 'status', 'borrower', 'due_back', 'id')

    list_filter = ('status', 'due_back')

    fieldsets = (
        ('Екземпляр Книги', {
            'fields': ('book', 'imprint', 'inv_num')
        }),
        ('Статус книги',{
            'fields': ('status', 'due_back', 'borrower')
        })
    )

    
#admin.site.register(BookInstance, BookInstanceAdmin)


