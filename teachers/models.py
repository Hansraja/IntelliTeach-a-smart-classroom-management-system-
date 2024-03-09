from django.db import models

# Create your models here.
class Assignment_Questions(models.Model):
    question = models.CharField(max_length=10000, blank=True, null=True)
    description = models.CharField(max_length=10000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    attechments = models.FileField(upload_to='assignment_questions/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'assignment_questions'

    def __str__(self):
        return self.question

class AssignMents(models.Model):
    teacher = models.ForeignKey('Admin.Faculty', on_delete=models.CASCADE, related_name='teacher_assignments', null=True, blank=True)
    title = models.CharField(max_length=500, blank=True, null=True)
    description = models.CharField(max_length=10000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField(blank=True, null=True)
    questions = models.ManyToManyField(Assignment_Questions, related_name='assignment_questions')
    attechments = models.FileField(upload_to='assignments/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'assignments'

    def __str__(self):
        return self.title
    
class Important_Topics(models.Model):
    teacher = models.ForeignKey('Admin.Faculty', on_delete=models.CASCADE, related_name='teacher_important_topics', null=True, blank=True)
    title = models.CharField(max_length=500, blank=True, null=True)
    description = models.CharField(max_length=10000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    attechments = models.FileField(upload_to='important_topics/', blank=True, null=True)

    class Meta:
        db_table = 'important_topics'

    def __str__(self):
        return self.title