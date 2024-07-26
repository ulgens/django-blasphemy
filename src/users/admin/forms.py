from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm
from django.contrib.auth.forms import UserCreationForm as AbstractUserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

User = get_user_model()


class UserCreationForm(AbstractUserCreationForm):
    error_messages = {  # noqa: RUF012
        **AbstractUserCreationForm.error_messages,
        "duplicate_email": _("A user with that email already exists."),
    }

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


class UserChangeForm(BaseUserChangeForm):
    """
    Removes Meta.field_classes["username"] from base class
    """

    class Meta:
        model = User
        fields = "__all__"
