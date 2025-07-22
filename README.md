# Neutrino

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
