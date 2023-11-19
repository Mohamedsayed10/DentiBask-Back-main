from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.signing import Signer
import uuid
import six
import json
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.signing import TimestampSigner, BadSignature
import time
from django.contrib.auth.tokens import default_token_generator
timestamp_signer = TimestampSigner()

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) + str(timestamp) +
            str(user.is_active)
        )

account_activation_token = TokenGenerator()
reset_token_signer = Signer()

# class TokenGen(PasswordResetTokenGenerator):
#     def _make_hash_value(self, user, timestamp):
#         return (
#             six.text_type(user.pk) + six.text_type(timestamp) +
#             six.text_type(user.is_active)
#         )
#
# account_activation_token2 = TokenGen()

class TokenGen(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # Include the token generated by Django's PasswordResetTokenGenerator
        token = self.make_token(user.email)
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(token)
        )

    def generate_reset_token(self, user):
        timestamp = int(time.time())
        hash_value = self._make_hash_value(user, timestamp)
        return f"{hash_value}-{timestamp}"

    def check_reset_token(self, user, reset_token, max_age=None):
        try:
            uidb64, token, timestamp = reset_token.split("-")
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_user_model().objects.get(pk=uid)
            reset_token_data = {
                'user_id': user.pk,
                'timestamp': int(timestamp),
                'token': reset_token,
            }
            if max_age and not self._check_age(reset_token_data['timestamp'], max_age):
                return False
            return self.check_token(user, reset_token_data)
        except (ValueError, BadSignature, ObjectDoesNotExist):
            return False

    def _check_age(self, timestamp, max_age):
        current_time = int(time.time())
        return current_time - timestamp <= max_age

account_activation_token2 = TokenGen()




def verify_one_time_token(token_data_str, max_age):
    if token_data_str is None:
        return None

    try:
        # Try to load token_data as JSON. If successful, it's a token generated by account_activation_token2.
        token_data = json.loads(token_data_str)
        timestamp = token_data.get('timestamp', 0)
        current_time = int(time.time())
        if current_time - timestamp <= max_age:
            return token_data
    except (json.JSONDecodeError, KeyError):
        pass

    # If decoding as JSON fails, assume it's a token generated by account_activation_token.
    try:
        # Use Django's default_token_generator to verify the signature.
        uidb64, token = token_data_str.split("-")
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
        reset_token_data = {
            'user_id': user.pk,
            'timestamp': int(timestamp_signer.unsign(token)),
        }
        if default_token_generator.check_token(user, reset_token_data['token']):
            return reset_token_data
    except (ValueError, BadSignature, ObjectDoesNotExist):
        pass

    # If both attempts fail, return None.
    return None
