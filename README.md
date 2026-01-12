# QuizEase

---

## Cuprins

* [Introducere](#introducere)
* [Tehnologii utilizate](#tehnologii-utilizate)
* [Funcționalități](#funcționalități)
* [Instalare și rulare](#instalare-și-rulare)
* [Structura proiectului](#structura-proiectului)
* [Utilizare](#utilizare)

---

## Introducere

QuizEase este o aplicatie adresata atat studentilor cat si profesorilor, care faciliteaza crearea, rezolvarea si notarea automata a quizurilor in cadrul unui curs.

---

## Tehnologii utilizate

* Python 3.13
* Django 5.2.5
* MySQL
* HTML / CSS

---

## Funcționalități

* Autentificare si autorizare utilizatori in baza contului institutional
* Crearea quiz-urilor cu raspuns multiplu si punctaj customizabil
* Vizualizarea de catre profesor a quiz-urilor create, si a studentilor care au completat quiz-ul
* Participarea studentului la quiz folosind un cod unic
* Rezolvarea quiz-ului si calculul automat al notei
* Vizualizarea de catre student a tuturor quiz-urilor finalizate

---

## Instalare și rulare

```bash
# Clonare repository
git clone https://github.com/LucaTarniceriu/proiectWeb.git
cd quizEase

# Migrații
python manage.py migrate

# Pornire server
python manage.py runserver
```

Aplicația va fi disponibilă la `http://127.0.0.1:8000/`.

---

## Structura proiectului

```text
quizEase/
│
├── core/
│   ├── static/
│   ├── templates/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── profesor/
│   ├── templates/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   └── urls.py
|
├── student/
│   ├── templates/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   └── urls.py
|
├── quizEase/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── manage.py
├── db.sqlite3
└── README.md
```

---

## Utilizare

* creare cont in baza email-ului institutional
* autentificare
* accesarea functionalitatilor

## Implementare
  ### Autentificare
