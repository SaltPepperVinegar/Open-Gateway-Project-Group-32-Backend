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

### How to run the server 

```bash
#run the server

docker compose up -d mongo

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

## before you commit 

```bash
#Python linter
ruff check .
#Formatter
black . 
#Type checker
mypy app
```
