from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models
from django.utils.text import slugify

User = get_user_model()


def gen_slug(slug):
    new_slug = slugify(slug, allow_unicode=True)
    return new_slug


class SlugMixin(object):
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.slug)
        super().save(*args, **kwargs)


class Category(SlugMixin, models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Категории"
        verbose_name = "Категория"


class Genre(SlugMixin, models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Жанры"
        verbose_name = "Жанр"


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=400, blank=True)
    genre = models.ManyToManyField(Genre, verbose_name="Жанр")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Категория")

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField()
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    score = models.PositiveSmallIntegerField(validators=[
        validators.MinValueValidator(1, message='оценка не может быть меньше 1'),
        validators.MaxValueValidator(10, message='оценка не может быть больше 10'), ])
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True, db_index=True)


class Comment(models.Model):
    text = models.TextField()
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True, db_index=True)
