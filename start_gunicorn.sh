#!/bin/bash
cd /app/vajrabox
exec gunicorn --config ../gunicorn.conf.py vajrabox.wsgi:application
