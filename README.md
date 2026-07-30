# Sam Writes (Blog Website)

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?logo=postgresql&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-EC2%20%7C%20S3-orange?logo=amazonaws&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen?logo=pytest&logoColor=white)

A full-stack blog application built with FastAPI, featuring secure JWT authentication, PostgreSQL, AWS S3 integration, asynchronous request handling, automated testing, and deployment on AWS EC2.

**Live Demo:** [https://samdindewrites.com](https://samdindewrites.com)
**API Documentation:** [https://samdindewrites.com/docs](https://samdindewrites.com/docs)

---

## Overview

Sam Writes is a production-oriented blog application built to explore modern backend development with FastAPI. The project exposes both a RESTful JSON API and a browser-based frontend, allowing users to register, authenticate, create blog posts, upload profile pictures, and interact with the application through a responsive web interface.

The project also demonstrates deployment practices such as reverse proxying with NGINX, HTTPS using Let's Encrypt, PostgreSQL database migrations with Alembic, cloud file storage using AWS S3, and automated testing with Pytest.

## Features

- User registration and login
- Secure JWT authentication
- Password hashing using Argon2
- CRUD operations for blog posts
- Browser-based frontend using Jinja2 templates
- RESTful API
- Automatic interactive API documentation (Swagger UI)
- PostgreSQL database
- SQLAlchemy ORM
- Database migrations with Alembic
- Async request handling
- Profile picture uploads
- AWS S3 integration for image storage
- Pagination
- Image validation and processing with Pillow
- Automated testing with Pytest
- Production deployment on AWS EC2 with NGINX and HTTPS

> **Note:** Password reset emails are currently configured using Mailtrap for development. AWS SES integration is planned for production.

## Tech Stack

**Backend**
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Pydantic
- PyJWT
- pwdlib (Argon2)

**Frontend**
- Jinja2
- Bootstrap
- JavaScript

**Cloud & Deployment**
- AWS EC2
- AWS S3
- NGINX
- Let's Encrypt (Certbot)

**Testing**
- Pytest
- Moto (AWS mocking)

## Project Structure

```
.
├── alembic/
├── routers/
├── models/
├── schemas/
├── services/
├── templates/
├── static/
├── tests/
├── main.py
├── database.py
├── config.py
└── README.md
```

## Environment Variables

Create a `.env` file containing:

```
SECRET_KEY=

DATABASE_URL=

MAIL_SERVER=
MAIL_PORT=
MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_FROM=
MAIL_USE_TLS=

FRONTEND_URL=

S3_BUCKET_NAME=
S3_REGION=
S3_ACCESS_KEY_ID=
S3_SECRET_ACCESS_KEY=
```

## Testing

Run the test suite with:

```bash
uv run pytest tests/
```

## Deployment

The application is deployed on AWS EC2 using:

- NGINX as a reverse proxy
- HTTPS with Let's Encrypt (Certbot)
- PostgreSQL
- AWS S3 for media storage

## License

This project is licensed under the MIT License. Replace this section with your actual license if different.