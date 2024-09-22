# Utiliser une image Python comme base
FROM python:3.10

ENV PYTHONUNBUFFERED 1

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Install pipenv
RUN pip install --upgrade pip 
RUN pip install pipenv

# Copier uniquement Pipfile et Pipfile.lock dans le conteneur
COPY Pipfile Pipfile.lock /app/


RUN pipenv install --system --dev

# Copy the application files into the image
COPY . /app/


# Exposer le port sur lequel l'application sera disponible
EXPOSE 8000

# Commande pour démarrer l'application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
