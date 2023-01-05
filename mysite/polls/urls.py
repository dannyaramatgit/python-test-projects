from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = 'polls'
from .views import ChoiseViewSet
from rest_framework import renderers

choice_list = ChoiseViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

urlpatterns = [
    # path('', views.IndexView.as_view(), name='index'),
    path('index/', views.list, name='index'),
    path('', views.d_log_in, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('delete_question/', views.delete_question, name='delete_question'),
    path('delete_messages/', views.DeleteMessages.as_view(), name='delete_messages'),
    path('add_new/', views.add_new, name='add_new'),
    path('new-q/', views.new_q, name='new-q'),
    path('questions/', views.QuestionList.as_view()),
    path('questions/<int:pk>/', views.QuestionDetail.as_view()),
    path('choices/', choice_list),
    path('choices/<int:pk>/', views.ChoiceDetail.as_view(), name='choice'),
    path('api/', views.api_root),
]


# snippet_detail = SnippetViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy'
# })
urlpatterns = format_suffix_patterns(urlpatterns)
