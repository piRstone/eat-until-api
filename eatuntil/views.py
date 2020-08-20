from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'home.html'


class CGUView(TemplateView):
    template_name = 'cgu.html'
