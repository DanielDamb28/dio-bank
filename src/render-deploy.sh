set -e

flask --app src.app db upgrade
flask gunicorn src.wsgi:app 