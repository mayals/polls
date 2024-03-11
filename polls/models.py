from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify



class Question(models.Model):
    slug          = models.SlugField(max_length=120, blank=True, null=True)
    question_text = models.CharField(max_length=200, blank=False, null=True)
    published_at  = models.DateTimeField(default=timezone.now) 

    def __str__(self):
        return self.question_text

    def save(self, *args, **kwargs):    
        self.slug = slugify(self.question_text)
        super().save(*args, **kwargs)
    
    
    def get_absolute_url(self):
        # return reverse("blog:post-detail", args=[str(self.slug)])
        return reverse("polls:question-detail", kwargs={"question_slug": self.slug,
                                                                  "year": self.published_at.year,
                                                                 "month":self.published_at.month,
                                                              "day":self.published_at.day})

    class Meta:
        verbose_name        = 'Question'
        verbose_name_plural = 'Questions'
        unique_together     =['question_text','published_at']







class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    choice_votes_count  = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
