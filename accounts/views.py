from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.utils.translation import gettext_lazy as _

from persian_tools import phone_number

from BANPars.redis_conf import redis

from customUser.models import User
from .models import Profile

from .forms import (RegistrationForm, VerificationForm, UserLoginForm, 
                    SetNewPasswordForm, UserEditForm, ProfileDataForm, 
                    ProfileAvatarForm, ChangePassword)

from .utils import generate_token, save_session
from .tasks import send_otp

import json


# Tip : a decorator for authenticated users is required so authenticated users don't have access to
# register, login, verify, reset password pages




def accounts_register(request) :
    form = RegistrationForm()

    if request.method == 'POST' :
        form = RegistrationForm(request.POST)
        if form.is_valid() :
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = User.objects.create_user(username=username, password=password)

            send_otp.apply_async((user.username, ))

            request.session['user_mobile'] = user.username
            return redirect('accounts:verify')

    return render(request, 'registration/signup.html', {'form' : form})


def verify_account(request) :
    if request.user.is_authenticated :
        return redirect('introduction:company')

    # if not request.session.get('user_mobile') :
    #     return redirect('accounts:register')

    if request.method == 'GET' :
        initial = {}
        if request.session.get('user_mobile') :
            initial['number'] = request.session.get('user_mobile')

        form = VerificationForm(initial=initial)

    # Policy for resending the OTP
    if request.method == 'POST' and request.is_ajax() :
        number = json.loads(request.body.decode("utf-8"))['phone']

        try :
            user = User.objects.get(username=number)
        except :
            response = {'response':'Something went wrong'}
            return JsonResponse(response, status=400)

        if user.is_active :
            response = {'response':'Something went wrong'}
            return JsonResponse(response, status=400)
        else :
            if redis.exists(f'{number}') != 0 :
                response = 'Already reported'
                status = 208
            else :
                send_otp.apply_async((number, ))
                response = 'OTP is sent'
                status = 201
            return JsonResponse({'data':response}, status=status)

    # Policy for verifing user
    if request.method == 'POST' and not request.is_ajax() :
        if request.POST.get('number') == request.session.get('user_mobile') :
            form = VerificationForm(request.POST)
            if form.is_valid() :
                user = get_object_or_404(User, username=request.POST.get('number'))
                user.is_active = True
                user.save()

                redis.delete(request.POST.get('number'))
                del request.session['user_mobile']
                save_session(request)

                login(request, user)
                return redirect('introduction:company')

    return render(request, 'registration/verify.html', {'form' : form})


def logout_user(request) :
    if not request.user.is_authenticated :
        return redirect('introduction:company')
    else :
        logout(request)
    return redirect('introduction:company')


def login_user(request) :
    if request.user.is_authenticated :
        return redirect('introduction:company')
    
    form = UserLoginForm()

    if request.method == 'POST' :
        form = UserLoginForm(request.POST)
        if form.is_valid() :
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user != None :
                login(request, user)
                return redirect('introduction:company')
            else :
                messages.add_message(request, messages.ERROR, _('Wrong credentials'))

    return render(request, 'registration/login.html', {'form' : form})


def forgotten_password(request) :
    if request.user.is_authenticated :
        return redirect('introduction:company')

    if request.method == 'GET' :
        initial = {}
        if request.session.get('password_reset') :
            initial['number'] = request.session.get('password_reset')

        form = VerificationForm(initial=initial)


    if request.method == 'POST' and request.is_ajax() :
        number = json.loads(request.body.decode("utf-8"))['phone']
        if phone_number.validate(number) :
            try :
                user = User.objects.get(username=number)
            except :
                response = {'response':'Something went wrong'}
                return JsonResponse(response, status=400)

            if not user.is_active :
                response = {'response':'Something went wrong'}
                return JsonResponse(response, status=400)
            else :
                if redis.exists(f'{number}') != 0 :
                    response = 'Already reported'
                    status = 208
                else :
                    send_otp.apply_async((number, ))
                    response = 'OTP is sent'
                    status = 201
                return JsonResponse({'data':response}, status=status)

    if request.method == 'POST' and not request.is_ajax() :
        form = VerificationForm(request.POST)
        if form.is_valid() :
            user = get_object_or_404(User, username=request.POST.get('number'))
            request.session['password_reset'] = user.username
            token = generate_token.make_token(user)
            return redirect('accounts:change_forgotten_password', token=token)

        messages.add_message(request, messages.ERROR, _('Something went wrong, Please try again'))

    return render(request, 'registration/forget_password_form.html', {'form': form, })


def change_forgotten_password(request, token) :
    if request.user.is_authenticated :
        return redirect('introduction:company')

    if not request.session.get('password_reset') :
        messages.add_message(request, messages.ERROR, _('Verify your number first'))
        return redirect('accounts:forgetPass')

    if request.method == 'GET' :
        try :
            number = request.session.get('password_reset')
            user = User.objects.get(username=number)
        except :
            user = None
        if user != None and generate_token.check_token(user, token) :
            form = SetNewPasswordForm()
        else :
            messages.add_message(request, messages.ERROR, _('Reset password time expired'))
            return redirect('accounts:forgetPass')

    if request.method == 'POST' :
        form = SetNewPasswordForm(request.POST)
        if form.is_valid() :
            number = request.session.get('password_reset')
            user = get_object_or_404(User, username=number)
            user.set_password(request.POST.get('password'))
            user.save()
            
            del request.session['password_reset']
            save_session(request)
            messages.add_message(request, messages.SUCCESS, _('Password successfully changed'))
            return redirect('accounts:login')

    return render(request, 'registration/change_forgotten_password.html', {'form' : form})


@login_required
def profileEdit(request) :
    if not request.user.is_authenticated :
        return redirect('accounts:login')

    form = UserEditForm(initial={'fullname': request.user.fullname, 'email': request.user.email})
    user_profile = Profile.objects.get(user=request.user)
    profileDataForm = ProfileDataForm(initial={'bio': user_profile.bio, 'comapny': user_profile.company,
                                    'website': user_profile.website})
    profileAvatarForm = ProfileAvatarForm(initial={'avatar': user_profile.avatar, })
    avatar = user_profile.avatar

    if request.method == 'POST' :
        if 'data-submit' in request.POST :
            # print('data')
            form = UserEditForm(instance=request.user, data=request.POST)
            print(form.is_valid())
            profileDataForm = ProfileDataForm(request.POST, instance=request.user.profile)
            if form.is_valid() and profileDataForm.is_valid() :
                form.save()
                profileDataForm.save()
                messages.add_message(request, messages.SUCCESS, _('Your personal info was successfully updated'))
                return redirect('store:product_all')


        if 'image-submit' in request.POST and request.FILES :
            profileAvatarForm = ProfileAvatarForm(request.POST, request.FILES, instance=request.user.profile)
            if profileAvatarForm.is_valid() :
                profileAvatarForm.save()
                messages.add_message(request, messages.SUCCESS, _('Your image profile was successfully updated'))
                return redirect('store:product_all')

        if 'delete-submit' in request.POST :
            try :
                temp = Profile.objects.get(user=request.user)
                temp.avatar = 'profiles/no_profile.png'
                temp.save()

                messages.add_message(request, messages.SUCCESS, _('Your image profile was successfully removed'))
            except :
                messages.add_message(request, messages.ERROR, _('Something went wrong in removing your profile image'))
            return redirect('store:product_all')


    context = {'user_form': form, 'profile_data_form': profileDataForm,
                'profile_avatar_form': profileAvatarForm, 'avatar' : avatar}
    return render(request, 'accounts/edit_profile.html', context)


@login_required
def change_password(request) :
    if request.method == 'GET' :
        form = ChangePassword(user=request.user)

    if request.method == 'POST' :
        form = ChangePassword(user=request.user, data=request.POST)
        if form.is_valid() :
            user = request.user
            user.set_password(request.POST['password'])
            user.save()

            messages.add_message(request, messages.SUCCESS, _('Password was successfully changed'))
            return redirect('store:product_all')


    context = {'form' : form}
    return render(request, 'accounts/change_password.html', context)