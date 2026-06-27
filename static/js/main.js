// ===============================================
// AI Healthcare Chatbot - Main JavaScript
// ===============================================

// Global State
const app = {
    currentUser: null,
    socket: null,
    chatMessages: [],
    notifications: []
};

// ===============================================
// Utility Functions
// ===============================================

// Show loading overlay
function showLoading() {
    const overlay = document.createElement('div');
    overlay.className = 'loading-overlay';
    overlay.id = 'loading-overlay';
    overlay.innerHTML = '<div class="spinner"></div>';
    document.body.appendChild(overlay);
}

// Hide loading overlay
function hideLoading() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.remove();
    }
}

// Show alert message
function showAlert(message, type = 'info') {
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.innerHTML = `
        <span>${message}</span>
        <button onclick="this.parentElement.remove()" style="margin-left: auto; background: none; border: none; cursor: pointer; font-size: 1.2rem;">&times;</button>
    `;
    
    const container = document.querySelector('.container') || document.body;
    container.insertBefore(alert, container.firstChild);
    
    setTimeout(() => alert.remove(), 5000);
}

// Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Validate email
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// ===============================================
// API Functions
// ===============================================

// Make API request
async function apiRequest(url, method = 'GET', data = null) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json'
        }
    };
    
    if (data) {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(url, options);
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.error || 'Request failed');
        }
        
        return result;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// ===============================================
// Authentication Functions
// ===============================================

// Login
async function login(username, password) {
    showLoading();
    try {
        const result = await apiRequest('/api/login', 'POST', { username, password });
        
        if (result.success) {
            app.currentUser = result.user;
            localStorage.setItem('user', JSON.stringify(result.user));
            showAlert('Login successful!', 'success');
            
            // Redirect to dashboard
            setTimeout(() => {
                window.location.href = '/dashboard';
            }, 1000);
        }
    } catch (error) {
        showAlert(error.message, 'danger');
    } finally {
        hideLoading();
    }
}

// Register
async function register(formData) {
    showLoading();
    try {
        const result = await apiRequest('/api/register', 'POST', formData);
        
        if (result.success) {
            showAlert('Registration successful! Please login.', 'success');
            
            // Switch to login tab
            setTimeout(() => {
                document.querySelector('[data-tab="login"]').click();
            }, 1500);
        }
    } catch (error) {
        showAlert(error.message, 'danger');
    } finally {
        hideLoading();
    }
}

// Logout
function logout() {
    localStorage.removeItem('user');
    app.currentUser = null;
    window.location.href = '/';
}

// Check authentication
function checkAuth() {
    const user = localStorage.getItem('user');
    if (user) {
        app.currentUser = JSON.parse(user);
        return true;
    }
    return false;
}

// ===============================================
// Form Handling
// ===============================================

// Handle login form
function handleLoginForm(event) {
    event.preventDefault();
    const form = event.target;
    const username = form.username.value.trim();
    const password = form.password.value;
    
    if (!username || !password) {
        showAlert('Please fill in all fields', 'warning');
        return;
    }
    
    login(username, password);
}

// Handle register form
function handleRegisterForm(event) {
    event.preventDefault();
    const form = event.target;
    
    const formData = {
        username: form.username.value.trim(),
        password: form.password.value,
        email: form.email.value.trim(),
        full_name: form.full_name.value.trim(),
        role: form.role.value
    };
    
    // Validation
    if (!formData.username || !formData.password || !formData.email || !formData.full_name) {
        showAlert('Please fill in all required fields', 'warning');
        return;
    }
    
    if (!validateEmail(formData.email)) {
        showAlert('Please enter a valid email address', 'warning');
        return;
    }
    
    if (formData.password.length < 6) {
        showAlert('Password must be at least 6 characters', 'warning');
        return;
    }
    
    if (formData.password !== form.confirm_password.value) {
        showAlert('Passwords do not match', 'warning');
        return;
    }
    
    register(formData);
}

// ===============================================
// Dashboard Functions
// ===============================================

// Load dashboard stats
async function loadDashboardStats() {
    try {
        const stats = await apiRequest('/api/dashboard/stats');
        
        // Update stat cards
        document.getElementById('total-appointments').textContent = stats.total_appointments || 0;
        document.getElementById('pending-appointments').textContent = stats.pending_appointments || 0;
        document.getElementById('active-prescriptions').textContent = stats.active_prescriptions || 0;
        document.getElementById('recent-reports').textContent = stats.recent_reports || 0;
    } catch (error) {
        console.error('Failed to load stats:', error);
    }
}

