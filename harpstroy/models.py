from django.db import models
from django.core.validators import MinValueValidator, FileExtensionValidator
from django.urls import reverse


class Advantage(models.Model):
    """Модель преимуществ компании"""
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    icon = models.CharField(
        max_length=50, 
        verbose_name="Иконка (класс Font Awesome)",
        help_text="Например: fas fa-check-circle"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок отображения"
    )

    class Meta:
        verbose_name = "Преимущество"
        verbose_name_plural = "Преимущества"
        ordering = ['order']

    def __str__(self):
        return self.title

class FenceType(models.Model):
    """Модель типов ограждений"""
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(
        upload_to='fence_types/',
        verbose_name="Изображение"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена за м.п.",
        validators=[MinValueValidator(0)]
    )
    features = models.TextField(
        verbose_name="Особенности",
        blank=True,
        null=True
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок отображения"
    )

    class Meta:
        verbose_name = "Тип ограждения"
        verbose_name_plural = "Типы ограждений"
        ordering = ['order']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('fence_type_detail', kwargs={'pk': self.pk})

class GateType(models.Model):
    """Модель типов ворот и калиток"""
    GATE_CHOICES = [
        ('swing', 'Распашные'),
        ('sliding', 'Откатные'),
        ('gate', 'Калитка'),
    ]

    name = models.CharField(max_length=100, verbose_name="Название")
    gate_type = models.CharField(
        max_length=20,
        choices=GATE_CHOICES,
        verbose_name="Тип конструкции"
    )
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(
        upload_to='gate_types/',
        verbose_name="Изображение"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
        validators=[MinValueValidator(0)]
    )
    automation_possible = models.BooleanField(
        default=False,
        verbose_name="Возможна автоматизация"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок отображения"
    )

    class Meta:
        verbose_name = "Тип ворот/калитки"
        verbose_name_plural = "Типы ворот/калиток"
        ordering = ['order']

    def __str__(self):
        return f"{self.get_gate_type_display()} - {self.name}"

class Testimonial(models.Model):
    """Модель видеоотзывов"""
    name = models.CharField(max_length=100, verbose_name="Имя клиента")
    video_file = models.FileField(
        upload_to='testimonials/videos/',
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'webm', 'ogg'])],
        verbose_name="Видеофайл",
        help_text="Поддерживаемые форматы: mp4, webm, ogg"
    )
    thumbnail = models.ImageField(
        upload_to='testimonials/thumbnails/',
        null=True,
        blank=True,
        verbose_name="Превью видео"
    )
    text = models.TextField(
        verbose_name="Текст отзыва",
        blank=True,
        null=True
    )
    rating = models.PositiveSmallIntegerField(
        choices=[(i, i) for i in range(1, 6)],
        verbose_name="Оценка",
        default=5
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок отображения"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активный"
    )

    class Meta:
        verbose_name = "Видеоотзыв"
        verbose_name_plural = "Видеоотзывы"
        ordering = ['order', '-created_at']

    def get_thumbnail_url(self):
        if self.thumbnail and hasattr(self.thumbnail, 'url'):
            return self.thumbnail.url
        return ''  
    
    def __str__(self):
        return self.name

class CalculatorQuestion(models.Model):
    QUESTION_TYPES = [
        ('fence_type', 'Тип ограждения'),
        ('length_slider', 'Длина забора (слайдер)'),
        ('height_choice', 'Высота забора'),
        ('gate_type', 'Тип ворот'),
        ('gate_count', 'Количество калиток'),
        ('installation', 'Способ установки'),
        ('timing', 'Сроки установки'),
        ('location', 'Населенный пункт'),
    ]
    
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    question_text = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)
class CalculatorAnswer(models.Model):
    question = models.ForeignKey(CalculatorQuestion, on_delete=models.CASCADE, related_name='answers')
    answer_text = models.CharField(max_length=255)
    image = models.ImageField(upload_to='calculator/', blank=True, null=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    min_value = models.IntegerField(blank=True, null=True)  # Для слайдера
    max_value = models.IntegerField(blank=True, null=True)  # Для слайдера
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Ответ калькулятора'
        verbose_name_plural = 'Ответы калькулятора'

    def __str__(self):
        return f"{self.question.question_text} - {self.answer_text}"

class CalculatorSubmission(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    fence_type = models.CharField(max_length=100, blank=True, null=True)
    fence_length = models.IntegerField(blank=True, null=True)
    height = models.CharField(max_length=50, blank=True, null=True)
    gate_type = models.CharField(max_length=100, blank=True, null=True)
    gate_count = models.CharField(max_length=50, blank=True, null=True)
    installation = models.CharField(max_length=100, blank=True, null=True)
    timing = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Заявка с калькулятора'
        verbose_name_plural = 'Заявки с калькулятора'

    def __str__(self):
        return f"Заявка от {self.name} ({self.created_at})"

class Page(models.Model):
    """Модель статических страниц"""
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="URL"
    )
    content = models.TextField(verbose_name="Содержание")
    meta_title = models.CharField(
        max_length=200,
        verbose_name="Мета-заголовок",
        blank=True,
        null=True
    )
    meta_description = models.TextField(
        verbose_name="Мета-описание",
        blank=True,
        null=True
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активная"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )

    class Meta:
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('page_detail', kwargs={'slug': self.slug})

class SiteSettings(models.Model):
    """Модель настроек сайта"""
    site_name = models.CharField(
        max_length=100,
        default="ХарпСтрой",
        verbose_name="Название сайта"
    )
    phone1 = models.CharField(
        max_length=20,
        default="+7 (993) 020-40-20",
        verbose_name="Телефон 1"
    )
    phone2 = models.CharField(
        max_length=20,
        default="+7 (383) 212-18-12",
        verbose_name="Телефон 2"
    )
    email = models.EmailField(
        default="2121812@list.ru",
        verbose_name="Email"
    )
    address = models.TextField(
        default="г. Новосибирск, ул. Толстого, д. 133, 4 этаж, офис 404",
        verbose_name="Адрес"
    )
    work_hours = models.CharField(
        max_length=100,
        default="Пн-Пт: 9:00-18:00, Сб: 10:00-15:00",
        verbose_name="Режим работы"
    )
    whatsapp_link = models.URLField(
        default="https://wa.me/79930204020",
        verbose_name="Ссылка на WhatsApp"
    )
    vk_link = models.URLField(
        blank=True,
        null=True,
        verbose_name="Ссылка на ВКонтакте"
    )
    telegram_link = models.URLField(
        blank=True,
        null=True,
        verbose_name="Ссылка на Telegram"
    )
    yandex_map_code = models.TextField(
        blank=True,
        null=True,
        verbose_name="Код карты Яндекса"
    )

    class Meta:
        verbose_name = "Настройка сайта"
        verbose_name_plural = "Настройки сайта"

    def __str__(self):
        return "Настройки сайта"

    def save(self, *args, **kwargs):
        # Разрешаем только одну запись настроек
        self.__class__.objects.exclude(id=self.id).delete()
        super().save(*args, **kwargs)

   