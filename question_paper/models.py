import uuid
from django.db import models
from django.utils import timezone

class TestBatch(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    exam_name = models.CharField(max_length=255) # Fixed here
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return self.exam_name

class Question(models.Model):
    batch = models.ForeignKey(TestBatch, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    option_1 = models.CharField(max_length=255) # Fixed here
    option_2 = models.CharField(max_length=255) # Fixed here
    option_3 = models.CharField(max_length=255) # Fixed here
    option_4 = models.CharField(max_length=255) # Fixed here
    correct_answer = models.CharField(max_length=255) # Fixed here

    def __str__(self):
        return self.question_text[:50]

class StudentAttempt(models.Model):
    batch = models.ForeignKey(TestBatch, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=100) # Fixed here
    score = models.IntegerField()
    answers_data = models.JSONField() 
    attempted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_id} - {self.batch.exam_name}"