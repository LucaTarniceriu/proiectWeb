# QuizEase

---

## Cuprins

* Introducere
* Tehnologii utilizate
* Funcționalități
* Instalare și rulare
* Structura proiectului
* Utilizare
* Arhitectura bazei de date
* Arhitectura aplicatiei
* Implementare
    - Autentificare
    - Crearea quiz-urilor si adaugarea intrebarilor
    - Participarea studentului la un quiz
    - Vizualizarea quiz-urilor si a participantilor
    - Tratarea erorilor

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

## Functionalitati

* Autentificare si autorizare utilizatori in baza contului institutional
* Crearea quiz-urilor cu raspuns multiplu si punctaj customizabil
* Vizualizarea de catre profesor a quiz-urilor create, si a studentilor care au completat quiz-ul
* Participarea studentului la quiz folosind un cod unic
* Rezolvarea quiz-ului si calculul automat al notei
* Vizualizarea de catre student a tuturor quiz-urilor finalizate

---

## Instalare si rulare

```bash
# Clonare repository
git clone https://github.com/LucaTarniceriu/proiectWeb.git
cd quizEase

# Migrații
python manage.py migrate

# Pornire server
python manage.py runserver
```

Aplicatia va fi disponibila la `http://127.0.0.1:8000/`.

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

