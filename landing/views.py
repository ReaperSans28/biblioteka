from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from landing.forms import ItemsForm
from landing.models import Item


class HomeView(TemplateView):
    template_name = "landing/index.html"

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}", status=500)


class ItemsCreateView(CreateView):
    model = Item
    form_class = ItemsForm
    success_url = reverse_lazy("landing:home")
