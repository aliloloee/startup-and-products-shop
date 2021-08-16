from django.contrib.auth.tokens import PasswordResetTokenGenerator

from kavenegar import *


generate_token = PasswordResetTokenGenerator()


def save_session(request) :
    request.session.modified = True
