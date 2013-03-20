from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.template import RequestContext
from django.shortcuts import render, render_to_response, get_object_or_404
from django.views.generic.base import View
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from braces.views import LoginRequiredMixin

from .models import Quiz, Question, QuizResult
from .forms import QuizForm, QuestionForm


class QuizHome(ListView):
    """
    Show live quizzes. We can use either a model or a queryset attribute.
    If provided, the value of queryset supersedes the value provided for model.
    Using model = Quiz is just a shorthand for queryset = Quiz.objects.all()
    In this case we want just live quizzes so we use that manager.
    """

    queryset = Quiz.live.all()
    paginate_by = 2

class QuizDetail(DetailView):
    """
    Show details for one quiz. As in QuizHome, we can use either model or queryset here.
    We chose queryset to make sure we only show live quizzes.
    """
    queryset = Quiz.live.all()

    def get_context_data(self, **kwargs):
        """
        Get the enabled questions order by weight for this quiz.
        TODO: get just the first question to start taking the quiz but only if user is authenticated, then the form comes.
        """
        context = super(QuizDetail, self).get_context_data(**kwargs)
        #context['question_list'] = self.object.question_set.filter(enabled=True).order_by('weight')
        if self.request.user.is_authenticated():
            context['first_question_id'] = self.object.getFirstQuestionId()
        return context

    #def get_object(self):
    #    """
    #    We could do something more with the object here
    #    """
    #    object = super(QuizDetail, self).get_object()
    #    return object

class QuestionDetail(LoginRequiredMixin, FormView, SingleObjectMixin):
    """
    This should be a FormView actually, to show the question and radio buttons with possible answers.
    It should include the pk for the next question in this quiz.
    """

    form_class = QuestionForm
    template_name = 'vodkamartiniquiz/question_form.html'
    queryset = Question.objects.filter(enabled=True)

    def get_initial(self):
        self.object = self.get_object()
        self.pk = self.object.pk
        self.question_pk_list = self.object.getQuestionsPkList()
        self.num_questions = len(self.question_pk_list)
        self.num_current_question = self.question_pk_list.index(self.pk) + 1
        self.next_question_id = self.getQuestionNextPk()
        self.previous_question_id = self.getQuestionPreviousPk()
        return {'question': self.object, 
                'user': self.request.user,
                'num_questions': self.num_questions,
                'num_current_question': self.num_current_question,
                'next_question_id': self.next_question_id,
                'previous_question_id': self.previous_question_id,
               }

    #def get_success_url(self):
    #    return '/some-url/'

    #def get(self, request, *args, **kwargs):
    #    self.object = self.get_object()
    #    print self.object
    #    response = super(QuestionDetail, self).get(request, *args, **kwargs)
    #    return response

    #def get_form(self, form):
    #    pass

    def form_valid(self, form):
        self.success_url = form.save()
        messages.info(self.request, 'Question answered.')
        return super(QuestionDetail, self).form_valid(form)

    #def form_invalid(self, form):
    #    messages.info(self.request, 'Submission problem, please try again.')
    #    return super(QuestionDetail, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        """
        Populate the context. Most of these details are initialized on self.get_initial
        """
        context = super(QuestionDetail, self).get_context_data(**kwargs)
        context['object'] = self.object
        context['quiz_slug'] = self.object.quiz.slug
        context['pk'] = self.pk
        context['question_pk_list'] = self.question_pk_list
        context['num_questions'] = self.num_questions
        context['num_current_question'] = self.num_current_question
        context['next_question_id'] = self.next_question_id
        context['previous_question_id'] = self.previous_question_id
        return context

    def getQuestionNextPk(self):
        pk_list = self.question_pk_list
        index = pk_list.index(self.pk)
        try:
            next_pk =  pk_list[index + 1]
        except IndexError:
            next_pk = None

        return next_pk

    def getQuestionPreviousPk(self):
        pk_list = self.question_pk_list
        index = pk_list.index(self.pk)
        if index > 0:
            previous_pk =  pk_list[index - 1]
        else:
            previous_pk = None

        return previous_pk

class QuizResult(DetailView):
    """
    Show result for quiz for currently logged in user
    """
    model = QuizResult
    #pass
    #return HttpResponse('text result')

#class QuizDetail(View):
#    greeting = 'Hola'
#
#    def get(self, request, *args, **kwargs):
#        if 'slug' in self.kwargs:
#            slug = self.kwargs['slug']
#            object = Quiz.objects.get(slug=slug, status = Quiz.LIVE_STATUS)
#
#        return render(request, 
#                      'vodkamartiniquiz/quiz_detail.html',
#                      {
#                        'object': object,
#                        'slug': slug,
#                        'greeting': self.greeting,
#                      },
#                      )

#class QuizCreate(View):
#    form_class = QuizForm
#    initial = {'title': 'Quiz X', 'body': 'This is all about X'}
#    template_name = 'vodkamartiniquiz/quiz_form.html'
#
#    def get(self, request, *args, **kwargs):
#        form = self.form_class(initial=self.initial)
#        return render(request, self.template_name, {'form': form})
#
#    def post(self, request, *args, **kwargs):
#        form = self.form_class(request.POST)
#        if form.is_valid():
#            # process form cleaned_data
#            quiz = form.save()
#            print quiz
#            #return HttpResponseRedirect(object.get_absolute_url())
#            return HttpResponseRedirect(reverse('vodkamartiniquiz_quiz_home'))
#        return render(request, self.template_name, {'form': form})
#
#class QuizCreate(FormView):
#    form_class = QuizForm
#    initial = {'title': 'Quiz X', 'body': 'This is all about X'}
#    template_name = 'vodkamartiniquiz/quiz_form.html'
#    success_url = reverse_lazy('vodkamartiniquiz_quiz_home') # use reverse_lazy because URLconf is not processed yet
#
#    def form_valid(self, form):
#        quiz = form.save()
#        print quiz
#        return super(QuizCreate, self).form_valid(form)
