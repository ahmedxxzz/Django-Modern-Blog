from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class Sign_Up_Form(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "email", "is_subscribed")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True
