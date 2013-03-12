from django.conf.urls.defaults import patterns, include, url
from vodkamartiniquiz.views import QuizHome, QuizDetail

urlpatterns = patterns('vodkamartiniquiz.views',
    #url(r'^$', 'quiz_index', {'page': 1}, name='vodkamartiniquiz_home'),
    url(r'^$', QuizHome.as_view(), name='vodkamartiniquiz_home'),
    url(r'^(?P<slug>[-\w]+)/$', QuizDetail.as_view(), name='vodkamartiniquiz_quiz_detail'),
    #url(r'^question/(?P<pk>\d+)/$', 'question_detail', name='vodkamartiniquiz_question_detail'),
    #url(r'^question/(?P<pk>\d+)/$', 'question_detail', name='vodkamartiniquiz_question_detail'),
#    url(r'^page-(?P<page>\d+)/$', 'skeleton_index', name='vodkamartiniskeleton_index'),
)
