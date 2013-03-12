from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render, render_to_response, get_object_or_404
from django.views.generic import TemplateView

class QuizHome(TemplateView):
    template_name = 'vodkamartiniquiz/quiz_list.html'

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
