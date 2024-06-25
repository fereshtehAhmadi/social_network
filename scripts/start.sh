#!/bin/sh

set -o errexit
set -o pipefail
set -o nounset

pip3 install -r ./requirements/base.txt && \
python3 manage.py wait_for_db && \
python3 manage.py wait_for_db && \
python3 manage.py migrate --database=default && \
python3 manage.py collectstatic --no-input && \
gunicorn --bind 0.0.0.0:$PORT core.wsgi
