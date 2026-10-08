set -e

.venv/Scripts/Activate
flask --app src.app db upgrade
gunicorn src.wsgi:app