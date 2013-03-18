from django.contrib.admin import widgets
from django import forms
from vodkamartiniquiz.models import Quiz, Question, Answer
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

class QuestionForm(forms.Form):

    answer = forms.ModelChoiceField(queryset=Answer.objects.none(), widget=forms.RadioSelect, empty_label=None, label='What would be your answer?')

    def __init__(self, *args, **kwargs):
        """
        ##Fill author_id with author's id obtained from instance.
        Notice how we need to call __init__ from superclass first, if we don't do this
        then we won't be able to access attributes such as fields and instance.
        """
        super(QuestionForm, self).__init__(*args, **kwargs)
        if self.initial:
            self.question = self.initial['question']
            self.user = self.initial['user']
            self.fields['answer'].queryset = self.question.answer_set.all().order_by('letter')

    def save(self):
        question = {'answer': self.cleaned_data['answer']}
        print "user is", self.user
        print "email is", self.user.email
        # TODO save result in this model and then return something to move to 
        # either the next question or display results for the quiz for this user
        #class UserQuizAnswer(models.Model):
        #    user = models.ForeignKey(User)
        #    quiz = models.ForeignKey(Quiz)
        #    answer = models.ForeignKey(Answer)
        return question

    #def save(self):
    #    if self.question_id:
    #        """ existing question, no need to change author or status """
    #        question = Question.objects.get(pk=self.question_id)
    #        question.title = self.cleaned_data['title']
    #        question.body = self.cleaned_data['body']
    #    else:
    #        question = Question(title=self.cleaned_data['title'], body=self.cleaned_data['body'], author=self.author, status=Question.LIVE_STATUS)

    #    question.save()

    #    return question
