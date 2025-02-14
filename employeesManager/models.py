from djongo import models

class Employee(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    salary = models.FloatField()
    hire_date = models.DateField()
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.name
