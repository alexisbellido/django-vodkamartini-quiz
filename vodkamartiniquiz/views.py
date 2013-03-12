from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render, render_to_response, get_object_or_404
#from django.views.generic import TemplateView
from django.views.generic.base import View

class QuizHome(View):
    def get(self, request, *args, **kwargs):
        return render(request, 
                      'vodkamartiniquiz/quiz_list.html',
                      {
                        'object_list': ['a', 'b', 'c'],
                      },
                      )

class QuizDetail(View):
    greeting = 'Hola'

    def get(self, request, *args, **kwargs):
        print "kwargs", kwargs
        if 'slug' in self.kwargs:
            slug = self.kwargs['slug']

        return render(request, 
                      'vodkamartiniquiz/quiz_list.html',
                      {
                        'object_list': ['a', 'b', 'c'],
                        'slug': slug,
                        'greeting': self.greeting,
                      },
                      )


def quiz_index(request, page=1):
    """
    Explain the purpose of this view.
    """

    # do something
    output = "A test for quiz app"
    return HttpResponse(output)

def question_detail(request, pk):
    output = "Question %s for quiz" % pk
    return HttpResponse(output)
