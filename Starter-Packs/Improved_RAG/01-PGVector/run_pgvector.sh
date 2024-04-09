docker run --name my_postgres -e POSTGRES_USER=demouser -e POSTGRES_PASSWORD=demopasswd \
-e POSTGRES_DB=mydb -p 5432:5432 \
-d pgvector/pgvector:pg12
