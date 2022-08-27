docker build -t web:latest .
docker run -d --name ecart-server --env-file .env -p 8000:8000 web:latest