from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('vodkamartiniquiz.views',
    url(r'^$', 'quiz_index', {'page': 1}, name='vodkamartiniquiz_home'),
    url(r'^question/(?P<pk>\d+)/$', 'question_detail', name='vodkamartiniquiz_question_detail'),
#    url(r'^page-(?P<page>\d+)/$', 'skeleton_index', name='vodkamartiniskeleton_index'),
#    url(r'^(?P<slug>[-\w]+)/$', 'skeleton_detail', name='vodkamartiniskeleton_detail'),
)
