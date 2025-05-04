from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Testimonial
import os
from PIL import Image
import ffmpeg
import tempfile

@receiver(post_save, sender=Testimonial)
def generate_video_thumbnail(sender, instance, **kwargs):
    if instance.video_file and not instance.thumbnail:
        try:
            # Создаем временный файл для превью
            temp_img = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
            
            # Используем ffmpeg для получения кадра из видео
            (
                ffmpeg
                .input(instance.video_file.path)
                .filter('scale', 320, -1)
                .output(temp_img.name, vframes=1, format='image2', vcodec='mjpeg')
                .run(capture_stdout=True, capture_stderr=True)
            )
            
            # Сохраняем превью
            instance.thumbnail.save(
                os.path.basename(temp_img.name),
                temp_img
            )
            instance.save()
            
            # Закрываем и удаляем временный файл
            temp_img.close()
            os.unlink(temp_img.name)
            
        except Exception as e:
            print(f"Error generating thumbnail: {e}")