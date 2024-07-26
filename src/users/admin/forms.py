from django.contrib.auth import get_user_model
from django.contrib.auth.forms import BaseUserCreationForm
from django.core.exceptions import ValidationError

User = get_user_model()


class UserCreationForm(BaseUserCreationForm):
    def clean_email(self):
        """
        Reject emails that differ only in case.
        """
        email = self.cleaned_data["email"]

        if email and self._meta.model.objects.filter(email__iexact=email).exists():
            self._update_errors(
                ValidationError(
                    {"email": self.instance.unique_error_message(self._meta.model, ["email"])},
                )
            )
        else:
            return email

    class Meta:
        model = User
        fields = ("email", "full_name", "short_name")
