import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Time(models.Model):
    created_at = models.DateTimeField(
        _("created date"),
        auto_created=True,
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        _("date updated"),
        auto_created=True,
        auto_now=True,
    )

    class Meta:
        abstract = True


class Genre(Time):
    id = models.UUIDField(
        _("id"),
        primary_key=True,
        default=uuid.uuid4,
    )
    name = models.TextField(
        _("title"),
        max_length=255,
        unique=True,
    )
    description = models.TextField(_("description"), blank=True, null=True)

    class Meta:
        db_table = "genre"
        ordering = ("-updated_at",)
        verbose_name = _(
            "genre",
        )
        verbose_name_plural = _(
            "genres",
        )

    def __str__(self):
        return self.name


class FilmWorkType(models.TextChoices):
    MOVIE = "movie", _("movie")
    TV_SHOW = "tv_show", _("tv show")


class FilmWork(Time):
    id = models.UUIDField(
        _("id"),
        primary_key=True,
        default=uuid.uuid4,
    )
    title = models.TextField(
        _("title"),
        max_length=255,
    )
    description = models.TextField(
        _("description"),
        blank=True,
    )
    creation_date = models.DateField(
        _("created date the film"),
        blank=True,
        null=True,
    )
    certificate = models.TextField(
        _("certificate"),
        blank=True,
        null=True,
    )
    file_path = models.FileField(
        _("file"),
        upload_to="film_works_img/",
        blank=True,
        null=True,
    )
    rating = models.FloatField(
        _("rating"),
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        blank=True,
    )
    type = models.TextField(
        _("type"),
        max_length=20,
        choices=FilmWorkType.choices,
    )
    persons = models.ManyToManyField(
        "Person",
        through="PersonFilmWork",
        related_name="film_works",
        verbose_name=_("персона"),
    )
    genres = models.ManyToManyField(
        "Genre",
        through="FilmWorkGenre",
        related_name="film_works",
        verbose_name=_("жанры"),
    )

    class Meta:
        db_table = "film_work"
        ordering = ("-creation_date",)
        verbose_name = _("cinema")
        verbose_name_plural = _("cinema")

    def __str__(self):
        return self.title


class Person(Time):
    id = models.UUIDField(
        _("id"),
        primary_key=True,
        default=uuid.uuid4,
    )
    full_name = models.TextField(
        _("full name"),
        max_length=120,
    )
    birth_date = models.DateField(
        _("birth date"),
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "person"
        ordering = ("-updated_at",)
        verbose_name = _("role")
        verbose_name_plural = _("roles")

    def __str__(self):
        return self.full_name


class RoleType(models.TextChoices):
    director = "director", _("director")
    actor = "actor", _("actor")
    writer = "writer", _("writer")


class PersonFilmWork(models.Model):
    id = models.UUIDField(
        _("id"),
        primary_key=True,
        default=uuid.uuid4,
    )
    film_work = models.ForeignKey(
        FilmWork,
        on_delete=models.CASCADE,
        related_name="person_film_work",
        verbose_name=_("cinema"),
    )
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="person_film_work",
        verbose_name=_("person"),
    )
    role = models.TextField(
        _("role"),
        choices=RoleType.choices,
    )
    created_at = models.DateTimeField(
        _("created date"),
        auto_created=True,
        auto_now_add=True,
    )

    class Meta:
        db_table = "person_film_work"

    def __str__(self):
        return str(self.person)


class FilmWorkGenre(models.Model):
    id = models.UUIDField(
        _("id"),
        primary_key=True,
        default=uuid.uuid4,
    )
    film_work = models.ForeignKey(
        FilmWork,
        on_delete=models.CASCADE,
        related_name="film_work_genre",
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name="film_work_genre",
        verbose_name=_("genre"),
    )
    created_at = models.DateTimeField(
        _("created date"),
        auto_created=True,
        auto_now_add=True,
    )

    class Meta:
        db_table = "genre_film_work"
