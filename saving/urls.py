from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name="saving"),
    path('add-saving', views.add_saving, name="add-saving"),
    path('edit-saving/<int:id>', views.saving_edit, name="saving-edit"),
    path('delete-saving/<int:id>', views.delete_saving, name="delete-saving"),
    # path('search-saving', csrf_exempt(views.search_saving), name="search_saving"),
    # path('saving-summary', views.saving_summary, name="saving-summary"),
    # path('saving-stats', views.saving_stats_view, name="saving-stats"),
    # path('saving_csv', views.saving_csv, name="saving-csv")
]