from django.contrib import admin
from .models import *


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created', 'modified')
    list_filter = ('name', 'description')
    list_display_links = ('name',)
    list_editable = ('description',)
    search_fields = ('name', 'description')


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInline)
    list_display = ('title', 'description', 'creation_date', 'rating', 'type',
                    'created', 'modified')
    list_filter = ('rating', 'creation_date')
    list_display_links = ('title',)
    list_editable = ('description',)
    search_fields = ('title', 'description')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'created', 'modified')
    list_filter = ('full_name',)
    list_display_links = ('full_name',)
    search_fields = ('full_name',)


