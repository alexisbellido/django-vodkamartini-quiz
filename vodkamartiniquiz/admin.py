from django.contrib import admin
from vodkamartiniquiz.models import Quiz, Question, Answer, QuizResult


class QuestionInline(admin.TabularInline):
    model = Question
    fields = ('question', 'enabled', 'weight')
    #readonly_fields = ('one', 'two')

class QuizAdmin(admin.ModelAdmin):
    list_filter = ['created', 'status']
    search_fields = ['title']
    prepopulated_fields = {"slug": ("title", )}
    list_display = ('__unicode__', 'author', 'created', 'status')
    exclude = ('enable_comments', 'categories', 'featured')
    raw_id_fields = ('author',)
    inlines = [QuestionInline]

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
