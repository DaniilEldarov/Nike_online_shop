from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from .choices import MyUserRoleEnum

# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self,username,email,password=None):
        user=self.model(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,username,email,password):
        user=self.create_user(username,email,password)
        user.is_admin=True
        user.set_password(password)
        user.save(using=self._db)


class MyUser(AbstractUser):
    username = models.CharField(max_length=150, verbose_name="Имя пользователя")
    email = models.EmailField(unique=True, verbose_name="Адрес электронной почты")
    role = models.CharField(choices=MyUserRoleEnum,
                            verbose_name="Роль"
                            ,default=MyUserRoleEnum.STANDART_USER)
    is_admin = models.BooleanField(
        default=False
    )
    is_2fa_enabled = models.BooleanField(
        default=False
    )
    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.email} "

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin

class OTP(models.Model):
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)