from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Question, Choice

# Create your views here.
def index(request):
    latest_question_list = Question.objects.all()
    # return HttpResponse("Estás en la página principal de Premios Platzi App")
    # Ahora retornamos nuestra template
    return render(request, "polls/index.html", {
        "latest_question_list": latest_question_list
    })


def detail(request, question_id):
    # return HttpResponse(f"Estás viendo la pregunta número {question_id}")

    # question = Question.objects.get(pk=question_id)
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {
        "question": question
    })


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {
        "question": question
    })


# Generic View. equivalente al método index que es una function view
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """ Return the last five published questions """
        return Quetions.objects.order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

class ResultView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def vote(request, question_id):

    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html", {
                "question": question,
                "error_message": "No elegiste una respuesta"
            })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        #reverse es lo mimos que utilizar {% url en la parte de HTML%}
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
