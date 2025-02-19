from django import template

register = template.Library()

@register.filter
def username_from_email(email):
    """Extracts the username part before '@' from an email."""
    return email.split('@')[0] if email else ''
