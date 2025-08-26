
# from allauth.account.adapter import DefaultAccountAdapter

# class CustomAccountAdapter(DefaultAccountAdapter):
#     """
#     Adapter for API-only registration.
#     Saves extra fields from serializer (name, phone).
#     """
#     def save_user(self, request, user, form, commit=True):
#         user = super().save_user(request, user, form, commit=False)

#         # request.data comes from DRF serializer
#         data = getattr(request, 'data', {})
#         user.name = data.get('name', '')
#         user.phone = data.get('phone', '')

#         if commit:
#             user.save()
#         return user
    
#     def get_phone(self, user):
#         return getattr(user, "phone", None),False
    
    
    
#     def send_verification_code_sms(self, *args, **kwargs):
#         pass 

#     def phone_verification_redirect_url(self, request, user):

#         return None
