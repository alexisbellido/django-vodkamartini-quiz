from django.contrib.admin import widgets
from django import forms
from vodkamartiniquiz.models import Quiz
from django.contrib import admin

class QuizAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        """
        Fill author_id with author's id obtained from instance.
        Notice how we need to call __init__ from superclass first, if we don't do this
        then we won't be able to access attributes such as fields and instance.
        """
        super(QuizAdminForm, self).__init__(*args, **kwargs)
        if self.initial:
            self.fields['author_id'].initial = self.instance.author.id

    author_id = forms.CharField(widget=widgets.ForeignKeyRawIdWidget(Quiz._meta.get_field('author').rel, admin.site),
                                               required=False,
                                               label="Author User Id",
                                               help_text="Enter a user id or click on the magnifying glass to choose a user. If empty the current\
                                                          logged in user will be used.",
                                              )

    class Meta:
        model = Quiz
        exclude = ('enable_comments', 'categories', 'featured', 'author')

    def save(self, commit=False):
        """
        Calling superclass's save method with commit=False means that object won't be saved
        so we can do some extra processing and use save_model in QuizAdmin.
        """
        quiz = super(QuizAdminForm, self).save(commit=False)
        return quiz

class QuizForm(forms.Form):

    #def __init__(self, author, quiz_id=0, request=None, *args, **kwargs):
    #    super(QuizForm, self).__init__(*args, **kwargs)
    #    self.author = author
    #    self.quiz_id = quiz_id
    #    self.request = request

    title = forms.CharField()
    body = forms.CharField(widget=forms.Textarea, label='Enter a description for your quiz')

    def save(self):
        quiz = {'title': self.cleaned_data['title'], 'body': self.cleaned_data['body']}
        return quiz

    #def save(self):
    #    if self.quiz_id:
    #        """ existing quiz, no need to change author or status """
    #        quiz = Quiz.objects.get(pk=self.quiz_id)
    #        quiz.title = self.cleaned_data['title']
    #        quiz.body = self.cleaned_data['body']
    #    else:
    #        quiz = Quiz(title=self.cleaned_data['title'], body=self.cleaned_data['body'], author=self.author, status=Quiz.LIVE_STATUS)

    #    quiz.save()

    #    return quiz
