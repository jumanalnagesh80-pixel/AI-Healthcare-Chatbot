// ===============================================
// AI Healthcare Chatbot - Enhanced JavaScript v2.0
// Complete API Integration & Real-time Features
// ===============================================

// ===============================================
// Global State Management
// ===============================================
const App = {
    state: {
        user: null,
        isAuthenticated: false,
        socket: null,
        notifications: [],
        loading: false
    },
    
    // Update state and trigger UI updates
    setState(updates) {
        this.state = { ...this.state, ...updates };
        this.emit('stateChange', this.state);
    },
    
    // Event emitter
    listeners: {},
    on(event, callback) {
        if (!this.listeners[event]) this.listeners[event] = [];
        this.listeners[event].push(callback);
    },
    emit(event, data) {
        if (this.listeners[event]) {
            this.listeners[event].forEach(callback => callback(data));
        }
    }
};

// ===============================================
// API Client
// ===============================================
const API = {
    baseURL: window.location.origin,
    
    // Generic request method
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            method: options.method || 'GET',
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            credentials: 'include',
            ...options
        };
        
        if (options.body) {
            config.body = JSON.stringify(options.body);
        }
        
        try {
            const response = await fetch(url, config);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || `HTTP ${response.status}`);
            }
            
            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },
    
    // Authentication endpoints
    auth: {
        register: (data) => API.request('/api/register', { method: 'POST', body: data }),
        login: (data) => API.request('/api/login', { method: 'POST', body: data }),
        logout: () => API.request('/api/logout', { method: 'POST' }),
        checkAuth: () => API.request('/api/check-auth')
    },
    
    // Dashboard endpoints
    dashboard: {
        getStats: () => API.request('/api/dashboard/stats')
    },
    
    // Appointments endpoints
    appointments: {
        list: (params) => API.request('/api/appointments' + (params ? `?${new URLSearchParams(params)}` : '')),
        create: (data) => API.request('/api/appointments', { method: 'POST', body: data }),
        update: (id, data) => API.request(`/api/appointments/${id}`, { method: 'PUT', body: data }),
        delete: (id) => API.request(`/api/appointments/${id}`, { method: 'DELETE' })
    },
    
    // Prescriptions endpoints
    prescriptions: {
        list: (params) => API.request('/api/prescriptions' + (params ? `?${new URLSearchParams(params)}` : '')),
        create: (data) => API.request('/api/prescriptions', { method: 'POST', body: data })
    },
    
    // Vital signs endpoints
    vitalSigns: {
        list: (params) => API.request('/api/vital-signs' + (params ? `?${new URLSearchParams(params)}` : '')),
        create: (data) => API.request('/api/vital-signs', { method: 'POST', body: data }),
        delete: (id) => API.request(`/api/vital-signs/${id}`, { method: 'DELETE' })
    },
    
    // Lab reports endpoints
    labReports: {
        list: (params) => API.request('/api/lab-reports' + (params ? `?${new URLSearchParams(params)}` : '')),
        create: (data) => API.request('/api/lab-reports', { method: 'POST', body: data })
    },
    
    // Chat endpoints
    chat: {
        send: (message) => API.request('/api/chat', { method: 'POST', body: { message } }),
        getHistory: (limit) => API.request(`/api/chat/history?limit=${limit || 50}`)
    },
    
    // Profile endpoints
    profile: {
        get: () => API.request('/api/profile'),
        update: (data) => API.request('/api/profile', { method: 'PUT', body: data })
    },
    
    // Activity logs
    activityLogs: {
        list: (limit) => API.request(`/api/activity-logs?limit=${limit || 100}`)
    }
};

