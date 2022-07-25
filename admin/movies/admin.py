from django.contrib import admin

from .models import FilmWork, Genre, Person


class PersonRoleInline(admin.TabularInline):
    exclude = ("id",)
    model = FilmWork.persons.through
    extra = 1
    raw_id_fields = [
        "person",
    ]
    ordering = ("role", "person__full_name")


class FilmWorkGenreInline(admin.TabularInline):
    exclude = ("id",)
    model = FilmWork.genres.through
    extra = 1


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "type",
        "rating",
        "creation_date",
        "updated_at",
    )
    list_filter = ("type",)
    search_fields = (
        "title",
        "rating",
    )
    fieldsets = (
        (
            "Общее",
            {
                "fields": (
                    "title",
                    "type",
                    "description",
                )
            },
        ),
        ("Дата создания фильма", {"fields": ("creation_date",)}),
        ("Сертификат", {"fields": ("certificate",)}),
        ("Рейтинг фильма", {"fields": ("rating",)}),
        ("Файл", {"fields": ("file_path",)}),
    )

    inlines = [PersonRoleInline, FilmWorkGenreInline]


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "birth_date",
        "created_at",
        "updated_at",
    )
    search_fields = ("full_name",)
    fields = (
        "full_name",
        "birth_date",
    )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "created_at",
        "updated_at",
    )
    search_fields = ("name",)
    fields = (
        "name",
        "description",
    )
