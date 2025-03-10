from django.shortcuts import render

def home(request):
    """
    Homepage view for the supplychain app
    """
    return render(request, 'supplychain/home.html', {
        'title': 'TropiConnect Homg page'
    })

def register_farmer(request):
    """
    View function for farmer registration (UI only)
    """
    return render(request, 'supplychain/register_farmer.html', {
        'title': 'Farmer Registration'
    })

def register_buyer(request):
    """
    View function for buyer registration (UI only)
    """
    return render(request, 'supplychain/register_buyer.html', {
        'title': 'Buyer Registration'
    })