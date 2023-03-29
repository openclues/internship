from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from users.models import Practise, Student
from users.permissions import IsCoordinator
from users.serializers import PractiseSerializer


class PractiseApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PractiseSerializer
    queryset = Practise.objects.all()

    def get_queryset(self):
        if Student.objects.get(user_id=self.request.user.id):
            return Practise.objects.filter(students__user_id=self.request.user.id)
        else:
            return Practise.objects.filter(coordinator=self.request.user.id)


class CreatePractiseApiView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsCoordinator]
    serializer_class = PractiseSerializer
    queryset = Practise.objects.all()


class ListPractiseApiView(generics.ListCreateAPIView):
    serializer_class = PractiseSerializer
    permission_classes = [IsAuthenticated, ]

    queryset = Practise.objects.all()

    def get_queryset(self):
        if Student.objects.get(user_id=self.request.user.id):
            return Practise.objects.filter(students__user_id=self.request.user.id)
        else:
            return Practise.objects.filter(coordinator__user_id=self.request.user.id)



