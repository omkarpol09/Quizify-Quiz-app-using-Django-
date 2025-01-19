from django.shortcuts import render
from .models import Event, QuizQuestion, QuizResponse
from django.shortcuts import get_object_or_404, redirect
from .forms import UserRegistrationForm, QuizForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request, 'index.html')

def home(request):
    events = Event.objects.all()
    return render(request, 'home.html', {'events':events})

@login_required
def quiz(request, eventId):
    score = 0
    event = get_object_or_404(Event, id=eventId)
    # questions = event.eventQuiz.all()
    questions = QuizQuestion.objects.filter(event_id=eventId)
    correct_answers = {question.id: question.answer for question in questions}


    if request.method == 'POST':
        form = QuizForm(request.POST, questions=questions)
        if form.is_valid():
            # Process the answers
            user_answers = {}
            for question in questions:
                user_answers[question.id] = form.cleaned_data[f'question_{question.id}']
                # print(user_answers[question.id])

                if user_answers[question.id] == correct_answers[question.id]:
                    score += 1

            for question in questions:
                selected_option = form.cleaned_data[f'question_{question.id}']
                QuizResponse.objects.create(
                    user=request.user,  # The logged-in user
                    question=question,
                    selected_option=selected_option,
                    score=score,
                )

            # You can use `user_answers` for further processing
            return render(request, 'result.html', {'user_answers': user_answers, 'score': score})
    else:
        form = QuizForm(questions=questions)
    
    return render(request, 'quiz.html', {'form': form, 'questions': questions, 'event': event})
    # return render(request, 'quiz.html', {'event': event, 'questions': questions})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})


