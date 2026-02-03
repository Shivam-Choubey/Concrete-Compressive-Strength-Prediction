// Form reset functionality
function resetForm() {
    const form = document.getElementById('prediction-form');
    if (form) {
        form.reset();
        showToast('Form has been reset to default values', 'info');
    }
}

// Toast notification system
function showToast(message, type = 'info') {
    // Remove existing toasts
    const existingToasts = document.querySelectorAll('.toast');
    existingToasts.forEach(toast => toast.remove());
    
    // Create new toast
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <div class="toast-content">
            <i class="fas fa-${getToastIcon(type)}"></i>
            <span>${message}</span>
        </div>
        <button onclick="this.parentElement.remove()">&times;</button>
    `;
    
    // Add styles
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${getToastColor(type)};
        color: white;
        padding: 15px 20px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 15px;
        min-width: 300px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(toast);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (toast.parentElement) {
            toast.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        }
    }, 5000);
}

function getToastIcon(type) {
    const icons = {
        'success': 'check-circle',
        'error': 'exclamation-circle',
        'warning': 'exclamation-triangle',
        'info': 'info-circle'
    };
    return icons[type] || 'info-circle';
}

function getToastColor(type) {
    const colors = {
        'success': 'linear-gradient(135deg, #48bb78 0%, #38a169 100%)',
        'error': 'linear-gradient(135deg, #f56565 0%, #c53030 100%)',
        'warning': 'linear-gradient(135deg, #ed8936 0%, #dd6b20 100%)',
        'info': 'linear-gradient(135deg, #4299e1 0%, #3182ce 100%)'
    };
    return colors[type] || colors.info;
}

// Add CSS animations for toast
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .toast-content {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .toast button {
        background: none;
        border: none;
        color: white;
        font-size: 1.5rem;
        cursor: pointer;
        opacity: 0.7;
        transition: opacity 0.3s;
    }
    
    .toast button:hover {
        opacity: 1;
    }
`;
document.head.appendChild(style);

// Input validation
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('prediction-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            let isValid = true;
            const inputs = form.querySelectorAll('input[type="number"]');
            
            inputs.forEach(input => {
                if (!input.value || parseFloat(input.value) < parseFloat(input.min)) {
                    isValid = false;
                    input.style.borderColor = '#fc8181';
                    input.style.boxShadow = '0 0 0 3px rgba(252, 129, 129, 0.1)';
                } else {
                    input.style.borderColor = '';
                    input.style.boxShadow = '';
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showToast('Please fill in all fields with valid values', 'error');
            }
        });
        
        // Add input validation on blur
        inputs = form.querySelectorAll('input[type="number"]');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                if (this.value && parseFloat(this.value) < parseFloat(this.min)) {
                    this.style.borderColor = '#fc8181';
                    showToast(`Value cannot be less than ${this.min}`, 'warning');
                }
            });
        });
    }
});

// Share result functionality
function shareResult() {
    if (navigator.share) {
        const strength = document.querySelector('.strength-value').textContent;
        navigator.share({
            title: 'Concrete Strength Prediction',
            text: `My concrete strength prediction: ${strength}`,
            url: window.location.href
        });
    } else {
        const text = `My concrete strength prediction: ${document.querySelector('.strength-value').textContent}`;
        navigator.clipboard.writeText(text).then(() => {
            showToast('Result copied to clipboard!', 'success');
        });
    }
}