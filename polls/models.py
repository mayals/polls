from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.conf import settings



class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False ,null=True)
    slug = models.SlugField(max_length=120, blank=True, null=True)
    polls_count = models.PositiveIntegerField(default=0, blank=True)
    
    def __str__(self):
        return self.name
 
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)      
        super().save(*args, **kwargs)
    
    
    def get_absolute_url(self):
        return reverse("polls:category-detail", args=[str(self.slug)])
         
    





class Poll(models.Model):
    class Status(models.TextChoices):
        DRAFT     = 'DR' , 'Draft'
        PUBLISHED = 'PB' , 'Published'
    
    category      = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='polls_category', null=True)
    poll_slug     = models.SlugField(max_length=120, blank=True,  null=True)
    poll_question = models.CharField(max_length=200, unique=True, blank=False, null=True)
    poll_user     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='polls_user')
    published_at  = models.DateTimeField(default=timezone.now) 
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)
    status        = models.CharField(max_length=2, choices=Status.choices, default=Status.PUBLISHED)
    poll_voters   = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True)
    poll_voters_count   = models.PositiveIntegerField(default=0, null=True, blank=True)
    
    def __str__(self):
        return self.poll_question

    def save(self, *args, **kwargs):    
        self.poll_slug = slugify(self.poll_question)
        super().save(*args,**kwargs)
    
    def get_absolute_url(self):
        # return reverse("blog:post-detail", args=[str(self.slug)])
        return reverse("polls:poll-detail", kwargs={"poll_slug": self.poll_slug,
                                                         "year": self.published_at.year,
                                                        "month":self.published_at.month,
                                                          "day":self.published_at.day})

    class Meta:
        verbose_name        = 'Poll'
        verbose_name_plural = 'Polls'



class Choice(models.Model):
    choice_poll         = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text         = models.CharField(max_length=200,blank=False)
    choice_votes_count  = models.IntegerField(default=0)
    choice_votes_users  = models.ManyToManyField(settings.AUTH_USER_MODEL)
    
    def __str__(self):
        return str(self.id)
    
    
