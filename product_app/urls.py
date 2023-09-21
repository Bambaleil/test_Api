from django.urls import path

from product_app.views import CatalogView, LessonListView, LessonDetailView, ProductStatsView

app_name = "product_app"

urlpatterns = [
    path("catalog/", CatalogView.as_view(), name="catalog"),
    path("lesson_api/", LessonListView.as_view(), name="lesson_api"),
    path("lesson_detail/<int:product_id>/", LessonDetailView.as_view(), name="lesson_detail"),
    path('product_stats/', ProductStatsView.as_view(), name='product_stats'),
]
