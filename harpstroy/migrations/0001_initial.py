# Generated by Django 5.2 on 2025-04-12 19:46

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Advantage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('description', models.TextField(verbose_name='Описание')),
                ('icon', models.CharField(help_text='Например: fas fa-check-circle', max_length=50, verbose_name='Иконка (класс Font Awesome)')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Порядок отображения')),
            ],
            options={
                'verbose_name': 'Преимущество',
                'verbose_name_plural': 'Преимущества',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='CalculatorQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_type', models.CharField(choices=[('fence_type', 'Тип ограждения'), ('length_slider', 'Длина забора (слайдер)'), ('height_choice', 'Высота забора'), ('gate_type', 'Тип ворот'), ('gate_count', 'Количество калиток'), ('installation', 'Способ установки'), ('timing', 'Сроки установки'), ('location', 'Населенный пункт')], max_length=20)),
                ('question_text', models.CharField(max_length=255)),
                ('order', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='CalculatorSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('fence_type', models.CharField(blank=True, max_length=100, null=True)),
                ('fence_length', models.IntegerField(blank=True, null=True)),
                ('height', models.CharField(blank=True, max_length=50, null=True)),
                ('gate_type', models.CharField(blank=True, max_length=100, null=True)),
                ('gate_count', models.CharField(blank=True, max_length=50, null=True)),
                ('installation', models.CharField(blank=True, max_length=100, null=True)),
                ('timing', models.CharField(blank=True, max_length=100, null=True)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Заявка с калькулятора',
                'verbose_name_plural': 'Заявки с калькулятора',
            },
        ),
        migrations.CreateModel(
            name='FenceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('image', models.ImageField(upload_to='fence_types/', verbose_name='Изображение')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Цена за м.п.')),
                ('features', models.TextField(blank=True, null=True, verbose_name='Особенности')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Порядок отображения')),
            ],
            options={
                'verbose_name': 'Тип ограждения',
                'verbose_name_plural': 'Типы ограждений',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='GateType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('gate_type', models.CharField(choices=[('swing', 'Распашные'), ('sliding', 'Откатные'), ('gate', 'Калитка')], max_length=20, verbose_name='Тип конструкции')),
                ('description', models.TextField(verbose_name='Описание')),
                ('image', models.ImageField(upload_to='gate_types/', verbose_name='Изображение')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Цена')),
                ('automation_possible', models.BooleanField(default=False, verbose_name='Возможна автоматизация')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Порядок отображения')),
            ],
            options={
                'verbose_name': 'Тип ворот/калитки',
                'verbose_name_plural': 'Типы ворот/калиток',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Заголовок')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='URL')),
                ('content', models.TextField(verbose_name='Содержание')),
                ('meta_title', models.CharField(blank=True, max_length=200, null=True, verbose_name='Мета-заголовок')),
                ('meta_description', models.TextField(blank=True, null=True, verbose_name='Мета-описание')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активная')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
            ],
            options={
                'verbose_name': 'Страница',
                'verbose_name_plural': 'Страницы',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(default='ХарпСтрой', max_length=100, verbose_name='Название сайта')),
                ('phone1', models.CharField(default='+7 (993) 020-40-20', max_length=20, verbose_name='Телефон 1')),
                ('phone2', models.CharField(default='+7 (383) 212-18-12', max_length=20, verbose_name='Телефон 2')),
                ('email', models.EmailField(default='2121812@list.ru', max_length=254, verbose_name='Email')),
                ('address', models.TextField(default='г. Новосибирск, ул. Толстого, д. 133, 4 этаж, офис 404', verbose_name='Адрес')),
                ('work_hours', models.CharField(default='Пн-Пт: 9:00-18:00, Сб: 10:00-15:00', max_length=100, verbose_name='Режим работы')),
                ('whatsapp_link', models.URLField(default='https://wa.me/79930204020', verbose_name='Ссылка на WhatsApp')),
                ('vk_link', models.URLField(blank=True, null=True, verbose_name='Ссылка на ВКонтакте')),
                ('telegram_link', models.URLField(blank=True, null=True, verbose_name='Ссылка на Telegram')),
                ('yandex_map_code', models.TextField(blank=True, null=True, verbose_name='Код карты Яндекса')),
            ],
            options={
                'verbose_name': 'Настройка сайта',
                'verbose_name_plural': 'Настройки сайта',
            },
        ),
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя клиента')),
                ('video_file', models.FileField(help_text='Поддерживаемые форматы: mp4, webm, ogg', upload_to='testimonials/videos/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp4', 'webm', 'ogg'])], verbose_name='Видеофайл')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='testimonials/thumbnails/', verbose_name='Превью видео')),
                ('text', models.TextField(blank=True, null=True, verbose_name='Текст отзыва')),
                ('rating', models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=5, verbose_name='Оценка')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Порядок отображения')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активный')),
            ],
            options={
                'verbose_name': 'Видеоотзыв',
                'verbose_name_plural': 'Видеоотзывы',
                'ordering': ['order', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='CalculatorAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.CharField(max_length=255)),
                ('image', models.ImageField(blank=True, null=True, upload_to='calculator/')),
                ('value', models.CharField(blank=True, max_length=100, null=True)),
                ('min_value', models.IntegerField(blank=True, null=True)),
                ('max_value', models.IntegerField(blank=True, null=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='harpstroy.calculatorquestion')),
            ],
            options={
                'verbose_name': 'Ответ калькулятора',
                'verbose_name_plural': 'Ответы калькулятора',
                'ordering': ['order'],
            },
        ),
    ]
