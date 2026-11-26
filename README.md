# Global Investment Website

A custom full-stack web platform developed for an Eritrean investment initiative.

## Overview

The Global Investment Website was built to support an Eritrean investment initiative through a web-based platform. It combines backend services, frontend interfaces and persistent data storage to provide an online environment for investment-related projects and user interaction.

The project was originally deployed at [eritreaninvestment.com](https://eritreaninvestment.com/). The website is currently offline because the domain and hosting services could not be renewed due to financial constraints. The live service is therefore temporarily unavailable, but the source code is preserved here for reference and portfolio purposes.

## Features

The platform includes functionality for:

- User registration, login and profile management
- Investment project creation and management
- Project discovery across different investment sectors
- Investment applications and collaboration
- Notifications and user interaction
- Contact and support pages
- Multilingual interface support

## Technology Stack

- **Backend:** Python, Django
- **Frontend:** HTML, CSS, JavaScript
- **Database:** Django-supported persistent data storage
- **Additional components:** Django REST Framework, reCAPTCHA, WhiteNoise and environment-based configuration

## Project Structure

- `global_investment/` – Main Django project configuration
- `projects/` – Investment project functionality, views, models and templates
- `users/` – User-related functionality
- `static/` – Static frontend assets
- `locale/` – Translation files
- `requirements.txt` – Python dependencies
- `.env.example` – Example environment configuration

## Local Setup

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd "Global Investment Website Project"
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

On Windows:

```powershell
venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root using `.env.example` as a reference.

Set your own Django secret key and configure any required email, reCAPTCHA and PayPal credentials.

Do not commit `.env` or publish real credentials.

### 5. Apply database migrations

```bash
python manage.py migrate
```

### 6. Start the development server

```bash
python manage.py runserver
```

## Configuration and Security

- Keep secret keys, passwords and API credentials outside source control.
- Use `.env.example` as a configuration template.
- Do not commit local databases, uploaded media or generated static files.
- Review security settings and third-party integrations before any future deployment.

## Project Status

This repository contains the source code of a previously deployed investment platform. It is published for portfolio, reference and educational purposes. It is not presented as a currently maintained or production-ready service.

## License

No license has been specified yet. All rights are reserved unless a license is added to this repository.
