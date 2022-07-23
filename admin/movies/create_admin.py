from django.contrib.auth import get_user_model


def create_admin() -> None:
    User = get_user_model()
    if not User.objects.exists():
        print(User.objects.exists())
        User.objects.create_superuser("admin", "admin@gmail.com", "admin")


if __name__ == "__main__":
    create_admin()
