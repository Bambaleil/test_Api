from django.contrib.auth.models import User
from django.http import Http404
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from product_app.models import Product, Lesson
from product_app.serializers import LessonSerializer, ProductSerializer


class CatalogView(TemplateView):
    model = Product
    template_name = "Catalog.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context_data = {
            "products": Product.objects.filter(user_id=user, archived=False),
            "users": User.objects.all(),
        }
        context.update(context_data)
        return context_data


class LessonListView(APIView):
    def get(self, request: Request) -> Response:
        user = self.request.user

        accessible_lessons = Lesson.objects.filter(products__user_id=user, archived=False)
        serialized_lessons = LessonSerializer(accessible_lessons, many=True)

        return Response(serialized_lessons.data, status=status.HTTP_200_OK)


class LessonDetailView(APIView):
    def get(self, request: Request, product_id: int) -> Response:
        user = self.request.user

        try:
            product = Product.objects.get(id=product_id, user_id=user)
            lessons = product.get_all_lesson()
            serialized_lessons = LessonSerializer(lessons, many=True)
        except Product.DoesNotExist:
            raise Http404("Продукт не найден")

        return Response(serialized_lessons.data, status=status.HTTP_200_OK)


class ProductStatsView(APIView):
    def get(self, request: Request) -> Response:
        products = Product.objects.all()

        stats = []
        for product in products:
            total_lessons_viewed = product.get_total_lessons_viewed()
            total_view_time = product.get_total_view_time()
            total_students = product.get_total_students()
            purchase_percentage = product.get_acquisition_percentage()

            stats.append({
                'id': product.id,
                'title': product.title,
                'description': product.description,
                'total_lessons_viewed': total_lessons_viewed,
                'total_view_time': total_view_time,
                'total_students': total_students,
                'purchase_percentage': purchase_percentage
            })

        serializer = ProductSerializer(stats, many=True)
        return Response(serializer.data)
