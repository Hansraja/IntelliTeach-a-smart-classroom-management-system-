from django.shortcuts import render

class HomePage:
    def as_view(request):
        return render(request=request, template_name='index.html', context={'title': 'Home'})