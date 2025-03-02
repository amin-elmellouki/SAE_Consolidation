
FROM python:3.10


WORKDIR /

COPY . /

# Installe les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Expose le port 8000 pour Django
EXPOSE 8000

# Lancement de Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
