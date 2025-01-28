# Django Tutorial

## Set Up the Project Directory
```bash
mkdir djangotutorial
cd djangotutorial
django-admin startproject mysite .
```

## Start the Development Server
```bash
python manage.py runserver
```

## Create a Polls App
```bash
python manage.py startapp polls
```

## Create a Superuser
```bash
python manage.py createsuperuser
```

## Register the App in `settings.py`
```python
# mysite/settings.py

INSTALLED_APPS = [
    "polls.apps.PollsConfig",  # Register your app here
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
```

## Define Models
```python
# polls/models.py

from django.db import models
import datetime
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published", auto_now_add=True)

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.question.question_text + " = " + self.choice_text
```

## Run Migrations
```bash
python manage.py makemigrations polls
python manage.py migrate
```

## Run Django Shell
```bash
python manage.py shell
```

### Example Commands in Shell
```python
>>> from polls.models import Choice, Question
>>> from django.utils import timezone

# Create and save a new question
>>> q = Question(question_text="What's new?", pub_date=timezone.now())
>>> q.save()

# Access the saved question
>>> Question.objects.all()
<QuerySet [<Question: What's new?>]>
```

## Admin Configuration
```python
# polls/admin.py

from django.contrib import admin
from .models import Question

admin.site.register(Question)
```

## Define Views
```python
# polls/views.py

from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from .models import Question

# Index View
def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    template = loader.get_template("polls/index.html")
    context = {
        "latest_question_list": latest_question_list,
    }
    return HttpResponse(template.render(context, request))

# Detail View
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})

# Results View
def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

# Vote View
def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
```

## Define URLs
```python
# polls/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:question_id>/", views.detail, name="detail"),
    path("<int:question_id>/results/", views.results, name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
]
```

## Templates

### `polls/templates/polls/index.html`
```html
{% if latest_question_list %}
    <ul>
    {% for question in latest_question_list %}
        <li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
    {% endfor %}
    </ul>
{% else %}
    <p>No polls are available.</p>
{% endif %}
```

### `polls/templates/polls/detail.html`
```html
<h1>{{ question.question_text }}</h1>
<ul>
{% for choice in question.choice_set.all %}
    <li>{{ choice.choice_text }}</li>
{% endfor %}
</ul>
```

## Using Forms
```python
# polls/forms.py

from django import forms
from .models import Question, Choice

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']
