// Form validation and submission handling
document.addEventListener('DOMContentLoaded', function() {
    // Get all forms on the page
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(form);
            const data = {};

            formData.forEach((value, key) => {
                data[key] = value;
            });

            // Send form data to server
            fetch(form.action, {
                method: form.method,
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.href = data.redirect || '/';
                } else {
                    // Show error message
                    const alert = document.createElement('div');
                    alert.className = 'alert';
                    alert.textContent = data.message || 'An error occurred';
                    form.insertBefore(alert, form.firstChild);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });

    // Dynamic pass status updates
    const statusElements = document.querySelectorAll('.pass-status');
    statusElements.forEach(element => {
        const expiryDate = new Date(element.dataset.expiry);
        const today = new Date();
        
        if (today > expiryDate) {
            element.textContent = 'Expired';
            element.classList.add('expired');
        }
    });
});

// Responsive navigation menu
const navToggle = document.querySelector('.nav-toggle');
if (navToggle) {
    navToggle.addEventListener('click', () => {
        const navLinks = document.querySelector('.nav-links');
        navLinks.classList.toggle('show');
    });
}