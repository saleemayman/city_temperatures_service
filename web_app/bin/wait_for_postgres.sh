#!/bin/sh
# The script waits and checks if postgresDB is ready to accept
# connections. The script exits once DB is ready.
# Without this the Flask app will try to connect to DB before it
# is up and accepting connections.
set -e
  
shift
cmd="$@"

# wait for postgres DB to be started and setup.
echo "Postgres is starting, will take a  4 to 5 minutes . . ."
sleep 240
until PGPASSWORD=$POSTGRES_PASSWORD psql -d $POSTGRES_DB -h $DATABASE_HOST -U $POSTGRES_USER -c '\q'; do
  >&2
  echo ""
  echo "Postgres not yet accepting connections, retrying . . ."
  sleep 30
done

>&2 echo "Postgres is up."
exec "$@"
