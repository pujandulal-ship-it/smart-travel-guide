// Travel Guide JavaScript
document.addEventListener('DOMContentLoaded', function() {
    console.log('Travel Guide JS loaded!');
    
    const form = document.getElementById('travelForm');
    const resultsDiv = document.getElementById('results');
    const submitBtn = document.querySelector('button[type="submit"]');
    
    if (form) {
        // Form validation
        form.addEventListener('submit', function(e) {
            const destination = document.getElementById('destination').value.trim();
            const season = document.getElementById('season').value;
            
            if (!destination) {
                e.preventDefault();
                alert('Please enter a destination!');
                return false;
            }
            
            if (!season) {
                e.preventDefault();
                alert('Please select a season!');
                return false;
            }
            
            // Show loading state
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Getting Recommendations...';
            submitBtn.disabled = true;
            
            // Hide results until new submission
            if (resultsDiv) {
                resultsDiv.style.opacity = '0.5';
            }
        });
        
        // Reset button after form submission (if needed)
        form.addEventListener('submit', function() {
            setTimeout(() => {
                submitBtn.innerHTML = 'Get Recommendations';
                submitBtn.disabled = false;
            }, 2000);
        });
    }
    
    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Add fade-in animation for elements
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
            }
        });
    }, observerOptions);
    
    // Observe feature cards and other elements
    document.querySelectorAll('.feature-card, .step-card, .preview-card').forEach(el => {
        observer.observe(el);
    });
});