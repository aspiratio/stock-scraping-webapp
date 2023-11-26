#!/bin/bash

if [ "$ENVIRONMENT" = "local" ]; then
  cd /app/app && uvicorn main:app --host 0.0.0.0 --port 8000 --reload
else
  cd /app/app && uvicorn main:app
fi