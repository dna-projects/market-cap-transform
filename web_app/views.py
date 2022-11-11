from django.views.generic import TemplateView
from django.shortcuts import render

class IndexView(TemplateView):
    template_name = "index.html"

    def get(self, request):
        print('🐍 Hello from the Django backend! 🐍')
        return render(request, self.template_name)