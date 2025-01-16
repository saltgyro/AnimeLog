from django import forms
from .models import Users
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class RegistForm(forms.ModelForm):
    
    class Meta:
        model = Users
        fields = ['nickname', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
            # 'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nickname': 'ニックネーム',
            'email': 'メールアドレス',
            'password': 'パスワード',
        }
    
    def save(self,commit=False):
        user = super().save(commit=False)
        # パスワードの検証
        validate_password(self.cleaned_data['password'], user)
        # パスワードのハッシュ化
        user.set_password(self.cleaned_data['password'])
        # ユーザーの保存
        user.save()
        return user
    

class UserForm(forms.ModelForm):
    
    class Meta:
        model = Users
        fields = {'nickname','email','password'}
        widgets = {
            'password':forms.PasswordInput
        }
        
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Users  
        fields = ['nickname', 'email', 'password1', 'password2']  

        widgets = {
            'nickname': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nickname': 'ニックネーム',
            'email': 'メールアドレス',
            'password1': 'パスワード',
            'password2': '確認用パスワード'
        }
        def clean_password1(self):
            password = self.cleaned_data.get('password1')
            print(f"Password1 validation: {password}")  # デバッグ用
            if len(password) < 8:
                raise ValidationError('パスワードは最低8文字以上でなければなりません。')
            if password.isdigit():
                raise ValidationError('数字だけのパスワードは使用できません。')
            return password

        def clean_password2(self):
            password1 = self.cleaned_data.get('password1')
            password2 = self.cleaned_data.get('password2')
            print(f"Password2 validation: {password1}, {password2}")  # デバッグ用
            if password1 != password2:
                raise ValidationError('パスワードが一致しません。')
            return password2

class UserLoginForm(forms.Form):#ログインの際に使用するフォーム
    email = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード',widget=forms.PasswordInput())
    remember = forms.BooleanField(
    label='ログインしたままにする',
    required=False,
    widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'display: inline-block; margin-right: 5px;'})
)

class UserEditForm(forms.ModelForm):#更新処理するフォーム
    
    current_password = forms.CharField(
        label="現在のパスワード",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )
    new_password = forms.CharField(
        label="新しいパスワード",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        validators=[validate_password]
    )
    new_password_confirm = forms.CharField(
        label="新しいパスワード（確認用）",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )
    
    class Meta:
        model = Users
        fields =['nickname', 'email']  # 変更可能なフィールドを指定
        labels = {
            'nickname': 'ニックネーム',
            'email': 'メールアドレス',
        }
        widgets = {
            'nickname': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        required = {
            'nickname':False,
            'email': False,
        }
        
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)# `user` キーワード引数を取り除いてインスタンスに保存
        super().__init__(*args, **kwargs)
    
    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        # パスワードが入力されていない場合は検証をスキップ
        if not current_password:
            return current_password
        # 入力されている場合のみ検証を実施
        if not self.user.check_password(current_password):
            raise forms.ValidationError("現在のパスワードが正しくありません。")
        return current_password
    
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        new_password_confirm = cleaned_data.get('new_password_confirm')

        if new_password or new_password_confirm:
            if new_password != new_password_confirm:
                raise forms.ValidationError("新しいパスワードが一致しません。")
        return cleaned_data
    
    def save(self, commit=True):
        if self.cleaned_data.get('new_password'):
            self.user.set_password(self.cleaned_data['new_password'])
        if commit:
            self.user.save()
        return self.user