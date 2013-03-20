from django.contrib.admin import widgets
from django import forms
from django.contrib import admin
from django.core.urlresolvers import reverse
from vodkamartiniquiz.models import Quiz, Question, Answer, UserQuizAnswer

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
        Notice how we need to call __init__ from superclass first, if we don't do this
        then we won't be able to access attributes such as fields and instance.
        """
        super(QuestionForm, self).__init__(*args, **kwargs)
        if self.initial:
            self.question = self.initial['question']
            self.user = self.initial['user']
            self.next_question_id = self.initial['next_question_id']
            self.fields['answer'].queryset = self.question.answer_set.all().order_by('letter')

    def save(self):
        #print "quiz", self.question.quiz
        #print "question", self.question
        #print "answer", self.cleaned_data['answer']
        #print "user is", self.user
        #print "next_question_id", self.next_question_id
        #userquizanswer = UserQuizAnswer(user=self.user, quiz=self.question.quiz, answer=self.cleaned_data['answer'])
        #userquizanswer.save()
        if self.next_question_id:
            success_url = reverse('vodkamartiniquiz_question_detail', kwargs={'slug': self.question.quiz.slug, 'pk': self.next_question_id})
        else:
            success_url = reverse('vodkamartiniquiz_quiz_home')
            # TODO if this was the last question then we need to go to something like a /quiz/slug/result URL generated from other view
        print "success_url in form.save", success_url
        return success_url

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
