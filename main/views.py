from django.shortcuts import render

def show_main(request):
    context = {
        'name': 'Wildan Anshari Hidayat',
        'class': 'PBP B'
    }

    return render(request, "main.html", context)
