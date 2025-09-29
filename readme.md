# 📚 FastAPI Book Processing API

A simple API for **authentication**, **book storage**, and **pagination**.
This project is built using:

- [FastAPI](https://fastapi.tiangolo.com/) for API framework
- [Pydantic v2](https://docs.pydantic.dev/latest/) for data validation
- [Dependency Injector](https://python-dependency-injector.ets-labs.org/) for dependency injection
- OAuth2 (Password Bearer with scopes `read` & `write`) for authentication

---

## 🚀 Features

- **OAuth2 authentication** with scopes (`read`, `write`)
- **Upload book data** in plain text format
- **Data validation** with detailed error feedback
- **Book pagination** (skip & limit)
- **Interactive API docs** (Swagger UI & ReDoc)

---


📝 Use virtual env:
• python -m venv venv
• source venv/bin/activate   # Mac/Linux
• venv\Scripts\activate      # Windows

📖 API Documentation
•	Swagger UI: http://127.0.0.1:8000/docs
•	ReDoc: http://127.0.0.1:8000/redoc

⚒️  Project Structure
├── main.py                 # FastAPI entry point
├── containers.py           # Dependency Injection container
├── auth.py                 # Authentication service
├── services.py             # Book services
├── serializers.py          # Serializer & parser
├── model.py                # Pydantic models
├── requirements.txt
└── README.md

📌 Notes
	•	Book data is stored in-memory (saved_books). Restarting the server will reset the data.


By Muhammad Taftiyan Ilham Akbar for Accenture Skill Interview Assessment
