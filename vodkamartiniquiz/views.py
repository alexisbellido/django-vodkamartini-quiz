from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.template import RequestContext
from django.shortcuts import render, render_to_response, get_object_or_404
from django.views.generic.base import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from .models import Quiz
from .forms import QuizForm


class QuizHome(ListView):
    """
    Show live quizzes. We can use either a model or a queryset attribute.
    If provided, the value of queryset supersedes the value provided for model.
    Using model = Quiz is just a shorthand for queryset = Quiz.objects.all()
    In this case we want just live quizzes so we use that manager.
    """

    queryset = Quiz.live.all()
    paginate_by = 2

class QuizBasicDetail(DetailView):
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
        context = super(QuizBasicDetail, self).get_context_data(**kwargs)
        context['question_list'] = self.object.question_set.filter(enabled=True).order_by('weight')
        return context

    #def get_object(self):
    #    """
    #    We could do something more with the object here
    #    """
    #    object = super(QuizBasicDetail, self).get_object()
    #    return object


#class QuizBasicDetail(View):
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

class QuizCreate(FormView):
    form_class = QuizForm
    initial = {'title': 'Quiz X', 'body': 'This is all about X'}
    template_name = 'vodkamartiniquiz/quiz_form.html'
    success_url = reverse_lazy('vodkamartiniquiz_quiz_home') # use reverse_lazy because URLconf is not processed yet

    def form_valid(self, form):
        quiz = form.save()
        print quiz
        return super(QuizCreate, self).form_valid(form)
