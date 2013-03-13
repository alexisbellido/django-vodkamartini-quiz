from django.conf.urls.defaults import patterns, url
from .views import QuizHome, QuizBasicDetail
from .views import QuizCreate

urlpatterns = patterns('vodkamartiniquiz.views',
    url(r'^$', QuizHome.as_view(), name='vodkamartiniquiz_quiz_home'),
    url(r'^add/$', QuizCreate.as_view(), name='vodkamartiniquiz_quiz_create'),
    url(r'^(?P<slug>[-\w]+)/$', QuizBasicDetail.as_view(), name='vodkamartiniquiz_quiz_detail'),
    #url(r'^question/(?P<pk>\d+)/$', 'question_detail', name='vodkamartiniquiz_question_detail'),
    #url(r'^question/(?P<pk>\d+)/$', 'question_detail', name='vodkamartiniquiz_question_detail'),
)
