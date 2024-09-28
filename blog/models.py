from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Blog(models.Model):

    title = models.CharField(max_length=100, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание статьи', **NULLABLE)
    image = models.ImageField(upload_to="blog/image", verbose_name='Изображение', **NULLABLE)
    views_counter = models.IntegerField(default=0, verbose_name='Количество просмотров')
    create_at = models.DateTimeField(auto_now=True, verbose_name='Дата публикации')

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
        ordering = ('title',)

    def __str__(self):
        return self.title
