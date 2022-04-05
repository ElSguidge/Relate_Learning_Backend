
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from profiles.models import Profile
from PIL import Image, ImageOps
from ckeditor_uploader.fields import RichTextUploadingField



class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    short_description = models.TextField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title

class Course(models.Model):

    NO_EXAM = 'None'
    EXAM = 'exam'

    CHOICES_COURSE_TYPE = (
        (NO_EXAM, 'None'),
        (EXAM, 'Exam'),
    )

    categories = models.ManyToManyField(Category)
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    short_description = models.TextField(blank=True, null=True)
    long_description = models.TextField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='uploads', blank=True, null=True)
    course_type = models.CharField(max_length=20, choices=CHOICES_COURSE_TYPE, default=NO_EXAM)


    def __str__(self):
        return self.title

    def get_image(self):
        if self.image:
            return settings.WEBSITE_URL + self.image.url
        else:
            return 'http://bulma.io/images/placeholders/1280x960.png'

class Lesson(models.Model):
    DRAFT = 'draft'
    PUBLISHED = 'published'

    CHOICES_STATUS = (
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published')
    )

    ARTICLE = 'article'
    QUIZ = 'quiz'
    # EXAM = 'exam'

    CHOICES_LESSON_TYPE = (
        (ARTICLE, 'Article'),
        (QUIZ, 'Quiz'),
        # (EXAM, 'Exam')
    )

    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    short_description = models.TextField(blank=True, null=True)
    long_description = RichTextUploadingField(config_name='default')
    status = models.CharField(max_length=20, choices=CHOICES_STATUS, default=PUBLISHED)
    lesson_type = models.CharField(max_length=20, choices=CHOICES_LESSON_TYPE, default=ARTICLE)

    def __str__(self):
        return self.title

    def get_image(self):
        if self.long_description:
            return settings.WEBSITE_URL + self.long_description.url
        else:
            return 'http://bulma.io/images/placeholders/1280x960.png'

class Photo(models.Model):

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to ='uploads/')

    # resizing the image, you can change parameters like size and quality.
    def save(self, *args, **kwargs):
       super(Photo, self).save(*args, **kwargs)
       img = Image.open(self.photo.path)
       fixed_image = ImageOps.exif_transpose(img)
       if fixed_image.height > 1125 or fixed_image.width > 1125:
           fixed_image.thumbnail((400,400))
       fixed_image.save(self.photo.path,quality=70,optimize=True)


class Comment(models.Model):
    course = models.ForeignKey(Course, related_name='comments', on_delete=models.CASCADE)
    user_avatar = models.ForeignKey(Profile, null=True, blank=True, related_name="comments", on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)

class Quiz(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='quizzes', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True)
    question_number = models.IntegerField(default=1, null=True)
    question = RichTextUploadingField(config_name='default', null=True)
    answer = models.CharField(max_length=200, null=True)
    op1 = models.CharField(max_length=200, null=True)
    op2 = models.CharField(max_length=200, null=True)
    op3 = models.CharField(max_length=200, null=True)
    op4 = models.CharField(max_length=200, null=True)

    
    class Meta:
        verbose_name_plural = 'Quizzes'
    
    def __str__(self):
        return self.question

class QuizResult(models.Model):
    student = models.ForeignKey(User, related_name="results", on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, related_name="results", on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, null=True, blank=True, related_name="results", on_delete=models.CASCADE)
    score = models.FloatField(blank=True, null=True)
    complete = models.BooleanField(default=False)

class MainExam(models.Model):
    course = models.ForeignKey(Course, related_name='exams', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True)
    question_number = models.IntegerField(default=1, null=True)
    question = RichTextUploadingField(config_name='default', null=True)
    answer = models.CharField(max_length=200, null=True)
    op1 = models.CharField(max_length=200, null=True)
    op2 = models.CharField(max_length=200, null=True)
    op3 = models.CharField(max_length=200, null=True)
    op4 = models.CharField(max_length=200, null=True)

    
    class Meta:
        verbose_name_plural = 'Exams'
    
    def __str__(self):
        return self.question

class ExamResult(models.Model):
    student = models.ForeignKey(User, related_name="exam_results", on_delete=models.CASCADE)
    exam = models.ForeignKey(MainExam, related_name="exam_results", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, null=True, blank=True, related_name="exam_results", on_delete=models.CASCADE)
    score = models.FloatField(blank=True, null=True)
    complete = models.BooleanField(default=False)
