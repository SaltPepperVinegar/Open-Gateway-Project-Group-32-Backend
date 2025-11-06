# Open-Gateway-Project

# FastAPI Backend

A backend service built with [FastAPI](https://fastapi.tiangolo.com/) and [Beanie](https://beanie-odm.dev/) (MongoDB ODM).  
Runs on **Python 3.13** inside a virtual environment.

---

## 🚀 Setup
 
```bash
uv python install 3.13.0 --force
uv venv --python 3.13 .venv
source .venv/bin/activate
 
python -m pip install -U pip setuptools wheel "pip-tools==7.4.1"
pip install -r requirements.txt
pip install -r requirements-dev.txt

pre-commit install

cp .env.example .env
```

### Firebase Auth Setup for Development

#### 1. Generate Service Account Key
- Go to [Firebase Console](https://console.firebase.google.com/)  
- Select project **ogwp** → **Project settings** → **Service accounts**  
- Click **Generate new private key**  
- Download the `.json` file (keep it private, do not commit)

#### 2. Store the Key
- Move the file into:  
  `Open-Gateway-Project-Group-32/secrets/your-firebase-private-key.json`

#### 3. Configure `.env`
Add the following new line to .env
`FIREBASE_CRED_PATH=secrets/your-firebase-private-key.json`

#### 4. Access in code
```
from app.core.config import settings
print(settings.FIREBASE_CRED_PATH)
# -> secrets/your-firebase-private-key.json
```

### How to run the server locally 

```bash
#run the server

docker compose up --build

#quick test

python -m pytest -q
```

### everytime after you added dependency

```bash
pip-compile --no-header --no-annotate --strip-extras \
-o requirements.txt requirements.in
pip-compile --no-header --no-annotate --strip-extras \
    -o requirements-dev.txt requirements-dev.in

pip install -r requirements.txt

pip install -r requirements-dev.txt
```

### before you commit 

```bash
#Python linter
ruff check .
#Formatter
black . 
#Type checker
mypy app
```


# 📦 Deployment
### This project (Open-Gateway-Project) is a FastAPI backend powered by MongoDB and Firebase authentication, containerized via Docker, and deployable on Google Cloud Run.

## Prerequisites

- Google Cloud Project (with billing enabled)

- gcloud CLI installed (install guide)

- Docker installed and running

- A configured MongoDB Atlas Cluster (or self-hosted MongoDB)

- Firebase project service account key (.json) placed under secrets/


## Service Information

Project Name: Open-Gateway-Project

Service Name: open-gateway-project-group-32-backend

Cloud Provider: Google Cloud Platform (GCP)

Region: australia-southeast2

Runtime: Python 3.13 (FastAPI + Beanie + MongoDB)

Database: MongoDB Atlas (remote cluster)

Authentication: Firebase (Admin SDK + Frontend credentials)

Deployment Method: Google Cloud Build (GitHub hook) → Cloud Run

### Service URL: https://open-gateway-project-group-32-backend-758384409722.australia-southeast2.run.app

## Deployment Steps Taken

### 1. Built and Tested Locally

- Verified FastAPI backend with Docker Compose + MongoDB.

- Confirmed endpoints (/health, /docs) work.

### 2. Dockerized Application

- Production-ready Dockerfile created.

- Image tagged as gcr.io/saltpeppervinegar/open-gateway-project-backend

### 3. Google Cloud Build Setup

- Configured GitHub repository trigger in Google Cloud Build.

- Trigger runs on push to main branch.

- Build steps:

  1. docker build image

  2. push to Google Artifact Registry / Container Registry
    
  3. Deployed to Cloud Run

- Service deployed successfully with revision-based rollout.

- Environment variables configured:

- MONGO_DSN: Atlas connection string

- FIREBASE_CRED: 
  - Firebase Admin SDK service account (JSON, base64-encoded in secrets).

  - Used for backend authentication & verification of user tokens. 

- FIREBASE_FRONTEND_CRED
  - Firebase Frontend SDK config (API key, projectId, messagingSenderId, etc.).

  - Used to allow client-side apps (web/mobile) to authenticate against the same Firebase project.

## Continuous Deployment (CI/CD)

- GitHub Actions Workflow set up for auto-deploy on main branch push
- CI Workflow: .github/workflows/ci.yml
- CD Workflow: .github/workflows/cd.yml

### GitHub → Google Cloud Build → Cloud Run pipeline is active.

#### On every push to main:

1. Google Cloud Build runs.

2. Docker image is built & pushed to registry.

3. Cloud Run deploys new revision.

4. Traffic gradually shifted to new revision (safe rollout).

## Deployment Outcome

- Status: ✅ Successful

- Cloud Run Revision: latest deployment serving 100% traffic

- Scalability: Auto-scaled by Cloud Run (min instances = 0, max = dynamic)

- MongoDB succesfully connected

- Firebase Authen successfully connected 


##  Security

- **Firebase Auth** enabled

- **IAM authentication** enabled  

- .env secrets managed via **Cloud Run environment variables**

- secrets managed by **Google Cloud secret manager**

- **MongoDB IP** filter (in future)