// Load recent appointments
async function loadRecentAppointments() {
    try {
        const result = await apiRequest('/api/appointments?limit=5');
        const appointments = result.appointments || [];
        
        const tbody = document.getElementById('recent-appointments-body');
        if (!tbody) return;
        
        tbody.innerHTML = appointments.map(apt => `
            <tr>
                <td>${apt.doctor_name || 'N/A'}</td>
                <td>${formatDate(apt.appointment_date)}</td>
                <td><span class="badge badge-${getStatusColor(apt.status)}">${apt.status}</span></td>
                <td>
                    <button onclick="viewAppointment(${apt.id})" class="btn btn-primary" style="padding: 0.5rem 1rem;">View</button>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Failed to load appointments:', error);
    }
}

// Get status color
function getStatusColor(status) {
    const colors = {
        'Scheduled': 'info',
        'Confirmed': 'success',
        'Completed': 'success',
        'Cancelled': 'danger',
        'Pending': 'warning'
    };
    return colors[status] || 'info';
}

// ===============================================
// Appointments Functions
// ===============================================

// Load all appointments
async function loadAppointments() {
    showLoading();
    try {
        const result = await apiRequest('/api/appointments');
        const appointments = result.appointments || [];
        
        const tbody = document.getElementById('appointments-tbody');
        if (!tbody) return;
        
        tbody.innerHTML = appointments.map(apt => `
            <tr>
                <td>${apt.id}</td>
                <td>${apt.patient_name || 'N/A'}</td>
                <td>${apt.doctor_name || 'N/A'}</td>
                <td>${formatDate(apt.appointment_date)}</td>
                <td>${apt.reason || 'N/A'}</td>
                <td><span class="badge badge-${getStatusColor(apt.status)}">${apt.status}</span></td>
                <td>
                    <button onclick="editAppointment(${apt.id})" class="btn btn-primary" style="padding: 0.5rem 1rem; margin-right: 0.5rem;">Edit</button>
                    <button onclick="deleteAppointment(${apt.id})" class="btn btn-danger" style="padding: 0.5rem 1rem;">Cancel</button>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        showAlert('Failed to load appointments', 'danger');
    } finally {
        hideLoading();
    }
}

// Book appointment
async function bookAppointment(formData) {
    showLoading();
    try {
        const result = await apiRequest('/api/appointments', 'POST', formData);
        showAlert('Appointment booked successfully!', 'success');
        closeModal('appointment-modal');
        loadAppointments();
    } catch (error) {
        showAlert(error.message, 'danger');
    } finally {
        hideLoading();
    }
}

// ===============================================
// Prescriptions Functions
// ===============================================

// Load prescriptions
async function loadPrescriptions() {
    showLoading();
    try {
        const result = await apiRequest('/api/prescriptions');
        const prescriptions = result.prescriptions || [];
        
        const container = document.getElementById('prescriptions-container');
        if (!container) return;
        
        container.innerHTML = prescriptions.map(presc => `
            <div class="card">
                <h3>${presc.medication_name}</h3>
                <p><strong>Dosage:</strong> ${presc.dosage}</p>
                <p><strong>Frequency:</strong> ${presc.frequency}</p>
                <p><strong>Duration:</strong> ${presc.duration}</p>
                <p><strong>Prescribed by:</strong> ${presc.doctor_name || 'N/A'}</p>
                <p><strong>Date:</strong> ${formatDate(presc.prescribed_date)}</p>
                ${presc.instructions ? `<p><strong>Instructions:</strong> ${presc.instructions}</p>` : ''}
                <span class="badge badge-${presc.status === 'Active' ? 'success' : 'warning'}">${presc.status}</span>
            </div>
        `).join('');
    } catch (error) {
        showAlert('Failed to load prescriptions', 'danger');
    } finally {
        hideLoading();
    }
}

// ===============================================
// Vital Signs Functions
// ===============================================

// Load vital signs
async function loadVitalSigns() {
    showLoading();
    try {
        const result = await apiRequest('/api/vital-signs');
        const vitalSigns = result.vital_signs || [];
        
        const tbody = document.getElementById('vital-signs-tbody');
        if (!tbody) return;
        
        tbody.innerHTML = vitalSigns.map(vital => `
            <tr>
                <td>${formatDate(vital.recorded_date)}</td>
                <td>${vital.blood_pressure || 'N/A'}</td>
                <td>${vital.heart_rate || 'N/A'} bpm</td>
                <td>${vital.temperature || 'N/A'} °F</td>
                <td>${vital.respiratory_rate || 'N/A'} /min</td>
                <td>${vital.oxygen_saturation || 'N/A'} %</td>
                <td>${vital.weight || 'N/A'} kg</td>
                <td>
                    <button onclick="viewVitalDetails(${vital.id})" class="btn btn-primary" style="padding: 0.5rem 1rem;">Details</button>
                </td>
            </tr>
        `).join('');
        
        // Load chart if available
        if (vitalSigns.length > 0) {
            renderVitalsChart(vitalSigns);
        }
    } catch (error) {
        showAlert('Failed to load vital signs', 'danger');
    } finally {
        hideLoading();
    }
}

// Add vital signs
async function addVitalSigns(formData) {
    showLoading();
    try {
        const result = await apiRequest('/api/vital-signs', 'POST', formData);
        showAlert('Vital signs recorded successfully!', 'success');
        closeModal('vital-signs-modal');
        loadVitalSigns();
    } catch (error) {
        showAlert(error.message, 'danger');
    } finally {
        hideLoading();
    }
}

// ===============================================
// Lab Reports Functions
// ===============================================

// Load lab reports
async function loadLabReports() {
    showLoading();
    try {
        const result = await apiRequest('/api/lab-reports');
        const reports = result.lab_reports || [];
        
        const container = document.getElementById('lab-reports-container');
        if (!container) return;
        
        container.innerHTML = reports.map(report => `
            <div class="card">
                <h3>${report.test_name}</h3>
                <p><strong>Test Date:</strong> ${formatDate(report.test_date)}</p>
                <p><strong>Result:</strong> ${report.result || 'Pending'}</p>
                <p><strong>Status:</strong> <span class="badge badge-${report.status === 'Completed' ? 'success' : 'warning'}">${report.status}</span></p>
                ${report.doctor_comments ? `<p><strong>Comments:</strong> ${report.doctor_comments}</p>` : ''}
                <button onclick="downloadReport(${report.id})" class="btn btn-secondary mt-2">Download Report</button>
            </div>
        `).join('');
    } catch (error) {
        showAlert('Failed to load lab reports', 'danger');
    } finally {
        hideLoading();
    }
}

// ===============================================
// AI Chat Functions
// ===============================================

// Initialize chat
function initializeChat() {
    const chatInput = document.getElementById('chat-input');
    const sendButton = document.getElementById('send-message');
    
    if (chatInput && sendButton) {
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });
        
        sendButton.addEventListener('click', sendMessage);
    }
    
    // Initialize WebSocket
    initializeWebSocket();
}

