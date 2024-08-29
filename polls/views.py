from django.http import HttpResponse, Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.db.models import F


from polls.models import Question, Choice


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

# After voting in a question, we want vote view to redirect to the results of that question.
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # request.POST lets us access data by submitted key name (like a dict).
        # request.POST[choice] specifically, returns the ID of choice as a STRING.
        # request.POST ALWAYS returns a STRING.
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    # if choice wasn't provided in POST data, a KeyError is raised, which then
    # redisplays the question with a error message.
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        # Instructing the database to increment votes by 1
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        # The reverse function makes it so we don't have to hardcode a
        # URL in the view function. It would return the string
        # "/polls/3/results/".
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))