# Neutrino

## Project Style guid 
```bash 

project_name/  
├── config/                  # settings (Django Project)  
│   ├── __init__.py  
│   ├── settings/  
│   │   ├── base.py          # base settings 
│   │   ├── development.py   # development.py  
│   │   ├── production.py    # production  
│   │   └── ...  
│   ├── urls.py  
│   └── wsgi.py  
├── apps/                    # apps :from django  
│   ├── accounts/            # account 
│   ├── otp/                # otp
│   └── posts/
|   └── ... 
├── static/                  
├── manage.py  
├── requirements.txt         #  dependencies  
└── .env                     
```
- for more info  abuot django style guide  <a>https://github.com/HackSoftware/Django-Styleguide.git</a>


# info about apps 
## account 
```bash
├── account
# show that api is work ? ..
    ├── ConnectionService
    ├── LogginService
    └── SignService
    ---
    ├── ./tasks.py
    ├── ./tests.py
    ├── ./urls.py
    ├── ./validator.py
    └── ./views.py

```
## why am use th diffrend app 

```bash
project/
├── apps/
│   ├── api/               #  API (Views, Serializers)
│   ├── core/              #  bussines logic aont depended With api Artichetre 
│   │   ├── core.py     
│   └── ...
└── ...
```
Business Logic from API Layer in Django
🧠 Why should we separate business logic from API?

Reusability: Business logic can be used by multiple APIs or even different UIs.

Better testability: It is easier to test business logic independently of the API layer.

Flexibility: If requirements or technologies change (e.g., switching from REST to GraphQL), only the API layer needs to change.

Readability and maintainability: The code becomes cleaner and more organized.

Security: Centralized control over critical business operations.

```python 

from myapp.mybusinesslogic.core.service import TO_DO_something

from rest_framework.views import APIView
from rest_framework.response import Response

class CustomApiView(APIView):
    def get(self , request , **kwargs):
        
        
        return Response(TO_DO_something)

```

if i want to change my Logic  Dont not to Refactor Code from 
Api we just change bussiness logic 

```python 
from myapp.mybusinesslogic1.core1.service1 import TO_DO_something1 as TO_DO_something1
class CustomApiView(APIView):
    def get(self , request , **kwargs):
        
        
        return Response(TO_DO_something)

```
## how about Architecture of api

# Authentication API Documentation

## Overview

This Django REST Framework API provides a flexible and secure authentication system with multiple login methods:

- **Phone OTP login** (via SMS)  
- **Email login** (placeholder for future implementation)  
- **Username/password login** with JWT tokens  

---

## Key Components

### 1. BaseLoginApi (Abstract Base Class)

The core foundation for all authentication endpoints, providing:

- Standardized request and response handling  
- Centralized logging infrastructure  
- Serializer management  
- Abstract method to implement custom login logic

```python
class BaseLoginApi(APIView, ABC):
    # Defines core authentication flow structure
```



# Security 
# 🛡️ XSS Protection System for Django Apps

## ✨ Overview

Before deploying any application to production, **user input must be sanitized** to prevent malicious attacks like **Cross Site Scripting (XSS)**.

This small but powerful module provides an extendable and maintainable structure for XSS protection by combining:

- ✅ Custom request validators
- ✅ Regex-based input filtering
- ✅ Django middleware integration
- ✅ **SOLID** principles for clean, scalable architecture

---

## 🚀 Features

- Detects potentially malicious XSS payloads using customizable regex
- Integrates easily with Django middleware and views
- Built with abstraction in mind for future extension
- Promotes **Dependency Inversion** and **Single Responsibility** principles
- Follows the **Open/Closed Principle** (easy to extend, no need to modify)

---

## 🧠 Architecture & Design Principles

This project is built on **SOLID Principles**:

| Principle | Applied How |
|----------|--------------|
| ✅ S - Single Responsibility | Each class has one responsibility: validation, request handling, configuration, etc. |
| ✅ O - Open/Closed | Easily extend or plug in new validators without modifying core logic |
| ✅ L - Liskov Substitution | Abstract classes/interfaces make it easy to substitute validators |
| ✅ I - Interface Segregation | Interfaces (`abstractmethod`) ensure each class only implements what it needs |
| ✅ D - Dependency Inversion | Validators are injected and separated from their usage contexts |

---

## 🧩 Code Structure

### 1. `BaseRequestValidator`

An abstract class for any validation provider that uses a `configure()` method on request:

```python
class BaseRequestValidator(ABC):
    def __init__(self, request):
        self._request = request
        self.configure()

    @abstractmethod
    def configure(self):
        ...
```


## XssSecurityProvider

### 1. `BaseRequestValidator`

A concrete implementation that scans all POST data and checks it against a regex pattern: 

```python
class XssSecurityProvider(BaseRequestValidator):
    def configure(self):
        regex_validator = RegexDjangovalidation()
        for key, value in self.request.POST.items():
            regex_validator.validate(value)

```
## Middleware Integration

### 1. `BaseRequestValidator`

Add full protection to your entire application by plugging in the middleware:
```python


class XssSanitizerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method in ['POST', 'PUT']:
            try:
                XssSecurityProvider(request)
            except Exception as e:
                return JsonResponse(
                    {'error': 'Potential XSS attack detected', 'detail': str(e)},
                    status=403
                )
        return self.get_response(request)

```
➕ Add to your Django settings:
```python
# settings 
MIDDLEWARE = [
    ...,
    'yourapp.middleware.xss_middleware.XssSanitizerMiddleware',
]
```
   

# and why we just use midleware ???

- ### it is adaptabe to use in your api 
- Middleware is great for global protection, but sometimes you need fine-grained control.

