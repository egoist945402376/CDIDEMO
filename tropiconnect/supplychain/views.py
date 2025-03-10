from django.shortcuts import render

def home(request):
    """
    Homepage view for the supplychain app
    """
    return render(request, 'supplychain/home.html', {
        'title': 'TropiConnect Homg page'
    })