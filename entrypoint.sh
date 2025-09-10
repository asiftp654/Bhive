
echo "Waiting for database..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done
echo "Database is ready!"

# Run Alembic migrations
echo "Running Alembic migrations..."
alembic upgrade head
