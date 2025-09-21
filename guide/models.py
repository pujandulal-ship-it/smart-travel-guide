from django.db import models

class Destination(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class Season(models.Model):
    name = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return self.name

class Activity(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class TravelRecommendation(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    recommended_items = models.TextField()
    famous_places = models.TextField()
    recommended_apps = models.TextField()
    tips = models.TextField()
    
    class Meta:
        unique_together = ['destination', 'season', 'activity']
    
    def get_items_list(self):
        return [item.strip() for item in self.recommended_items.split(',')]
    
    def get_places_list(self):
        return [place.strip() for place in self.famous_places.split(',')]
    
    def get_apps_list(self):
        return [app.strip() for app in self.recommended_apps.split(',')]
    
    def get_tips_list(self):
        return [tip.strip() for tip in self.tips.split(',')]
    
    def __str__(self):
        return f"{self.destination} - {self.season} - {self.activity}"