from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=45)

    def __str__(self):
        return '%s' % self.name

class Board(models.Model):
    link = models.CharField(max_length=15)
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    defAnon = models.CharField(max_length=64, default="Anonymous")
    readOnly = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % self.link

class Thread(models.Model):
    title = models.CharField(max_length=64)
    updateTime = models.DateTimeField()
    postCount = models.IntegerField()
    closed = models.BooleanField(default=False)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)

    def __str__(self):
        return '%s/%s' % (str(self.board), str(self.title))

class Post(models.Model):
    number = models.CharField(max_length=3)
    name = models.CharField(max_length=64)
    text = models.CharField(max_length=15000)
    publishionTime = models.DateTimeField(auto_now_add=True)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    authorID = models.CharField(max_length=9)

    def __str__(self):
        return "%s/%s" % (str(self.thread), str(self.number))
