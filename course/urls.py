from django.urls import path

from course import views

urlpatterns = [
    path('', views.get_courses),
    path('get_frontpage_courses/', views.get_frontpage_courses),
    path('get_categories/', views.get_categories),
    path('get_progress/', views.user_progress),
    path('get_exams/', views.exam_progress),
    path('<int:pk>/post_progress/', views.post_progress),
    path('<slug:slug>/', views.get_course),
    path('<slug:course_slug>/<slug:lesson_slug>/', views.add_comment),
    path('<slug:course_slug>/<slug:lesson_slug>/get-comments/', views.get_comments),
    path('<slug:course_slug>/<slug:lesson_slug>/get-images/', views.get_lesson_photo),
    path('<slug:course_slug>/<slug:lesson_slug>/get-quiz/', views.get_quiz),
    path('<slug:course_slug>/<int:pk>/post-exam-progress/', views.post_exam_progress),
    
]