// ===============================================
// WebSocket Manager
// ===============================================
const WebSocketManager = {
    socket: null,
    reconnectAttempts: 0,
    maxReconnectAttempts: 5,
    reconnectDelay: 2000,
    
    connect() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsURL = `${protocol}//${window.location.host}/socket.io/`;
        
        try {
            this.socket = io(window.location.origin, {
                transports: ['websocket', 'polling']
            });
            
            this.socket.on('connect', () => {
                console.log('✅ WebSocket connected');
                this.reconnectAttempts = 0;
                showToast('Connected to server', 'success');
            });
            
            this.socket.on('disconnect', () => {
                console.log('❌ WebSocket disconnected');
                this.handleReconnect();
            });
            
            this.socket.on('connect_error', (error) => {
                console.error('WebSocket error:', error);
                this.handleReconnect();
            });
            
            this.socket.on('chat_response', (data) => {
                this.handleChatResponse(data);
            });
            
            this.socket.on('chat_error', (data) => {
                showToast(data.error || 'Chat error occurred', 'danger');
            });
            
            App.setState({ socket: this.socket });
            
        } catch (error) {
            console.error('Failed to initialize WebSocket:', error);
        }
    },
    
    handleReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            console.log(`Reconnecting... Attempt ${this.reconnectAttempts}`);
            setTimeout(() => this.connect(), this.reconnectDelay);
        } else {
            showToast('Unable to connect to server. Please refresh the page.', 'danger');
        }
    },
    
    sendMessage(message) {
        if (this.socket && this.socket.connected) {
            this.socket.emit('chat_message', { message });
        } else {
            showToast('Not connected to server', 'warning');
        }
    },
    
    handleChatResponse(data) {
        App.emit('chatResponse', data);
    },
    
    disconnect() {
        if (this.socket) {
            this.socket.disconnect();
        }
    }
};

// ===============================================
// UI Utilities
// ===============================================
const UI = {
    // Show loading overlay
    showLoading() {
        let overlay = document.getElementById('loading-overlay');
        if (!overlay) {
            overlay = document.createElement('div');
            overlay.id = 'loading-overlay';
            overlay.className = 'modal-overlay';
            overlay.innerHTML = '<div class="spinner"></div>';
            document.body.appendChild(overlay);
        }
        overlay.style.display = 'flex';
        App.setState({ loading: true });
    },
    
    // Hide loading overlay
    hideLoading() {
        const overlay = document.getElementById('loading-overlay');
        if (overlay) {
            overlay.style.display = 'none';
        }
        App.setState({ loading: false });
    },
    
    // Show modal
    showModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.style.display = 'flex';
            modal.classList.add('animate-fade-in');
        }
    },
    
    // Hide modal
    hideModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.style.display = 'none';
        }
    },
    
    // Toggle element visibility
    toggle(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.classList.toggle('hidden');
        }
    }
};

