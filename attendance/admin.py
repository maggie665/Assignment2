from django.contrib import admin
from attendance.models import Lecturer, Student, Class, Course, CollegeDay, Semester, Attendance

# Register your models here.
admin.site.register(Lecturer)
admin.site.register(Student)
admin.site.register(Class)
admin.site.register(Course)
admin.site.register(CollegeDay)
admin.site.register(Semester)
admin.site.register(Attendance)