from django.contrib import admin

# Register your models here.

from .models import Author, Genre, Book, BookInstance, Language, Adaptation

# admin.site.register(Author)
# admin.site.register(Book)
# admin.site.register(BookInstance)
admin.site.register(Genre)

# next line because I completed the challenge in the tutorial
admin.site.register(Language)


class BooksInline(admin.TabularInline):
    model = Book
    extra = 0


# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "date_of_birth", "date_of_death")
    fields = ["first_name", "last_name", ("date_of_birth", "date_of_death")]
    inlines = [BooksInline]


# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0


# Register the Admin classes for Book using the decorator
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "display_genre")
    inlines = [BooksInstanceInline]


# Register the Admin classes for BookInstance using the decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ("book", "status", "due_back", "imprint", "id", "borrower")
    list_filter = ("status", "due_back")

    fieldsets = (
        (None, {"fields": ("book", "imprint", "id")}),
        ("Availability", {"fields": ("status", "due_back", "borrower")}),
    )

@admin.register(Adaptation)
class AdaptationAdmin(admin.ModelAdmin):
    list_display = ("title", "media_type", "release_date", "book_display", "creator_display")
    search_fields = ("title",)
    list_filter = ("media_type", "release_date")
    filter_horizontal = ("creator",)

    def book_display(self, obj):
        """Display the related book title."""
        return obj.book.title
    book_display.short_description = "Book"

    def creator_display(self, obj):
        """Display creators as a comma-separated list."""
        return ", ".join(author.__str__() for author in obj.creator.all())
    creator_display.short_description = "Creators"
