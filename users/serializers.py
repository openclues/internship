from rest_framework import serializers
from rest_framework.response import Response

from users.models import Practise, PractiseSubmission, Student, Coordinator


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
