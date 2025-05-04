$(document).ready(function() {
    // Инициализация карусели отзывов
    $('.testimonial-carousel').owlCarousel({
        loop: true,
        margin: 20,
        nav: true,
        responsive: {
            0: { items: 1 },
            768: { items: 2 },
            992: { items: 3 }
        }
    });

    // Обработка формы обратной связи
    $('#contactForm, #mainContactForm').submit(function(e) {
        e.preventDefault();
        var form = $(this);
        
        $.ajax({
            url: '/submit-contact-form/',
            type: 'POST',
            data: form.serialize(),
            headers: {
                'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function(response) {
                if (response.success) {
                    alert('Спасибо за заявку! Мы свяжемся с вами в ближайшее время.');
                    form[0].reset();
                } else {
                    alert('Произошла ошибка. Пожалуйста, попробуйте еще раз.');
                }
            },
            error: function() {
                alert('Произошла ошибка. Пожалуйста, попробуйте еще раз.');
            }
        });
    });

    // Плавная прокрутка для якорных ссылок
    $('a[href^="#"]').on('click', function(event) {
        event.preventDefault();
        $('html, body').animate({
            scrollTop: $($(this).attr('href')).offset().top - 70
        }, 500);
    });
});

// Анимация при скролле
function animateOnScroll() {
    const elements = document.querySelectorAll('.advantage-card, .fence-card');
    
    elements.forEach(element => {
        const elementPosition = element.getBoundingClientRect().top;
        const screenPosition = window.innerHeight / 1.2;
        
        if (elementPosition < screenPosition) {
            element.style.animation = `fadeInUp 0.6s forwards`;
        }
    });
}

// Запуск при загрузке и скролле
window.addEventListener('load', animateOnScroll);
window.addEventListener('scroll', animateOnScroll);

// Инициализация карусели отзывов
$('.testimonial-carousel').owlCarousel({
    loop: true,
    margin: 20,
    nav: true,
    dots: true,
    autoplay: true,
    autoplayTimeout: 5000,
    autoplayHoverPause: true,
    responsive: {
        0: {
            items: 1
        },
        768: {
            items: 2
        },
        992: {
            items: 3
        }
    },
    onInitialized: function() {
        
        $('.testimonial-item').each(function(index) {
            $(this).css({
                'animation-delay': (index * 0.2) + 's'
            });
        });
    }
});

$(window).scroll(function() {
    if ($(this).scrollTop() > 50) {
        $('.header').addClass('scrolled');
    } else {
        $('.header').removeClass('scrolled');
    }
});

// Плавная прокрутка с учетом высоты шапки
$('.nav-link').on('click', function(e) {
    if (this.hash !== '') {
        e.preventDefault();
        const hash = this.hash;
        const headerHeight = $('.header').outerHeight();
        $('html, body').animate({
            scrollTop: $(hash).offset().top - headerHeight + 10
        }, 800);
        $('.navbar-collapse').collapse('hide');
    }
});