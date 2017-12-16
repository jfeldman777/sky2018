from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import SignUpForm
from .models import NewsRecord, MagicNode
from django.contrib.auth.models import User

from collections import Counter
from operator import itemgetter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import NameForm
# Create your views here.
def topic_tree(request,id):
    get = lambda node_id: MagicNode.objects.get(pk=node_id)
    children = []
    siblings = []
    try:
        try:
            node = get(id)
        except:
            node = MagicNode.get_first_root_node()

        if node.is_root():
            node = node.get_first_child()

        children = node.get_children()
        parent = node.get_parent()
        siblings = node.get_siblings()
    except:
        pass
    return render(request,'topic_tree.html',
                    {'node':node,
                     'children':children,
                     'parent':parent,
                     'siblings':siblings,
                     })

def topic_search(request):
    result = None
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            name = form.cleaned_data['name']
            result = MagicNode.objects.filter(desc__icontains=name)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'topic_search.html',
        {'form': form,
         'result': result,
        })

def msg(request,msg):
    return render(request, 'msg.html', {'msg': msg})

def password_change_done(request):
    return msg(request, 'Your password was changed successfully!')

def password_reset_done(request):
    return msg(request, 'Your password was changed successfully!')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                User.objects.get(email = email)
                return msg(request,'This email is in DB, probably you have been registered')
            except:
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def index(request):
    try:
        news = NewsRecord.objects.all()[:1].get()
    except:
        news = None
    return render(request,'index.html',
        {'news':news
        })

def news(request):
    x_list = NewsRecord.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(x_list, 10)
    try:
        qs = paginator.page(page)
    except PageNotAnInteger:
        qs = paginator.page(1)
    except EmptyPage:
        qs = paginator.page(paginator.num_pages)

    return render(request,'news.html',
            {'qs':qs,
            })
