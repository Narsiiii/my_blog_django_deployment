from django.shortcuts import render, redirect
from django.http import HttpResponse
from.models import Room, Topic, Message
from .forms import RoomForm,TopicForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.forms import UserCreationForm

def register_user(request):
    form = UserCreationForm()
    if request.method =="POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
        
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request,"Registration Successfull..")
            return redirect('home')
        else:
            form = UserCreationForm()
            messages.error(request,"Registration Failed..")

    context={'form':form}
    return render(request, 'blog/register.html', context)


def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username =  request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect('home')
        else:
            messages.error(request, "Login failed. Please check your credentials.")
            return redirect('login')
    return render(request, 'blog/login.html')

def logout_user(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def home(request):
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(request, 'blog/home.html', context)

def room(request,pk):
    room = Room.objects.get(id=pk)
    comments = room.message_set.all().order_by('-created')
    
    if request.method == "POST":
        comments= Message.objects.create(
            user =request.user,
            room = room,
            body = request.POST.get('body')
        )
        return redirect('room', pk = room.id)
    context={'room':room, 'comments':comments}
    return render(request,'blog/rooms.html', context)



def room_id(request):
    rooms=Room.objects.all()
    context={'rooms':rooms}
    return render(request,'blog/rooms.html', context)

def CreateTopic(request):
    if request.method =="POST":
        topic = TopicForm(request.POST)
        if topic.is_valid():
            topic.save()
            return redirect('home')
        else:
            return redirect('create-topic')
    else:
        topic =TopicForm()
    context={'topic': topic}
    return render(request, 'blog/topic_form.html', context)

def createRoom(request):
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
                # Redirect to a success page or do something else upon successful form submission
                # Example: return redirect('success-url')
        else:
                # If form is not valid, you may render the form again with errors
            context = {'form': form}
            return render(request, 'blog/room_form.html', context)
    else:
            # If request method is not POST, just render the empty form
        form = RoomForm()
        
    context = {'form': form}
    return render(request, 'blog/room_form.html', context)

def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance= room)

    if request.user != room.host:
        return HttpResponse("You are not allowed here!")
    
    if request.method =="POST":
        form = RoomForm(request.POST, instance= room)
        if form.is_valid():
            form.save()
            messages.success(request,"Updated successfully..")
            return redirect ('home')
        
    context ={'form': form}
    return render(request, 'blog/edit.html', context)
    

def deleteRoom(request,pk):
    room = Room.objects.get(id = pk)

    if request.user != room.host:
        return HttpResponse("You are not allowed here!")
    
    if request.method == 'POST':
        room.delete()
        return redirect ('home')
    return render (request, 'blog/delete.html', {'obj': room})

