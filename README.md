# Open-Gateway-Project

# FastAPI Backend

A backend service built with [FastAPI](https://fastapi.tiangolo.com/) and [Beanie](https://beanie-odm.dev/) (MongoDB ODM).  
Runs on **Python 3.13** inside a virtual environment.

---

## 🚀 Getting Started

uv python install 3.13.0 --force
uv venv --python 3.13 .venv
source .venv/bin/activate

python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt


#run the server
uvicorn app.main:app --reload

#mock mongodb
docker run --rm -d --name mongo_poc -p 27017:27017 mongo:7

#quick test
python -m pytest -q
