def denormalize_email(email, case_method):
    """
    Denormalize the email address by applying a case method to the domain part of it.

    Opposite of django.contrib.auth.base_user.BaseUserManager.normalize_email
    """
    email = email or ""

    try:
        email_name, domain_part = email.strip().rsplit("@", 1)
    except ValueError:
        pass
    else:
        email = email_name + "@" + case_method(domain_part)

    return email
