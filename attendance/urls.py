from django.urls import path, include, re_path
from attendance.views import SemesterApiView, CourseApiView, LecturerApiView, StudentApiView, CollegeDayApiView, AttendanceApiView, ClassApiView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'semesters', SemesterApiView, basename='semester')
router.register(r'courses', CourseApiView, basename='course')
router.register(r'lecturers', LecturerApiView, basename='lecturer')
router.register(r'students', StudentApiView, basename='student')
router.register(r'collegedays', CollegeDayApiView, basename='collegeday')
router.register(r'attendances', AttendanceApiView, basename='attendance')
router.register(r'classes', ClassApiView, basename='class')
urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
]
urlpatterns += router.urls