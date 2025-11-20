from django.shortcuts import render, redirect

from landing.models import Item


def index(request):
    return render(request, template_name="index.html")


def post_item(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        description = request.POST.get("description")
        Item.objects.create(name=name, description=description)
        return redirect('index')
    return render(request, 'post.html')
