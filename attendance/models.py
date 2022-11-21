from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class Lecturer(models.Model):
    staff_id = models.PositiveIntegerField()
    lecturer_fname = models.CharField(max_length=200, null=False, blank=False)
    lecturer_lname = models.CharField(max_length=200, null=False, blank=False)
    lecturer_email = models.CharField(max_length=200, null=False, blank=False)
    DOB = models.DateField(null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.staff_id.__str__()


class Student(models.Model):
    student_id = models.PositiveIntegerField()
    student_fname = models.CharField(max_length=200, null=False, blank=False)
    student_lname = models.CharField(max_length=200, null=False, blank=False)
    student_email = models.CharField(max_length=200, null=False, blank=False)
    DOB = models.DateField(null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.student_id.__str__()


class Course(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    code = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    hours_per_day = models.IntegerField(blank=False)
    totalhours = models.IntegerField(blank=False)

    def __str__(self):
        return self.id.__str__()


class Semester(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    year = models.PositiveIntegerField()
    semester = models.CharField(max_length=200, null=True, blank=True)
    course = models.ManyToManyField(Course, related_name='semester_course', blank=True)

    def __str__(self):
        return self.id.__str__()


class Class(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    number = models.PositiveIntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='class_course', blank=False)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE, blank=True)
    student = models.ManyToManyField(Student, related_name='class_student', blank=False)

    def __str__(self):
        return self.number.__str__()


class Attendance(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=False)
    classes = models.ForeignKey(Class, on_delete=models.CASCADE, blank=False)
    absent_hours = models.IntegerField(blank=False)
    attendance_rate = models.FloatField(blank=False)

    def __str__(self):
        return self.id.__str__()


class CollegeDay(models.Model):
    id = models.PositiveIntegerField(primary_key=True, blank=False)
    date = models.DateField()
    Class = models.ManyToManyField(Class, blank=True, related_name="collegeday_class")

    def __str__(self):
        return self.date.__str__()
