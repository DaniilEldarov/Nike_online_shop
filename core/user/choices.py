from django.db.models import TextChoices

class MyUserRoleEnum(TextChoices):
    STANDART_USER = 'StandardUser','Обычный пользователь'
    MANAGER = 'Manager','Манеджер'
    ACCOUNTANT = 'Accountant','Бухгалтер'