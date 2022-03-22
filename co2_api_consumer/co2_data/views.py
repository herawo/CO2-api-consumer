from django.views.generic import ListView
from co2_data.models import CO2Data
from co2_data.models import CO2DataFrequency

class CO2DataListView(ListView):
    model = CO2Data
    template_name = "co2_data_table.html"

    def get_context_data(self, **kwargs):
        latests = self.model.objects.order_by('-date')[:20]
        context = super().get_context_data(**kwargs)
        context['latests'] = latests
        print('latest', latests)
        return context

class CO2DataFrequencyListView(ListView):
    model = CO2DataFrequency
    template_name = "co2_data_frequency_table.html"
    
    def get_context_data(self, **kwargs):
        times = self.model.objects.all().order_by('time').values('time').distinct()
        context = super().get_context_data(**kwargs)
        context['times'] = [time.get('time').strftime("%H-%M") for time in times]
        return context
    