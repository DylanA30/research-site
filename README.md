# Research Projects Site — Setup Guide

This scaffold gives you a Django "projects" app: models, admin, search/filter
views, and templates. You still need to create the outer Django project
shell (Django generates that for you), then drop these files in.

## 1. Set up your environment

```bash
python -m venv venv
source venv/bin/activate      # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Create the Django project shell

```bash
django-admin startproject research_site .
```

This generates `manage.py` and a `research_site/` folder with
`settings.py`, `urls.py`, etc. — don't overwrite the files I gave you,
they go alongside this.

## 3. Create the app folder

The `projects/` folder I gave you (models.py, admin.py, views.py,
urls.py, templates/) should sit at the same level as `manage.py`.

## 4. Update settings.py

Open `research_site/settings.py` and apply the changes shown in
`settings_additions.py` (add `"projects"` to INSTALLED_APPS, add the
STATIC/MEDIA config).

## 5. Update urls.py

Open `research_site/urls.py` and replace it with the contents of
`research_site_urls_example.py` (or merge the relevant lines in).

## 6. Create the database tables

```bash
python manage.py makemigrations projects
python manage.py migrate
```

## 7. Create an admin login

```bash
python manage.py createsuperuser
```

Follow the prompts (username, email, password).

## 8. Run it

```bash
python manage.py runserver
```

- Visit **http://127.0.0.1:8000/admin/** — log in, add some Tags, then
  add a Project (you can upload a cover image right in this form).
- Visit **http://127.0.0.1:8000/projects/** — see your projects, try
  the search box and tag filters.

## Notes for later

- Right now anyone can see /admin if they know your password — fine
  for local dev, but for production consider a stronger setup.
- When you're ready to deploy, `DEBUG = False` in settings.py and
  you'll need a real place to store uploaded images (S3, Cloudinary,
  etc.) since most hosts don't persist local files between deploys.
- To add more fields later (e.g. a PDF attachment, a "featured"
  checkbox), add them to `models.py`, then run
  `python manage.py makemigrations` and `migrate` again.
