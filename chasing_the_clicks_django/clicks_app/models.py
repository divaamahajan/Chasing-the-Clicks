from django.db import models

# Create your models here.
class ClickCount(models.Model):
    geoLocation = models.CharField(max_length=255)
    count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Count: {self.count} at {self.created_at} from {self.geoLocation}"
    
    class Meta:
        app_label = None
