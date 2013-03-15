from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.template import RequestContext
from django.shortcuts import render, render_to_response, get_object_or_404
from django.views.generic.base import View
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin

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

class QuestionDetail(FormView, SingleObjectMixin):
    """
    This should be a FormView actually, to show the question and radio buttons with possible answers.
    It should include the pk for the next question in this quiz.
    """

    form_class = QuestionForm
    initial = {'title': 'This is question', 'body': 'Question is'}
    template_name = 'vodkamartiniquiz/question_form.html'
    queryset = Question.objects.filter(enabled=True)

    def get_context_data(self, **kwargs):
        """
        Get the enabled questions order by weight for this quiz.
        TODO: get just the first question to start taking the quiz but only if user is authenticated, then the form comes.
        """
        context = super(QuestionDetail, self).get_context_data(**kwargs)
        context['object'] = self.get_object()
        context['quiz_slug'] = context['object'].quiz.slug
        # TODO get this question order to get the next one and that should be used as pk for building url action in form
        #context['first_question_id'] = self.object.getQuestionId(0)
        context['pk'] = context['object'].pk
        context['next_question_id'] = context['object'].getNextQuestionId()
        return context



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
