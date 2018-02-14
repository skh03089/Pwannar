from django.db import models
from django.urls import reverse
from django.conf import settings


class Tag(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(
        max_length=30,
        verbose_name='동아리 이름'
    )
    content = models.TextField(verbose_name='동아리 소개')
    liker_set = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked_article_set',
    )
    number = models.CharField(
        max_length=30,
        verbose_name='모집 인원'
    )
    due = models.DateTimeField(
        verbose_name='마감 기한 #YYYY-MM-DD 형식으로 입력하세요.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='생성일자'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='최종수정일자'
    )
    tag = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return '{0}.{1}'.format(self.pk, self.title)

    def get_absolute_url(self):
        return reverse('core:board_detail', kwargs={'pk': self.pk, })


class Comment(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
