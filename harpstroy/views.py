from django.shortcuts import render
from django.core.mail import send_mail
from django.http import JsonResponse
from .models import (
    Testimonial, 
    Advantage, 
    FenceType, 
    GateType,
    SiteSettings,
    CalculatorAnswer,
    CalculatorQuestion,
    CalculatorSubmission,
)
import json
from django.views.decorators.csrf import csrf_exempt

def home(request):
    context = {
       'testimonials': Testimonial.objects.filter(is_active=True).exclude(video_file='').order_by('order'),
        'advantages': Advantage.objects.all().order_by('order'),
        'fence_types': FenceType.objects.all().order_by('order'),
        'gate_types': GateType.objects.all().order_by('order'),
        'site_settings': SiteSettings.objects.first()
    }
    return render(request, 'index.html', context)

def about(request):
    context = {
        'advantages': Advantage.objects.all().order_by('order'),
        'site_settings': SiteSettings.objects.first()
    }
    return render(request, 'about.html', context)

def price(request):
    context = {
        'fence_types': FenceType.objects.all().order_by('order'),
        'gate_types': GateType.objects.all().order_by('order'),
        'site_settings': SiteSettings.objects.first()
    }
    return render(request, 'price.html', context)

def contacts(request):
    context = {
        'site_settings': SiteSettings.objects.first()
    }
    return render(request, 'contacts.html', context)

def calculator_view(request):
    questions = CalculatorQuestion.objects.all().prefetch_related('answers')
    
    # Собираем данные для шаблона
    context = {
        'fence_type_answers': CalculatorAnswer.objects.filter(
            question__question_type='fence_type'
        ).order_by('order'),
        'height_answers': CalculatorAnswer.objects.filter(
            question__question_type='height_choice'
        ).order_by('order'),
        'gate_type_answers': CalculatorAnswer.objects.filter(
            question__question_type='gate_type'
        ).order_by('order'),
        'gate_count_answers': CalculatorAnswer.objects.filter(
            question__question_type='gate_count'
        ).order_by('order'),
        'installation_answers': CalculatorAnswer.objects.filter(
            question__question_type='installation'
        ).order_by('order'),
        'timing_answers': CalculatorAnswer.objects.filter(
            question__question_type='timing'
        ).order_by('order'),
        
        # Данные для слайдера длины
        'length_slider': CalculatorAnswer.objects.filter(
            question__question_type='length_slider'
        ).first()
    }
    
    return render(request, 'calculator_modal.html', context)

@csrf_exempt
def submit_calculator(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.POST.get('calculator_data', '{}'))
            
            submission = CalculatorSubmission(
                name=request.POST.get('name'),
                phone=request.POST.get('phone'),
                email=request.POST.get('email'),
                fence_type=data.get('fence_type', {}).get('text', ''),
                fence_length=int(data.get('fence_length', {}).get('value', 0)),
                height=data.get('height', {}).get('text', ''),
                gate_type=data.get('gate_type', {}).get('text', ''),
                gate_count=data.get('gate_count', {}).get('text', ''),
                installation=data.get('installation', {}).get('text', ''),
                timing=data.get('timing', {}).get('text', ''),
                location=data.get('location', {}).get('text', ''),
            )
            submission.save()
            
            # Отправка email
            subject = f'Новая заявка на расчет забора от {submission.name}'
            message = f'''
            Имя: {submission.name}
            Телефон: {submission.phone}
            Email: {submission.email if submission.email else "не указан"}
            
            Данные заказа:
            Тип ограждения: {submission.fence_type}
            Длина забора: {submission.fence_length} м
            Высота: {submission.height}
            Тип ворот: {submission.gate_type}
            Количество калиток: {submission.gate_count}
            Способ установки: {submission.installation}
            Сроки установки: {submission.timing}
            Населенный пункт: {submission.location}
            '''
            
            send_mail(
                subject,
                message,
                'noreply@yourdomain.com',
                ['sales@yourdomain.com'],
                fail_silently=False,
            )
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})

