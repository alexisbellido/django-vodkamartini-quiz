from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

def quiz_index(request, page=1):
    """
    Explain the purpose of this view.
    """

    # do something
    output = "A test for quiz app"
    return HttpResponse(output)