// Initialize WebSocket
function initializeWebSocket() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws`;
    
    try {
        app.socket = new WebSocket(wsUrl);
        
        app.socket.onopen = () => {
            console.log('WebSocket connected');
            addSystemMessage('Connected to AI Healthcare Assistant');
        };
        
        app.socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.message) {
                addBotMessage(data.message);
            }
        };
        
        app.socket.onclose = () => {
            console.log('WebSocket disconnected');
            setTimeout(initializeWebSocket, 5000); // Reconnect after 5s
        };
        
        app.socket.onerror = (error) => {
            console.error('WebSocket error:', error);
        };
    } catch (error) {
        console.error('Failed to initialize WebSocket:', error);
    }
}

// Send message
function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Add user message to chat
    addUserMessage(message);
    
    // Send to server
    if (app.socket && app.socket.readyState === WebSocket.OPEN) {
        app.socket.send(JSON.stringify({ message }));
    } else {
        // Fallback to HTTP request
        sendMessageHTTP(message);
    }
    
    input.value = '';
}

// Send message via HTTP
async function sendMessageHTTP(message) {
    try {
        const result = await apiRequest('/api/chat', 'POST', { message });
        if (result.response) {
            addBotMessage(result.response);
        }
    } catch (error) {
        addSystemMessage('Failed to send message. Please try again.');
    }
}

// Add user message to chat
function addUserMessage(message) {
    const messagesContainer = document.getElementById('chat-messages');
    if (!messagesContainer) return;
    
    const messageEl = document.createElement('div');
    messageEl.className = 'message user';
    messageEl.innerHTML = `
        <div class="message-avatar">U</div>
        <div class="message-content">${escapeHtml(message)}</div>
    `;
    
    messagesContainer.appendChild(messageEl);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Add bot message to chat
function addBotMessage(message) {
    const messagesContainer = document.getElementById('chat-messages');
    if (!messagesContainer) return;
    
    const messageEl = document.createElement('div');
    messageEl.className = 'message bot';
    messageEl.innerHTML = `
        <div class="message-avatar">AI</div>
        <div class="message-content">${escapeHtml(message)}</div>
    `;
    
    messagesContainer.appendChild(messageEl);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Add system message
function addSystemMessage(message) {
    const messagesContainer = document.getElementById('chat-messages');
    if (!messagesContainer) return;
    
    const messageEl = document.createElement('div');
    messageEl.className = 'alert alert-info';
    messageEl.textContent = message;
    
    messagesContainer.appendChild(messageEl);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ===============================================
// Chart Functions
// ===============================================

// Render vitals chart
function renderVitalsChart(vitalSigns) {
    const canvas = document.getElementById('vitals-chart');
    if (!canvas || !window.Chart) return;
    
    const ctx = canvas.getContext('2d');
    
    const dates = vitalSigns.map(v => formatDate(v.recorded_date)).reverse();
    const heartRates = vitalSigns.map(v => v.heart_rate || 0).reverse();
    const temperatures = vitalSigns.map(v => v.temperature || 0).reverse();
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [
                {
                    label: 'Heart Rate (bpm)',
                    data: heartRates,
                    borderColor: '#ef4444',
                    backgroundColor: 'rgba(239, 68, 68, 0.1)',
                    tension: 0.4
                },
                {
                    label: 'Temperature (°F)',
                    data: temperatures,
                    borderColor: '#f59e0b',
                    backgroundColor: 'rgba(245, 158, 11, 0.1)',
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Vital Signs Trend'
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// ===============================================
// Modal Functions
// ===============================================

// Open modal
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
    }
}

// Close modal
function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
    }
}

// ===============================================
// Tab Functions
// ===============================================

// Switch tabs
function switchTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.login-form').forEach(form => {
        form.classList.remove('active');
    });
    
    // Remove active class from all tab buttons
    document.querySelectorAll('.login-tab').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Show selected tab
    const selectedForm = document.getElementById(`${tabName}-form`);
    if (selectedForm) {
        selectedForm.classList.add('active');
    }
    
    // Add active class to clicked tab button
    const selectedTab = document.querySelector(`[data-tab="${tabName}"]`);
    if (selectedTab) {
        selectedTab.classList.add('active');
    }
}

// ===============================================
// Navigation
// ===============================================

// Handle navigation
function navigateTo(page) {
    window.location.href = page;
}

// ===============================================
// Initialization
// ===============================================

// Initialize app on DOM load
document.addEventListener('DOMContentLoaded', () => {
    // Check if user is logged in
    checkAuth();
    
    // Add scroll effect to navbar
    const nav = document.querySelector('nav');
    if (nav) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                nav.classList.add('scrolled');
            } else {
                nav.classList.remove('scrolled');
            }
        });
    }
    
    // Initialize login/register forms
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLoginForm);
    }
    
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', handleRegisterForm);
    }
    
    // Initialize dashboard
    if (document.getElementById('dashboard-page')) {
        loadDashboardStats();
        loadRecentAppointments();
    }
    
    // Initialize appointments page
    if (document.getElementById('appointments-page')) {
        loadAppointments();
    }
    
    // Initialize prescriptions page
    if (document.getElementById('prescriptions-page')) {
        loadPrescriptions();
    }
    
    // Initialize vital signs page
    if (document.getElementById('vital-signs-page')) {
        loadVitalSigns();
    }
    
    // Initialize lab reports page
    if (document.getElementById('lab-reports-page')) {
        loadLabReports();
    }
    
    // Initialize chat page
    if (document.getElementById('chat-page')) {
        initializeChat();
    }
    
    // Close modals when clicking outside
    window.addEventListener('click', (e) => {
        if (e.target.classList.contains('modal')) {
            e.target.classList.remove('active');
        }
    });
});

// Export functions for global access
window.app = app;
window.login = login;
window.logout = logout;
window.switchTab = switchTab;
window.openModal = openModal;
window.closeModal = closeModal;
window.bookAppointment = bookAppointment;
window.addVitalSigns = addVitalSigns;
window.navigateTo = navigateTo;
