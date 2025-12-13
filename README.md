# 🎬 StreamEvents

**StreamEvents** is a web platform for discovering, creating, and managing live streaming events. Built with Django and MongoDB, it allows users to organize events across various categories like gaming, music, education, and more.

## ✨ Features

- **👤 User Authentication**: Custom user model with profile management
- **🎯 Event Management**: Create, edit, schedule, and delete streaming events
- **📊 Categories**: Organized events across multiple categories (Gaming, Music, Education, etc.)
- **🔍 Smart Filtering**: Search and filter events by category, status, date, and tags
- **📱 Responsive Design**: Mobile-friendly interface with Bootstrap 5
- **🔴 Live Streaming**: Integration with YouTube and Twitch streaming platforms
- **⭐ Featured Events**: Highlight special events on the homepage
- **📅 Event Status**: Real-time status tracking (Scheduled, Live, Finished, Cancelled)

## 🛠️ Tech Stack

- **Backend**: Django 4.1, Django REST Framework
- **Database**: MongoDB with Djongo ORM
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Templates**: Django Template Language (DTL)
- **Authentication**: Django's built-in auth with custom user model
- **Deployment**: Ready for deployment on platforms like Heroku, Railway, or PythonAnywhere

## 📁 Project Structure

```
streamevents/
├── config/                 # Django project settings
│   ├── settings.py        # Project configuration
│   ├── urls.py           # URL routing
│   └── wsgi.py           # WSGI configuration
├── users/                 # User management app
│   ├── models.py         # CustomUser model
│   ├── views.py          # User views (profile, registration)
│   ├── forms.py          # User forms
│   └── templates/        # User templates
├── events/                # Core events app
│   ├── models.py         # Event model with categories
│   ├── views.py          # Event CRUD operations
│   ├── forms.py          # Event creation/editing forms
│   └── management/
│       └── commands/     # Custom management commands
│           ├── seed_events.py    # Generate sample events
│           └── cleanup_data.py   # Data cleanup utilities
├── templates/             # Base templates
│   ├── base.html         # Main template
│   ├── home.html         # Landing page
│   └── includes/         # Reusable components
├── static/               # Static files (CSS, JS, images)
├── media/                # User-uploaded files (ignored in git)
├── fixtures/             # Sample data
└── requirements.txt      # Python dependencies
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MongoDB (local or cloud)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/streamevents.git
   cd streamevents
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate
   
   # Mac/Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Copy example environment file
   cp .env.example .env
   
   # Edit .env with your settings
   # SECRET_KEY=your-secret-key-here
   # DEBUG=True
   # ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Seed database with sample data** (optional)
   ```bash
   python manage.py seed_users --users 10
   python manage.py seed_events --events 20
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```

9. **Visit the application**
   - Homepage: http://localhost:8000
   - Admin: http://localhost:8000/admin
   - Events: http://localhost:8000/events

## 📊 Database Models

### User Model (`users/models.py`)
- Custom user with extended fields (display name, bio, avatar)
- Profile management system
- Event creator relationships

### Event Model (`events/models.py`)
- **Title & Description**: Event details
- **Category**: Gaming, Music, Education, Sports, etc.
- **Status**: Scheduled, Live, Finished, Cancelled
- **Scheduling**: Date/time with automatic status updates
- **Streaming**: YouTube/Twitch URL integration with embed support
- **Tags**: Categorization and search optimization
- **Featured Events**: Highlight special events

## 🎮 Management Commands

### Create Sample Data
```bash
# Create 10 sample users
python manage.py seed_users --users 10

# Create 15 sample events
python manage.py seed_events --events 15

# Clear all data and start fresh
python manage.py cleanup_data --force
```

### Available Options
```bash
# Seed users with specific options
python manage.py seed_users --users 20 --clear --with-follows

# Seed events with specific options
python manage.py seed_events --events 25 --clear --with-users

