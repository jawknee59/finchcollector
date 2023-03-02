from django.shortcuts import render
from .models import Finch

# dummy finches data
# finches = [
#     {'name': 'Tweety', 'color':'yellow', 'age': 2},
#     {'name': 'Toucan', 'color':'blue', 'age': 5},
#     {'name': 'Pecan', 'color':'brown', 'age': 1},
# ]

# Create your views here.
# home route
def home(request):
    return render(request, 'home.html')

# about route
def about(request):
    return render(request, 'about.html')

# index route
def finches_index(request):
    finches = Finch.objects.all()
    return render(request, 'finches/index.html', {'finches': finches })

# detail route for finches
def finches_detail(request, finch_id):
    finch = Finch.objects.get(id=finch_id)
    return render(request, 'finches/detail.html', {'finch': finch })

