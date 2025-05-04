document.addEventListener('DOMContentLoaded', function() {
  const steps = document.querySelectorAll('.calculator-step');
  const nextButtons = document.querySelectorAll('.next-step');
  const answerButtons = document.querySelectorAll('.answer-btn');
  const form = document.getElementById('calculatorForm');
  const slider = document.getElementById('fenceLengthSlider');
  const sliderValue = document.getElementById('fenceLengthValue');
  
  let currentStep = 1;
  let answers = {};
  
  // Инициализация слайдера
  if (slider) {
      slider.addEventListener('input', function() {
          sliderValue.textContent = this.value + ' м';
      });
  }
  
  // Обработка кнопок ответов
  answerButtons.forEach(button => {
      button.addEventListener('click', function() {
          // Удаляем выделение у всех кнопок в этой группе
          const question = this.getAttribute('data-question');
          document.querySelectorAll(`[data-question="${question}"]`).forEach(btn => {
              btn.classList.remove('active');
              btn.classList.remove('btn-primary');
              btn.classList.add('btn-outline-secondary');
          });
          
          // Добавляем выделение текущей кнопке
          this.classList.add('active');
          this.classList.add('btn-primary');
          this.classList.remove('btn-outline-secondary');
          
          // Сохраняем ответ
          answers[question] = this.getAttribute('data-value');
          
          // Автоматически переходим к следующему шагу, если это не слайдер
          if (question !== 'fence_length') {
              setTimeout(() => {
                  goToStep(currentStep + 1);
              }, 300);
          }
      });
  });
  
  // Обработка кнопок "Далее"
  nextButtons.forEach(button => {
      button.addEventListener('click', function() {
          // Для шага с длиной забора сохраняем значение слайдера
          if (currentStep === 2) {
              answers['fence_length'] = slider.value;
          }
          // Для шага с населенным пунктом сохраняем значение поля ввода
          if (currentStep === 8) {
              answers['location'] = document.getElementById('locationInput').value;
          }
          
          goToStep(currentStep + 1);
      });
  });
  
  // Функция перехода к шагу
  function goToStep(step) {
      // Скрываем текущий шаг
      document.querySelector(`.calculator-step[data-step="${currentStep}"]`).style.display = 'none';
      
      // Показываем новый шаг
      document.querySelector(`.calculator-step[data-step="${step}"]`).style.display = 'block';
      
      currentStep = step;
  }
  
  // Обработка формы
  if (form) {
      form.addEventListener('submit', function(e) {
          e.preventDefault();
          
          // Собираем все данные
          const formData = new FormData(form);
          const contactData = {};
          formData.forEach((value, key) => {
              contactData[key] = value;
          });
          
          // Объединяем с ответами
          const allData = {...answers, ...contactData};
          
          // Отправка данных на сервер
          fetch('/send-calculator-data', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
              },
              body: JSON.stringify(allData),
          })
          .then(response => response.json())
          .then(data => {
              goToStep('thank-you');
          })
          .catch(error => {
              console.error('Error:', error);
              alert('Произошла ошибка при отправке данных. Пожалуйста, попробуйте еще раз.');
          });
      });
  }
});