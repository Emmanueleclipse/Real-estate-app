# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import TemplateView

# Create your views here.
class SimulationMortgageView(TemplateView):
    template_name = "simulation-mortgage.html"

class SimulationCapitalGainsView(TemplateView):
    template_name = "simulation-capital-gains.html"

class SimulationSeasonalRentalView(TemplateView):
    template_name = "simulation-holiday-rental.html"

