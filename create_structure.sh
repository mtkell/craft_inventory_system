#!/bin/bash

# Backend structure
mkdir -p backend/app/{api,crud,db,core,models,schemas,utils}
touch backend/app/{api,crud,db,core,models,schemas,utils}/__init__.py
touch backend/app/main.py
cat <<EOF > backend/Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

# Frontend structure
mkdir -p frontend/public frontend/src/{components,pages,services,utils}
echo "<!-- HTML entry -->" > frontend/public/index.html
echo "// React app entry point" > frontend/src/main.jsx

# Docker Compose
cat <<EOF > docker-compose.yml
version: '3.9'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app

  frontend:
    image: node:18
    working_dir: /app
    volumes:
      - ./frontend:/app
    command: ["npm", "run", "dev"]
    ports:
      - "3000:3000"

  db:
    image: postgres:16
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: inventory
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
EOF

# Docker placeholder for Caddy/NGINX configs
mkdir -p docker