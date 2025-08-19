
// Main JavaScript functionality for AI Research Assistant
console.log('Main.js loaded successfully');

document.addEventListener('DOMContentLoaded', function() {
    console.log('Main.js DOM ready');
    
    // Initialize tooltips if Bootstrap is available
    if (typeof bootstrap !== 'undefined') {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    // Smooth scroll for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
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

    // Add loading states to download buttons
    const downloadButtons = document.querySelectorAll('.btn[href*="download"]');
    downloadButtons.forEach(button => {
        button.addEventListener('click', function() {
            const originalText = this.innerHTML;
            this.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Downloading...';
            this.disabled = true;
            
            // Re-enable after download starts (3 seconds)
            setTimeout(() => {
                this.innerHTML = originalText;
                this.disabled = false;
            }, 3000);
        });
    });

    // Auto-resize textareas
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        // Initial resize
        autoResize(textarea);
        
        // Resize on input
        textarea.addEventListener('input', function() {
            autoResize(this);
        });
    });

    // Add copy functionality to code blocks and pre elements
    const codeBlocks = document.querySelectorAll('pre, code');
    codeBlocks.forEach(block => {
        if (block.textContent.length > 50) {
            // Only add copy button to larger code blocks
            const wrapper = document.createElement('div');
            wrapper.style.position = 'relative';
            
            const copyBtn = document.createElement('button');
            copyBtn.innerHTML = '<i class="fas fa-copy"></i>';
            copyBtn.className = 'btn btn-sm btn-outline-secondary copy-btn';
            copyBtn.style.position = 'absolute';
            copyBtn.style.top = '10px';
            copyBtn.style.right = '10px';
            copyBtn.style.zIndex = '10';
            copyBtn.title = 'Copy to clipboard';
            
            // Wrap the block and add button
            block.parentNode.insertBefore(wrapper, block);
            wrapper.appendChild(block);
            wrapper.appendChild(copyBtn);
            
            copyBtn.addEventListener('click', () => {
                copyToClipboard(block.textContent);
                copyBtn.innerHTML = '<i class="fas fa-check"></i>';
                copyBtn.style.color = '#28a745';
                
                setTimeout(() => {
                    copyBtn.innerHTML = '<i class="fas fa-copy"></i>';
                    copyBtn.style.color = '';
                }, 2000);
            });
        }
    });

    // Add fade-in animation to elements
    const animatedElements = document.querySelectorAll('.feature-card, .research-card, .progress-card');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    });

    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });

    // Initialize research form if it exists
    initializeResearchForm();
    
    // Initialize report formatting
    formatReportContent();
});

// Auto-resize textarea function
function autoResize(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 300) + 'px';
}

// Copy to clipboard function
async function copyToClipboard(text) {
    try {
        if (navigator.clipboard && window.isSecureContext) {
            await navigator.clipboard.writeText(text);
        } else {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
        }
        showNotification('Copied to clipboard!', 'success');
    } catch (err) {
        console.error('Failed to copy text: ', err);
        showNotification('Failed to copy text', 'error');
    }
}

