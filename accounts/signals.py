
def set_normalized_email(instance, *args, **kwargs):  # pylint: disable=unused-argument
    instance.normalized_email = instance.email.lower()
