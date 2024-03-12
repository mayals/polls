from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.conf import settings


class Poll(models.Model):
    class Status(models.TextChoices):
        DRAFT     = 'DR' , 'Draft'
        PUBLISHED = 'PB' , 'Published'
    
    poll_slug     = models.SlugField(max_length=120, blank=True,  null=True)
    poll_question = models.CharField(max_length=200, blank=False, null=True)
    poll_user     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='polls_user')
    published_at  = models.DateTimeField(default=timezone.now) 
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)
    status        = models.CharField(max_length=2, choices=Status.choices, default=Status.PUBLISHED)
    
    

    def __str__(self):
        return self.poll_question

    def save(self, *args, **kwargs):    
        self.poll_slug = slugify(self.poll_question)
        super().save(*args, **kwargs)
    
    
    def get_absolute_url(self):
        # return reverse("blog:post-detail", args=[str(self.slug)])
        return reverse("polls:poll-detail", kwargs={"poll_slug": self.poll_slug,
                                                         "year": self.published_at.year,
                                                        "month":self.published_at.month,
                                                          "day":self.published_at.day})

    class Meta:
        verbose_name        = 'Poll'
        verbose_name_plural = 'Polls'
        unique_together     =['poll_question','published_at']




class Choice(models.Model):
    choice_poll        = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text        = models.CharField(max_length=200)
    choice_votes_count = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
