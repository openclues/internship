from djoser.serializers import UserSerializer, TokenSerializer
from rest_framework import serializers
from rest_framework.response import Response

from users.models import Practise, PractiseSubmission, Student, Coordinator, CareerCenter


class PractiseSerializer(serializers.ModelSerializer):
    coordinator_name = serializers.CharField(source='coordinator.name', read_only=True)

    class Meta:
        model = Practise
        fields = "__all__"
        read_only_fields = ('coordinator_name',)

    def create(self, validated_data):
        user = self.context['request'].user
        coordinator = user.coordinator  # assuming Coordinator is a model with user as OneToOne field
        validated_data['coordinator'] = coordinator
        students_data = validated_data.pop('students', [])
        practise = Practise.objects.create(**validated_data)

        for student_data in students_data:
            student = Student.objects.get(pk=student_data)
            practise.students.add(student)

        return practise

    def update(self, instance, validated_data):
        user = self.context['request'].user
        coordinator = user.coordinator
        validated_data['coordinator'] = coordinator

        students_data = validated_data.pop('students', None)
        if students_data is not None:
            instance.students.clear()
            for student_id in students_data:
                student = Student.objects.get(pk=student_id)
                instance.students.add(student)

        # Update instance fields
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.form = validated_data.get('form', instance.form)
        instance.due_Time = validated_data.get('due_Time', instance.due_Time)
        instance.save()

        return instance


class PractiseSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PractiseSubmission
        fields = '__all__'


class UserAccountSerializer(UserSerializer):
    type = serializers.SerializerMethodField()
    practises = serializers.SerializerMethodField(read_only=True)

    class Meta(UserSerializer.Meta):
        fields = ("email", 'type', 'username', 'practises')

    def get_type(self, obj):
        if Student.objects.filter(user=obj.id).exists():
            return "Student"
        elif Coordinator.objects.filter(user=obj.id).exists():
            return "Coordinator"
        elif CareerCenter.objects.filter(user=obj.id).exists():
            return "Career Center"
        else:
            return "Admin"

    def get_practises(self, obj):
        if Student.objects.filter(user=obj.id).exists():
            practise = Practise.objects.filter(students__exact=obj.id)
            return Response(PractiseSerializer(practise, many=True).data).data
        elif Coordinator.objects.filter(user=obj.id).exists():
            practise = Practise.objects.filter(coordinator__exact=obj.id)
            return Response(PractiseSerializer(practise, many=True).data).data


# class AuthTokenSerizliesr(UserSerializer):
#     type = serializers.SerializerMethodField()
#
#     class Meta(UserSerializer.Meta):
#         fields = ("key", 'type')
#
#     def get_type(self, obj):


class AuthTokenSerizlier(TokenSerializer):
    def to_representation(self, instance):
        """
        Add additional data to the token response.
        """
        data = super().to_representation(instance)
        # Add user ID to the response
        data['user_id'] = instance.user.id

        if Student.objects.filter(user=instance.user.id).exists():
            data["type"] = "Student"
        elif Coordinator.objects.filter(user=instance.user.id).exists():
            data["type"] = "Coordinator"
        elif CareerCenter.objects.filter(user=instance.user.id).exists():
            data["type"] = "Career Center"
        else:
            data["type"] = "Admin"

        return data
