from django.contrib import admin


from .models import Category, Course, Lesson, Comment, Photo, Quiz, MainExam

class PhotoAdmin(admin.StackedInline):
    model = Photo

class LessonCommentInline(admin.TabularInline):
    model = Comment
    raw_id_fields = ['lesson']

class LessonAdmin(admin.ModelAdmin):

    list_display = ['title', 'course', 'status', 'lesson_type']
    list_filter = ['status', 'lesson_type']
    search_fields = ['title', 'short_description', 'long_description']
    inlines = [PhotoAdmin, LessonCommentInline]

    class Meta:
        model = Lesson

class QuizAdmin(admin.ModelAdmin):

    list_display = ['question', 'title','question_number','lesson']
    search_fields = ['question', 'title','answer', 'lesson']

    class Meta:
        model = Quiz

class ExamAdmin(admin.ModelAdmin):

    list_display = ['question', 'title','question_number','course']
    search_fields = ['question', 'title','answer', 'course']

    class Meta:
        model = MainExam


admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Photo)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Comment)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(MainExam, ExamAdmin)



