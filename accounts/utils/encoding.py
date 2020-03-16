from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


def uidb64_encode(string):
    return urlsafe_base64_encode(force_bytes(string))


def uidb64_decode(string):
    return urlsafe_base64_decode(string).decode()
