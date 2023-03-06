from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from .models import Finch, Toy
from .forms import FeedingForm

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

    # first we'll get a list of ids of toys the finch owns
    id_list = finch.toys.all().values_list('id')
    # then we'll make a list of the toys the finch does not have
    toys_finch_doesnt_have = Toy.objects.exclude(id__in=id_list)

    feeding_form = FeedingForm()
    return render(request, 'finches/detail.html', {'finch': finch, 'feeding_form': feeding_form, 'toys': toys_finch_doesnt_have })

class FinchCreate(CreateView):
    model = Finch
    # the fields attribute is required for a createview.
    fields = '__all__'

class FinchUpdate(UpdateView):
    model = Finch
    fields = ['color', 'age']

class FinchDelete(DeleteView):
    model = Finch
    success_url = '/finches/'

# add this new function below finches_detail
def add_feeding(request, finch_id):
  # create a ModelForm instance using the data in request.POST
  form = FeedingForm(request.POST)
  # we need to validate the form, that means "does it match our data?"
  if form.is_valid():
    # don't save the form to the db until it
    # has the finch_id assigned
    new_feeding = form.save(commit=False)
    new_feeding.finch_id = finch_id
    new_feeding.save()
  return redirect('detail', finch_id=finch_id)

def assoc_toy(requet, finch_id, toy_id):
    Finch.objects.get(id=finch_id).toys.add(toy_id)
    return redirect('detail', finch_id=finch_id)

def unassoc_toy(requet, finch_id, toy_id):
    Finch.objects.get(id=finch_id).toys.remove(toy_id)
    return redirect('detail', finch_id=finch_id)

# ToyList
class ToyList(ListView):
    model = Toy
    template_name = 'toys/index.html'

# ToyDetail
class ToyDetail(DetailView):
    model = Toy
    template_name = 'toys/detail.html'

# ToyCreate
class ToyCreate(CreateView):
    model = Toy
    fields = ['name', 'color']

    # define what the inheritance method is_valid does(we'll update this later)
    def form_valid(self, form):
        # we'll use this later, but implement right now
        # we'll need this when we add auth
        # super allows for the original inherited CreateView function to work as it was intended
        return super().form_valid(form)

# ToyUpdate
class ToyUpdate(UpdateView):
    model = Toy
    fields = ['name', 'color']

# ToyDelete
class ToyDelete(DeleteView):
    model = Toy
    success_url = '/toys'

