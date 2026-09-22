# Best Cars Dealerships — Full Stack Developer Capstone

A full-stack car dealership review application built with **Django**, **React**, **Node.js/Express**, and **MongoDB**, with a **Flask** microservice for review sentiment analysis.

## Project overview

Best Cars Dealerships lets visitors browse car dealerships across the US, filter them by state, view dealer details and customer reviews, and (once registered/logged in) post their own reviews. Each review's sentiment (positive/neutral/negative) is analyzed automatically by a standalone sentiment-analysis microservice.

## Architecture

- **`server/djangoproj` + `server/djangoapp`** — Django backend serving the React app, handling authentication (register/login/logout), car make/model data (SQLite), and acting as a proxy layer to the Node.js backend and sentiment microservice.
- **`server/frontend`** — React single-page application (dealers list, dealer detail + reviews, post-review form, login/register).
- **`server/database`** — Node.js/Express API backed by MongoDB, serving dealership and review data.
- **`server/djangoapp/microservices`** — Flask microservice using NLTK's VADER sentiment analyzer, deployed independently (e.g. on IBM Code Engine).

## Getting started

1. Install Python and Node.js dependencies:
   ```bash
   cd server && pip install -r requirements.txt
   cd frontend && npm install
   ```
2. Run the Node/Mongo backend (`server/database`) via Docker Compose.
3. Configure `server/djangoapp/.env` with `backend_url` and `sentiment_analyzer_url`.
4. Run migrations and start the Django server:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```
