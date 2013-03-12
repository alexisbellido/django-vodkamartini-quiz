from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.template import RequestContext
from django.shortcuts import render, render_to_response, get_object_or_404
from django.views.generic.base import View
from django.views.generic import ListView
from django.views.generic.edit import FormView
from .models import Quiz
from .forms import QuizForm


class QuizHome(ListView):
    #model = Quiz
    queryset = Quiz.live.all()

    #def get_context_data(self, **kwargs):
    #    context = super(QuizHome, self).get_context_data(**kwargs)
    #    context['myvar'] = 'my variable goes here'
    #    return context

class QuizBasicDetail(View):
    greeting = 'Hola'

    def get(self, request, *args, **kwargs):
        if 'slug' in self.kwargs:
            slug = self.kwargs['slug']
            object = Quiz.objects.get(slug=slug, status = Quiz.LIVE_STATUS)

        return render(request, 
                      'vodkamartiniquiz/quiz_detail.html',
                      {
                        'object': object,
                        'slug': slug,
                        'greeting': self.greeting,
                      },
                      )

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
