from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from .models import (
    Advantage,
    FenceType,
    GateType,
    Testimonial,
    CalculatorQuestion,
    CalculatorAnswer,
    CalculatorSubmission,
    Page,
    SiteSettings
)




@admin.register(Advantage)
class AdvantageAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'order')
    list_editable = ('order',)
    search_fields = ('title', 'description')

@admin.register(FenceType)
class FenceTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'order')
    list_editable = ('price', 'order')
    search_fields = ('name', 'description')
    prepopulated_fields = {'features': ('name',)}

@admin.register(GateType)
class GateTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'gate_type', 'price', 'automation_possible', 'order')
    list_editable = ('price', 'order', 'automation_possible')
    list_filter = ('gate_type', 'automation_possible')
    search_fields = ('name', 'description')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'video_preview', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    list_filter = ('rating', 'is_active')
    readonly_fields = ('video_preview',)
    
    def video_preview(self, obj):
        if obj.video_file:
            return mark_safe(
                f'<video width="320" controls><source src="{obj.video_file.url}"></video>'
            )
        return "Нет видео"
    video_preview.short_description = "Предпросмотр"


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_active')
    list_editable = ('is_active',)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'content')

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Разрешаем только одну запись настроек
        return not SiteSettings.objects.exists()
    
class CalculatorAnswerInline(admin.TabularInline):
    model = CalculatorAnswer
    extra = 1
    fields = ('answer_text', 'image', 'value', 'min_value', 'max_value', 'order')
    ordering = ('order',)

class CalculatorAnswerInline(admin.TabularInline):
    model = CalculatorAnswer
    extra = 1
    fields = ('answer_text', 'image', 'value', 'min_value', 'max_value',  'order')
    ordering = ('order',)

@admin.register(CalculatorQuestion)
class CalculatorQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_type', 'question_text', 'order')
    list_editable = ('order',)
    list_filter = ('question_type',)
    inlines = [CalculatorAnswerInline]
    ordering = ('order',)

@admin.register(CalculatorSubmission)
class FenceCalculatorSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'fence_type', 'fence_length', 'height', 'created_at')
    list_filter = ('fence_type', 'height', 'created_at')
    search_fields = ('name', 'phone', 'email', 'location')
    readonly_fields = ('created_at', 'formatted_data')
    fieldsets = (
        (None, {
            'fields': ('name', 'phone', 'email', 'created_at')
        }),
        ('Данные забора', {
            'fields': ('fence_type', 'fence_length', 'height', 'gate_type', 'gate_count', 
                      'installation', 'timing', 'location')
        }),
        ('Полные данные', {
            'fields': ('formatted_data',),
            'classes': ('collapse',)
        }),
    )
    
    def formatted_data(self, obj):
        return format_html(
            f"<strong>Тип ограждения:</strong> {obj.fence_type}<br>"
            f"<strong>Длина:</strong> {obj.fence_length} м<br>"
            f"<strong>Высота:</strong> {obj.height}<br>"
            f"<strong>Тип ворот:</strong> {obj.gate_type or 'не указано'}<br>"
            f"<strong>Калитки:</strong> {obj.gate_count or 'не указано'}<br>"
            f"<strong>Установка:</strong> {obj.installation}<br>"
            f"<strong>Сроки:</strong> {obj.timing}<br>"
            f"<strong>Местоположение:</strong> {obj.location}"
        )
    formatted_data.short_description = 'Полные данные'