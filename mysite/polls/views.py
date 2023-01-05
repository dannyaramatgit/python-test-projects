from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.views import generic,View
from django.utils import timezone
from .models import Question, Choice
from log_reg_app.models import LoginUser

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from rest_framework import status, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from  rest_framework import generics
from rest_framework.views import APIView
import datetime


from .serializers import QuestionSerializer, ChoiceSerializer
from .forms import NewQuestionForm, DeleteMessagesForm, UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def d_log_in(request):
    if request.method == 'POST':
        # u = User.objects.get(username='admin')
        # u.set_password('1234')
        # u.save()
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.get_short_name() is not None:
                request.session['username'] = user.get_short_name()
            else:
                request.session['username'] = user.get_username()
            return HttpResponseRedirect(reverse('polls:index'))
        else:
            msg = 'User not found'
            form = UserForm()
            return render(request, 'polls/login.html',{'form': form, 'msg': msg})
    else:
        form = UserForm()
        return render(request, 'polls/login.html',{'form': form})
        
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('polls:login'))

def add_new(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('polls:login'))
    d = datetime.timedelta
    form = NewQuestionForm()
    return render(request, 'polls/name.html', {'form': form})
  

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]
    
class DeleteMessages(View):
    template_name = 'polls/delete_messages.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('polls:login'))
        form = DeleteMessagesForm()
        return render(request, 'polls/delete_messages.html', {'form': form})

    
class DetailView(generic.DetailView):
    template_name = 'polls/detail.html'
    model = Question

class ResultsView(generic.DetailView):
    template_name = 'polls/results.html'
    model = Question

def list(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('polls:login'))

    questions = Question.objects.all()
    return HttpResponse(render(request,'polls/index.html',{'latest_question_list': questions, "username" : request.user.username}))
    

def detail(request, question_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('polls:login'))
    question = get_object_or_404(Question, pk=question_id)
    return HttpResponse(render(request,'polls/detail.html',{'question': question}))


def results(request, question_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('polls:login'))
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

    
def vote(request, question_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('polls:login'))
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])

    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes+=1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        


def new_q(request):
    form = NewQuestionForm(request.POST)
        # check whether it's valid:
    if form.is_valid():
        question_text = form.cleaned_data['question_text']
        pub_date = form.cleaned_data['pub_date']
        Question.objects.create(question_text=question_text, pub_date=pub_date)
    else:
        pass
    return HttpResponseRedirect(reverse('polls:index'))

def delete_question(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('polls:login'))
    if request.method == 'POST':
    
        form = DeleteMessagesForm(request.POST)
        if form.is_valid():
            q_for_delete=form.cleaned_data['questions']
            print("q_for_delete: ",q_for_delete)
            for q in q_for_delete:
                try:
                    question = get_object_or_404(Question, pk=q)
                    question.delete()
            
                except:
                    pass
            
   
    return HttpResponseRedirect(reverse('polls:index'))


# API

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

@api_view(['GET','POST'])
def question_list(request, format=None):
    """
    List all code questions, or create a new snippet.
    """
    if request.method == 'GET':
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = QuestionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','POST','PUT'])
@csrf_exempt
def question_detail(request, pk, format=None):
    """
    Retrieve, update or delete a question.
    """
    try:
        request.session['username']='DANNY'

        question = Question.objects.get(pk=pk)
    except Question.DoesNotExist:
        return Response(status=404)
    if request.method == 'GET':
        serializer = QuestionSerializer(question)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = QuestionSerializer(question, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class QuestionList(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

# class QuestionList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Question.objects.all()
#     serializer_class = QuestionSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)


#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# class QuestionDetail(mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin, APIView):
#     """
#     Retrieve, update or delete a snippet instance.
#     """
#     def get_object(self, pk):
#         try:
#             return Question.objects.get(pk=pk)
#         except Question.DoesNotExist:
#             raise Http404

#     def get(self, request, pk, format=None):
#         question = self.get_object(pk)
#         serializer = QuestionSerializer(question)
#         return Response(serializer.data)

#     def put(self, request, pk, format=None):
#         question = self.get_object(pk)
#         serializer = QuestionSerializer(question, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk, format=None):
#         question = self.get_object(pk)
#         question.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class ChoiceList(generics.ListCreateAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer


class ChoiceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'questions': reverse('questions', request=request, format=format),
        'choices': reverse('choices', request=request, format=format)
    })



from rest_framework import viewsets

class ChoiseViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer