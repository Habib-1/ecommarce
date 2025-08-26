from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from common.models import BaseModel
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self,name, email, phone , password=None):
        if not name :
            raise ValueError("User must set a name")
        if not email :
            raise ValueError("User must have an email")
        if not phone:
            raise ValueError("User must have a phone number")
        
        email=self.normalize_email(email)
        user=self.model(
            name=name,
            email=email,
            phone=phone
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,name,email,phone,password=None):
        user=self.create_user(
            name,email,phone,password

        )
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.is_active=True

        user.save(using=self._db)
        return user
    

class User(AbstractBaseUser,PermissionsMixin,BaseModel):
    name = models.CharField(max_length=150,blank=True ,null=True)
    email = models.EmailField(verbose_name='email', max_length=150, unique=True)
    phone = models.CharField(max_length=20,null=True , blank=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','phone']
    
    objects = UserManager()
    
    def __str__(self):
        return self.email
    

class Customer(BaseModel):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=False,related_name='customer')
    address=models.TextField(blank=True,null=True)
    city=models.CharField(max_length=100,blank=True,null=True)
    state=models.CharField(max_length=100, blank=True,null=True)
    postal_code=models.CharField(max_length=20,blank=True,null=True)
    country=models.CharField(max_length=100,default="Bangladesh")

    class Meta:
        verbose_name_plural = 'Customers'

    def __str__(self):
        return self.user.email