- Middleware is great for global protection, but sometimes you need fine-grained control.
```python
from neutrino.core.provider import XssSecurityProvider

class CustomApiView:
    requests_provider = (XssSecurityProvider,)

```

# 🔐 Django `SECRET_KEY` Rotation with Celery

## 📌 Overview

This project includes a Celery task that automatically **rotates Django's **``, updates the `.env` file, and **restarts the service** using `supervisorctl`.

This mechanism improves application security and is useful in scenarios like periodic secret rotation or on-demand key changes.

---

## ✅ Current Implementation

- Uses Python's `secrets.token_urlsafe(64)` to generate a strong secret key.
- Safely replaces the old `SECRET_KEY` in the `.env` file by rewriting it (instead of using `sed`).
- Restarts the Django service (e.g., `neutrino`) via `supervisorctl`.
- Logs all actions and handles errors gracefully.

### Celery Task Code

```python
@shared_task(ignore_result=True) #TODO add The hasicorp value
def SECRET_KEY_CHANGE():
    new_secret_key = secrets.token_urlsafe(64)
    sed_command = f"sed -i 's/^SECRET_KEY=.*/SECRET_KEY={new_secret_key}/' .env && supervisorctl restart neutrino"
    subprocess.run(sed_command , shell=True , check=False)

```

---

## 🚧 Future Plans

> 🛠 **TODO: Integrate HashiCorp Vault**

- This current method is suitable for development and temporary setups.
- In production, we plan to **store **``** securely in HashiCorp Vault**, and dynamically fetch it at runtime or inject it through a secrets manager or environment injection system.
- This will eliminate the need to store sensitive keys in plaintext `.env` files and allow for secure secret rotation and audit logging.

---

```docker
$ docker run --cap-add=IPC_LOCK -e 'VAULT_DEV_ROOT_TOKEN_ID=neutrino' -e 'VAULT_DEV_LISTEN_ADDRESS=0.0.0.0:1234' hashicorp/vault
```
- get The my_secret_value

```bash 
vault kv put secret/neutrino/config SECRET_KEY="my_secret_value"
```
- how het it 
```bash
vault kv get secret/myapp/config
```

# How About Proudction 

## Compare About how we use docker registery 

**Required:**

- traefik
- docker


## Installation

```bash
# Basic version
docker compose up -d 


docker pull regitery.parsakhaki.com/services/backend/neutrino:lastest

```
# for more info about docker and docker registry 
- ## https://github.com/overdoseparsa/Django-Ci-CD.git
<br><br>
<img src="readmePhoto/docker-regisrty.png" alt="MANDRILL" >



--OTP 
Overview

This module provides flexible authentication services for Django applications, supporting multiple authentication methods including:

    Phone number OTP login

    Email OTP login (TODO)

    Username/password login (JWT)

Features

    Multiple Authentication Methods: OTP (Phone/Email) and traditional username/password

    JWT Support: Secure token-based authentication

    Request Validation: Built-in rate limiting and OTP verification

    Factory Pattern: Flexible user retrieval system

    Logging: Comprehensive activity logging

API Endpoints
1. Phone OTP Login

    Endpoint: /loggin/

    Method: POST

    Request Body:
    json
```bash
{
  "token": "OTP_TOKEN"
}

Response:
json

    {
      "user": { /* user details */ },
      "access": "JWT_ACCESS_TOKEN",
      "refresh": "JWT_REFRESH_TOKEN"
    }

2. Username/Password Login

    Endpoint: /loggin/username/

    Method: POST

    Request Body:
    json

    {
      "username": "USERNAME",
      "password": "PASSWORD"
    }

    Response: Same as Phone OTP Login
```
Architecture
Core Components

    BaseLoginApi (api.py)

        Abstract base class for all authentication APIs

        Handles request validation, logging, and response formatting

        Uses JWT for token generation

    BaseOtpLoginService (selector.py)

        Abstract service class for OTP-based authentication

        Validates OTP tokens and request limitations

        Implements factory pattern for user retrieval

    User Factories (selector.py)

        SimpleOrmFactory: Basic ORM user lookup

        HashFindFactory: Hashed field lookup (TODO)

Authentication Flows
OTP Login Flow

    Client submits OTP token

    System verifies OTP validity

    Factory retrieves user based on OTP context (phone/email)

    Returns user details with JWT tokens

Username/Password Flow

    Client submits credentials

    System verifies against database

    Returns user details with JWT tokens

Security Features

    JWT token authentication

    Request rate limiting

    OTP token validation and auto-expiry

    Comprehensive logging

Dependencies

    Django REST Framework

    djangorestframework-simplejwt

    drf-spectacular (for API documentation)

Usage Example
```python

# Phone OTP login
import requests
response = requests.post(
    'https://yourdomain.com/api/loggin/',
    data={'token': 'OTP_TOKEN'}
)

# Username/password login
response = requests.post(
    'https://yourdomain.com/api/loggin/username/',
    data={'username': 'user123', 'password': 'securepassword'}
)
```
TODO

    Implement Email OTP login

    Complete HashFindFactory for hashed field lookups

    Add more comprehensive error handling

    Enhance documentation with Swagger/OpenAPI details



## project setup

1- compelete cookiecutter workflow (recommendation: leave project_slug empty) and go inside the project
```
cd Neutrino
```

2- SetUp venv
```
virtualenv -p python3.10 venv
source venv/bin/activate
```

3- install Dependencies
```
pip install -r requirements_dev.txt
pip install -r requirements.txt
```

4- create your env
```
cp .env.example .env
```

5- Create tables
```
python manage.py migrate
```

6- spin off docker compose
```
docker compose -f docker-compose.dev.yml up -d
```

7- run the project
```
python manage.py runserver
```
