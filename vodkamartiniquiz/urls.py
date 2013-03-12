from django.conf.urls.defaults import patterns, url
from vodkamartiniquiz.views import QuizHome, QuizBasicDetail

urlpatterns = patterns('vodkamartiniquiz.views',
    url(r'^$', QuizHome.as_view(), name='vodkamartiniquiz_quiz_home'),
    url(r'^(?P<slug>[-\w]+)/$', QuizBasicDetail.as_view(), name='vodkamartiniquiz_quiz_detail'),
    #url(r'^question/(?P<pk>\d+)/$', 'question_detail', name='vodkamartiniquiz_question_detail'),
    #url(r'^question/(?P<pk>\d+)/$', 'question_detail', name='vodkamartiniquiz_question_detail'),
)
