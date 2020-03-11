
def set_normalized_email(instance, *args, **kwargs):
    instance.normalized_email = instance.email.lower()
