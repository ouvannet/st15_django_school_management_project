from rest_framework import serializers
from project_1.models.teacher import Teacher

class TeacherSerializer(serializers.ModelSerializer):
    date_of_birth = serializers.DateField(format='%Y-%m-%d')
    photo = serializers.ImageField(use_url=True, allow_null=True)
    subject_id = serializers.IntegerField(source='subject_id.id', allow_null=True, default=None, read_only=True)
    subject_name = serializers.CharField(source='subject_id.subject_name', allow_null=True, default='N/A', read_only=True)

    class Meta:
        model = Teacher
        fields = ['id', 'first_name', 'last_name', 'gender', 'date_of_birth', 'address', 'salary', 'photo', 'subject_id', 'subject_name']