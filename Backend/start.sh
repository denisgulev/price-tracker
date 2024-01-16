#!/bin/bash

# Wait for the database to be ready
wait-for-it database:5432 -t 60

# Start your backend application
python app.py