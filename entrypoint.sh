
echo "Waiting for database..."
python3 /app/wait_for_db.py

# Run Alembic migrations
echo "Running Alembic migrations..."
alembic upgrade head
