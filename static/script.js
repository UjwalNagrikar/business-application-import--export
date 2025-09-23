// Smooth scrolling for navigation links and active link highlighting
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            // Close mobile menu if open
            const navLinks = document.getElementById('navLinks');
            const mobileMenu = document.getElementById('mobileMenu');
            navLinks.classList.remove('active');
            mobileMenu.classList.remove('active');
            
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
            
            // Update active link
            updateActiveLink(this.getAttribute('href'));
        }
    });
});

// Update active navigation link
function updateActiveLink(targetHref) {
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    document.querySelector(`a[href="${targetHref}"]`).classList.add('active');
}

// Mobile menu toggle functionality
function toggleMobileMenu() {
    const navLinks = document.getElementById('navLinks');
    const mobileMenu = document.getElementById('mobileMenu');
    
    navLinks.classList.toggle('active');
    mobileMenu.classList.toggle('active');
}

// Close mobile menu when clicking outside
document.addEventListener('click', function(e) {
    const nav = document.querySelector('nav');
    const navLinks = document.getElementById('navLinks');
    const mobileMenu = document.getElementById('mobileMenu');
    
    if (!nav.contains(e.target)) {
        navLinks.classList.remove('active');
        mobileMenu.classList.remove('active');
    }
});

// Highlight active section on scroll
window.addEventListener('scroll', function() {
    const sections = document.querySelectorAll('section[id]');
    const scrollPos = window.scrollY + 100;
    
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.offsetHeight;
        const sectionId = section.getAttribute('id');
        
        if (scrollPos >= sectionTop && scrollPos < sectionTop + sectionHeight) {
            updateActiveLink(`#${sectionId}`);
        }
    });
});

// Form submission handler
document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.querySelector('.contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            // Validate form before submission
            if (!validateForm()) {
                e.preventDefault();
                alert('Please fill in all required fields correctly.');
                return;
            }
            
            // Let the form submit normally to Flask backend
            // The form will be processed by the /submit route
        });
    }
});

// Add scroll effect to header
window.addEventListener('scroll', function() {
    const header = document.querySelector('header');
    if (window.scrollY > 50) {
        header.style.background = 'rgba(44, 62, 80, 0.95)';
        header.style.backdropFilter = 'blur(10px)';
    } else {
        header.style.background = '#2c3e50';
        header.style.backdropFilter = 'none';
    }
});

// Initialize animations and set initial active link when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Set initial active link
    updateActiveLink('#home');
    
    // Animate navigation elements
    const navElements = document.querySelectorAll('nav .animate-on-load');
    navElements.forEach((element, index) => {
        setTimeout(() => {
            element.classList.add('visible');
        }, 100 + (index * 100));
    });
    
    // Animate service cards with staggered timing
    const serviceCards = document.querySelectorAll('.service-card.fade-in');
    serviceCards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.add('visible');
        }, 300 + (index * 150));
    });
    
    // Animate about image with slide-in-right
    const aboutImage = document.querySelector('.about-image.slide-in-right');
    if (aboutImage) {
        setTimeout(() => {
            aboutImage.classList.add('visible');
        }, 600);
    }
    
    // Animate contact form with slide-in-left
    const contactForm = document.querySelector('.contact-form.slide-in-left');
    if (contactForm) {
        setTimeout(() => {
            contactForm.classList.add('visible');
        }, 800);
    }
    
    // Animate any remaining elements
    const otherElements = document.querySelectorAll('.animate-on-load:not(.visible), .fade-in:not(.visible), .slide-in-left:not(.visible), .slide-in-right:not(.visible)');
    otherElements.forEach((element, index) => {
        setTimeout(() => {
            element.classList.add('visible');
        }, 1000 + (index * 100));
    });
});

// Mobile menu toggle (enhanced version)
function toggleMobileMenu() {
    const navLinks = document.querySelector('.nav-links');
    const mobileMenu = document.querySelector('.mobile-menu');
    navLinks.classList.toggle('active');
    mobileMenu.classList.toggle('active');
}

// Form validation
function validateForm() {
    const form = document.querySelector('.contact-form');
    const inputs = form.querySelectorAll('input[required], textarea[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.style.borderColor = '#dc3545';
            isValid = false;
        } else {
            input.style.borderColor = '#e9ecef';
        }
    });
    
    // Email validation
    const emailInput = document.querySelector('#email');
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (emailInput.value && !emailPattern.test(emailInput.value)) {
        emailInput.style.borderColor = '#dc3545';
        isValid = false;
    }
    
    return isValid;
}

// Add real-time form validation
document.addEventListener('DOMContentLoaded', () => {
    const formInputs = document.querySelectorAll('.contact-form input, .contact-form textarea');
    
    formInputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.hasAttribute('required') && !this.value.trim()) {
                this.style.borderColor = '#dc3545';
            } else {
                this.style.borderColor = '#e9ecef';
            }
        });
        
        input.addEventListener('input', function() {
            if (this.style.borderColor === 'rgb(220, 53, 69)') {
                this.style.borderColor = '#e9ecef';
            }
        });
    });
});

// Scroll to top functionality
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Show/hide scroll to top button
window.addEventListener('scroll', () => {
    const scrollButton = document.querySelector('.scroll-to-top');
    if (scrollButton) {
        if (window.scrollY > 300) {
            scrollButton.style.display = 'block';
        } else {
            scrollButton.style.display = 'none';
        }
    }
});

// Add loading animation for page
window.addEventListener('load', function() {
    // First make sure body is visible
    document.body.classList.add('loaded');
    
    // Hide loader after a delay
    setTimeout(function() {
        const loader = document.querySelector('.page-loader');
        if (loader) {
            loader.classList.add('hidden');
        }
        
        // Animate elements with animate-on-load class with staggered timing
        const navElements = document.querySelectorAll('nav .animate-on-load');
        navElements.forEach((element, index) => {
            setTimeout(() => {
                element.classList.add('visible');
            }, 300 + (index * 100));
        });
        
        // Animate service cards with more delay
        const serviceCards = document.querySelectorAll('.service-card.animate-on-load');
        serviceCards.forEach((card, index) => {
            setTimeout(() => {
                card.classList.add('visible');
            }, 800 + (index * 150));
        });
        
        // Animate about section
        const aboutElements = document.querySelectorAll('.about .animate-on-load');
        aboutElements.forEach((element, index) => {
            setTimeout(() => {
                element.classList.add('visible');
            }, 1200 + (index * 200));
        });
        
        // Animate contact section
        const contactElements = document.querySelectorAll('.contact .animate-on-load');
        contactElements.forEach((element, index) => {
            setTimeout(() => {
                element.classList.add('visible');
            }, 1500 + (index * 200));
        });
        
        // Animate any remaining elements
        const otherElements = document.querySelectorAll('.animate-on-load:not(.visible)');
        otherElements.forEach((element, index) => {
            setTimeout(() => {
                element.classList.add('visible');
            }, 1800 + (index * 100));
        });
    }, 1000); // Delay before hiding loader
});

// Lazy loading for images (if you add images later)
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}