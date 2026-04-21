from django.urls import path
from .views import ContactView, NewsletterSubscribeView, NewsletterUnsubscribeView

urlpatterns = [
    path("",              ContactView.as_view()),
    path("newsletter/",   NewsletterSubscribeView.as_view()),
    path("unsubscribe/",  NewsletterUnsubscribeView.as_view()),
]
