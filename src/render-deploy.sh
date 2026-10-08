set -e

flask --app src.app db upgrade
exec gunicorn --bind "0.0.0.0:${PORT:-10000}" src.wsgi:app