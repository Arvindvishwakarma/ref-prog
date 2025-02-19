from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import View
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .utils import TokenGenerator, generate_token
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import PasswordResetTokenGenerator

# Create your views here.
def signup(request):
    if request.method=="POST":
        email=request.POST['email']
        password=request.POST['pass1']
        confirm_password=request.POST['pass2']
        if password != confirm_password:
            messages.warning(request, "Password is Not Matching")
            #return HttpResponse("password incorrect")
            return render(request, 'authentication/signup.html')
        
        try:
            if User.objects.get(username=email):
                #return HttpResponse("email already exist")
                messages.info(request, "Email is already taken!")
                return render(request, 'authentication/signup.html')
        except Exception as identifier:
            pass
        user = User.objects.create_user(email, email, password)
        user.is_active=False
        user.save()
        email_subject="Activate Your Account"
        message=render_to_string('authentication/activate.html', {
        'user':user,
        'domain':'127.0.0.1:8000',
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':generate_token.make_token(user)
        })
        email_message = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, 
                                     [email])
        email_message.send()
        messages.success(request, "Account Activation link has been sent to your email, Please Verify.")
        return redirect('/auth/login/')

    return render(request, "authentication/signup.html")

class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as identifier:
            user = None
        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.info(request, "Account Activated Successfully")
            return redirect('/auth/login/')
        return render(request, 'authentication/activatefail.html')


def handlelogin(request):
    if request.method == 'POST':
  
        username = request.POST['email']
        userpassword = request.POST['pass1']
        myuser = authenticate(username = username, password = userpassword)
        
        if myuser is not None:
            login(request, myuser)
            # messages.success(request, f' welcome {username} !!')
            return render(request, 'index.html')
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('/auth/login')


    return render(request, "authentication/login.html")

def handlelogout(request):
    logout(request)
    messages.info(request, "Logout Success")
    return redirect('/auth/login')


class RequestResetEmailView(View):
    def get(self, request):
        return render(request, 'authentication/request-reset-email.html')
    
    def post(self, request):
        email=request.POST['email']
        user=User.objects.filter(email=email)
        if user.exists():
            #current_site=get_current_site(request)
            email_subject='[Reset Your Password]'
            message=render_to_string('authentication/reset-user-password.html', {
            'domain': '127.0.0.1:8000',
            'uid':urlsafe_base64_encode(force_bytes(user[0].pk)),
            'token': PasswordResetTokenGenerator().make_token(user[0])
            })

            
            email_message=EmailMessage(email_subject, message, settings.EMAIL_HOST_USER,
            [email])
            email_message.send()

            messages.info(request, "Password reset link has been to your registered email.")
            return render(request, 'authentication/request-reset-email.html')
        

class SetNewPasswordView(View): 
    def get(self, request, uidb64, token):
        context = {
            'uidb64' :uidb64, 
            'token': token
        }
        try:        
            user_id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=user_id)
            
            if not PasswordResetTokenGenerator().check_token(user, token): 
                messages.warning(request, "Password Reset Link is Invalid") 
                return render(request, 'authentication/request-reset-email.html')
            
        except UnicodeDecodeError as identifier:
            pass

        return render(request, 'authentication/set-new-password.html', context)
    
    def post(self, request, uidb64, token):
        context={
            'uidb64':uidb64,
            'token':token
        }
        password=request.POST['pass1']
        confirm_password=request.POST['pass2']
        if password!=confirm_password:
            messages.warning(request, "Password is Not Matching")
            return render(request, 'authentication/set-new-password.html', context)
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            
            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.warning(request, "Password Reset Link is Invalid")
                return render(request, 'authentication/request-reset-email.html')
            
            user.set_password(password)
            user.save()
            messages.success(request, "Your password has been reset successfully. You can log in now.")
            return redirect('auth/login')
        
        except (UnicodeDecodeError, User.DoesNotExist):
            messages.error(request, "Something went wrong. Please try again.")
            return render(request, 'authentication/set-new-password.html', context)
        

def terms_conditions(request):
    return render(request, 'authentication/terms_conditions.html')