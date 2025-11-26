IoT Device Security Management System (IoT-DSMS)

## Objectiff
Développer un système complet pour sécuriser, superviser et maintenir un parc d’appareils IoT.
Il combine :

Gestion sécurisée des appareils

Détection d’anomalies via ML

Automatisation des mises à jour (OTA)

Analyse de logs et génération de rapports PDF

API REST + Dashboard web admin

Architecture modulaire et extensible

## Fonctionnalités principales
1️.Device Security & Monitoring

Ajout, suppression et inventaire des appareils

Attribution de clés API sécurisées

Vérification d’intégrité

Scan de vulnérabilités basique

Suivi en temps réel (status, dernière communication)

2️.Automated Updates (OTA)

Déploiement de mises à jour firmware via API

Planification automatique

Validation cryptographique des firmware

Logs complets d’installation + rollback si échec

3️.Threat Detection (ML)

Analyse statistique ou modèle ML (Isolation Forest)

Détection d’anomalies réseau

Alertes automatiques vers le dashboard

Ajout possible d’un mode “honeypot IoT personnel”

4️.Log Analysis & Reporting

Agrégation des logs des appareils

Analyse sécurité (tentatives d’accès, anomalies)

Génération automatique de rapport PDF horodaté

Export pour audit de sécurité

5️.REST API + Web Dashboard

API FastAPI documentée (Swagger inclus)

Authentification par token

Dashboard simple (Flask + Bootstrap)

Visualisation : devices, rapports, alertes, mises à jour

## Structure du projet

IoT-DSMS/
│── src/
│   ├── api/               # API REST (FastAPI)
│   ├── core/              # Logic: devices, updates, security
│   ├── ml/                # Anomaly detection model
│   ├── reports/           # PDF report generator
│   └── dashboard/         # Flask admin dashboard
│
│── tests/                 # Tests unitaires
│── firmware/              # Exemples de firmware
│── requirements.txt
│── README.md
│── .gitignore

## Stack technique utilisée
Back-end

Python 3.10

FastAPI, Flask

SQLAlchemy

SQLite / PostgreSQL

Pydantic

PyPDF2 / reportlab

Security

bcrypt

Token-based Auth (HMAC)

Vérification intégrité SHA-256

Bonne gestion des secrets

Machine Learning

Scikit-learn — Isolation Forest

Détection d’anomalies IoT

Export / import du modèle

DevOps

Virtualenv

Git / GitHub Workflow

Logging structuré

Architecture modulaire

## Aperçu du Dashboard
TODO: add screenshots

## Exemple de cas d’utilisation
1) Ajouter un appareil

POST /devices/register
→ Génère clé API + tag de sécurité

2) Envoi de logs

POST /logs/send
→ Le système détecte anomalies → alerte

3) Lancer une mise à jour OTA

POST /updates/deploy

4) Générer un rapport sécurité

GET /reports/generate

## Installation & Lancement

    git clone https://github.com/<ton-username>/IoT-DSMS.git
    cd IoT-DSMS
    python -m venv .venv
    source .venv/bin/activate       # Windows: .venv\Scripts\activate
    pip install -r requirements.txt
    uvicorn src.api.main:app --reload
