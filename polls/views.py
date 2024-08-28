from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.shortcuts import get_object_or_404

from polls.models import Question


# Views simply only need to do two things: return an HttpResponse or an Exception.

# Returns the last 5 questions, separated by commas, in ascending order of publication date.
def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    template = loader.get_template("polls/index.html")
    # Contexts are dictionaries - mapping template variable names to python objects
    context = {
        "latest_question_list": latest_question_list,
    }
    return HttpResponse(template.render(context, request))

# This does the same thing as the above method but just uses django shortcuts.
# The render() function takes the request object first, then template name, then a dict as 3rd optional final object.
#
# def index(request):
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     context = {"latest_question_list": latest_question_list}
#     return render(request, "polls/index.html", context)

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, "polls/detail.html", {"question":question})

# This does the same thing as the above method but just uses django shortcuts.
# The get_object_or_404() function takes a django model first and then x number of keyword arguments,
# which is then passed to the get() function. It raises a 404 if object doesn't exist.

def results(request, question_id):
    response = "Currently viewing results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
