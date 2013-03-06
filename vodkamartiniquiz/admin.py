from django.contrib import admin
from django.contrib.auth.models import User
from vodkamartiniquiz.models import Quiz, Question, Answer, QuizResult
from vodkamartiniquiz.forms import QuizAdminForm


class QuestionInline(admin.TabularInline):
    model = Question
    fields = ('question', 'enabled', 'weight')

class QuizAdmin(admin.ModelAdmin):
    form = QuizAdminForm
    list_filter = ['created', 'status']
    search_fields = ['title']
    prepopulated_fields = {"slug": ("title", )}
    list_display = ('__unicode__', 'author', 'created', 'status')
    inlines = [QuestionInline]

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

#class AnswerAdmin(admin.ModelAdmin):
#    pass

class QuizResultAdmin(admin.ModelAdmin):
    raw_id_fields = ('quiz',)

#admin.site.register(Answer, AnswerAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuizResult, QuizResultAdmin)
