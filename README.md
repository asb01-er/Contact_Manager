Contact Manager

A contact-management application built with HTMX. Users can create, edit and delete contacts, with asynchronous HTML updates that refresh only the relevant part of the page instead of reloading it.

Live demo: https://contact-manager-amgu.onrender.com
Code: https://github.com/asb01-er/Contact_Manager

The demo runs on a free Render server, so the first load can take up to 30 seconds.

Features
Add new contacts
Edit existing contacts
Delete contacts
HTMX-powered updates without a full browser reload
Tech stack
HTMX
Server-rendered HTML
Python and Django (if this project uses them, keep this line; otherwise replace it with your backend)
Getting started
bash
git clone https://github.com/asb01-er/Contact_Manager.git
cd Contact_Manager

python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

Open http://127.0.0.1:8000.

Deployment

Deployed on Render. Set any required environment variables (such as SECRET_KEY) in Render's Environment tab and start the app with Gunicorn.

Author

Ernest Ekelem — GitHub · LinkedIn
