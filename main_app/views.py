from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from .models import Timeslot, Profile, Photo
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .forms import NewUserForm, UserForm, ProfileForm
import uuid
import boto3


S3_BASE_URL = 'https://s3.us-east-2.amazonaws.com/'
BUCKET = 'silverwareseatselector'

def assoc_timeslot(request, user_id, timeslot_id):
    profile = Profile.objects.get(user_id=user_id).timeslots.add(timeslot_id)
    print(profile)
    return redirect('userpage')



def profile_update(request, user_id):
    user = User.objects.get(id=user_id)
    print(user.username)
    
    user.first_name = request.POST['first_name']
    user.last_name = request.POST['last_name']

    user.save()
    print(user.first_name)
    return redirect('/user')

def profile_edit(request, user_id):
    profile = Profile.objects.get(user_id=user_id)
    return render(request, 'profile/edit.html', {'profile': profile})

def userpage(request):
    user_form = UserForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)
    timeslots = Timeslot.objects.all()
    print(timeslots)
    return render(request, "profile/user.html", {"user":request.user, "user_form":user_form, "profile_form":profile_form, 'timeslots':timeslots })

def home(request):
    timeslot = Timeslot.objects.all()
    print(timeslot)
    return render(request, 'home.html', {'timeslot':timeslot})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
            #
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("index")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request, "registration/login.html", {"form":form})

def signup(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    form = NewUserForm
    return render (request=request, template_name="register.html", context={"form":form})




# def signup(request):
#     error_message = ''
#     if request.method == 'POST':
#         form = CreateUserForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('index')
#         else:
#             error_message = 'Invalid sign up - try again'
#     form = CreateUserForm()
#     context = {'form': form, 'error_message': error_message}
#     return render(request, 'registration/signup.html', context)



def index(request):


    userList = User.objects.values()
    # displays all usernames including for user currently signed in
    timeslot = Timeslot.objects.values()
    # profile = Profile.objects.get(user_id=5)

    print(userList)
    print(request.user.id)
    # print(profile)
    return render(request, 'index.html', {
      'userList': userList,
      'timeslot': timeslot,
    #   'profile': profile
      })
    

    

    # if not request.user.is_authenticated:
    #     print("authenticated")
    #     return HttpResponse("yes")
    # else:
    #     print("no")
    #     return render(request, 'index.html', {
    #   'userList': userList,
    #   'timeslot': timeslot
    #   })
    


def add_photo(request, profile_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    try:
      s3.upload_fileobj(photo_file, BUCKET, key)
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
      photo = Photo(url=url, profile_id=profile_id)
      photo.save()
    except:
      print('An error occurred uploading file to S3')
    return redirect('detail', profile_id=profile_id)



class ProfileCreate(CreateView):
    model = Profile
    fields = ['name', 'bio', 'role']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProfileUpdate(UpdateView):
    model = Profile
    fields = ['name', 'bio', 'role']


class ProfileDelete(DeleteView):
    model = Profile
    success_url = '/'


def profile_detail(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    return render(request, 'profile/detail.html', {'profile': profile})


class TimeslotDetail(DetailView):
    model = Timeslot
