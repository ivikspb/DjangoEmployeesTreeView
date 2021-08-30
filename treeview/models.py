from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Department(MPTTModel):
    name = models.CharField('Подразделение', max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                            related_name='children', verbose_name="Находится в подразделении")

    class Meta:
        verbose_name = 'Подразделение'
        verbose_name_plural = 'Подразделения'

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class Employee(models.Model):
    name = models.CharField('ФИО', max_length=50)
    position = models.CharField('Должность', max_length=50)
    hired_date = models.DateField('Дата приема на работу')
    salary = models.DecimalField('Размер заработной платы', max_digits=11, decimal_places=2)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Сотрудника'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return f'[ID{str(self.id)}] {self.name}'
