# StreamEvents

Aplicació **Django** per gestionar esdeveniments i usuaris (extensible): base educativa amb bones pràctiques (entorns, estructura, separació de templates/static, etc.).  
Opcionalment es pot integrar **MongoDB** (via `djongo`) més endavant.

---

## ✨ Objectius

- Practicar un projecte **Django modular**.  
- Treballar amb un **usuari personalitzat** (`app users`).  
- Organitzar **templates**, **static** i **media** correctament.  
- Introduir fitxers d'entorn (`.env`) i bones pràctiques **Git**.  
- Preparar el terreny per a futures funcionalitats (**API**, **auth avançada**, etc.).

---

## 🧱 Stack Principal

- **Python 3.11+**
- **Django 5+**
- **SQLite** (per defecte) o **MongoDB** (opcional via `djongo`)
- **dotenv** per gestió d'entorns
- **Faker** per generació de dades de prova

---

## 📂 Estructura Simplificada

streamevents/
├── config/
├── users/
├── templates/
├── static/
│ ├── css/
│ ├── js/
│ └── img/
├── media/
├── fixtures/
├── seeds/
├── requirements.txt
├── README.md
├── env.example
└── manage.py


---

## ✅ Requisits previs

- Python 3.11 o superior
- Pip i virtualenv instal·lats
- Git configurat

---

## 🚀 Instal·lació ràpida

```bash
git clone https://github.com/<usuari>/streamevents.git
cd streamevents
python -m venv venv
source venv/bin/activate    # o .\venv\Scripts\activate a Windows
pip install -r requirements.txt
cp env.example .env
python manage.py migrate
python manage.py runserver

🔐 Variables d'entorn (env.example)

DEBUG=True
SECRET_KEY=canvicontrasegna123
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3

👤 Superusuari

Crea un superusuari per accedir al panell d’administració:

python manage.py createsuperuser

🗃️ Migrar a MongoDB (opcional futur)

Si vols utilitzar MongoDB:

pip install djongo

Actualitza el teu settings.py:

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'streamevents_db',
    }
}

🛠️ Comandes útils

python manage.py runserver
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
python manage.py shell

💾 Fixtures (exemple)

Les fixtures s’utilitzen per carregar dades inicials com grups i usuaris.

📁 Fitxers:

users/fixtures/
├── 01_groups.json
└── 02_users.json

🧩 Carregar dades

Carregar grups

python manage.py loaddata users/fixtures/01_groups.json

Carregar usuaris

python manage.py loaddata users/fixtures/02_users.json

Verificar

python manage.py shell -c "from django.contrib.auth.models import Group; print(Group.objects.all())"
python manage.py shell -c "from django.contrib.auth import get_user_model; User=get_user_model(); print(User.objects.all())"

🌱 Seeds (exemple d’script)

El Seeder permet generar usuaris de prova automàticament amb dades realistes.

📄 Fitxer principal:

users/management/commands/seed_users.py

▶️ Ús bàsic

Crear 10 usuaris nous

python manage.py seed_users

Crear 25 usuaris nous

python manage.py seed_users --users 25

Esborrar usuaris antics i crear-ne de nous

python manage.py seed_users --clear

👥 Què crea

    Grups: Organitzadors, Participants, Moderadors

    Superusuari:
    Usuari: admin@streamevents.com
    Contrasenya: admin123

    Usuaris de prova amb contrasenya password123

📜 Llicència

Aquest projecte és d’ús educatiu i obert a millores. Pots reutilitzar-lo amb crèdit adequat.