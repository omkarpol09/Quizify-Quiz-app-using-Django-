from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class QuizForm(forms.Form):
    def __init__(self, *args, **kwargs):
        # Expecting questions to be passed in as a keyword argument
        questions = kwargs.pop('questions', None)
        super().__init__(*args, **kwargs)
        
        if questions:
            for question in questions:
                self.fields[f'question_{question.id}'] = forms.ChoiceField(
                    label=question.question,
                    choices=[
                        ('A', question.optionA),
                        ('B', question.optionB),
                        ('C', question.optionC),
                        ('D', question.optionD),
                    ],
                    widget=forms.RadioSelect,
                    required=True,
                )