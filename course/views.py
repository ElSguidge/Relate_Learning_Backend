from django.shortcuts import render
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
import requests

from rest_framework import permissions
from .models import Course, Lesson, Comment, Category, Quiz, QuizResult, MainExam, ExamResult
from .serializers import (CourseListSerializer, CourseDetailSerializer, LessonListSerializer, CommentsSerializer, 
                          CategorySerializer, PhotoSerializer, QuizSerializer, QuizResultSerializer, MainExamSerializer,
                          ExamResultSerializer)
                            

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_courses(request):
    category_id = request.GET.get('category_id', '')
    courses = Course.objects.all()

    if category_id:
        courses = courses.filter(categories__in=[int(category_id)])

    serializer = CourseListSerializer(courses, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_frontpage_courses(request):
    courses = Course.objects.all()[0:4]
    serializer = CourseListSerializer(courses, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_course(request, slug):
    course = Course.objects.get(slug=slug)
    course_serializer = CourseDetailSerializer(course)
    lesson_serializer = LessonListSerializer(course.lessons.all(), many=True)
    exam_serializer = MainExamSerializer(course.exams.all(), many=True)
    

    if request:
        course_data = course_serializer.data
    else:
        course_data = {}

    data = {
        'course': course_data,
        'lessons': lesson_serializer.data,
        'exam_questions': exam_serializer.data
    }

    return Response(data)

@api_view(['GET'])
def get_comments(request, course_slug, lesson_slug):
    lesson = Lesson.objects.get(slug=lesson_slug)
    serializer = CommentsSerializer(lesson.comments.all(), many=True)
    return Response(serializer.data)

@api_view(['POST'])
def add_comment(request, course_slug, lesson_slug):
    data = request.data
    name = data.get('name')
    content = data.get('content')

    course = Course.objects.get(slug=course_slug)
    lesson = Lesson.objects.get(slug=lesson_slug)

    comment = Comment.objects.create(course=course, lesson=lesson, name=name, content=content, created_by=request.user)

    serializer = CommentsSerializer(comment)

    return Response(serializer.data)

@api_view(['GET'])
def get_lesson_photo(request, course_slug, lesson_slug):
    course = Course.objects.get(slug=course_slug)
    lesson = Lesson.objects.get(slug=lesson_slug)

    serializer = PhotoSerializer(lesson.photos.all(), many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
def get_quiz(request, course_slug, lesson_slug):
    lesson = Lesson.objects.get(slug=lesson_slug)
    serializer = QuizSerializer(lesson.quizzes.all(), many=True)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def user_progress(request):
    progress = QuizResult.objects.all()
    serializer = QuizResultSerializer(progress, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
def post_progress(request, pk):
    data = request.data
    score = data.get('score') 
    # assert score != None

    complete = data.get('complete')
    # assert complete != None
    quiz = Quiz.objects.get(pk=pk)


    user_progress = QuizResult.objects.create(quiz=quiz, score=score, complete=complete, student=request.user)

    serializer = QuizResultSerializer(user_progress)

    return Response(serializer.data)

@api_view(['PUT'])
def post_exam_progress(request, course_slug, pk):
    data = request.data
    score = data.get('score') 
    # assert score != None

    complete = data.get('complete')
    # assert complete != None
    # exam = MainExam.objects.get(pk=pk)
    course = Course.objects.get(slug=course_slug)
    exam = MainExam.objects.get(pk=pk)


    user_progress = ExamResult.objects.create(exam=exam, course=course, score=score, complete=complete, student=request.user)

    serializer = ExamResultSerializer(user_progress)

    return Response(serializer.data)

@api_view(['GET'])
def exam_progress(request):

    progress = ExamResult.objects.all()

    serializer = ExamResultSerializer(progress, many=True)
    return Response(serializer.data)
