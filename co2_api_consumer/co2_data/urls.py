from django.urls import path
from co2_data.views import CO2DataListView
from co2_data.views import CO2DataFrequencyListView

urlpatterns = [
    path('table/', CO2DataListView.as_view()),
    path('table_frequency/', CO2DataFrequencyListView.as_view()),
]