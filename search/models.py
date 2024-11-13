from django.db import models
from django.contrib.auth.models import User
from allClass.models import MyClass

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)  # Người dùng thực hiện tìm kiếm
    query = models.CharField(max_length=255,null=True,blank=True)  # Từ khóa tìm kiếm
    timestamp = models.DateTimeField(auto_now_add=True,null=True,blank=True)  # Thời gian tìm kiếm
    class_id=models.ForeignKey(MyClass, on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return f"{self.user.username} searched for '{self.query}' on {self.timestamp}"