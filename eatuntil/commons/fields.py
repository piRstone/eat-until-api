from django.urls import reverse

from rest_framework import serializers
from rest_framework.fields import get_attribute
from sorl.thumbnail import get_thumbnail


class HyperlinkedSorlImageField(serializers.ImageField):
    """
    DRF serializer field that returns an hyperlink for scaled and cached images
    """

    def __init__(self, size, options=None, *args, **kwargs):
        """
        Store sorl thumbnail size and options
        """
        self.size = size
        self.options = options or {}

        super().__init__(*args, **kwargs)

    def to_representation(self, value):
        """
        Render a thumbnail link
        """
        # Return thumbnail only if the image exists
        if value:
            image = get_thumbnail(value, self.size, **self.options)

            # If the request is given in the context, build
            # and absolute image uri
            if 'request' in self.context:
                return self.context['request'].build_absolute_uri(image.url)

            # Otherwise, return relative image uri
            return super().to_representation(image.url)

        # Fallback to original representation
        return super().to_representation(value)


class ProtectedFileURLField(serializers.URLField):

    def __init__(self, viewname, *args, **kwargs):
        """
        Store field specific args and make field read only
        """
        self.viewname = viewname
        kwargs['read_only'] = True

        super().__init__(*args, **kwargs)

    def get_attribute(self, obj):
        """
        Return initial object
        """
        return obj

    def build_uri(self, obj, absolute=True):
        """
        Build and return an absolute URI using the viewname

        If the request if provided in the context and absolute is True,
        it returns an absolute URI
        """
        # Build URI
        uri = reverse(self.viewname, args=[obj.pk])

        if absolute and 'request' in self.context:
            uri = self.context['request'].build_absolute_uri(uri)

        return uri

    def to_representation(self, obj):
        """
        Return the URI or None
        """
        # Retrieve the value from the object
        value = get_attribute(obj, self.source_attrs)

        if value:
            # Build and return the URI
            return super().to_representation(self.build_uri(obj))

        return None