// ===============================================
// Toast Notifications
// ===============================================
function showToast(message, type = 'info', duration = 5000) {
    // Create toast container if it doesn't exist
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container';
        document.body.appendChild(container);
    }
    
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast toast-${type} animate-slide-in-right`;
    
    const icons = {
        success: '✓',
        danger: '✕',
        warning: '⚠',
        info: 'ℹ'
    };
    
    toast.innerHTML = `
        <span style="font-size: 1.25rem; font-weight: bold;">${icons[type] || 'ℹ'}</span>
        <span>${message}</span>
        <button onclick="this.parentElement.remove()" style="margin-left: auto; background: none; border: none; cursor: pointer; font-size: 1.25rem; opacity: 0.7;">×</button>
    `;
    
    container.appendChild(toast);
    
    // Auto remove after duration
    setTimeout(() => {
        toast.style.animation = 'fadeOut 0.3s ease-out forwards';
        setTimeout(() => toast.remove(), 300);
    }, duration);
}

// ===============================================
// Form Validation
// ===============================================
const Validator = {
    email(value) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(value);
    },
    
    password(value) {
        return value.length >= 6;
    },
    
    required(value) {
        return value && value.trim().length > 0;
    },
    
    phone(value) {
        const re = /^[\d\s\-\+\(\)]+$/;
        return re.test(value);
    },
    
    validate(formId) {
        const form = document.getElementById(formId);
        if (!form) return false;
        
        let isValid = true;
        const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
        
        inputs.forEach(input => {
            const error = input.parentElement.querySelector('.form-error');
            if (error) error.remove();
            
            if (!this.required(input.value)) {
                this.showError(input, 'This field is required');
                isValid = false;
            } else if (input.type === 'email' && !this.email(input.value)) {
                this.showError(input, 'Please enter a valid email');
                isValid = false;
            } else if (input.type === 'password' && !this.password(input.value)) {
                this.showError(input, 'Password must be at least 6 characters');
                isValid = false;
            }
        });
        
        return isValid;
    },
    
    showError(input, message) {
        const error = document.createElement('div');
        error.className = 'form-error';
        error.textContent = message;
        input.parentElement.appendChild(error);
        input.classList.add('error');
    }
};

// ===============================================
// Date & Time Utilities
// ===============================================
const DateTime = {
    format(dateString, format = 'short') {
        const date = new Date(dateString);
        
        if (format === 'short') {
            return date.toLocaleDateString('en-US', {
                month: 'short',
                day: 'numeric',
                year: 'numeric'
            });
        } else if (format === 'long') {
            return date.toLocaleDateString('en-US', {
                weekday: 'long',
                month: 'long',
                day: 'numeric',
                year: 'numeric'
            });
        } else if (format === 'time') {
            return date.toLocaleTimeString('en-US', {
                hour: '2-digit',
                minute: '2-digit'
            });
        } else if (format === 'datetime') {
            return date.toLocaleString('en-US', {
                month: 'short',
                day: 'numeric',
                year: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
        }
        
        return date.toLocaleDateString();
    },
    
    relative(dateString) {
        const date = new Date(dateString);
        const now = new Date();
        const diff = now - date;
        const seconds = Math.floor(diff / 1000);
        const minutes = Math.floor(seconds / 60);
        const hours = Math.floor(minutes / 60);
        const days = Math.floor(hours / 24);
        
        if (seconds < 60) return 'just now';
        if (minutes < 60) return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
        if (hours < 24) return `${hours} hour${hours > 1 ? 's' : ''} ago`;
        if (days < 7) return `${days} day${days > 1 ? 's' : ''} ago`;
        
        return this.format(dateString);
    }
};

// ===============================================
// Authentication Functions
// ===============================================
async function login(username, password) {
    UI.showLoading();
    
    try {
        const result = await API.auth.login({ username, password });
        
        if (result.success) {
            App.setState({
                user: result.user,
                isAuthenticated: true
            });
            
            showToast('Login successful! Redirecting...', 'success');
            
            setTimeout(() => {
                window.location.href = '/dashboard';
            }, 1000);
        }
    } catch (error) {
        showToast(error.message || 'Login failed', 'danger');
    } finally {
        UI.hideLoading();
    }
}

async function register(formData) {
    UI.showLoading();
    
    try {
        const result = await API.auth.register(formData);
        
        if (result.success) {
            showToast('Registration successful! Please login.', 'success');
            
            // Switch to login tab after delay
            setTimeout(() => {
                switchTab('login');
            }, 1500);
        }
    } catch (error) {
        showToast(error.message || 'Registration failed', 'danger');
    } finally {
        UI.hideLoading();
    }
}

async function logout() {
    if (!confirm('Are you sure you want to logout?')) return;
    
    UI.showLoading();
    
    try {
        await API.auth.logout();
        App.setState({ user: null, isAuthenticated: false });
        WebSocketManager.disconnect();
        showToast('Logged out successfully', 'success');
        setTimeout(() => {
            window.location.href = '/login';
        }, 1000);
    } catch (error) {
        showToast('Logout failed', 'danger');
    } finally {
        UI.hideLoading();
    }
}

async function checkAuth() {
    try {
        const result = await API.auth.checkAuth();
        
        if (result.authenticated) {
            App.setState({
                user: result.user,
                isAuthenticated: true
            });
            return true;
        }
        return false;
    } catch (error) {
        return false;
    }
}

// ===============================================
// Dashboard Functions
// ===============================================
async function loadDashboardStats() {
    try {
        const result = await API.dashboard.getStats();
        
        if (result.success && result.stats) {
            updateStatCards(result.stats);
        }
    } catch (error) {
        console.error('Failed to load stats:', error);
    }
}

function updateStatCards(stats) {
    const elements = {
        'total-appointments': stats.total_appointments || 0,
        'pending-appointments': stats.pending_appointments || 0,
        'active-prescriptions': stats.active_prescriptions || 0,
        'recent-reports': stats.recent_reports || 0,
        'total-patients': stats.total_patients || 0,
        'vital-records': stats.vital_records || 0
    };
    
    Object.entries(elements).forEach(([id, value]) => {
        const element = document.getElementById(id);
        if (element) {
            animateCounter(element, value);
        }
    });
}

function animateCounter(element, target) {
    const duration = 1000;
    const start = 0;
    const increment = target / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current);
        }
    }, 16);
}

// ===============================================
// Appointments Functions
// ===============================================
async function loadAppointments(filter = {}) {
    UI.showLoading();
    
    try {
        const result = await API.appointments.list(filter);
        
        if (result.success) {
            displayAppointments(result.appointments || []);
        }
    } catch (error) {
        showToast('Failed to load appointments', 'danger');
    } finally {
        UI.hideLoading();
    }
}

function displayAppointments(appointments) {
    const tbody = document.getElementById('appointments-tbody');
    if (!tbody) return;
    
    if (appointments.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="text-center p-6">No appointments found</td></tr>';
        return;
    }
    
    tbody.innerHTML = appointments.map(apt => `
        <tr class="animate-fade-in-up">
            <td>${apt.id}</td>
            <td>${apt.patient_name || 'N/A'}</td>
            <td>${apt.doctor_name || 'N/A'}</td>
            <td>${DateTime.format(apt.appointment_date)} ${apt.appointment_time || ''}</td>
            <td>${apt.reason || apt.symptoms || 'N/A'}</td>
            <td><span class="badge badge-${getStatusClass(apt.status)}">${apt.status}</span></td>
            <td>
                <button onclick="editAppointment(${apt.id})" class="btn btn-sm btn-primary">Edit</button>
                <button onclick="deleteAppointment(${apt.id})" class="btn btn-sm btn-danger">Cancel</button>
            </td>
        </tr>
    `).join('');
}

async function createAppointment(formData) {
    UI.showLoading();
    
    try {
        const result = await API.appointments.create(formData);
        
        if (result.success) {
            showToast('Appointment booked successfully!', 'success');
            UI.hideModal('appointment-modal');
            loadAppointments();
        }
    } catch (error) {
        showToast(error.message || 'Failed to create appointment', 'danger');
    } finally {
        UI.hideLoading();
    }
}

async function deleteAppointment(id) {
    if (!confirm('Are you sure you want to cancel this appointment?')) return;
    
    UI.showLoading();
    
    try {
        const result = await API.appointments.delete(id);
        
        if (result.success) {
            showToast('Appointment cancelled successfully', 'success');
            loadAppointments();
        }
    } catch (error) {
        showToast('Failed to cancel appointment', 'danger');
    } finally {
        UI.hideLoading();
    }
}

// ===============================================
// Prescriptions Functions
// ===============================================
async function loadPrescriptions(filter = {}) {
    UI.showLoading();
    
    try {
        const result = await API.prescriptions.list(filter);
        
        if (result.success) {
            displayPrescriptions(result.prescriptions || []);
        }
    } catch (error) {
        showToast('Failed to load prescriptions', 'danger');
    } finally {
        UI.hideLoading();
    }
}

function displayPrescriptions(prescriptions) {
    const container = document.getElementById('prescriptions-container');
    if (!container) return;
    
    if (prescriptions.length === 0) {
        container.innerHTML = '<div class="card text-center p-6">No prescriptions found</div>';
        return;
    }
    
    container.innerHTML = prescriptions.map(rx => `
        <div class="card animate-fade-in-up">
            <h3 class="text-primary">${rx.medication_name}</h3>
            <p><strong>Dosage:</strong> ${rx.dosage || 'N/A'}</p>
            <p><strong>Frequency:</strong> ${rx.frequency || 'N/A'}</p>
            <p><strong>Duration:</strong> ${rx.duration || 'N/A'}</p>
            ${rx.instructions ? `<p><strong>Instructions:</strong> ${rx.instructions}</p>` : ''}
            <p><strong>Doctor:</strong> ${rx.doctor_name || 'N/A'}</p>
            <p><strong>Start Date:</strong> ${DateTime.format(rx.start_date)}</p>
            ${rx.end_date ? `<p><strong>End Date:</strong> ${DateTime.format(rx.end_date)}</p>` : ''}
            ${rx.refills_remaining !== undefined ? `<p><strong>Refills:</strong> ${rx.refills_remaining} remaining</p>` : ''}
            <span class="badge badge-${rx.status === 'Active' ? 'success' : 'warning'}">${rx.status}</span>
        </div>
    `).join('');
}

// Continue in next part...



// ===============================================
// Vital Signs Functions
// ===============================================
async function loadVitalSigns(limit = 30) {
    UI.showLoading();
    
    try {
        const result = await API.vitalSigns.list({ limit });
        
        if (result.success) {
            displayVitalSigns(result.vital_signs || []);
            if (result.vital_signs.length > 0 && window.Chart) {
                renderVitalSignsChart(result.vital_signs);
            }
        }
    } catch (error) {
        showToast('Failed to load vital signs', 'danger');
    } finally {
        UI.hideLoading();
    }
}

function displayVitalSigns(vitalSigns) {
    const tbody = document.getElementById('vital-signs-tbody');
    if (!tbody) return;
    
    if (vitalSigns.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" class="text-center p-6">No vital signs records found</td></tr>';
        return;
    }
    
    tbody.innerHTML = vitalSigns.map(vs => `
        <tr class="animate-fade-in-up">
            <td>${DateTime.format(vs.recorded_at, 'datetime')}</td>
            <td>${vs.blood_pressure || `${vs.blood_pressure_systolic}/${vs.blood_pressure_diastolic}` || 'N/A'}</td>
            <td>${vs.heart_rate || 'N/A'} ${vs.heart_rate ? 'bpm' : ''}</td>
            <td>${vs.temperature || 'N/A'} ${vs.temperature ? '°F' : ''}</td>
            <td>${vs.respiratory_rate || 'N/A'} ${vs.respiratory_rate ? '/min' : ''}</td>
            <td>${vs.oxygen_saturation || 'N/A'} ${vs.oxygen_saturation ? '%' : ''}</td>
            <td>${vs.weight || 'N/A'} ${vs.weight ? 'kg' : ''}</td>
            <td>${vs.bmi || 'N/A'}</td>
        </tr>
    `).join('');
}

async function recordVitalSigns(formData) {
    UI.showLoading();
    
    try {
        const result = await API.vitalSigns.create(formData);
        
        if (result.success) {
            showToast('Vital signs recorded successfully!', 'success');
            if (result.bmi) {
                showToast(`Calculated BMI: ${result.bmi}`, 'info');
            }
            UI.hideModal('vital-signs-modal');
            loadVitalSigns();
        }
    } catch (error) {
        showToast(error.message || 'Failed to record vital signs', 'danger');
    } finally {
        UI.hideLoading();
    }
}

// ===============================================
// Lab Reports Functions
// ===============================================
async function loadLabReports(filter = {}) {
    UI.showLoading();
    
    try {
        const result = await API.labReports.list(filter);
        
        if (result.success) {
            displayLabReports(result.lab_reports || []);
        }
    } catch (error) {
        showToast('Failed to load lab reports', 'danger');
    } finally {
        UI.hideLoading();
    }
}

function displayLabReports(reports) {
    const container = document.getElementById('lab-reports-container');
    if (!container) return;
    
    if (reports.length === 0) {
        container.innerHTML = '<div class="card text-center p-6">No lab reports found</div>';
        return;
    }
    
    container.innerHTML = reports.map(report => `
        <div class="card animate-fade-in-up ${report.abnormal_flag ? 'border-warning' : ''}">
            <div class="flex justify-between items-start mb-4">
                <h3 class="text-primary">${report.test_name}</h3>
                <span class="badge badge-${report.status === 'Completed' ? 'success' : 'warning'}">${report.status}</span>
            </div>
            ${report.test_type ? `<p><strong>Type:</strong> ${report.test_type}</p>` : ''}
            <p><strong>Test Date:</strong> ${DateTime.format(report.test_date)}</p>
            ${report.result_value ? `<p><strong>Result:</strong> ${report.result_value} ${report.unit || ''}</p>` : ''}
            ${report.reference_range ? `<p><strong>Reference Range:</strong> ${report.reference_range}</p>` : ''}
            ${report.doctor_comments ? `
                <div class="mt-4 p-4 bg-gray rounded-lg">
                    <strong>Doctor's Comments:</strong>
                    <p class="mt-2">${report.doctor_comments}</p>
                </div>
            ` : ''}
            ${report.abnormal_flag ? '<p class="text-warning mt-4">⚠️ Abnormal result - Please consult your doctor</p>' : ''}
        </div>
    `).join('');
}

// ===============================================
// Chat Functions
// ===============================================
let chatInitialized = false;

function initializeChat() {
    if (chatInitialized) return;
    
    const chatInput = document.getElementById('chat-input');
    const sendButton = document.getElementById('send-message');
    
    if (!chatInput || !sendButton) return;
    
    // Enter key to send
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendChatMessage();
        }
    });
    
    // Send button click
    sendButton.addEventListener('click', sendChatMessage);
    
    // Listen for chat responses
    App.on('chatResponse', (data) => {
        addBotMessage(data.response || data.message, data.intent, data.sentiment);
    });
    
    // Connect WebSocket
    WebSocketManager.connect();
    
    chatInitialized = true;
}

async function sendChatMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Add user message to UI
    addUserMessage(message);
    input.value = '';
    
    // Show typing indicator
    showTypingIndicator();
    
    try {
        // Try WebSocket first
        if (App.state.socket && App.state.socket.connected) {
            WebSocketManager.sendMessage(message);
        } else {
            // Fallback to HTTP
            const result = await API.chat.send(message);
            if (result.success) {
                hideTypingIndicator();
                addBotMessage(result.response, result.intent, result.sentiment);
            }
        }
    } catch (error) {
        hideTypingIndicator();
        showToast('Failed to send message', 'danger');
    }
}

function addUserMessage(message) {
    const messagesContainer = document.getElementById('chat-messages');
    if (!messagesContainer) return;
    
    const messageEl = document.createElement('div');
    messageEl.className = 'chat-message user animate-fade-in-up';
    messageEl.innerHTML = `
        <div class="chat-avatar">👤</div>
        <div class="chat-bubble">${escapeHtml(message)}</div>
    `;
    
    messagesContainer.appendChild(messageEl);
    scrollToBottom(messagesContainer);
}

function addBotMessage(message, intent, sentiment) {
    const messagesContainer = document.getElementById('chat-messages');
    if (!messagesContainer) return;
    
    const messageEl = document.createElement('div');
    messageEl.className = 'chat-message bot animate-fade-in-up';
    
    // Format message (convert markdown-like syntax)
    const formattedMessage = formatBotMessage(message);
    
    messageEl.innerHTML = `
        <div class="chat-avatar">🤖</div>
        <div class="chat-bubble">
            ${formattedMessage}
            ${intent ? `<div class="text-xs mt-2 opacity-70">Intent: ${intent}</div>` : ''}
        </div>
    `;
    
    messagesContainer.appendChild(messageEl);
    scrollToBottom(messagesContainer);
}

function formatBotMessage(message) {
    // Convert **bold** to <strong>
    message = message.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Convert bullet points
    message = message.replace(/^• (.+)$/gm, '<li>$1</li>');
    message = message.replace(/(<li>.*<\/li>)/s, '<ul class="mt-2 ml-4">$1</ul>');
    
    // Convert line breaks
    message = message.replace(/\n/g, '<br>');
    
    return message;
}

function showTypingIndicator() {
    const messagesContainer = document.getElementById('chat-messages');
    if (!messagesContainer) return;
    
    const indicator = document.createElement('div');
    indicator.id = 'typing-indicator';
    indicator.className = 'chat-message bot';
    indicator.innerHTML = `
        <div class="chat-avatar">🤖</div>
        <div class="chat-bubble">
            <div class="flex gap-1">
                <span class="animate-bounce" style="animation-delay: 0s;">●</span>
                <span class="animate-bounce" style="animation-delay: 0.2s;">●</span>
                <span class="animate-bounce" style="animation-delay: 0.4s;">●</span>
            </div>
        </div>
    `;
    
    messagesContainer.appendChild(indicator);
    scrollToBottom(messagesContainer);
}

function hideTypingIndicator() {
    const indicator = document.getElementById('typing-indicator');
    if (indicator) {
        indicator.remove();
    }
}

function sendQuickMessage(message) {
    const input = document.getElementById('chat-input');
    if (input) {
        input.value = message;
        sendChatMessage();
    }
}

function clearChat() {
    if (!confirm('Are you sure you want to clear the chat history?')) return;
    
    const messagesContainer = document.getElementById('chat-messages');
    if (messagesContainer) {
        messagesContainer.innerHTML = `
            <div class="chat-message bot">
                <div class="chat-avatar">🤖</div>
                <div class="chat-bubble">
                    Chat cleared. How can I help you today?
                </div>
            </div>
        `;
    }
    showToast('Chat history cleared', 'success');
}

// ===============================================
// Chart Rendering (Chart.js)
// ===============================================
function renderVitalSignsChart(vitalSigns) {
    const canvas = document.getElementById('vitals-chart');
    if (!canvas || !window.Chart) return;
    
    // Prepare data (reverse to show chronological order)
    const reversedData = [...vitalSigns].reverse();
    const dates = reversedData.map(v => DateTime.format(v.recorded_at, 'short'));
    const heartRates = reversedData.map(v => v.heart_rate || null);
    const temperatures = reversedData.map(v => v.temperature || null);
    const systolic = reversedData.map(v => v.blood_pressure_systolic || null);
    const diastolic = reversedData.map(v => v.blood_pressure_diastolic || null);
    
    // Destroy existing chart if any
    if (canvas.chart) {
        canvas.chart.destroy();
    }
    
    const ctx = canvas.getContext('2d');
    canvas.chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [
                {
                    label: 'Heart Rate (bpm)',
                    data: heartRates,
                    borderColor: '#ef4444',
                    backgroundColor: 'rgba(239, 68, 68, 0.1)',
                    tension: 0.4,
                    fill: true
                },
                {
                    label: 'Systolic BP',
                    data: systolic,
                    borderColor: '#f59e0b',
                    backgroundColor: 'rgba(245, 158, 11, 0.1)',
                    tension: 0.4,
                    fill: true
                },
                {
                    label: 'Diastolic BP',
                    data: diastolic,
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    tension: 0.4,
                    fill: true
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Vital Signs Trend'
                },
                tooltip: {
                    mode: 'index',
                    intersect: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Value'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Date'
                    }
                }
            },
            interaction: {
                mode: 'nearest',
                axis: 'x',
                intersect: false
            }
        }
    });
}

// ===============================================
// Utility Functions
// ===============================================
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function scrollToBottom(element) {
    element.scrollTop = element.scrollHeight;
}

function getStatusClass(status) {
    const statusMap = {
        'Scheduled': 'warning',
        'Confirmed': 'info',
        'Completed': 'success',
        'Cancelled': 'danger',
        'Pending': 'warning',
        'Active': 'success'
    };
    return statusMap[status] || 'info';
}

function switchTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.auth-form').forEach(form => {
        form.classList.remove('active');
    });
    
    // Remove active class from buttons
    document.querySelectorAll('.auth-tab').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Show selected tab
    const selectedForm = document.getElementById(`${tabName}-form`);
    if (selectedForm) {
        selectedForm.classList.add('active');
    }
    
    // Add active class to button
    const selectedTab = document.querySelector(`[data-tab="${tabName}"]`);
    if (selectedTab) {
        selectedTab.classList.add('active');
    }
}

function navigateTo(url) {
    window.location.href = url;
}

// ===============================================
// Form Handlers
// ===============================================
function handleLoginForm(event) {
    event.preventDefault();
    
    if (!Validator.validate('login-form')) return;
    
    const form = event.target;
    const username = form.username.value.trim();
    const password = form.password.value;
    
    login(username, password);
}

function handleRegisterForm(event) {
    event.preventDefault();
    
    if (!Validator.validate('register-form')) return;
    
    const form = event.target;
    const password = form.password.value;
    const confirmPassword = form.confirm_password?.value;
    
    if (confirmPassword && password !== confirmPassword) {
        showToast('Passwords do not match', 'danger');
        return;
    }
    
    const formData = {
        username: form.username.value.trim(),
        password: password,
        email: form.email.value.trim(),
        full_name: form.full_name.value.trim(),
        phone: form.phone?.value.trim() || '',
        role: form.role?.value || 'patient'
    };
    
    register(formData);
}

function handleAppointmentForm(event) {
    event.preventDefault();
    
    if (!Validator.validate('appointment-form')) return;
    
    const form = event.target;
    const formData = {
        doctor_name: form.doctor_name.value.trim(),
        specialty: form.specialty?.value || '',
        appointment_date: form.appointment_date.value,
        appointment_time: form.appointment_time.value,
        reason: form.reason.value.trim(),
        symptoms: form.symptoms?.value.trim() || '',
        notes: form.notes?.value.trim() || ''
    };
    
    createAppointment(formData);
}

function handleVitalSignsForm(event) {
    event.preventDefault();
    
    if (!Validator.validate('vital-signs-form')) return;
    
    const form = event.target;
    const formData = {
        blood_pressure: form.blood_pressure?.value.trim() || '',
        heart_rate: form.heart_rate.value,
        temperature: form.temperature.value,
        respiratory_rate: form.respiratory_rate?.value || null,
        oxygen_saturation: form.oxygen_saturation?.value || null,
        weight: form.weight?.value || null,
        glucose_level: form.glucose_level?.value || null,
        notes: form.notes?.value.trim() || ''
    };
    
    recordVitalSigns(formData);
}

// ===============================================
// Page Initialization
// ===============================================
document.addEventListener('DOMContentLoaded', async () => {
    console.log('🏥 AI Healthcare Chatbot - Enhanced v2.0');
    
    // Check authentication
    const isAuthenticated = await checkAuth();
    
    // Add scroll effect to navbar
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                navbar.classList.add('navbar-scrolled');
            } else {
                navbar.classList.remove('navbar-scrolled');
            }
        });
    }
    
    // Initialize forms
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLoginForm);
    }
    
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', handleRegisterForm);
    }
    
    const appointmentForm = document.getElementById('appointment-form');
    if (appointmentForm) {
        appointmentForm.addEventListener('submit', handleAppointmentForm);
    }
    
    const vitalSignsForm = document.getElementById('vital-signs-form');
    if (vitalSignsForm) {
        vitalSignsForm.addEventListener('submit', handleVitalSignsForm);
    }
    
    // Page-specific initializations
    const currentPage = window.location.pathname;
    
    if (currentPage.includes('dashboard')) {
        loadDashboardStats();
    } else if (currentPage.includes('appointments')) {
        loadAppointments();
    } else if (currentPage.includes('prescriptions')) {
        loadPrescriptions();
    } else if (currentPage.includes('vital-signs')) {
        loadVitalSigns();
    } else if (currentPage.includes('lab-reports')) {
        loadLabReports();
    } else if (currentPage.includes('chat')) {
        initializeChat();
    }
    
    // Close modals when clicking outside
    window.addEventListener('click', (e) => {
        if (e.target.classList.contains('modal-overlay')) {
            e.target.style.display = 'none';
        }
    });
    
    // Add escape key to close modals
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            document.querySelectorAll('.modal-overlay').forEach(modal => {
                modal.style.display = 'none';
            });
        }
    });
    
    console.log('✅ Application initialized');
});

// ===============================================
// Export functions for global access
// ===============================================
window.App = App;
window.API = API;
window.UI = UI;
window.login = login;
window.register = register;
window.logout = logout;
window.loadDashboardStats = loadDashboardStats;
window.loadAppointments = loadAppointments;
window.createAppointment = createAppointment;
window.deleteAppointment = deleteAppointment;
window.editAppointment = (id) => alert('Edit feature coming soon!');
window.loadPrescriptions = loadPrescriptions;
window.loadVitalSigns = loadVitalSigns;
window.recordVitalSigns = recordVitalSigns;
window.loadLabReports = loadLabReports;
window.sendChatMessage = sendChatMessage;
window.sendQuickMessage = sendQuickMessage;
window.clearChat = clearChat;
window.switchTab = switchTab;
window.navigateTo = navigateTo;
window.showToast = showToast;

console.log('✅ Enhanced JavaScript v2.0 loaded');
