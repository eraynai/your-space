
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import Timeslot, Profile, Photo
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic.edit import DeleteView
# from django.views.generic import DetailView // future dev
from .forms import NewUserForm, UserForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
import boto3


S3_BASE_URL = 'https://s3.us-east-2.amazonaws.com/'
BUCKET = 'silverwareseatselector'


@login_required
def assoc_timeslot(request,timeslot_id , user_id):
    p = Profile.objects.filter(timeslots__id = timeslot_id).count()
    if p > 0:
        messages.error(request,"We're sorry, that timeslot just got booked.")
        return redirect(f'/user/{user_id}/timeslot')
    else:
        Profile.objects.get(user_id=user_id).timeslots.add(timeslot_id)
        return redirect(f'/user/{user_id}/timeslot')


@login_required
def unassoc_timeslot(request, user_id, timeslot_id):
    Profile.objects.get(id=user_id).timeslots.remove(timeslot_id)
    return redirect(f'/user/{user_id}/timeslot')




@login_required
def profile_update(request, user_id):
    user = User.objects.get(id=user_id)
    profile = Profile.objects.get(user_id=user_id)

    user.first_name = request.POST['first_name']
    user.last_name = request.POST['last_name']
    user.email= request.POST['email']
    profile.role = request.POST['role']
    profile.bio = request.POST['bio']
    profile.linkedin = request.POST['linkedin']

    user.save()
    profile.save()
    return redirect(f'/user/{user.id}')


@login_required
def profile_edit(request, user_id):
    profile = Profile.objects.get(user_id=user_id)
    return render(request, 'profile/edit.html', {'profile': profile})


@login_required
def userpage(request, user_id):
    user_form = UserForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)
    profile = Profile.objects.get(user_id=user_id)
    available_timeslots = Timeslot.objects.filter(profile=None).order_by('id')

    return render(request, "profile/user.html", {"user": request.user, "user_form": user_form, "profile_form": profile_form, 'timeslot': available_timeslots, 'profile': profile})


@login_required
def index(request):

    userList = User.objects.values()
    # displays all usernames including for user currently signed in
    timeslot = Timeslot.objects.all()
    profile = Profile.objects.get(user_id=request.user.id)
    profile_timeslot = profile.timeslots.all()

    return render(request, 'index.html', {
        'userList': userList,
        'timeslot': timeslot,
        'profile_timeslot': profile_timeslot,
        'profile': profile
    })


def home(request):
    timeslot = Timeslot.objects.all()
    return render(request, 'home.html', {'timeslot': timeslot})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(
                    request, f"You are now logged in as {username}.")
                return redirect("index")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})


def signup(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    form = NewUserForm

    return render(request=request, template_name="register.html", context={"form": form})


@login_required
def add_photo(request, user_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
  try:
      s3.upload_fileobj(photo_file, BUCKET, key)
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
      photo = Photo(url=url, user_id=user_id)
      photo.save()
  except:
      messages.error(request,'An error occurred uploading your')
  return redirect('userpage', user_id=user_id)

@login_required
def photo_delete(request,user_id):
    photo = Photo.objects.get(user_id=user_id)
    photo.delete()
    return redirect('userpage', user_id=user_id)



@login_required
def profile_detail(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    return render(request, 'profile/detail.html', {'profile': profile})


# future dev
# class TimeslotDetail(LoginRequiredMixin, DetailView):
#     model = Timeslot



@login_required
def timeslot_index(request, user_id):
    user_form = UserForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)
    profile = Profile.objects.get(user_id=user_id)
    available_timeslots = Timeslot.objects.filter(profile=None).order_by('id')
    return render(request, 'profile/timeslot_list.html', {
        "user": request.user,
        "user_form": user_form,
        "profile_form": profile_form,
        'timeslot': available_timeslots,
        'profile': profile})
