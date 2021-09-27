#!/bin/sh

python -m wait_for_service --service-name redis &&
uvicorn src.main:app --host 0.0.0.0 --port 5000 --workers 9