## Arhitectura bazei de date
![UML class](https://github.com/user-attachments/assets/47fffb82-2ac3-411c-957d-0141fad6f145)

## Arhitectura aplicatiei
![Use case diagram](https://github.com/user-attachments/assets/af7d651c-bf4a-4aad-bbea-f77874c3ef38)


## Implementare
  ### Autentificare
  Utilizatorii pot crea un cont in aplicatie folosind adresa institutionala 'e-uvt.ro'. Permisiunile vor fi atribuite contului in functie de tipul adresei
  Tipul adresei este determinat folosind o expersie regulata care analizeaza componenta adresei.
    
  ```python
  # Adresa de tip student
  if re.search("[a-z]+\.[a-z]+[0-9]{2}@e-uvt\.ro", email);
    User.objects.create_user(username=email, email=email, password=password, isProfesor = False):
  # Adresa de tip profesor
  elif re.search("[a-z]+\.[a-z]+@e-uvt\.ro", email):
    User.objects.create_user(username=email, email=email, password=password, isProfesor = True):
```
  Autentificare este gestionata folosind sistemul integrat in Django, astfel este asigurata protectia datelor sensibile si gestionarea corecta a sesiunilor.

  ### Crearea quiz-urilor si adaugarea intrebarilor
  Informatiile referitoare la quiz-ul adaugat sunt preluate de la utilizator prin intermediul unui formular, si inregistrate in baza de date.
  La crearea unui quiz, se creaza automat o intrebare initiala fara date, care marcheaza inceputul quizului si care devine activa in momentul inceperii quiz-ului, atunci cand studentul se afla pe pagina de titlu al quiz-ului respectiv.

  Fiecare intrebare adaugata este un obiect "Question" nou in baza de date, care contine o referinta catre quiz-ul din care face parte.
  La selectarea optiuni "finalizare quiz", este calculat numarul total de intrebari, si salvat in obiectul quiz-ului din baza de date.

  Paginile pentru crearea quiz-urilor si adaugarea intrebarilor sunt incarcate doar daca utilizatorul conectat are permisiuni de profesor marcate prin atributul "isProfesor" in obiectul "User". 
  Aceasta verificare se face inainte de incarcarea efectiva a paginii si a datelor. In cazul in care utilizatorul nu are permisiunile necesare, acesta este redirectionat catre o pagina de eroare.
  ```python
  def createQuiz(request):
    if request.user.is_authenticated and request.user.isProfesor:
    else:
      return redirect('error', error_id='permission_err')

  def addQuestion(request, questionNumber):
    if request.user.is_authenticated and request.user.isProfesor:
    else:
      return redirect('error', error_id='permission_err')
  ```

  ### Participarea studentului la un quiz
  La crearea unui quiz de catre profesor, va fi afisat un id al quiz-ului. Acest id va fi transmis studentilor pentru a putea participa la quiz.
  Id-ul este introdus in campul paginii "Join quiz", iar astfel informatiile despre quiz sunt extrase din baza de date, conform id-ului introdus.
  Formularul de pe pagina "Join quiz" trimite id-ul pagini "Active quiz" care se ocupa de afisarea datelor quizu-lui si de afisarea intrebarilor.
  In momentul accesari quiz-ului, quiz-ul este marcat ca activ in contul studentului. Astfel, daca studentul paraseste quiz-ul nefinalizat, iar apoi il acceseaza din nou, nu va fi considerata ca o rezolvare noua. De asemenea, intrebarea initiala creata odata cu quiz-ul, va fi marcata ca activa.
  ```python
  request.user.activeQuiz = formId
  request.user.activeQuestion = Question.objects.get(quiz=quiz, questionNumber=0).id
  ```
  Pe masura ce studentul avanseaza prin intrebari, id-ul intrebarii corespunzatoare va fi marcat ca activa.
  ```python
   request.user.activeQuestion = Question.objects.get(quiz=Quiz.objects.get(id=request.user.activeQuiz), questionNumber=int(currentQuestion.questionNumber) + 1).id
  ```
  Dupa submiterea fiecarei intrebari, este verificata corectitudinea acesteia, si salvat punctajul obtinut.
  ```python
  for answer in request.POST.getlist("answers"):
    studentAnswers += (answer + ";")
    correctAnswers = Question.objects.get(id=request.user.activeQuestion).correctAnswer
    score = 0
    if correctAnswers == studentAnswers:
      score = Question.objects.get(id=request.user.activeQuestion).points
      
  Submits.objects.update_or_create(student=request.user.email, question_id=Question.objects.get(id=request.user.activeQuestion).id, answers=studentAnswers, quiz_id=quiz.id, points=score)
  ```
  In functie de optiunile selectate de profesor la crearea quiz-ului, poate fi disponibil un buton de intoarcere la intrebarea anterioara.
  ```python
  if allowReturn == "allow_return":
    context["allowReturn"] = True
  else:
    context["allowReturn"] = False
  ```
  Dupa trimiterea tuturor intrebarilor, va fi calculat punctajul obtinut de student. Acesta nu va fi afisat la final-ul quiz-ului decat daca profesorul a selectat acest lucru la crearea quiz-ului.

  ```python
  if quiz.showGrade:
      context["grade"] = 0
      submissions = Submits.objects.filter(student=request.user.username, quiz_id=quiz.id)
      for entry in submissions:
          context["grade"] += entry.points
  else:
      context["grade"] = "not_allowed"
  return render(request, 'finish.html', context)
```
La trimiterea raspunsurilor, id-ul quiz-ului va fi salvat intr-un string in obiectul din baza de date al User-ului, astfel incat quiz-ul sa nu mai poata fi accesat odata ce a fost trimis.
```python
request.user.finishedQuizzes += (str(quiz.id) + ";")
```
### Vizualizarea quiz-urilor si a participantilor
Un profesor are posibilitatea de a vizualiza toate quiz-urile pe care le-a creat, toti studentii care au incarcat un raspuns pentru un anume quiz, alaturi de nota pe care au luat-o, cat si sa stearga un anume quiz.
Toate acestea sunt accesibile prin meniul "View quizzes". Tot in acest meniu sunt afisate id-urile quiz-urilor pentru a putea fi transmise studentilor.

```python
# vizualizare quiz-uri
context['quizDatabase'] = Quiz.objects.filter(createdBy=request.user)

# selectarea tuturor studentilor care au trimis quiz-ul cu id-ul selectat
students = User.objects.filter(isProfesor=False)
for student in students:
    if quiz_id in student.finishedQuizzes.split(';'):
        name = student.username.split("@")[0].split(".")
```
### Tratarea erorilor
Atunci cand sunt intampinate erori precum: utilizatorul nu are permisiuni necesare pentru efectuarea unei actiuni, utilizatorul nu este logat in cont etc, utilizatorul este redirectionat catre o pagina de eroare cu un cod corespunzator problemei intampinate.
Cauza erorii este afisata pe ecran si se ofera optiunea intoarcerii la pagina principala sau accesarea pagini le "Login" dupa caz.
```python
if error_id == "permission_err":
    context['errorMessage'] = "You are not logged in with the right permissions to access this page"
elif error_id == "no_login":
    context['errorMessage'] = "You are not logged in"
elif error_id == "quiz_submission_err":
    context['errorMessage'] = "Quiz submission failed"
elif error_id == "no_active_quiz":
    context['errorMessage'] = "No active quiz"
elif error_id == "already_responded":
    context['errorMessage'] = "Quiz was already sent"
else:
    context['errorMessage'] = "Error: something went wrong"
```


















  
