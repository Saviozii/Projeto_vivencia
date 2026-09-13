#!/bin/sh
set -e

if [ "${DJANGO_SETUP:-true}" = "true" ]; then
  echo "==> Aplicando migrações..."
  python manage.py migrate --noinput

  echo "==> Coletando arquivos estáticos..."
  python manage.py collectstatic --noinput

  if [ -n "$DJANGO_SUPERUSER_USERNAME" ]; then
    echo "==> Criando/atualizando superusuário..."
    python manage.py shell -c "
import os
from django.contrib.auth import get_user_model
User = get_user_model()
u, criado = User.objects.get_or_create(
    username=os.environ.get('DJANGO_SUPERUSER_USERNAME'),
    defaults={
        'email': os.environ.get('DJANGO_SUPERUSER_EMAIL', ''),
        'is_staff': True,
        'is_superuser': True,
    },
)
u.is_staff = True
u.is_superuser = True
u.set_password(os.environ.get('DJANGO_SUPERUSER_PASSWORD', ''))
u.save()
print('Superusuário pronto' if criado else 'Superusuário já existia')
"
  fi
fi

exec "$@"