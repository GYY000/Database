from django.db import models

class User(models.Model):
    uid = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30)
    register_date = models.DateField(auto_now_add=True)
    profile_photo = models.BinaryField(null=True, blank=True)

class Team(models.Model):
    tid = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=30, unique=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateField(auto_now_add=True)
    profile_photo = models.BinaryField()

class ReUserTeam(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    tid = models.ForeignKey(Team, on_delete=models.CASCADE)
    join_date = models.DateField(auto_now_add=True)
    is_admin = models.BooleanField()

    class Meta:
        unique_together = ('uid', 'tid')

class Question(models.Model):
    qid = models.AutoField(primary_key=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    qsid = models.ForeignKey('QuestionSet', on_delete=models.CASCADE)
    content = models.CharField(max_length=400)
    answer = models.CharField(max_length=400)
    score = models.FloatField()
    serial_num = models.IntegerField()

class QuestionSet(models.Model):
    qsid = models.AutoField(primary_key=True)
    set_name = models.CharField(max_length=30, unique=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)

class QuestionSetPerm(models.Model):
    id = models.AutoField(primary_key=True)
    qsid = models.ForeignKey(QuestionSet, on_delete=models.CASCADE)
    tid = models.ForeignKey(Team, on_delete=models.CASCADE)

class Exam(models.Model):
    eid = models.AutoField(primary_key=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    qsid = models.ForeignKey(QuestionSet, on_delete=models.CASCADE)
    exam_name = models.CharField(max_length=30, unique=True)
    start_time = models.DateTimeField()
    duration = models.DurationField()

class SetHistory(models.Model):
    shid = models.AutoField(primary_key=True)
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    qsid = models.ForeignKey(QuestionSet, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    score = models.FloatField()

class QuestionHistory(models.Model):
    qhid = models.AutoField(primary_key=True)
    shid = models.ForeignKey(SetHistory, on_delete=models.CASCADE)
    answer = models.CharField(max_length=400)
    score = models.FloatField()

class SensitiveWord(models.Model):
    word = models.CharField(max_length=30, primary_key=True)

class Message(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=300)

class Post(models.Model):
    pid = models.AutoField(primary_key=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    pid = models.ForeignKey(Post, on_delete=models.CASCADE)
