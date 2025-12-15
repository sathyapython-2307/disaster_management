// Utility Functions
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// API Helper
const API = {
    get: (url) => fetch(url, {
        headers: {
            'Authorization': 'Bearer ' + getCookie('sessionid'),
            'X-CSRFToken': getCookie('csrftoken')
        }
    }).then(r => r.json()),

    post: (url, data) => fetch(url, {
        method: 'POST',
        headers: {
            'Authorization': 'Bearer ' + getCookie('sessionid'),
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then(r => r.json()),

    put: (url, data) => fetch(url, {
        method: 'PUT',
        headers: {
            'Authorization': 'Bearer ' + getCookie('sessionid'),
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then(r => r.json()),

    delete: (url) => fetch(url, {
        method: 'DELETE',
        headers: {
            'Authorization': 'Bearer ' + getCookie('sessionid'),
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
};

// Notification Helper
const Notify = {
    success: (message) => {
        showNotification(message, 'success');
    },
    error: (message) => {
        showNotification(message, 'danger');
    },
    info: (message) => {
        showNotification(message, 'info');
    },
    warning: (message) => {
        showNotification(message, 'warning');
    }
};

function showNotification(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.setAttribute('role', 'alert');
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.main-content');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        setTimeout(() => alertDiv.remove(), 5000);
    }
}

// Chart Helper
const ChartHelper = {
    createLineChart: (canvasId, labels, datasets) => {
        const ctx = document.getElementById(canvasId).getContext('2d');
        return new Chart(ctx, {
            type: 'line',
            data: { labels, datasets },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: true }
                },
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
    },

    createBarChart: (canvasId, labels, datasets) => {
        const ctx = document.getElementById(canvasId).getContext('2d');
        return new Chart(ctx, {
            type: 'bar',
            data: { labels, datasets },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: true }
                }
            }
        });
    },

    createDoughnutChart: (canvasId, labels, data) => {
        const ctx = document.getElementById(canvasId).getContext('2d');
        return new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels,
                datasets: [{
                    data,
                    backgroundColor: ['#667eea', '#f093fb', '#4facfe', '#fa709a', '#fd7e14']
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'bottom' }
                }
            }
        });
    }
};

// Map Helper
const MapHelper = {
    initMap: (elementId, center = [20, 0], zoom = 2) => {
        const map = L.map(elementId).setView(center, zoom);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 19
        }).addTo(map);
        return map;
    },

    addMarker: (map, lat, lng, title, color = 'blue') => {
        return L.circleMarker([lat, lng], {
            radius: 8,
            fillColor: color,
            color: '#000',
            weight: 1,
            opacity: 1,
            fillOpacity: 0.8
        }).bindPopup(title).addTo(map);
    },

    addGeofence: (map, coordinates, name) => {
        return L.polygon(coordinates, {
            color: '#667eea',
            weight: 2,
            opacity: 0.7,
            fillOpacity: 0.2
        }).bindPopup(name).addTo(map);
    }
};

// Date Helper
const DateHelper = {
    format: (date, format = 'YYYY-MM-DD HH:mm') => {
        const d = new Date(date);
        const year = d.getFullYear();
        const month = String(d.getMonth() + 1).padStart(2, '0');
        const day = String(d.getDate()).padStart(2, '0');
        const hours = String(d.getHours()).padStart(2, '0');
        const minutes = String(d.getMinutes()).padStart(2, '0');
        
        return format
            .replace('YYYY', year)
            .replace('MM', month)
            .replace('DD', day)
            .replace('HH', hours)
            .replace('mm', minutes);
    },

    daysAgo: (days) => {
        const date = new Date();
        date.setDate(date.getDate() - days);
        return date;
    }
};

// Form Helper
const FormHelper = {
    serialize: (formElement) => {
        const formData = new FormData(formElement);
        const data = {};
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }
        return data;
    },

    validate: (data, rules) => {
        const errors = {};
        for (let field in rules) {
            const rule = rules[field];
            const value = data[field];
            
            if (rule.required && !value) {
                errors[field] = `${field} is required`;
            }
            if (rule.minLength && value && value.length < rule.minLength) {
                errors[field] = `${field} must be at least ${rule.minLength} characters`;
            }
            if (rule.email && value && !value.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) {
                errors[field] = `${field} must be a valid email`;
            }
        }
        return errors;
    }
};

// Real-time Updates
const RealTime = {
    startPolling: (url, interval, callback) => {
        const poll = () => {
            API.get(url)
                .then(data => callback(data))
                .catch(err => console.error('Polling error:', err));
        };
        poll();
        return setInterval(poll, interval);
    },

    stopPolling: (intervalId) => {
        clearInterval(intervalId);
    }
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Add CSRF token to all fetch requests
    const csrftoken = getCookie('csrftoken');
    if (csrftoken) {
        document.querySelectorAll('form').forEach(form => {
            if (!form.querySelector('[name="csrfmiddlewaretoken"]')) {
                const input = document.createElement('input');
                input.type = 'hidden';
                input.name = 'csrfmiddlewaretoken';
                input.value = csrftoken;
                form.appendChild(input);
            }
        });
    }

    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
});

// Export for use in other scripts
window.API = API;
window.Notify = Notify;
window.ChartHelper = ChartHelper;
window.MapHelper = MapHelper;
window.DateHelper = DateHelper;
window.FormHelper = FormHelper;
window.RealTime = RealTime;