// Show notification function
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotifications = document.querySelectorAll('.toast-notification');
    existingNotifications.forEach(notification => notification.remove());
    
    const notification = document.createElement('div');
    notification.className = `alert alert-${type === 'error' ? 'danger' : type === 'success' ? 'success' : 'info'} toast-notification`;
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        opacity: 0;
        transform: translateX(100%);
        transition: all 0.3s ease;
    `;
    
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close float-end" aria-label="Close"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.opacity = '1';
        notification.style.transform = 'translateX(0)';
    }, 10);
    
    // Close button functionality
    const closeBtn = notification.querySelector('.btn-close');
    closeBtn.addEventListener('click', () => {
        removeNotification(notification);
    });
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            removeNotification(notification);
        }
    }, 5000);
}

function removeNotification(notification) {
    notification.style.opacity = '0';
    notification.style.transform = 'translateX(100%)';
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 300);
}

// Format numbers with commas
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// Debounce function for search inputs
function debounce(func, wait, immediate) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            timeout = null;
            if (!immediate) func.apply(this, args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(this, args);
    };
}

// Progress bar animation
function animateProgress(element, targetWidth, duration = 1000) {
    const start = parseFloat(element.style.width) || 0;
    const change = targetWidth - start;
    const startTime = performance.now();
    
    function updateProgress(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        const currentWidth = start + (change * progress);
        element.style.width = currentWidth + '%';
        
        if (progress < 1) {
            requestAnimationFrame(updateProgress);
        }
    }
    
    requestAnimationFrame(updateProgress);
}

// Initialize research form functionality
function initializeResearchForm() {
    const form = document.getElementById('researchForm');
    if (!form) return;
    
    const submitBtn = document.getElementById('startResearchBtn');
    const queryInput = document.getElementById('query');
    
    // Add character counter
    if (queryInput) {
        const maxLength = 1000;
        const counter = document.createElement('div');
        counter.className = 'form-text text-end mt-1';
        counter.style.fontSize = '0.8rem';
        queryInput.parentNode.appendChild(counter);
        
        function updateCounter() {
            const remaining = maxLength - queryInput.value.length;
            counter.textContent = `${queryInput.value.length}/${maxLength} characters`;
            counter.style.color = remaining < 100 ? '#dc3545' : remaining < 200 ? '#fd7e14' : '#6c757d';
        }
        
        queryInput.addEventListener('input', updateCounter);
        updateCounter();
        
        // Prevent typing beyond limit
        queryInput.addEventListener('keypress', function(e) {
            if (this.value.length >= maxLength && e.key !== 'Backspace' && e.key !== 'Delete') {
                e.preventDefault();
                showNotification('Maximum character limit reached!', 'error');
            }
        });
    }
    
    // Add example queries functionality
    const exampleQueries = [
        "Top 5 AI startups in Indian Healthcare",
        "Latest fintech trends in Southeast Asia",
        "Renewable energy investments in Europe 2025",
        "Machine learning applications in agriculture",
        "Blockchain technology in supply chain management"
    ];
    
    // Add example query buttons
    const examplesContainer = document.createElement('div');
    examplesContainer.className = 'mb-3';
    examplesContainer.innerHTML = `
        <small class="text-muted">Quick examples:</small>
        <div class="mt-1" id="exampleQueries"></div>
    `;
    
    const formGroup = queryInput.closest('.mb-4');
    formGroup.appendChild(examplesContainer);
    
    const examplesDiv = document.getElementById('exampleQueries');
    exampleQueries.forEach(query => {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'btn btn-outline-secondary btn-sm me-2 mb-1';
        btn.style.fontSize = '0.8rem';
        btn.textContent = query;
        btn.addEventListener('click', () => {
            queryInput.value = query;
            autoResize(queryInput);
            queryInput.focus();
        });
        examplesDiv.appendChild(btn);
    });
}

// Format report content
function formatReportContent() {
    const reportContent = document.querySelector('.report-content');
    if (!reportContent) return;
    
    // Format markdown-style content
    let html = reportContent.innerHTML;
    
    // Convert **bold** to <strong>
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Convert *italic* to <em>
    html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
    
    // Convert URLs to clickable links
    html = html.replace(/(https?:\/\/[^\s<>"{}|\\^`[\]]+)/g, '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>');
    
    // Add styling to headings
    html = html.replace(/<br>\s*#\s+(.+?)<br>/g, '<h2 class="mt-4 mb-3 text-primary border-bottom pb-2">$1</h2>');
    html = html.replace(/<br>\s*##\s+(.+?)<br>/g, '<h3 class="mt-3 mb-2 text-secondary">$1</h3>');
    html = html.replace(/<br>\s*###\s+(.+?)<br>/g, '<h4 class="mt-2 mb-2">$1</h4>');
    
    reportContent.innerHTML = html;
    
    // Add copy buttons to report sections
    const headings = reportContent.querySelectorAll('h2, h3, h4');
    headings.forEach(heading => {
        const copyBtn = document.createElement('button');
        copyBtn.className = 'btn btn-sm btn-outline-secondary ms-2';
        copyBtn.innerHTML = '<i class="fas fa-copy"></i>';
        copyBtn.title = 'Copy section';
        copyBtn.style.fontSize = '0.7rem';
        
        copyBtn.addEventListener('click', () => {
            const section = heading.nextElementSibling;
            if (section) {
                copyToClipboard(heading.textContent + '\n\n' + section.textContent);
            } else {
                copyToClipboard(heading.textContent);
            }
        });
        
        heading.appendChild(copyBtn);
    });
}

// Global test functions for debugging
window.testPost = function() {
    console.log('Testing POST request...');
    fetch('/test', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({test: 'hello from main.js', timestamp: new Date().toISOString()})
    })
    .then(r => r.json())
    .then(d => {
        console.log('Test response:', d);
        showNotification('POST test successful!', 'success');
    })
    .catch(e => {
        console.error('Test error:', e);
        showNotification('POST test failed!', 'error');
    });
};

window.testNotification = function(message = 'Test notification', type = 'info') {
    showNotification(message, type);
};

window.testCopy = function(text = 'Hello, World!') {
    copyToClipboard(text);
};

// Page performance monitoring
window.addEventListener('load', function() {
    const loadTime = performance.now();
    console.log(`Page loaded in ${Math.round(loadTime)}ms`);
    
    // Show load time in console for debugging
    if (loadTime > 3000) {
        console.warn('Slow page load detected:', Math.round(loadTime) + 'ms');
    }
});

// Error handling for unhandled promises
window.addEventListener('unhandledrejection', function(event) {
    console.error('Unhandled promise rejection:', event.reason);
    showNotification('An unexpected error occurred', 'error');
});

// Connection status monitoring
window.addEventListener('online', function() {
    showNotification('Connection restored', 'success');
});

window.addEventListener('offline', function() {
    showNotification('Connection lost - check your internet', 'error');
});

console.log('Main.js fully loaded and configured');
