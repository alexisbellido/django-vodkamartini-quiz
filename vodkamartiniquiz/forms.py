from django.contrib.admin import widgets
from django import forms
from vodkamartiniquiz.models import Quiz
from django.contrib import admin
from django.contrib.auth.models import User

class QuizAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # TODO how to get the instance data to autofill the author_id?
        #print "test"
        #print self.instance
        super(QuizAdminForm, self).__init__(*args, **kwargs)

    author_id = forms.CharField(widget=widgets.ForeignKeyRawIdWidget(Quiz._meta.get_field('author').rel, admin.site),
                                required=False,
                                label="Author User Id",
                               )

    class Meta:
        model = Quiz
        exclude = ('enable_comments', 'categories', 'featured', 'author')

    def save(self, commit=False):
        quiz = super(QuizAdminForm, self).save(commit=False)
        try:
            quiz.author = User.objects.get(pk=self.cleaned_data['author_id'])
        except (User.DoesNotExist, ValueError) as e:
            pass
        return quiz
