from django.core.urlresolvers import reverse
from django.contrib import admin
from django.contrib.auth.models import User
from .models import Quiz, Question, Answer, QuizResult, UserQuizAnswer
from .forms import QuizAdminForm

class QuizResultInline(admin.TabularInline):
    model = QuizResult

class QuestionInline(admin.TabularInline):
    model = Question
    fields = ('question', 'edit', 'enabled', 'weight')
    readonly_fields = ('edit',)

    def edit(self, instance):
        return '<a href="%s">%s</a>' % (reverse('admin:vodkamartiniquiz_question_change', args=(instance.id,)), 'Edit')

    edit.allow_tags = True

class QuizAdmin(admin.ModelAdmin):
    form = QuizAdminForm
    list_filter = ['created', 'status']
    search_fields = ['title']
    prepopulated_fields = {"slug": ("title", )}
    list_display = ('__unicode__', 'author', 'created', 'status')
    inlines = [QuestionInline, QuizResultInline]

    def save_model(self, request, obj, form, change):
        try:
            obj.author = User.objects.get(pk=form.cleaned_data['author_id'])
        except (User.DoesNotExist, ValueError) as e:
            obj.author = request.user
        obj.save()

class AnswerInline(admin.TabularInline):
    model = Answer
    fields = ('answer', 'letter', 'points')

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ('__unicode__', 'quiz')
    raw_id_fields = ('quiz',)

    fields = ('question', ('quiz', 'editquiz'), 'enabled', 'weight')
    readonly_fields = ('editquiz',)

    def editquiz(self, instance):
        return '<a href="%s">%s</a>' % (reverse('admin:vodkamartiniquiz_quiz_change', args=(instance.quiz.id,)), instance.quiz.title)

    editquiz.allow_tags = True
    editquiz.short_description = 'Edit quiz'


#class AnswerAdmin(admin.ModelAdmin):
#    pass

class QuizResultAdmin(admin.ModelAdmin):
    #fields = ('question', 'edit', 'enabled', 'weight')
    list_display = ('__unicode__', 'quiz', 'letter', 'min_points', 'max_points')
    raw_id_fields = ('quiz',)

class UserQuizAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'answer', 'question')

    def question(self, instance):
        return instance.answer.question

#admin.site.register(Answer, AnswerAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuizResult, QuizResultAdmin)
admin.site.register(UserQuizAnswer, UserQuizAnswerAdmin)
