from django.conf import settings
from django.core.files.storage import FileSystemStorage


PROTECTED_UPLOADS_STORAGE = FileSystemStorage(
    location=settings.PROTECTED_UPLOADS_ROOT)


class ThumbnailStorage(FileSystemStorage):
    """
    Custom thubmnail storage

    Overrides the __init__ because sorl-thumbnail forces the creation
    of a new instance
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, location=settings.PROTECTED_UPLOADS_ROOT, **kwargs)
