// HAMPR - Main JavaScript with Heavy Animations

document.addEventListener('DOMContentLoaded', () => {

    // Initialize AOS
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            easing: 'ease-out-cubic',
            once: true,
            offset: 50
        });
    }

    // 1. Hero Text Animations (Letter & Word Split)
    const splitText = (selector, type = 'letter') => {
        const elements = document.querySelectorAll(selector);
        elements.forEach(el => {
            const text = el.innerText;
            el.innerHTML = '';
            if (type === 'letter') {
                [...text].forEach((char, i) => {
                    const span = document.createElement('span');
                    span.innerText = char;
                    span.style.transitionDelay = `${i * 30}ms`;
                    el.appendChild(span);
                });
            } else {
                text.split(' ').forEach((word, i) => {
                    const span = document.createElement('span');
                    span.innerText = word + ' '; // Add space back
                    span.style.display = 'inline-block';
                    span.style.transitionDelay = `${i * 100}ms`;
                    el.appendChild(span);
                });
            }
            // Trigger animation after small delay
            setTimeout(() => {
                el.querySelectorAll('span').forEach(span => {
                    span.style.opacity = '1';
                    span.style.transform = 'translateY(0)';
                });
            }, 100);
        });
    };

    splitText('.letter-reveal-group', 'letter');
    splitText('.word-reveal-group', 'word');

    // 2. Intersection Observer for Scroll Animations
    const observerOptions = {
        threshold: 0.2, // Trigger when 20% visible
        rootMargin: "0px 0px -50px 0px"
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');

                // Trigger specific animations inside
                if (entry.target.querySelector('.counter')) {
                    startCounters(entry.target);
                }

                if (entry.target.classList.contains('letter-reveal-group-scroll')) {
                    splitText('.letter-reveal-group-scroll', 'letter');
                }

                observer.unobserve(entry.target); // Only animate once
            }
        });
    }, observerOptions);

    document.querySelectorAll('.animate-on-scroll, .section-header, .stat-box').forEach(el => {
        observer.observe(el);
    });

    // 3. Parallax Effect on Scroll
    window.addEventListener('scroll', () => {
        const scrolled = window.scrollY;

        document.querySelectorAll('.parallax-element').forEach(el => {
            const speed = el.getAttribute('data-speed') || 0.5;
            const yPos = -(scrolled * speed);
            // Apply transform to the image inside wrapper for smoother effect
            const img = el.querySelector('img');
            if (img) {
                img.style.transform = `translateY(${yPos * 0.2}px)`;
            } else {
                el.style.transform = `translateY(${yPos * 0.2}px)`;
            }
        });

        // Hero Parallax
        const heroBg = document.querySelector('.hero-image-wrapper');
        if (heroBg) {
            heroBg.style.transform = `translateY(${scrolled * 0.3}px)`;
        }
    });

    // 4. Number Counters (Anime.js)
    const startCounters = (container) => {
        const counters = container.querySelectorAll('.counter');
        counters.forEach(counter => {
            const target = +counter.getAttribute('data-target');
            const suffix = counter.getAttribute('data-suffix') || '';

            anime({
                targets: counter,
                innerHTML: [0, target],
                easing: 'easeOutExpo',
                round: 1, // No decimals
                duration: 2000,
                update: function (anim) {
                    counter.innerHTML = anim.animations[0].currentValue.toFixed(0) + suffix;
                }
            });
        });
    };

    // 5. 3D Tilt Effect on Hover
    document.addEventListener('mousemove', (e) => {
        const cards = document.querySelectorAll('.hover-3d');
        cards.forEach(card => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            // Only apply if mouse is near/over the card to save performance
            if (x > -50 && x < rect.width + 50 && y > -50 && y < rect.height + 50) {
                const xCenter = rect.width / 2;
                const yCenter = rect.height / 2;
                const rotateX = ((y - yCenter) / yCenter) * -5; // Max 5deg rotation
                const rotateY = ((x - xCenter) / xCenter) * 5;

                card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.02)`;
            } else {
                card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale(1)';
            }
        });
    });

    // 6. Navbar Transition
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('bg-white', 'shadow-sm', 'py-2');
            navbar.classList.remove('py-3');
        } else {
            navbar.classList.remove('bg-white', 'shadow-sm', 'py-2');
            navbar.classList.add('py-3');
        }
    });

    console.log('HAMPR Premium Animations Initialized');
});
