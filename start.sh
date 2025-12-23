#!/usr/bin/env bash
gunicorn App.wsgi:application
