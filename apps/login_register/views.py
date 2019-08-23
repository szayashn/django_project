from django.shortcuts import render, redirect
from apps.login_register.models import *
from django.contrib import messages
import bcrypt

def index(request):


    if 'email' in request.session:
        currnet_user = User.objects.get(email = request.session['email'])
        all_messages = Message.objects.all().order_by('-updated_at')
        all_comments = Comment.objects.all().order_by('updated_at')
        context = {
            "currnet_user": currnet_user,
            'all_messages': all_messages,
            'all_comments': all_comments
        }
        return render(request, 'login_register/posts.html',context)

    return render(request, 'login_register/index.html')

def register(request):
    if request.method == 'POST':
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            f_name = request.POST['f_name']
            l_name = request.POST['l_name']
            email = request.POST['email']
            b_day = request.POST['b_day']
            password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())

            User.objects.create(
                first_name = f_name,
                last_name = l_name,
                email = email,
                birthday = b_day,
                password = password
                )
            request.session['email'] = email

    return redirect('/')

def login(request):

    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
            for key, value in errors.items():
                messages.warning(request, value)
            return redirect('/')
    else:
        user = User.objects.get(email = request.POST['login'])
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['email'] = user.email
            return redirect('/')
        else:
            return redirect('/')     
                
    return redirect('/')

def logout(request):

    del request.session['email']

    return redirect('/') 

def post(request):

    if request.method == 'POST':
        message = request.POST['post_text']
        if len(message) > 1:
           user = User.objects.get(email = request.session['email'])
           Message.objects.create(message = message, user = user)
    
    return redirect('/')

def post_comment(request):
    if request.method == 'POST':
        comment_from_form = request.POST['post_comment']
        message_id_from_form = request.POST['post_comment_message_id']
        if len(comment_from_form) > 1:
           user = User.objects.get(email = request.session['email'])
           message = Message.objects.get(id = message_id_from_form)
           Comment.objects.create(comment = comment_from_form, user = user, message = message)
    
    return redirect('/')

def delete_comment(request):
    if request.method == 'POST':
        comment_id = request.POST['comment_id']
        if User.objects.get(email = request.session['email']).comments.filter(id = comment_id).exists():
            Comment.objects.get(id = comment_id).delete()


    return redirect('/')