# Cleanup options
python manage.py cleanup_data --events-only
python manage.py cleanup_data --users-only
python manage.py cleanup_data --force  # Skip confirmation
```

## 🌐 API Endpoints

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| GET | `/` | Homepage | Public |
| GET | `/events/` | List all events | Public |
| GET | `/events/<id>/` | Event details | Public |
| GET | `/events/category/<category>/` | Events by category | Public |
| GET | `/events/my-events/` | User's events | Required |
| POST | `/events/create/` | Create event | Required |
| PUT | `/events/<id>/edit/` | Update event | Owner only |
| DELETE | `/events/<id>/delete/` | Delete event | Owner only |
| GET | `/users/profile/` | User profile | Required |
| GET | `/users/register/` | User registration | Public |
| GET | `/users/login/` | User login | Public |
| POST | `/users/logout/` | User logout | Required |

## 🎨 UI Components

### Event Cards
- Responsive grid layout
- Category badges with icons
- Status indicators (Live, Scheduled, Finished)
- Featured event highlights
- Quick action buttons

### Navigation
- Category dropdown menu
- User authentication links
- Responsive mobile menu
- Breadcrumb navigation

### Forms
- Bootstrap-styled forms
- Form validation
- File upload for event thumbnails
- Date/time pickers

## 🔧 Configuration

### Django Settings (`config/settings.py`)
Key configurations:
```python
# Database (MongoDB with Djongo)
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'streamevents_db',
        'ENFORCE_SCHEMA': False,
        'CLIENT': {
            'host': 'mongodb://localhost:27017'
        }
    }
}

# Custom user model
AUTH_USER_MODEL = 'users.CustomUser'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Internationalization
LANGUAGE_CODE = 'ca'  # Catalan
TIME_ZONE = 'Europe/Madrid'
```

### Environment Variables
Create a `.env` file with:
```env
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

## 🚀 Deployment

### Heroku Deployment
```bash
# Create Procfile
echo "web: gunicorn config.wsgi --log-file -" > Procfile

# Create runtime.txt
echo "python-3.9.0" > runtime.txt

# Add MongoDB addon
heroku addons:create mongolab:sandbox

# Deploy
git push heroku main
```

### Railway Deployment
1. Connect your GitHub repository
2. Add MongoDB database
3. Set environment variables
4. Deploy

## 📱 Features in Detail

### Event Categories
- **🎮 Gaming**: Video game streams, tournaments, esports
- **🎵 Music**: Concerts, DJ sets, acoustic sessions
- **📚 Education**: Tutorials, workshops, courses
- **💬 Talk**: Discussions, debates, conferences
- **⚽ Sports**: Live sports, fitness streams
- **🎭 Entertainment**: Comedy, variety shows
- **💻 Technology**: Tech talks, coding streams
- **🎨 Art**: Creative streams, art tutorials

### Event Status System
- **🟢 Scheduled**: Future events (blue badge)
- **🔴 Live**: Currently streaming (red badge with animation)
- **⚫ Finished**: Completed events (gray badge)
- **⚪ Cancelled**: Cancelled events (dark badge)

### Streaming Integration
- **YouTube**: Automatic embed URL conversion
- **Twitch**: Channel embedding support
- **Custom URLs**: Any streaming platform support

## 🧪 Testing

Run the test suite:
```bash
# Run all tests
python manage.py test

# Test specific app
python manage.py test users
python manage.py test events
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👏 Acknowledgments

- [Django](https://www.djangoproject.com/) - The web framework
- [Bootstrap](https://getbootstrap.com/) - CSS framework
- [Djongo](https://www.djongomapper.com/) - MongoDB connector for Django
- [Font Awesome](https://fontawesome.com/) - Icons
- [Faker](https://faker.readthedocs.io/) - Test data generation

## 📞 Support

For support, email your-email@example.com or create an issue in the GitHub repository.

---

**Made by Mohammed Ben Brahim**