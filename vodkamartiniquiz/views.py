from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render, render_to_response, get_object_or_404
from django.views.generic.base import View
from django.views.generic import ListView
from vodkamartiniquiz.models import Quiz

class QuizHome(ListView):
    model = Quiz
    #def get(self, request, *args, **kwargs):
    #    return render(request, 
    #                  'vodkamartiniquiz/quiz_list.html',
    #                  {
    #                    'object_list': ['a', 'b', 'c'],
    #                  },
    #                  )

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

