from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CaseInsensitiveUserCreationForm(UserCreationForm):
    def clean(self):
        cleaned_data = super(CaseInsensitiveUserCreationForm, self).clean()
        username = cleaned_data.get('username')

        if username and User.objects.filter(username__iexact=username).exists():
            self.add_error('username', 'A user with that username already exists.')
        
        return cleaned_data