# StreamEvents – Fixtures i Seeders

## 📦 Instal·lació inicial

1️⃣ Carrega els grups:
python manage.py loaddata users/fixtures/01_groups.json

2️⃣ Carrega els usuaris:
python manage.py loaddata users/fixtures/02_users.json

3️⃣ Comprova la càrrega:
python manage.py shell -c "from django.contrib.auth.models import Group; print(Group.objects.all())"
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); print(User.objects.all())"
