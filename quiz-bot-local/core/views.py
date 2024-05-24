from django.shortcuts import render


def chat(request):
    if not request.session.session_key:
        request.session.create()

    return render(request, 'chat.html')
