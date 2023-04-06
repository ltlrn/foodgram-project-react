from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response


class RecipeActionsMixin:
    """Позволяет расширить вьюсет дополнительными методами,
    обобщающими повторяющуюся логику.
    """

    def action_function(self, request, model, pk):
        recipe = get_object_or_404(self.queryset, id=pk)
        serializer = self.add_serializer(recipe)
        queryset = model.objects.filter(
            Q(recipe__id=pk) & Q(user=request.user)
        )

        if (request.method == "POST") and not queryset:
            model.objects.create(recipe=recipe, user=request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if (request.method == "DELETE") and queryset:
            queryset[0].delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
