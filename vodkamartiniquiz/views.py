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

from .models import Quiz, Question
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
    TODO This view should be just for authenticated users. Use django-braces mixin here.
    """

    form_class = QuestionForm
    template_name = 'vodkamartiniquiz/question_form.html'
    queryset = Question.objects.filter(enabled=True)

    def get_initial(self):
        return {'question': self.get_object(), 'user': self.request.user}

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
        # TODO form.save() should return something to be used later in this method
        # and that something will indicate where to redirect next
        result = form.save()
        # TODO, change success_url to move to next question or to results
        self.success_url = '/quiz/quiz-2/question/41/'
        messages.info(self.request, 'Question answered.')
        return super(QuestionDetail, self).form_valid(form)

    #def form_invalid(self, form):
    #    messages.info(self.request, 'Submission problem, please try again.')
    #    return super(QuestionDetail, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        """
        Get the next enabled question for the quiz this question belongs to.
        """
        context = super(QuestionDetail, self).get_context_data(**kwargs)
        context['object'] = self.get_object()
        context['quiz_slug'] = context['object'].quiz.slug
        self.pk = context['object'].pk
        context['pk'] = self.pk
        self.question_pk_list = context['object'].getQuestionsPkList()
        context['question_pk_list'] = self.question_pk_list
        context['num_questions'] = len(self.question_pk_list)
        context['num_current_question'] = self.question_pk_list.index(self.pk) + 1
        context['next_question_id'] = self.getQuestionNextPk()
        context['previous_question_id'] = self.getQuestionPreviousPk()
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
