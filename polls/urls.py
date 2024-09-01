from django.urls import path

from . import views

## Views need to be mapped to the URLs. Once  you add views to views.py, add them in urlpatterns.

## We're adding namespaces to our URLconf so django can differentiate the URL names for all the
## applications, especially for something generic like {% url %}.
## When we do this, we're also going to have to change the templates involved.
app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    ##The angle brackets (<...>) captures that part of the URL and sends it as a keyword argument to the view.
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote")
]