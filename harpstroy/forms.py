from django import forms
from .models import Testimonial
from django.core.exceptions import ValidationError

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['name', 'video_file', 'thumbnail', 'order']
        
    def clean_video_file(self):
        video = self.cleaned_data.get('video_file')
        if video:
            if video.size > 25 * 1024 * 1024:  # 25MB limit
                raise ValidationError("Размер видео не должен превышать 25MB")
            return video