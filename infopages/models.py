from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.utils.html import strip_tags


class KCat(models.Model):
    title = models.CharField('Название', max_length=100)
    description = models.TextField('Описание', blank=True)
    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Kurse(models.Model):
    title = models.CharField('Название', max_length=100)
    shortdesc = models.TextField('Краткое описание', blank=True, max_length=200)
    description = RichTextUploadingField('Описание', blank=True)
    image = models.ImageField('Изображение', blank=True, upload_to='images')
    catid = models.ForeignKey(KCat, verbose_name='Категория', related_name='catid', on_delete=models.CASCADE,
                              default=None)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'
    objects = models.Manager()


class Nazn(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь',  on_delete=models.CASCADE)
    kurse = models.ManyToManyField(Kurse, related_name='kurse', verbose_name='Доступные модули')
    objects = models.Manager()

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'Назначение'
        verbose_name_plural = 'Назначения'


class Step(models.Model):
    order_number = models.DecimalField('№', max_digits=2, decimal_places=0, default=0)
    title = models.CharField('Название', max_length=150)
    kurseid = models.ForeignKey(Kurse, verbose_name='Модуль', related_name='kurseid', on_delete=models.CASCADE)
    text = RichTextUploadingField('Текст', blank=True, null=True)
    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Question(models.Model):
    kursid = models.ForeignKey(Kurse, related_name='kurs', verbose_name='Модуль', on_delete=models.CASCADE)
    stepid = models.ForeignKey(Step, related_name='stepid', verbose_name='Урок', on_delete=models.CASCADE)
    question = RichTextUploadingField('Текст вопроса', blank=True, null=True)
    objects = models.Manager()

    def __str__(self):
        return strip_tags(self.question)

    class Meta:
        verbose_name = ' Вопрос'
        verbose_name_plural = ' Вопросы'


class Answer(models.Model):
    questionid = models.ForeignKey(Question, related_name='questionid', verbose_name='Вопрос', on_delete=models.CASCADE)
    answer = models.CharField('Ответ', max_length=100)
    is_correct = models.BooleanField('Верный ответ', default=False)
    objects = models.Manager()

    def __str__(self):
        return self.answer

    class Meta:
        verbose_name = ' Ответ'
        verbose_name_plural = ' Ответы'


class Results(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, editable=False)
    kurseid = models.DecimalField('Номер модуля', max_digits=5, decimal_places=0, default=0, editable=False)
    result_int = models.DecimalField('Баллы', max_digits=3, decimal_places=0, default=0, editable=False)
    objects = models.Manager()

    def __str__(self):
        kurstitle = Kurse.objects.get(id=self.kurseid)
        a = str(self.user) + ': ' + str(kurstitle) + ' - ' + str(self.result_int) + ' баллов'
        return a

    class Meta:
        verbose_name = 'Результат'
        verbose_name_plural = 'Результаты'


class Zadanie(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь',  on_delete=models.CASCADE)
    text = RichTextUploadingField('Текст задания', blank=True, null=True)
    vipolnen = models.BooleanField('Выполнено успешно', default=False)
    objects = models.Manager()

    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'