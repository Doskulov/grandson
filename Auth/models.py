from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class PersonManager(BaseUserManager):
    def create_user(self, username, full_name, password=None):
        if not username or not full_name:
            raise ValueError('Users must have an username and full_name')

        user = self.model(
            username=username,
            full_name=full_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, full_name, password):
        user = self.create_user(
            username,
            full_name,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Person(AbstractBaseUser):
    username = models.CharField('Логин пользователя', max_length=30, unique=True)
    full_name = models.CharField('ФИО пользователя', max_length=100, null=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = PersonManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.username

    def has_module_perms(self, arg):
        return True

    def has_perm(self, arg):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'