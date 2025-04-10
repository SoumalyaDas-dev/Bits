// Main JavaScript for AI-Powered Local Business Booster

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all interactive elements
    initForm();
    initInfoCards();
    initAnimations();
    initCopyButtons();
});

/**
 * Initialize form with enhanced validation and animations
 */
function initForm() {
    const form = document.getElementById('business-form');
    if (!form) return;

    // Add input event listeners for real-time validation
    const inputs = form.querySelectorAll('input, textarea, select');
    inputs.forEach(input => {
        input.addEventListener('input', () => {
            validateField(input);
            if (input.validity.valid) {
                showSuccessState(input);
            }
        });

        input.addEventListener('blur', () => {
            validateField(input);
        });
    });

    // Form submission handler
    form.addEventListener('submit', async (event) => {
        if (!form.checkValidity()) {
            event.preventDefault();
            highlightInvalidFields(form);
            return;
        }

        // Show loading state
        const submitButton = form.querySelector('button[type="submit"]');
        submitButton.classList.add('loading');
        submitButton.disabled = true;

        try {
            // Let the form submit naturally to the server
            return true;
        } catch (error) {
            event.preventDefault();
            showToast('An error occurred. Please try again.', 'error');
            submitButton.classList.remove('loading');
            submitButton.disabled = false;
        }
    });
}

/**
 * Validate a single form field
 */
function validateField(input) {
    const errorMessage = input.parentElement.querySelector('.error-message');
    
    if (!input.validity.valid) {
        input.classList.add('invalid');
        input.classList.remove('valid');
        
        if (!errorMessage) {
            const error = document.createElement('div');
            error.className = 'error-message';
            error.textContent = getErrorMessage(input);
            input.parentElement.appendChild(error);
        }
    } else {
        input.classList.remove('invalid');
        if (errorMessage) {
            errorMessage.remove();
        }
    }
}

/**
 * Get appropriate error message for input
 */
function getErrorMessage(input) {
    if (input.validity.valueMissing) {
        return 'This field is required';
    }
    if (input.validity.tooShort) {
        return `Please enter at least ${input.minLength} characters`;
    }
    if (input.validity.tooLong) {
        return `Please enter no more than ${input.maxLength} characters`;
    }
    if (input.validity.typeMismatch) {
        return 'Please enter a valid value';
    }
    return input.validationMessage || 'Invalid input';
}

/**
 * Show success state for valid input
 */
function showSuccessState(input) {
    input.classList.add('valid');
    setTimeout(() => {
        input.classList.remove('valid');
    }, 2000);
}

/**
 * Initialize info cards with hover effects
 */
function initInfoCards() {
    const cards = document.querySelectorAll('.info-card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-5px)';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0)';
        });
    });
}

/**
 * Initialize animations for elements
 */
function initAnimations() {
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
    });
    
    animatedElements.forEach(element => {
        observer.observe(element);
    });
}

/**
 * Initialize copy to clipboard buttons
 */
function initCopyButtons() {
    const copyButtons = document.querySelectorAll('.btn-copy');
    
    copyButtons.forEach(button => {
        button.addEventListener('click', async () => {
            const content = button.dataset.content;
            try {
                await navigator.clipboard.writeText(content);
                showToast('Copied to clipboard!', 'success');
            } catch (err) {
                showToast('Failed to copy to clipboard', 'error');
            }
        });
    });
}

/**
 * Show toast notification
 */
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    // Trigger animation
    setTimeout(() => {
        toast.classList.add('show');
    }, 100);
    
    // Remove toast after animation
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 300);
    }, 3000);
}

/**
 * Highlight all invalid fields in form
 */
function highlightInvalidFields(form) {
    const invalidInputs = form.querySelectorAll(':invalid');
    
    invalidInputs.forEach(input => {
        input.classList.add('invalid');
        const errorMessage = input.parentElement.querySelector('.error-message');
        
        if (!errorMessage) {
            const error = document.createElement('div');
            error.className = 'error-message';
            error.textContent = getErrorMessage(input);
            input.parentElement.appendChild(error);
        }
    });
    
    // Scroll to first invalid input
    if (invalidInputs.length > 0) {
        invalidInputs[0].scrollIntoView({
            behavior: 'smooth',
            block: 'center'
        });
    }
}