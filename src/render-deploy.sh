set -e

.venv/Scripts/Activate
flask --app src.app db upgrade
flask gunicorn src.wsgi:app 