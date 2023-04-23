import uuid
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(TimeStampedMixin, UUIDMixin):
    name = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    film_works = models.ManyToManyField('Filmwork', through='GenreFilmwork',
                                        verbose_name=_('filmworks'))

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Filmwork(TimeStampedMixin, UUIDMixin):
    class Type(models.TextChoices):
        MOVIE = 'M', 'Movie'
        TV_SHOW = 'TV', 'TV-show'

    title = models.CharField(_('title'), max_length=500)
    description = models.TextField(_('description'), blank=True)
    creation_date = models.DateField(_('creation_date'))
    rating = models.FloatField(_('rating'), blank=True,
                               validators=[MinValueValidator(0),
                                           MaxValueValidator(100)])
    type = models.TextField(_('type'), choices=Type.choices, null=True)
    genres = models.ManyToManyField(Genre, through='GenreFilmwork',
                                    verbose_name=_('genres'))
    persons = models.ManyToManyField('Person', through='PersonFilmwork',
                                     verbose_name=_('persons'))

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'

    def __str__(self):
        return self.title


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE,
                                  verbose_name=_('filmwork'))
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE,
                              verbose_name=_('genre'))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        verbose_name = 'Жанр фильма'
        verbose_name_plural = 'Жанры фильма'


class Person(TimeStampedMixin, UUIDMixin):
    full_name = models.CharField(_('full name'), max_length=255)
    film_works = models.ManyToManyField(Filmwork, through='PersonFilmwork',
                                        verbose_name=_('filmworks'))

    class Meta:
        db_table = "content\".\"person"
        verbose_name = "Персона"
        verbose_name_plural = "Персоны"

    def __str__(self):
        return self.full_name


class PersonFilmwork(UUIDMixin):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name=_('person'))
    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE,
                                  verbose_name=_('filmwork'))
    role = models.CharField(_('role'), max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        verbose_name = "Персона в фильме"
        verbose_name_plural = "Персоны в фильме"
