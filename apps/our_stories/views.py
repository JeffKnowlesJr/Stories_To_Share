from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
from random import randint
import bcrypt

# INDEX PAGE
def index(request):
    print("\n<<--------------Rendering home page-------------->>\n")

    try:
        print("User id:", request.session['id'],"\n")
    except KeyError:
        print('no session id\n')
    return render(request, 'our_stories/index.html')

# CREATE NEW USER
def create(request):
    print("\n<<--------------Executing new user process-------------->>\n")

    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        print("ERRORS IN FORM: ", errors)
        return redirect('/login')
    else:
        pass_hash = bcrypt.hashpw(request.POST['password'].encode('utf-8'), bcrypt.gensalt())
        user = User.objects.create(username = request.POST['username'], email = request.POST['email'], password = pass_hash.decode('utf-8'))
        print("NEW USER CREATED: ", user)
        request.session['id'] = user.id
        request.session['username'] = user.username
        return redirect(f'/profile/{user.id}')

def profile(request, id):
    print("\n<<--------------Rendering Profile-------------->>\n")

    this_user = User.objects.get(id=id)

    context = {
        "this_user":this_user
    }
    return render(request, 'our_stories/profile.html',context)

def login(request):
    print("\n<<--------------Rendering Login-------------->>\n")

    return render(request, 'our_stories/login.html')

# LOGOUT PROCESS
def logout(request):
    print("\n<<--------------Logged Out-------------->>\n")

    request.session.clear()
    return redirect('/')

# LOGIN PROCESS
def process_login(request):
    print("\n<<--------------Executing login process-------------->>\n")

    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        print(errors)
        return redirect('/login')
    else:
        user = User.objects.get(username=request.POST['username'])
        if bcrypt.checkpw(request.POST['password'].encode('utf-8'), user.password.encode('utf-8')):
            request.session['id'] = user.id
            request.session['username'] = user.username
            return redirect(f'/profile/{user.id}')
        else:
            messages.error(request, 'Incorrect password.')
            pr('error bad login')
            return redirect('/login')

def write_story(request, id):
    print("\n<<--------------Executing write process-------------->>\n")

    return HttpResponse("Page under conflagration")

def write(request):
    print("\n<<--------------Rendering write page-------------->>\n")
    
    return render(request, 'our_stories/write_picker.html')


def write_process(request):
    print("\n<<--------------Executing write process-------------->>\n")

    #Create a genre object
    this_genre = Genre.objects.get(genre = request.POST['genre'])
    print("The genre chosen is: ", this_genre.genre)

    #Create a user object
    this_user = User.objects.get(id = request.session['id'])
    print("This user is: ", this_user.username)

    #Create a story object
    this_story = Story.objects.create(group=request.POST['group'], story_length = request.POST['story_length'])

    this_story.genres.add(this_genre)
    this_story.users.add(this_user)

    print("CREATED NEW STORY: ", this_story)

    #Generate a random trope
    all_tropes = this_genre.tropes.all()

    #---->Append all tropes from genre to array
    trope_arr = []
    for i in all_tropes:
        trope_arr.append(i.id)
        print("Trope array: ", trope_arr)

    #---->Get range of the array
    trope_range = len(trope_arr)
    print("Trope range: ", trope_range)

    #---->Generate random trope from arr length
    random_trope = randint(0,trope_range-1)
    print("Random trope: ", random_trope)

    #---->Set this_trope equal to rand point in arr
    this_trope = this_genre.tropes.get(id = trope_arr[random_trope]).trope

    print("Printing this trope: ", this_trope)

    #Store random trope in session
    request.session['trope'] = this_trope

    return render(request, 'our_stories/write_zone.html')

def sentence_process(request):
    response="Sentence processed"
    print("Printing sentence to be processed: ", request.POST['sentence'])

    request.session['sentence'] = request.POST['sentence']

    return render(request, 'our_stories/write_zone.html')

def explore(request):

    all_stories = Story.objects.all()

    context = {
        "all_stories":all_stories
    }

    return render(request,"our_stories/explore.html", context)
