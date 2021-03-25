from django import forms
from django.forms import ModelForm, ValidationError
from django.contrib.auth.forms import UserCreationForm
from .models import Webboard, User, Boardreply

class BoardCreateForm(ModelForm):

    def __init__(self, *args, **kwd):
        super(BoardCreateForm, self).__init__(*args, **kwd)
    class Meta:
        model = Webboard
        fields = ('writer','title','content')

class BoardTextViewForm(ModelForm):

    def __init__(self, *args, **kwd):
        super(BoardTextViewForm, self).__init__(*args, **kwd)
    
    class Meta:
        model = Webboard
        fields = ('writer','title','content',)
    
class BoardModifyForm(ModelForm):
    def __init__(self, *args, **kwd):
        super(BoardModifyForm, self).__init__(*args, **kwd)
    
    class Meta:
        model = Webboard
        fields = ('title','content',)

class BoardDeleteForm(ModelForm):
    def __init__(self, *args, **kwd):
        super(BoardDeleteForm, self).__init__(*args, **kwd)
    
    class Meta:
        model = Webboard
        fields = ('title','content','writer',)

class UserSigninForm(ModelForm):
    def __init__(self, *args, **kwd):
        super(UserSigninForm, self).__init__(*args, **kwd)
    
    class Meta:
        model = User
        fields = ('username','userpassword','usermail',)

class BoardUserNameSignInCheckForm(ModelForm):
    def __init__(self, *args, **kwd):
        super(BoardUserNameSignInCheckForm, self).__init__(*args, **kwd)
    
    class Meta:
        model = User
        fields = ('username',)

class BoardReplyForm(ModelForm):
    def __init__(self, *args, **kwd):
        super(BoardReplyForm, self).__init__(*args, **kwd)
    
    class Meta:
        model = Boardreply
        fields = ('replywriter','boardId','replycontent',)

