from django.shortcuts import render
from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = "main/index.html"

class HelpView(TemplateView):
    template_name = "main/help.html"

class RulesView(TemplateView):
    template_name = "main/rules.html"

class ContactUsView(TemplateView):
    template_name = "main/contactus.html"

