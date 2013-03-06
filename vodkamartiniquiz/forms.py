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
