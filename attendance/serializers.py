from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from django.contrib.auth.models import User
from attendance.models import Semester, Course, Lecturer, Student, Class, CollegeDay, Attendance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = '__all__'

    def create(self, validated_data):
        courses = validated_data.pop('course')
        semester = Semester.objects.create(**validated_data)
        for course in courses:
            course = Course.objects.filter(id=course.id).first()
            semester.course.add(course)
        semester.save()
        return semester


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

    def create(self, validated_data):
        course = Course.objects.create(**validated_data)
        return course


class LecturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecturer
        fields = '__all__'

    def create(self, validated_data):
        lecturer = Lecturer.objects.create(**validated_data)
        return lecturer


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'student_fname', 'student_lname', 'student_email', 'DOB')
        read_only_fields = ['id']

    def create(self, validated_data):
        student = Student.objects.create(**validated_data)
        return student


class ClassStudentSerializer(PrimaryKeyRelatedField, serializers.ModelSerializer):
    full_name = serializers.StringRelatedField(source="user.username", read_only=True)

    class Meta:
        model = Student
        fields = ('id', 'full_name', 'student_fname', 'student_lname', 'student_email', 'DOB')
        read_only_fields = ['id', 'full_name']

    def create(self, validated_data):
        student = Student.objects.create(**validated_data)
        return student


class ClassLecturerSerializer(serializers.ModelSerializer):
    student = ClassStudentSerializer(many=True, queryset=Student.objects.all())

    class Meta:
        model = Class
        fields = ('id', 'number', 'course', 'semester', 'lecturer', 'student')
        read_only_fields = ('id', 'number', 'course', 'semester', 'lecturer')

    def create(self, validated_data):
        classes = Class.objects.create(**validated_data)
        return classes


class ClassSerializer(serializers.ModelSerializer):
    student = ClassStudentSerializer(many=True, queryset=Student.objects.all())

    class Meta:
        model = Class
        fields = '__all__'

    def create(self, validated_data):
        classes = Class.objects.create(**validated_data)
        return classes


class AttendanceStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'
        read_only_fields = ('id', 'student', 'course', 'classes', 'absent_hours', 'attendance_rate')


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'

    def update(self, instance, validated_data):
        class_id = validated_data.pop("class_id")
        classes = Class.objects.get(id=class_id)
        course = Course.objects.get(id=classes.course.id)
        absent_student_ids = list(map(int, validated_data.pop("absent_student_ids")))
        students = classes.student.all()
        for student in students:
            if student.student_id in absent_student_ids:
                attendance = Attendance.objects.filter(student=student, course=course, classes=classes)
                if len(attendance) == 0:
                    print("attendance not found")
                else:
                    attendance[0].absent_hours += classes.course.hours_per_day
                    attendance[0].attendance_rate = (classes.course.totalhours - attendance[
                        0].absent_hours) / classes.course.totalhours
                    attendance[0].save()
            else:
                print("student not found")
        return instance


class CollegeDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = CollegeDay
        fields = '__all__'

    def create(self, validated_data):
        collegeDay = CollegeDay.objects.create(**validated_data)
        return collegeDay