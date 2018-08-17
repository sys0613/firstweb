from django.shortcuts import render
from django.shortcuts import render,get_object_or_404
from .models import Question,Choice
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.http import Http404
from django.views import generic
from django.utils import timezone

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions.
        (not including those set to be
         published in the future)."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:9]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'



# def detail(request,question_id):
#     question=get_object_or_404(Question,pk=question_id)
#     return render(request,'polls/detail.html',{'question':question})
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


# def results(request,question_id):
#     question=get_object_or_404(Question,pk=question_id)
#     return render(request,'polls/results.html',{'question':question})

def vote(request,question_id):
    question=get_object_or_404(Question,pk=question_id)
    try:
        select_choice=question.choice_set.get(pk=request.POST['choice'])
    except(KeyError,Choice.DoesNotExist):
        return render(request,'polls/detail.html',{
            'question':question,
            'error_message':"You didn't select a choice.",
        })
    else:
        select_choice.votes+=1
        select_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
