from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.urls import reverse
from django.views.generic import ListView, UpdateView, CreateView, DeleteView, View
from django.core.paginator import Paginator
from .forms import BoardCreateForm, BoardTextViewForm, BoardModifyForm, BoardDeleteForm, UserSigninForm, BoardUserNameSignInCheckForm, BoardReplyForm
from .models import Webboard, User, Boardreply
from django.db.models import Q
from django.db.models.functions import Length, Upper
from django.http import HttpResponse
import argon2, urllib, os, mimetypes

class BoardView(ListView):
    paginate_by = 10
    template_name = 'boardapp/webboard_list.html'
    queryset = Webboard.objects.order_by('-regDate')
    def get(self, request, *args, **kwargs):
        sessionUser = request.session.get('sessionUser')
        page_obj = Paginator(self.queryset,self.paginate_by)
        page_num = 1
        context = {
            'object_list':page_obj.get_page(page_num).object_list,
            'page_obj': page_obj.get_page(page_num),
            'sessionUser': sessionUser
        }
        return render(request, self.template_name, context)


class BoardTextCreate(CreateView):
    template_name = 'boardapp/boardwrite.html'
    model = Webboard
    form_class = BoardCreateForm
    def form_valid(self, form):
        ''' バリデーションを通った時 '''
        # upload_file(self.request)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        ''' バリデーションを失敗した時 '''
        return super().form_invalid(form)
    
    def get_success_url(self):
        return reverse('main')

def boardTextCreateFn(request):
    template_name = 'boardapp/boardwrite.html'
    sessionUser = request.session.get('sessionUser')
    if sessionUser == None or sessionUser == "":
        return render(request,template_name)
    else:
        context = {
            'sessionUser' : sessionUser
        }
        return render(request,template_name, context)

class BoardTextModify(UpdateView):
    template_name = 'boardapp/board_modify_form.html'
    model = Webboard
    form_class = BoardModifyForm
    
    def form_valid(self, form):
        ''' バリデーションを通った時 '''
        # messages.success(self.request, "修正しました。")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        ''' バリデーションを失敗した時 '''
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('main')


def BoardTextDeleteFn(request, pk):
    #reply削除
    Boardreply.objects.filter(Q(boardId = pk)).delete()
    Webboard.objects.filter(Q(id = pk)).delete()
    return redirect('main')    


def boardTextViewFn(request,pk):
    template_name = 'boardapp/boardRead.html'
    board = Webboard.objects.filter(Q(id = pk)).distinct()
    reply_list = Boardreply.objects.filter(Q(boardId  = pk)).order_by('-regdate')
    sessionUser = request.session.get('sessionUser')
    context = {
        'object':board[0],
        'reply_list': reply_list,
        'sessionUser': sessionUser
    }

    return render(request,template_name,context)

def boardTextSearch(request):
    template_name = 'boardapp/webboard_list.html'
    search_keyword = request.GET.get('search_keyword','')
    page_num = request.GET.get('page', '')
    if page_num == None or page_num == "":
        page_num = 1;
    
    board_list = Webboard.objects.filter(Q(title__icontains = search_keyword)).order_by('-regDate').distinct()
    page_obj = Paginator(board_list,10)

    context = {
        'object_list':page_obj.get_page(page_num).object_list,
        'page_obj': page_obj.get_page(page_num),
        'search_keyword' : search_keyword
    }

    return render(request,template_name,context)


def boardTextModifyFn(request,pk):
    template_name = 'boardapp/board_modify_form.html'
    board = Webboard.objects.filter(Q(id = pk)).distinct()
    context = {
        'object':board[0]
    }

    return render(request,template_name,context)

def signinFn(request):
    template_name = 'boardapp/signin.html'
    return render(request,template_name)

def userSignInFn(request):
    pwhasher = argon2.PasswordHasher()
    template_name = 'boardapp/signin.html'
    if request.method == 'POST':
        
        form = UserSigninForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('userpassword')
            password = pwhasher.hash(raw_password)
            # user = authenticate(username=username, password=password)
            new_user.userpassword = password
            new_user.save()
            
            new_user.userpassword = raw_password
            # login(request, user)
            return afterSignLogin(request, new_user )
        else:
            print('???')
    else:
        form = UserSigninForm()
    return render(request, template_name, {'form': form})

#
def afterSignLogin(request,user):
    template_name = 'boardapp/webboard_list.html'
    username = user.username;
    password = user.userpassword
    ph = argon2.PasswordHasher()
    userfind =  User.objects.filter(Q(username = username)).distinct()
    ph.verify(userfind[0].userpassword, password)
    page_num = 1
    board_list = Webboard.objects.order_by('-regDate')
    page_obj = Paginator(board_list,10)
    request.session['sessionUser'] = userfind[0].username
    context = {
        'object_list':page_obj.get_page(page_num).object_list,
        'page_obj': page_obj.get_page(page_num),
        'sessionUser': request.session['sessionUser']
    }    
    return render(request, template_name, context)

def logininFn(request):
    template_name = 'boardapp/login.html'
    return render(request,template_name)

def userLogInFn(request):
    template_name = 'boardapp/webboard_list.html'
    username = request.POST.get('username','')
    password = request.POST.get('userpassword','')
    userfind =  User.objects.filter(Q(username = username)).distinct()
    if len(userfind) == 0:
        context = {
            'loginError': "ユーザーのネームが存在しません。",
            'username': username,
            'password': password
        }
        return render(request, 'boardapp/login.html',context)
    
    
    ph = argon2.PasswordHasher()

    try:
        ph.verify(userfind[0].userpassword, password)
    except Exception as ex:
        context = {
            'loginError':"passwordが一致しません。",
            'username': username,
            'password': password
        }
        return render(request, 'boardapp/login.html', context)

    page_num = request.POST.get('page', '')
    if page_num == None or page_num == "":
        page_num = 1;
    board_list = Webboard.objects.order_by('-regDate')
    page_obj = Paginator(board_list,10)
    request.session['sessionUser'] = userfind[0].username

    context = {
        'object_list':page_obj.get_page(page_num).object_list,
        'page_obj': page_obj.get_page(page_num),
        'sessionUser': request.session['sessionUser']
    }
    return render(request, template_name, context)

def usernameCheckFn(request, name):
    template_name = 'boardapp/signin.html'

    if request.method == 'POST':
        form = BoardUserNameSignInCheckForm(request.POST)
        count = len(User.objects.filter(Q(username = name)).distinct())
        if count > 0:
            
            message = "このUsernameは既に存在します"
            idCheck = {
                'verification': False,
                'username': name,
                'message': message
            }

            return render(request, template_name, {'idCheck': idCheck})
        
        else:
            message = "登録可能なUsernameです。"
            idCheck = {
                'verification': True,
                'username': name,
                'message': message
            }

            return render(request, template_name, {'idCheck': idCheck})
    else:
        message = "error"
        return render(reqeust, template_name, {'message': message})

def logoutFn(request):
    if request.session.get('sessionUser'):
        request.session['sessionUser'] = ""
    return redirect('main')

def BoardReplyWriteFn(request):
    template_name = 'boardapp/boardRead.html'
    model = Boardreply
    form_class = BoardReplyForm
    if request.method == 'POST':
        form = BoardReplyForm(request.POST)
        objectId = request.POST.get('boardId')
        if form.is_valid():
            form.save()
            reply_list = Boardreply.objects.filter(Q(boardId = objectId)).order_by('-regdate')
            object_list = Webboard.objects.filter(Q(id = objectId)).distinct()
            context = {
                'object':object_list[0],
                'reply_list': reply_list,
                'sessionUser': request.session['sessionUser']
            }

            return render(request,template_name, context )
        else:
            return redirect('main')
    else:
        return redirect('main')



