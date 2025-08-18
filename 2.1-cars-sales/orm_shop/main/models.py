from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from datetime import datetime

class Client(models.Model):
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.name} {self.middle_name} {self.last_name}'

GEARBOX_CHOICES = (
    ('manual', 'Механика'),
    ('automatic', 'Автомат'),
    ('вариатор', 'CVT'),
    ('robot', 'Робот')
)

FUEL_TYPE_CHOICES = (
    ('gasoline', 'Бензин'),
    ('diesel', 'Дизель'),
    ('hybrid', 'Гибрид'),
    ('electro', 'Электро')
)

BODY_TYPE_CHOICES = (
    ('sedan', 'Седан'),
    ('hatchback', 'Хэтчбек'),
    ('SUV', 'Внедорожник'),
    ('wagon', 'Универсал'),
    ('minivan', 'Минивэн'),
    ('pickup', 'Пикап'),
    ('coupe', 'Купе'),
    ('cabrio', 'Кабриолет')
)


DRIVE_UNIT_CHOICES = (
    ('rear', 'Задний'),
    ('front', 'Передний'),
    ('full', 'Полный')
)


class Car(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    model = models.CharField(max_length=50)
    year = models.IntegerField(validators=[MinValueValidator(1950)])
    color = models.CharField(max_length=50)
    mileage = models.PositiveIntegerField()
    volume = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    body_type = models.CharField(max_length=20, choices=BODY_TYPE_CHOICES, default='sedan')
    drive_unit = models.CharField(max_length=20, choices=DRIVE_UNIT_CHOICES, default='front')
    gearbox = models.CharField(max_length=20, choices=GEARBOX_CHOICES, default='manual')
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPE_CHOICES, default='gasoline')
    price = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to='images', blank=True, null=True)

    def __str__(self):
        return f'{self.model} {self.year} {self.body_type} {self.color}'

    def clean(self):
        current_year = datetime.now().year
        if self.year > current_year:
            raise ValidationError({'year': f'Год выпуска не может быть больше {current_year}'})


class Sale(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.PROTECT, blank=False, null=False)
    car = models.ForeignKey(Car, on_delete=models.PROTECT, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Продажа {self.car} клиенту {self.client} от {self.created_at.date()}'
