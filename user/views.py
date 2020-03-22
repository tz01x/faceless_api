from django.shortcuts import render,redirect
from django.urls import reverse

from django.views.generic import TemplateView
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm
# Create your views here.
from django.conf import settings
from django.core.mail import send_mail

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string

from .tokens import account_activation_token
from .forms import loginform


from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.html import strip_tags


def send_mails(to,subject,template_name,context):



    html_mess=loader.render_to_string(template_name,context)

    text_content = strip_tags(html_mess) # Strip the html tag. So people can see the pure text at least.

    msg=EmailMultiAlternatives(subject, text_content,settings.EMAIL_HOST_USER, [to,settings.EMAIL_HOST_USER])
    # print(request.user.email)
    msg.attach_alternative(html_mess, "text/html")
    msg.send(fail_silently=True)

# @login_required
# def profile(request):
#     template_name='user/profile.html'
#     qs=Order.objects.all().filter(user=request.user).order_by('-created')
#     qs2=QuickOrder.objects.all().filter(user=request.user).order_by('-created')
#
#     order_page = request.GET.get('order_page', 1)
#     prescription_page = request.GET.get('prescription_page', 1)
#
#     paginator1 = Paginator(qs, 10)
#     paginator2 = Paginator(qs2, 10)
#
#     try:
#         qs = paginator1.page(order_page)
#         qs2 = paginator2.page(prescription_page)
#     except PageNotAnInteger:
#         qs = paginator1.page(1)
#         qs2 = paginator2.page(1)
#     except EmptyPage:
#         qs = paginator1.page(paginator1.num_pages)
#         qs2 = paginator2.page(paginator2.num_pages)
#
#
#     context={
#     'objects':qs,
#     'prescription':qs2,
#     }
#     return render(request,template_name,context)
#

def login_(request):
    n=request.GET.get('next',None)
    if request.method=='POST':

        form=loginform(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                if user.is_active:
                    login(request,user)

                    messages.success(request, f'Welcome {user.username.title()} ')
                    if n is not None:
                        return redirect("../.."+n)
                    return redirect('main:homeview')#url to index page
                else:
                    messages.warning(request, 'user is not active')
                    return HttpResponse('Sorry,user is not active')
            else:

                # form.errors['username']=form.error_class(['invalid info !'])
                form.errors['__all__']=form.error_class(['invalid information !'])

                return render(request = request,
                              template_name = "user/login.html",
                              context={"form":form})
        else:
            messages.warning(request, 'please enter valid user info'.title())


            return render(request = request,
                          template_name = "user/login.html",
                          context={"form":form})

    else:
        form = loginform()
    return render(request=request, template_name='user/login.html', context={'form': form})


# def register(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             user.refresh_from_db()  # load the profile instance created by the signal
#             user.profile.phone = form.cleaned_data.get('phone')
#             user.is_active = False
#             user.save()
#             current_site = get_current_site(request)
#             subject = 'Activate Your MySite Account'
#             message = render_to_string('user/account_activation_email.html', {
#                 'user': user,
#                 'domain': current_site.domain,
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token': account_activation_token.make_token(user),
#             })
#             send_mail(subject, message,settings.EMAIL_HOST_USER, [user.email,])
#             return redirect('user:account_activation_sent')
#     else:
#         form = CustomUserCreationForm()
#     return render(request = request,
#                                template_name = "user/registerPage.html",
#                                context={"form":form})

class account_activation_sent(TemplateView):
    template_name='user/account_activation_sent.html'

from django.contrib.auth.models import User
from .tokens import account_activation_token
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('main:homeview')
    else:
        return render(request, 'user/account_activation_invalid.html')

# def register(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             user.refresh_from_db()  # load the profile instance created by the signal
#             user.profile.phone = form.cleaned_data.get('phone')
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#
#             user = authenticate(username=username, password=raw_password)
#             if user is not None:
#                 if user.is_active:
#
#                     login(request, user)
#                     messages.success(request, 'Account !created successfully')
#                     return redirect('LUXOROSH_Homepage:home')#url to index page
#                 else:
#                     messages.warning(request, 'user is not active')
#                     return HttpResponse('Sorry,user is not active')
#         else:
#             for msg in form.error_messages:
#                 # print(form.error_messages[msg])
#                 messages.warning(request,form.error_messages[msg])
#
#             return render(request = request,
#                           template_name = "user/registerPage.html",
#                           context={"form":form})
#
#     else:
#         form = CustomUserCreationForm()
#     return render(request=request, template_name='user/registerPage.html', context={'form': form})
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            obj=form.save()
            obj.refresh_from_db()  # load the profile instance created by the signal
            obj.profile.phone = form.cleaned_data.get('phone')
            obj.profile.location = form.cleaned_data.get('address')
            obj.set_password(form.cleaned_data.get('password1'))
            #whey i use a set_password , because CustomUserCreationForm form dose not set set user password auto , thats whey you have to spceficly add this
            obj.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')

            user = authenticate(request,username=username, password=raw_password)
            if user is not None:
                # print('hmm55')

                if user.is_active:

                    login(request, user)
                    messages.success(request, 'Account been created Successfully')
                    return redirect('main:homeview')#url to index page
                else:
                    messages.warning(request, 'user is not active')
                    return HttpResponse('Sorry,user is not active')
        else:
            # for msg in form.error_messages:
            #     # print(form.error_messages[msg])
            #     messages.warning(request,form.error_messages[msg])

            return render(request = request,
                          template_name = "user/registerPage.html",
                          context={"form":form})

    else:
        form = CustomUserCreationForm()
    return render(request=request, template_name='user/registerPage.html', context={'form': form})

from django.contrib.auth.views import PasswordResetConfirmView

class PasswordResetConfirmViewCoustom(PasswordResetConfirmView):
    template_name='user/password_reset_confirm.html'
    def get_success_url(self):
        return reverse('user:password_reset_complete')



from django.db.models.query_utils import Q
from django.contrib.auth.forms import PasswordResetForm

from django.core.validators import validate_email
from django.core.exceptions import ValidationError


from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


def PasswordReset_View(request):
    template_name='user/password_reset.html'
    form = PasswordResetForm()
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            data=form.data.get('email')
            associated_users= User.objects.filter(Q(email=data))#|Q(username=data)
            #chenge for only one user

            if associated_users.exists():
                for user in associated_users:
                    c = {
                            'email': user.email,
                            'domain': request.META['HTTP_HOST'],
                            'site_name': 'Medicast',
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'user': user,
                            'token': default_token_generator.make_token(user),
                            'protocol': 'http',
                            }
                    send_mails(user.email,'Password Reset request form '.title(),'user/password_reset_email.html',c)

            return redirect('user:password_reset_done')

    return render(request,template_name,{'form':form})
