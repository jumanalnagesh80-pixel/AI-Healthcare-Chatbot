"""
Enhanced Appointments Template with Real Doctors
"""

ENHANCED_APPOINTMENTS_HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Book Appointment - AI Healthcare Chatbot</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Poppins', sans-serif;
            background: #f5f7fa;
            color: #333;
        }
        
        .navbar {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 15px 0;
            box-shadow: 0 2px 20px rgba(0,0,0,0.1);
            position: sticky;
            top: 0;
            z-index: 100;
        }
        
        .nav-content {
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .logo {
            font-size: 1.5em;
            font-weight: 700;
            color: white;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .nav-links {
            display: flex;
            gap: 5px;
        }
        
        .nav-links a {
            color: white;
            text-decoration: none;
            padding: 10px 20px;
            border-radius: 10px;
            transition: all 0.3s;
        }
        
        .nav-links a:hover {
            background: rgba(255,255,255,0.2);
        }
        
        .container {
            max-width: 1400px;
            margin: 30px auto;
            padding: 0 30px;
        }
        
        .page-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px;
            border-radius: 20px;
            color: white;
            margin-bottom: 30px;
        }
        
        .page-header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .page-header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .section {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            margin-bottom: 30px;
        }
        
        .section h2 {
            color: #667eea;
            margin-bottom: 25px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .doctors-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 25px;
            margin-bottom: 30px;
        }
        
        .doctor-card {
            background: white;
            border: 2px solid #e0e0e0;
            border-radius: 15px;
            padding: 25px;
            transition: all 0.3s;
            cursor: pointer;
        }
        
        .doctor-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
            border-color: #667eea;
        }
        
        .doctor-card.selected {
            border-color: #667eea;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
        }
        
        .doctor-header {
            display: flex;
            gap: 20px;
            margin-bottom: 15px;
        }
        
        .doctor-image {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 2em;
            font-weight: bold;
        }
        
        .doctor-info h3 {
            color: #333;
            margin-bottom: 5px;
        }
        
        .doctor-specialty {
            color: #667eea;
            font-weight: 500;
            margin-bottom: 5px;
        }
        
        .doctor-rating {
            color: #ffc107;
            font-size: 0.9em;
        }
        
        .doctor-details {
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #e0e0e0;
        }
        
        .doctor-detail-item {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 8px;
            font-size: 0.95em;
            color: #666;
        }
        
        .doctor-detail-item i {
            color: #667eea;
            width: 20px;
        }
        
        .doctor-actions {
            margin-top: 15px;
            display: flex;
            gap: 10px;
        }
        
        .btn {
            padding: 12px 25px;
            border: none;
            border-radius: 10px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            font-size: 0.95em;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            flex: 1;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        }
        
        .btn-secondary {
            background: #f5f7fa;
            color: #667eea;
            border: 2px solid #667eea;
        }
        
        .btn-secondary:hover {
            background: #667eea;
            color: white;
        }
        
        .booking-form {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            margin-bottom: 30px;
        }
        
        .form-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            color: #333;
            margin-bottom: 8px;
            font-weight: 500;
        }
        
        .form-group input, .form-group select, .form-group textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 1em;
            font-family: 'Poppins', sans-serif;
        }
        
        .form-group input:focus, .form-group select:focus, .form-group textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .message {
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 10px;
            text-align: center;
            display: none;
            animation: slideDown 0.3s;
        }
        
        @keyframes slideDown {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        .info {
            background: #d1ecf1;
            color: #0c5460;
            border: 1px solid #bee5eb;
        }
        
        .appointments-list {
            margin-top: 20px;
        }
        
        .appointment-card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 15px;
            border-left: 4px solid #667eea;
            transition: all 0.3s;
        }
        
        .appointment-card:hover {
            transform: translateX(5px);
            box-shadow: 0 3px 10px rgba(102, 126, 234, 0.2);
        }
        
        .appointment-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        
        .appointment-title {
            font-weight: 600;
            color: #333;
            font-size: 1.1em;
        }
        
        .status-badge {
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 500;
        }
        
        .status-confirmed { background: #d4edda; color: #155724; }
        .status-pending { background: #fff3cd; color: #856404; }
        .status-completed { background: #d1ecf1; color: #0c5460; }
        .status-cancelled { background: #f8d7da; color: #721c24; }
        
        .appointment-details {
            color: #666;
            font-size: 0.95em;
        }
        
        .appointment-details strong {
            color: #333;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            color: #999;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="nav-content">
            <div class="logo">
                <i class="fas fa-heartbeat"></i>
                AI Healthcare Chatbot
            </div>
            <div class="nav-links">
                <a href="/dashboard"><i class="fas fa-home"></i> Dashboard</a>
                <a href="/chat"><i class="fas fa-comments"></i> Chat</a>
                <a href="/appointments"><i class="fas fa-calendar"></i> Appointments</a>
                <a href="/vital-signs"><i class="fas fa-heartbeat"></i> Vitals</a>
                <a href="/logout"><i class="fas fa-sign-out-alt"></i> Logout</a>
            </div>
        </div>
    </nav>
    
    <div class="container">
        <div class="page-header">
            <h1><i class="fas fa-calendar-check"></i> Book Appointment</h1>
            <p>Choose from our expert doctors and book your consultation</p>
        </div>
        
        <div class="section">
            <h2><i class="fas fa-user-md"></i> Our Specialist Doctors</h2>
            <div id="loading" class="loading">
                <div class="spinner"></div>
                <p>Loading doctors...</p>
            </div>
            <div id="doctorsGrid" class="doctors-grid" style="display:none;"></div>
        </div>
        
        <div class="booking-form" id="bookingForm" style="display:none;">
            <h2><i class="fas fa-calendar-plus"></i> Appointment Details</h2>
            <div id="selectedDoctorInfo" style="margin-bottom: 20px;"></div>
            <div id="message" class="message"></div>
            <form id="appointmentForm">
                <input type="hidden" id="doctorId">
                <input type="hidden" id="doctorName">
                <input type="hidden" id="specialty">
                
                <div class="form-grid">
                    <div class="form-group">
                        <label><i class="fas fa-calendar"></i> Appointment Date *</label>
                        <input type="date" id="appointmentDate" required>
                    </div>
                    <div class="form-group">
                        <label><i class="fas fa-clock"></i> Preferred Time *</label>
                        <select id="appointmentTime" required>
                            <option value="">Select Time</option>
                            <option value="09:00">09:00 AM</option>
                            <option value="10:00">10:00 AM</option>
                            <option value="11:00">11:00 AM</option>
                            <option value="12:00">12:00 PM</option>
                            <option value="14:00">02:00 PM</option>
                            <option value="15:00">03:00 PM</option>
                            <option value="16:00">04:00 PM</option>
                            <option value="17:00">05:00 PM</option>
                        </select>
                    </div>
                </div>
                
                <div class="form-group">
                    <label><i class="fas fa-notes-medical"></i> Symptoms / Reason for Visit</label>
                    <textarea id="symptoms" rows="4" placeholder="Describe your symptoms or reason for consultation..."></textarea>
                </div>
                
                <button type="submit" class="btn btn-primary">
                    <i class="fas fa-check-circle"></i> Confirm Appointment
                </button>
            </form>
        </div>
        
        <div class="section">
            <h2><i class="fas fa-list-alt"></i> Your Appointments</h2>
            <div class="appointments-list">
                {% if appointments %}
                    {% for apt in appointments %}
                    <div class="appointment-card">
                        <div class="appointment-header">
                            <div class="appointment-title">
                                <i class="fas fa-user-md"></i> {{ apt[1] }} - {{ apt[2] }}
                            </div>
                            <span class="status-badge status-{{ apt[5] }}">{{ apt[5] }}</span>
                        </div>
                        <div class="appointment-details">
                            <p><strong>📅 Date:</strong> {{ apt[3] }}</p>
                            <p><strong>🕐 Time:</strong> {{ apt[4] }}</p>
                            {% if apt[6] %}
                            <p><strong>📝 Symptoms:</strong> {{ apt[6] }}</p>
                            {% endif %}
                        </div>
                    </div>
                    {% endfor %}
                {% else %}
                    <div style="text-align:center; padding:40px; color:#999;">
                        <i class="fas fa-calendar-times" style="font-size:3em; opacity:0.3; margin-bottom:15px;"></i>
                        <p>No appointments yet. Book your first appointment above!</p>
                    </div>
                {% endif %}
            </div>
        </div>
    </div>
    
    <script>
        let selectedDoctor = null;
        
        // Set min date to today
        const today = new Date().toISOString().split('T')[0];
        document.getElementById('appointmentDate').min = today;
        
        // Load doctors on page load
        window.addEventListener('load', loadDoctors);
        
        async function loadDoctors() {
            try {
                const response = await fetch('/api/doctors');
                const data = await response.json();
                
                document.getElementById('loading').style.display = 'none';
                
                if (data.success && data.doctors.length > 0) {
                    const grid = document.getElementById('doctorsGrid');
                    grid.style.display = 'grid';
                    
                    data.doctors.forEach(doctor => {
                        const card = createDoctorCard(doctor);
                        grid.appendChild(card);
                    });
                }
            } catch (error) {
                console.error('Error loading doctors:', error);
                document.getElementById('loading').innerHTML = '<p style="color:#dc3545;">Failed to load doctors. Please refresh the page.</p>';
            }
        }
        
        function createDoctorCard(doctor) {
            const card = document.createElement('div');
            card.className = 'doctor-card';
            card.onclick = () => selectDoctor(doctor, card);
            
            const initials = doctor.name.split(' ').map(n => n[0]).join('');
            const stars = '⭐'.repeat(Math.floor(doctor.rating));
            
            card.innerHTML = `
                <div class="doctor-header">
                    <div class="doctor-image">${initials}</div>
                    <div class="doctor-info">
                        <h3>${doctor.name}</h3>
                        <div class="doctor-specialty">${doctor.specialty}</div>
                        <div class="doctor-rating">${stars} ${doctor.rating} (${doctor.total_patients} patients)</div>
                    </div>
                </div>
                <div class="doctor-details">
                    <div class="doctor-detail-item">
                        <i class="fas fa-graduation-cap"></i>
                        <span>${doctor.qualification}</span>
                    </div>
                    <div class="doctor-detail-item">
                        <i class="fas fa-briefcase-medical"></i>
                        <span>${doctor.experience} years experience</span>
                    </div>
                    <div class="doctor-detail-item">
                        <i class="fas fa-phone"></i>
                        <span>${doctor.phone}</span>
                    </div>
                    <div class="doctor-detail-item">
                        <i class="fas fa-hospital"></i>
                        <span>${doctor.hospital}</span>
                    </div>
                    <div class="doctor-detail-item">
                        <i class="fas fa-dollar-sign"></i>
                        <span>Consultation: $${doctor.consultation_fee}</span>
                    </div>
                    <div class="doctor-detail-item">
                        <i class="fas fa-calendar-alt"></i>
                        <span>Available: ${doctor.available_days}</span>
                    </div>
                </div>
                <div class="doctor-actions">
                    <button class="btn btn-primary" onclick="selectDoctor(${JSON.stringify(doctor).replace(/"/g, '&quot;')}, this.parentElement.parentElement); event.stopPropagation();">
                        <i class="fas fa-calendar-plus"></i> Book Appointment
                    </button>
                </div>
            `;
            
            return card;
        }
        
        function selectDoctor(doctor, cardElement) {
            selectedDoctor = doctor;
            
            // Remove previous selection
            document.querySelectorAll('.doctor-card').forEach(c => c.classList.remove('selected'));
            cardElement.classList.add('selected');
            
            // Fill form
            document.getElementById('doctorId').value = doctor.id;
            document.getElementById('doctorName').value = doctor.name;
            document.getElementById('specialty').value = doctor.specialty;
            
            // Show booking form
            document.getElementById('bookingForm').style.display = 'block';
            
            // Show selected doctor info
            const info = document.getElementById('selectedDoctorInfo');
            info.innerHTML = `
                <div class="info message" style="display:block;">
                    <i class="fas fa-info-circle"></i> Booking appointment with <strong>${doctor.name}</strong> (${doctor.specialty})
                </div>
            `;
            
            // Scroll to form
            document.getElementById('bookingForm').scrollIntoView({ behavior: 'smooth' });
        }
        
        // Handle appointment form submission
        document.getElementById('appointmentForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            if (!selectedDoctor) {
                showMessage('Please select a doctor first', 'error');
                return;
            }
            
            const appointmentData = {
                doctor_id: document.getElementById('doctorId').value,
                doctor_name: document.getElementById('doctorName').value,
                specialty: document.getElementById('specialty').value,
                appointment_date: document.getElementById('appointmentDate').value,
                appointment_time: document.getElementById('appointmentTime').value,
                symptoms: document.getElementById('symptoms').value
            };
            
            try {
                const response = await fetch('/api/appointments', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(appointmentData)
                });
                
                const data = await response.json();
                
                if (data.success) {
                    showMessage(data.message, 'success');
                    setTimeout(() => { location.reload(); }, 2000);
                } else {
                    showMessage(data.message, 'error');
                }
            } catch (error) {
                showMessage('Booking failed. Please try again.', 'error');
            }
        });
        
        function showMessage(text, type) {
            const messageDiv = document.getElementById('message');
            messageDiv.className = `message ${type}`;
            messageDiv.textContent = text;
            messageDiv.style.display = 'block';
            
            setTimeout(() => {
                messageDiv.style.display = 'none';
            }, 5000);
        }
    </script>
</body>
</html>
'''
