from django.contrib import admin
#from django.core.exceptions import DoesNotExist 
from vodkamartiniquiz.models import Quiz, Question, Answer, QuizResult
from vodkamartiniquiz.forms import QuizAdminForm


class QuestionInline(admin.TabularInline):
    model = Question
    fields = ('question', 'enabled', 'weight')
    #readonly_fields = ('one', 'two')

class QuizAdmin(admin.ModelAdmin):
    form = QuizAdminForm
    list_filter = ['created', 'status']
    search_fields = ['title']
    prepopulated_fields = {"slug": ("title", )}
    list_display = ('__unicode__', 'author', 'created', 'status')
    #exclude = ('enable_comments', 'categories', 'featured', 'author')
    #raw_id_fields = ('author',)
    inlines = [QuestionInline]

    def save_model(self, request, obj, form, change):
        print "all fields for object"
        for field in obj._meta.fields:
            print field.name

        try:
            if obj.author:
                print "before obj.author", obj.author
                pass
        except:
            obj.author = request.user
            print "after obj.author", obj.author
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
