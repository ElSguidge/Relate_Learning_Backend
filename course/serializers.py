from django.conf import settings
from rest_framework import serializers
from django.contrib.auth.models import User

from profiles.serializers import UserSerializer
from .models import Course, Lesson, Comment, Category, Photo, Quiz, QuizResult, MainExam, ExamResult

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title', 'slug')

class CourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'title', 'slug', 'short_description', 'get_image')

class CourseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'title', 'slug', 'short_description', 'long_description', 'course_type')

class PhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photo
        fields = ("__all__") 

class LessonListSerializer(serializers.ModelSerializer):   
    images = PhotoSerializer(required=False, many=True)

    class Meta:
        model = Lesson
        fields = ('id', 'title', 'course', 'slug', 'short_description', 'lesson_type', 'status', 'long_description','photos','images')

class CommentsSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(required=False)
    class Meta:
        model = Comment
        fields = ('id', 'name', 'content', 'created_at', 'created_by')

class QuizSerializer(serializers.ModelSerializer):
    lesson = LessonListSerializer()
    class Meta:
        model = Quiz
        fields = ('id','lesson_id', 'question_number','lesson', 'question', 'answer', 'op1', 'op2', 'op3', 'op4')

class QuizResultSerializer(serializers.ModelSerializer):
    student = UserSerializer(required=True)
    quiz = QuizSerializer()

    class Meta:
        model = QuizResult
        fields = ('quiz','score', 'student',  'complete') 

class MainExamSerializer(serializers.ModelSerializer):
    course = CourseDetailSerializer()
    class Meta:
        model = MainExam
        fields = ('id', 'question_number','course', 'course_id','question', 'answer', 'op1', 'op2', 'op3', 'op4')

class ExamResultSerializer(serializers.ModelSerializer):
    student = UserSerializer(required=True)
    exam = MainExamSerializer()

    class Meta:
        model = ExamResult
        fields = ('exam','score', 'student',  'complete') 
