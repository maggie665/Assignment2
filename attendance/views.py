# Create your views here.
from django.contrib.auth import logout
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from attendance.models import Semester, Course, Lecturer, Student, Class, Attendance, CollegeDay
from attendance.serializers import SemesterSerializer, CourseSerializer, LecturerSerializer, StudentSerializer, \
    ClassLecturerSerializer, ClassSerializer, AttendanceStudentSerializer, AttendanceSerializer, CollegeDaySerializer, \
    UserSerializer
from django.contrib.auth.models import User, Group


class SemesterApiView(viewsets.ModelViewSet):
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer
    permission_classes = [permissions.IsAdminUser]

    def list(self, request, *args):
        semesters = Semester.objects.all()
        serializer = self.get_serializer(semesters, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            request.data.pop('id')
        except KeyError:
            request.data['id'] = len(self.queryset) + 1
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        return Response("")

    def getone(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance, many=False)
        return Response(serializer.data)


class CourseApiView(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAdminUser]

    def list(self, request, *args):
        courses = Course.objects.all()
        serializer = self.get_serializer(courses, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            request.data.pop('id')
        except KeyError:
            request.data['id'] = len(self.queryset) + 1
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        return Response("")

    def getone(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance, many=False)
        return Response(serializer.data)


class LecturerApiView(viewsets.ModelViewSet):
    queryset = Lecturer.objects.all()
    users = User.objects.all()
    serializer_class = LecturerSerializer
    permission_classes = [permissions.IsAdminUser]

    def list(self, request, *args):
        lecturers = Lecturer.objects.all()
        serializer = self.get_serializer(lecturers, many=True)
        return Response(serializer.data)

    def create(self, request, *args):
        data = request.data.copy()
        lecturer_fname = data['lecturer_fname']
        lecturer_lname = data['lecturer_lname']
        lecturer_email = data['lecturer_email']
        lecturer_DOB = data["DOB"]
        dob = str(lecturer_DOB).split(" ")[0].replace("-", "")
        user = User.objects.create_user(username=lecturer_fname + lecturer_lname, email=lecturer_email)
        user.set_password(dob)
        try:
            group = Group.objects.get(name='Lecturer')
            user.groups.add(group)
        except Group.DoesNotExist:
            group = Group.objects.create(name='Lecturer')
            group.save()
            user.groups.add(group)
        user.save()
        data['id'] = len(self.queryset) + 1
        data['staff_id'] = user.id
        data['user'] = user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        lecturer_fname = lecturer_lname = lecturer_email = lecturer_DOB = ""
        try:
            lecturer_fname = request.data.pop('lecturer_fname')
        except:
            pass
        try:
            lecturer_lname = request.data.pop('lecturer_lname')
        except:
            pass
        try:
            lecturer_email = request.data.pop('lecturer_email')
        except:
            pass
        try:
            lecturer_DOB = request.data.pop("lecturer_DOB")
        except:
            pass
        instance = Lecturer.objects.get(id=int(kwargs.pop('pk')))
        if lecturer_fname + lecturer_lname != "":
            instance.user.username = lecturer_fname + lecturer_lname
        if lecturer_email != "":
            instance.user.email = lecturer_email
        if lecturer_DOB != "":
            request.data['DOB'] = lecturer_DOB
            dob = str(instance.DOB).split(" ")[0].replace("-", "")
            instance.user.set_password(dob)
        serializer = self.get_serializer(instance=instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.user.delete()
        self.perform_destroy(instance)
        return Response("")

    def delete(self, request, *args, **kwargs):
        try:
            id = kwargs.pop('pk')
            lecturer = Lecturer.objects.get(id=int(id))
            lecturer.user.delete()
            lecturer.delete()
        except KeyError:
            for i in Lecturer.objects.all():
                i.user.delete()
                i.delete()
        return Response("")

    def getone(self, request, *args, **kwargs):
        instance = Lecturer.objects.get(id=int(kwargs.pop('pk')))
        serializer = self.get_serializer(instance=instance, many=False)
        return Response(serializer.data)


class StudentApiView(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    users = User.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAdminUser]

    def list(self, request, *args):
        students = Student.objects.all()
        serializer = self.get_serializer(students, many=True)
        return Response(serializer.data)

    def create(self, request, *args):
        data = request.data.copy()
        student_fname = data['student_fname']
        student_lname = data['student_lname']
        student_email = data['student_email']
        student_DOB = data["DOB"]
        dob = str(student_DOB).split(" ")[0].replace("-", "")
        user = User.objects.create_user(username=student_fname + student_lname, email=student_email)
        user.set_password(dob)
        try:
            group = Group.objects.get(name='Student')
            user.groups.add(group)
        except Group.DoesNotExist:
            group = Group.objects.create(name='Student')
            group.save()
            user.groups.add(group)
        user.save()
        data['id'] = len(self.queryset) + 1
        data['student_id'] = user.id
        data['user'] = user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        student_fname = student_lname = student_email = student_DOB = ""
        try:
            student_fname = request.data.pop('student_fname')
        except:
            pass
        try:
            student_lname = request.data.pop('student_lname')
        except:
            pass
        try:
            student_email = request.data.pop('student_email')
        except:
            pass
        try:
            student_DOB = request.data.pop("student_DOB")
        except:
            pass
        instance = Lecturer.objects.get(id=int(kwargs.pop('pk')))
        if student_fname + student_lname != "":
            instance.user.username = student_fname + student_lname
        if student_email != "":
            instance.user.email = student_email
        if student_DOB != "":
            request.data['DOB'] = student_DOB
            dob = str(instance.DOB).split(" ")[0].replace("-", "")
            instance.user.set_password(dob)
        serializer = self.get_serializer(instance=instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.user.delete()
        self.perform_destroy(instance)
        return Response("")

    def delete(self, request, *args, **kwargs):
        try:
            id = kwargs.pop('pk')
            student = Student.objects.get(id=int(id))
            student.user.delete()
            student.delete()
        except KeyError:
            for i in Student.objects.all():
                i.user.delete()
                i.delete()
        return Response("")

    def getone(self, request, *args, **kwargs):
        instance = Student.objects.get(id=int(kwargs.pop('pk')))
        serializer = self.get_serializer(instance=instance, many=False)
        return Response(serializer.data)


class CollegeDayApiView(viewsets.ModelViewSet):
    queryset = CollegeDay.objects.all()
    serializer_class = CollegeDaySerializer
    permission_classes = [permissions.IsAdminUser]

    def list(self, request, *args):
        collegeDay = CollegeDay.objects.all()
        serializer = self.get_serializer(collegeDay, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            request.data.pop('id')
        except KeyError:
            request.data['id'] = len(self.queryset) + 1
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        return Response("")

    def getone(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance, many=False)
        return Response(serializer.data)


class AttendanceApiView(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    # serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'head']

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return AttendanceSerializer
        else:
            for i in self.request.user.groups.all():
                if i.name == 'Lecturer':
                    return AttendanceSerializer
        return AttendanceStudentSerializer

    def list(self, request, *args):
        serializer = None
        if request.user.is_superuser:
            attendance = Attendance.objects.all()
            self.serializer_class = AttendanceSerializer
            serializer = self.get_serializer(attendance, many=True)
        else:
            for i in request.user.groups.all():
                if i.name == 'Lecturer':
                    attendance = Attendance.objects.filter(classes__lecturer__user=request.user)
                    self.serializer_class = AttendanceSerializer
                    serializer = self.get_serializer(attendance, many=True)
                    break
                elif i.name == 'Student':
                    self.http_method_names = ['get']
                    self.serializer_class = AttendanceStudentSerializer
                    attendance = Attendance.objects.filter(student__user=request.user)
                    serializer = self.get_serializer(attendance, many=True, read_only=True)
                    break
        if serializer is not None:
            return Response(serializer.data)
        return Response("")

    def post(self, request):
        try:
            request.data.pop('id')
        except KeyError:
            request.data['id'] = len(self.queryset) + 1
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        return Response("")

    def getone(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance, many=False)
        return Response(serializer.data)


class ClassApiView(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    # serializer_class = ClassSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'put', 'head']

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return ClassSerializer
        return ClassLecturerSerializer

    def list(self, request, *args):
        serializer = None
        if request.user.is_superuser:
            classes = Class.objects.all()
            self.http_method_names = ['get', 'post', 'put', 'head']
            self.serializer_class = ClassSerializer
            serializer = self.get_serializer(classes, many=True)
        else:
            for v in request.user.groups.all():
                if v.name == 'Lecturer':
                    classes = Class.objects.filter(lecturer__user=request.user)
                    self.http_method_names = ['get', 'put', 'head']
                    self.serializer_class = ClassLecturerSerializer
                    serializer = self.get_serializer(classes, many=True)
                    break
                elif self.http_method_names is not []:
                    self.http_method_names = []
                    self.serializer_class = ClassLecturerSerializer
        if serializer is not None:
            return Response(serializer.data)
        return Response("")

    def create(self, request, *args):
        data = request.data.copy()
        data['id'] = len(self.queryset) + 1
        course = Course.objects.get(id=data['course'])
        semester = Semester.objects.get(id=data['semester'])
        lecturer = Lecturer.objects.get(id=data['lecturer'])
        attendStudents = data.pop('student')
        student_all = Student.objects.all()
        classes = Class.objects.create(id=data['id'], number=data['number'], course=course, semester=semester,
                                       lecturer=lecturer)
        for student in student_all:
            if str(student.id) in attendStudents:
                classes.student.add(student)
        classes.save()
        serializer = self.get_serializer(instance=classes)
        for student in classes.student.all():
            Attendance.objects.create(student=student, course=course, classes=serializer.instance, absent_hours=0,
                                      attendance_rate=1.0)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        serializer = None
        if request.user.is_superuser:
            instance = self.get_object()
            self.http_method_names = ['get', 'post', 'put', 'head']
            self.serializer_class = ClassSerializer
            serializer = self.get_serializer(instance=instance, data=request.data, partial=True)
        else:
            for v in request.user.groups.all():
                if v.name == 'Lecturer':
                    instance = self.get_object()
                    self.http_method_names = ['get', 'put', 'head']
                    self.serializer_class = ClassLecturerSerializer
                    serializer = self.get_serializer(instance=instance, data=request.data, partial=True)
                    break
                elif self.http_method_names is not []:
                    self.http_method_names = []
        if serializer is not None:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        return Response("")

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        return Response("")

    def getone(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance, many=False)
        return Response(serializer.data)


class UserViewSets(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def User_logout(request):
    request.user.auth_token.delete()
    logout(request)
    return Response('User Logged out successfully')


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def User_ID_Search(request):
    return Response({"userid": request.user.id})