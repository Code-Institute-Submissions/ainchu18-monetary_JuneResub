from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name="salary"),
    path('add-salary', views.add_salary, name="add-salary"),
    path('edit-salary/<int:id>', views.salary_edit, name="salary-edit"),
    path('delete-salary/<int:id>', views.delete_salary, name="delete-salary"),
    path('search-salary', csrf_exempt(views.search_salary), name="search_salary"),
#     path('salary-summary', views.salary_summary, name="salary-summary"),
#     path('salary-stats', views.salary_stats_view, name="salary-stats"),
#     path('salary_csv', views.salary_csv, name="salary-csv")
]