"""
Modern UI Templates with Glassmorphism, Animations, and Chart.js
Ultra-Professional Healthcare Web Application Design
"""

# Modern Landing Page with Animations
MODERN_INDEX_HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Healthcare Chatbot - Your Personal Health Assistant</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            overflow-x: hidden;
        }
        
        /* Animated background particles */
        .particles {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
            opacity: 0.3;
        }
        
        .particle {
            position: absolute;
            background: white;
            border-radius: 50%;
            animation: float 15s infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0) translateX(0); }
            25% { transform: translateY(-100px) translateX(50px); }
            50% { transform: translateY(-200px) translateX(-50px); }
            75% { transform: translateY(-100px) translateX(100px); }
        }
        
        /* Glassmorphism navbar */
        .navbar {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.2);
            padding: 20px 0;
            z-index: 1000;
            animation: slideDown 0.5s ease;
        }
        
        @keyframes slideDown {
            from { transform: translateY(-100%); }
            to { transform: translateY(0); }
        }
        
        .nav-content {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .logo {
            font-size: 1.8em;
            font-weight: 700;
            color: white;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .logo i {
            font-size: 1.2em;
        }
        
        .nav-links {
            display: flex;
            gap: 30px;
        }
        
        .nav-links a {
            color: white;
            text-decoration: none;
            font-weight: 500;
            transition: all 0.3s;
            padding: 10px 20px;
            border-radius: 25px;
        }
        
        .nav-links a:hover {
            background: rgba(255, 255, 255, 0.2);
            transform: translateY(-2px);
        }
        
        .btn-primary {
            background: white;
            color: #667eea !important;
            padding: 12px 30px !important;
            border-radius: 25px;
            font-weight: 600;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        }
        
        .btn-primary:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        }
        
        /* Hero Section */
        .hero {
            position: relative;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 100px 30px 50px;
            z-index: 1;
        }
        
        .hero-content {
            max-width: 1200px;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 60px;
            align-items: center;
        }
        
        .hero-text {
            animation: fadeInLeft 1s ease;
        }
        
        @keyframes fadeInLeft {
            from {
                opacity: 0;
                transform: translateX(-50px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        .hero-text h1 {
            font-size: 3.5em;
            color: white;
            margin-bottom: 20px;
            line-height: 1.2;
            font-weight: 700;
        }
        
        .hero-text .highlight {
            background: linear-gradient(135deg, #ffd89b 0%, #19547b 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .hero-text p {
            font-size: 1.3em;
            color: rgba(255, 255, 255, 0.9);
            margin-bottom: 40px;
            line-height: 1.6;
        }
        
        .hero-buttons {
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
        }
        
        .btn {
            padding: 15px 40px;
            border-radius: 30px;
            font-size: 1.1em;
            font-weight: 600;
            text-decoration: none;
            transition: all 0.3s;
            border: none;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 10px;
        }
        
        .btn-white {
            background: white;
            color: #667eea;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }
        
        .btn-white:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
        }
        
        .btn-outline {
            background: transparent;
            color: white;
            border: 2px solid white;
        }
        
        .btn-outline:hover {
            background: white;
            color: #667eea;
            transform: translateY(-3px);
        }
        
        /* Hero Image Card */
        .hero-image {
            animation: fadeInRight 1s ease;
        }
        
        @keyframes fadeInRight {
            from {
                opacity: 0;
                transform: translateX(50px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        .glass-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 30px;
            padding: 40px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            animation: float-card 6s ease-in-out infinite;
        }
        
        @keyframes float-card {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-20px); }
        }
        
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
        }
        
        .feature-item {
            background: rgba(255, 255, 255, 0.15);
            padding: 25px;
            border-radius: 20px;
            text-align: center;
            transition: all 0.3s;
        }
        
        .feature-item:hover {
            background: rgba(255, 255, 255, 0.25);
            transform: scale(1.05);
        }
        
        .feature-item i {
            font-size: 2.5em;
            color: white;
            margin-bottom: 15px;
            display: block;
        }
        
        .feature-item h4 {
            color: white;
            font-size: 1.1em;
            margin-bottom: 8px;
        }
        
        .feature-item p {
            color: rgba(255, 255, 255, 0.8);
            font-size: 0.9em;
        }
        
        /* Features Section */
        .features-section {
            position: relative;
            padding: 100px 30px;
            background: white;
            z-index: 1;
        }
        
        .section-header {
            text-align: center;
            max-width: 700px;
            margin: 0 auto 60px;
        }
        
        .section-header h2 {
            font-size: 2.5em;
            color: #333;
            margin-bottom: 20px;
            font-weight: 700;
        }
        
        .section-header p {
            font-size: 1.2em;
            color: #666;
            line-height: 1.6;
        }
        
        .features-container {
            max-width: 1200px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
        }
        
        .feature-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px;
            border-radius: 20px;
            color: white;
            transition: all 0.3s;
            cursor: pointer;
        }
        
        .feature-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(102, 126, 234, 0.4);
        }
        
        .feature-card i {
            font-size: 3em;
            margin-bottom: 20px;
            display: block;
        }
        
        .feature-card h3 {
            font-size: 1.5em;
            margin-bottom: 15px;
        }
        
        .feature-card p {
            font-size: 1em;
            line-height: 1.6;
            opacity: 0.9;
        }
        
        /* Statistics Section */
        .stats-section {
            padding: 80px 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        .stats-container {
            max-width: 1200px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 40px;
        }
        
        .stat-card {
            text-align: center;
            color: white;
        }
        
        .stat-number {
            font-size: 3.5em;
            font-weight: 700;
            margin-bottom: 10px;
            animation: countUp 2s ease;
        }
        
        @keyframes countUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .stat-label {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        /* Footer */
        .footer {
            background: #1a1a2e;
            color: white;
            padding: 50px 30px 30px;
            text-align: center;
        }
        
        .footer-content {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .footer p {
            margin-bottom: 20px;
            opacity: 0.8;
        }
        
        .social-links {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 20px;
        }
        
        .social-links a {
            color: white;
            font-size: 1.5em;
            transition: all 0.3s;
        }
        
        .social-links a:hover {
            transform: translateY(-5px);
            color: #667eea;
        }
        
        /* Responsive */
        @media (max-width: 968px) {
            .hero-content {
                grid-template-columns: 1fr;
                text-align: center;
            }
            
            .hero-text h1 {
                font-size: 2.5em;
            }
            
            .hero-buttons {
                justify-content: center;
            }
            
            .nav-links {
                display: none;
            }
        }
    </style>
</head>
<body>
    <!-- Animated Particles -->
    <div class="particles" id="particles"></div>
    
    <!-- Navbar -->
    <nav class="navbar">
        <div class="nav-content">
            <div class="logo">
                <i class="fas fa-heartbeat"></i>
                AI Healthcare Chatbot
            </div>
            <div class="nav-links">
                <a href="#features">Features</a>
                <a href="#about">About</a>
                <a href="/login">Login</a>
                <a href="/register" class="btn-primary">Get Started</a>
            </div>
        </div>
    </nav>
    
    <!-- Hero Section -->
    <section class="hero">
        <div class="hero-content">
            <div class="hero-text">
                <h1>
                    Your Health,<br>
                    <span class="highlight">Simplified</span>
                </h1>
                <p>
                    Experience the future of healthcare with our AI-powered platform. 
                    Get instant medical advice, book appointments, and manage your health records - all in one place.
                </p>
                <div class="hero-buttons">
                    <a href="/register" class="btn btn-white">
                        <i class="fas fa-rocket"></i>
                        Start Free Trial
                    </a>
                    <a href="/login" class="btn btn-outline">
                        <i class="fas fa-sign-in-alt"></i>
                        Sign In
                    </a>
                </div>
            </div>
            
            <div class="hero-image">
                <div class="glass-card">
                    <div class="feature-grid">
                        <div class="feature-item">
                            <i class="fas fa-robot"></i>
                            <h4>AI Assistant</h4>
                            <p>24/7 Support</p>
                        </div>
                        <div class="feature-item">
                            <i class="fas fa-calendar-check"></i>
                            <h4>Appointments</h4>
                            <p>Easy Booking</p>
                        </div>
                        <div class="feature-item">
                            <i class="fas fa-file-medical"></i>
                            <h4>Records</h4>
                            <p>Digital Health</p>
                        </div>
                        <div class="feature-item">
                            <i class="fas fa-chart-line"></i>
                            <h4>Analytics</h4>
                            <p>Track Progress</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    
    <!-- Features Section -->
    <section class="features-section" id="features">
        <div class="section-header">
            <h2>Powerful Features</h2>
            <p>Everything you need to manage your health in one powerful platform</p>
        </div>
        
        <div class="features-container">
            <div class="feature-card">
                <i class="fas fa-comments"></i>
                <h3>AI Health Chat</h3>
                <p>Get instant answers to your health questions from our AI assistant, available 24/7.</p>
            </div>
            
            <div class="feature-card">
                <i class="fas fa-calendar-alt"></i>
                <h3>Smart Booking</h3>
                <p>Book appointments with specialists instantly. No waiting, no hassle.</p>
            </div>
            
            <div class="feature-card">
                <i class="fas fa-pills"></i>
                <h3>Prescription Tracking</h3>
                <p>Never miss a dose. Track your medications and get refill reminders.</p>
            </div>
            
            <div class="feature-card">
                <i class="fas fa-heartbeat"></i>
                <h3>Vital Signs Monitor</h3>
                <p>Track your blood pressure, heart rate, and more with beautiful charts.</p>
            </div>
            
            <div class="feature-card">
                <i class="fas fa-flask"></i>
                <h3>Lab Reports</h3>
                <p>Access all your lab results in one place with trend analysis.</p>
            </div>
            
            <div class="feature-card">
                <i class="fas fa-lock"></i>
                <h3>Secure & Private</h3>
                <p>Your data is encrypted and protected with bank-level security.</p>
            </div>
        </div>
    </section>
    
    <!-- Statistics Section -->
    <section class="stats-section">
        <div class="stats-container">
            <div class="stat-card">
                <div class="stat-number">50K+</div>
                <div class="stat-label">Active Users</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">100K+</div>
                <div class="stat-label">Consultations</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">500+</div>
                <div class="stat-label">Doctors</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">99%</div>
                <div class="stat-label">Satisfaction</div>
            </div>
        </div>
    </section>
    
    <!-- Footer -->
    <footer class="footer">
        <div class="footer-content">
            <div class="logo" style="justify-content: center; margin-bottom: 20px;">
                <i class="fas fa-heartbeat"></i>
                HealthCare Pro
            </div>
            <p>Your trusted partner in health management</p>
            <p>&copy; 2026 AI Healthcare Chatbot. All rights reserved.</p>
            <div class="social-links">
                <a href="#"><i class="fab fa-facebook"></i></a>
                <a href="#"><i class="fab fa-twitter"></i></a>
                <a href="#"><i class="fab fa-instagram"></i></a>
                <a href="#"><i class="fab fa-linkedin"></i></a>
            </div>
        </div>
    </footer>
    
    <script>
        // Create animated particles
        const particlesContainer = document.getElementById('particles');
        for (let i = 0; i < 50; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.width = Math.random() * 5 + 'px';
            particle.style.height = particle.style.width;
            particle.style.left = Math.random() * 100 + '%';
            particle.style.top = Math.random() * 100 + '%';
            particle.style.animationDelay = Math.random() * 15 + 's';
            particle.style.animationDuration = (Math.random() * 10 + 10) + 's';
            particlesContainer.appendChild(particle);
        }
        
        // Smooth scrolling
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            });
        });
        
        // Navbar background on scroll
        window.addEventListener('scroll', () => {
            const navbar = document.querySelector('.navbar');
            if (window.scrollY > 50) {
                navbar.style.background = 'rgba(102, 126, 234, 0.95)';
            } else {
                navbar.style.background = 'rgba(255, 255, 255, 0.1)';
            }
        });
    </script>
</body>
</html>
'''



# Modern Dashboard with Chart.js
MODERN_DASHBOARD_HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - AI Healthcare Chatbot</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        :root {
            --primary: #667eea;
            --secondary: #764ba2;
            --bg: #f5f7fa;
            --card-bg: white;
            --text: #333;
            --text-light: #666;
            --border: #e0e0e0;
        }
        
        [data-theme="dark"] {
            --bg: #1a1a2e;
            --card-bg: #16213e;
            --text: #f5f7fa;
            --text-light: #b8c1ec;
            --border: #0f3460;
        }
        
        body {
            font-family: 'Poppins', sans-serif;
            background: var(--bg);
            color: var(--text);
            transition: all 0.3s;
        }
        
        /* Modern Navbar */
        .navbar {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
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
            align-items: center;
        }
        
        .nav-links a, .theme-toggle {
            color: white;
            text-decoration: none;
            padding: 10px 20px;
            border-radius: 10px;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .nav-links a:hover {
            background: rgba(255,255,255,0.2);
        }
        
        .theme-toggle {
            cursor: pointer;
            background: rgba(255,255,255,0.1);
            border: none;
            font-size: 1em;
        }
        
        /* Main Container */
        .container {
            max-width: 1400px;
            margin: 30px auto;
            padding: 0 30px;
        }
        
        /* Welcome Section */
        .welcome-section {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            padding: 40px;
            border-radius: 20px;
            color: white;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
            animation: fadeIn 0.5s;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .welcome-section h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .welcome-section p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        /* Stats Grid */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: var(--card-bg);
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            transition: all 0.3s;
            animation: slideUp 0.5s;
        }
        
        @keyframes slideUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
        }
        
        .stat-icon {
            width: 60px;
            height: 60px;
            border-radius: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.8em;
            margin-bottom: 15px;
        }
        
        .stat-icon.blue { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
        .stat-icon.green { background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); color: white; }
        .stat-icon.orange { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; }
        .stat-icon.purple { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; }
        
        .stat-value {
            font-size: 2.5em;
            font-weight: 700;
            color: var(--primary);
            margin-bottom: 5px;
        }
        
        .stat-label {
            color: var(--text-light);
            font-size: 1em;
        }
        
        /* Charts Section */
        .charts-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .chart-card {
            background: var(--card-bg);
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        }
        
        .chart-card h3 {
            margin-bottom: 20px;
            color: var(--text);
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .chart-card h3 i {
            color: var(--primary);
        }
        
        /* Recent Activity */
        .activity-section {
            background: var(--card-bg);
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        }
        
        .activity-section h2 {
            margin-bottom: 25px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .activity-item {
            padding: 20px;
            background: var(--bg);
            border-radius: 10px;
            margin-bottom: 15px;
            border-left: 4px solid var(--primary);
            transition: all 0.3s;
        }
        
        .activity-item:hover {
            transform: translateX(5px);
            box-shadow: 0 3px 10px rgba(102, 126, 234, 0.2);
        }
        
        .activity-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
        }
        
        .activity-title {
            font-weight: 600;
            color: var(--text);
        }
        
        .activity-date {
            color: var(--text-light);
            font-size: 0.9em;
        }
        
        .status-badge {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 500;
        }
        
        .status-pending { background: #fff3cd; color: #856404; }
        .status-confirmed { background: #d4edda; color: #155724; }
        .status-completed { background: #d1ecf1; color: #0c5460; }
        
        /* Loading Animation */
        .loading {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0,0,0,0.5);
            z-index: 9999;
            align-items: center;
            justify-content: center;
        }
        
        .loading.active { display: flex; }
        
        .spinner {
            width: 50px;
            height: 50px;
            border: 5px solid rgba(255,255,255,0.3);
            border-top-color: white;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        @media (max-width: 768px) {
            .charts-grid { grid-template-columns: 1fr; }
            .welcome-section h1 { font-size: 1.8em; }
            .nav-links { display: none; }
        }
    </style>
</head>
<body data-theme="light">
    <!-- Loading Animation -->
    <div class="loading" id="loading">
        <div class="spinner"></div>
    </div>
    
    <!-- Navbar -->
    <nav class="navbar">
        <div class="nav-content">
            <div class="logo">
                <i class="fas fa-heartbeat"></i>
                AI Healthcare Chatbot
            </div>
            <div class="nav-links">
                <a href="/dashboard"><i class="fas fa-home"></i> Dashboard</a>
                <a href="/chat"><i class="fas fa-comments"></i> AI Chat</a>
                <a href="/appointments"><i class="fas fa-calendar"></i> Appointments</a>
                <a href="/vital-signs"><i class="fas fa-heartbeat"></i> Vitals</a>
                <a href="/files"><i class="fas fa-file-medical"></i> Files</a>
                <button class="theme-toggle" onclick="toggleTheme()">
                    <i class="fas fa-moon" id="themeIcon"></i>
                </button>
                <a href="/logout"><i class="fas fa-sign-out-alt"></i> Logout</a>
            </div>
        </div>
    </nav>
    
    <!-- Main Container -->
    <div class="container">
        <!-- Welcome Section -->
        <div class="welcome-section">
            <h1>Welcome back, {{ user_name }}! 👋</h1>
            <p>Here's your health overview for today</p>
        </div>
        
        <!-- Stats Grid -->
        <div class="stats-grid">
            <div class="stat-card" style="animation-delay: 0.1s">
                <div class="stat-icon blue">
                    <i class="fas fa-calendar-check"></i>
                </div>
                <div class="stat-value">{{ total_appointments }}</div>
                <div class="stat-label">Total Appointments</div>
            </div>
            
            <div class="stat-card" style="animation-delay: 0.2s">
                <div class="stat-icon green">
                    <i class="fas fa-comments"></i>
                </div>
                <div class="stat-value">{{ total_chats }}</div>
                <div class="stat-label">AI Consultations</div>
            </div>
            
            <div class="stat-card" style="animation-delay: 0.3s">
                <div class="stat-icon orange">
                    <i class="fas fa-heartbeat"></i>
                </div>
                <div class="stat-value" id="healthScore">95</div>
                <div class="stat-label">Health Score</div>
            </div>
            
            <div class="stat-card" style="animation-delay: 0.4s">
                <div class="stat-icon purple">
                    <i class="fas fa-chart-line"></i>
                </div>
                <div class="stat-value">Excellent</div>
                <div class="stat-label">Overall Status</div>
            </div>
        </div>
        
        <!-- Charts Section -->
        <div class="charts-grid">
            <div class="chart-card">
                <h3><i class="fas fa-heartbeat"></i> Vital Signs Trends</h3>
                <canvas id="vitalsChart"></canvas>
            </div>
            
            <div class="chart-card">
                <h3><i class="fas fa-calendar-alt"></i> Appointments Overview</h3>
                <canvas id="appointmentsChart"></canvas>
            </div>
        </div>
        
        <!-- Recent Activity -->
        <div class="activity-section">
            <h2><i class="fas fa-clock"></i> Recent Activity</h2>
            {% if recent_appointments %}
                {% for apt in recent_appointments %}
                <div class="activity-item">
                    <div class="activity-header">
                        <div class="activity-title">
                            <i class="fas fa-user-md"></i> {{ apt[0] }} - {{ apt[1] }}
                        </div>
                        <span class="status-badge status-{{ apt[4] }}">{{ apt[4] }}</span>
                    </div>
                    <div class="activity-date">
                        <i class="far fa-calendar"></i> {{ apt[2] }} at {{ apt[3] }}
                    </div>
                </div>
                {% endfor %}
            {% else %}
                <p style="color: var(--text-light); text-align: center; padding: 40px;">
                    <i class="fas fa-info-circle"></i> No recent activity. Start by booking an appointment or chatting with our AI!
                </p>
            {% endif %}
        </div>
    </div>
    
    <script>
        // Theme Toggle
        function toggleTheme() {
            const body = document.body;
            const currentTheme = body.getAttribute('data-theme');
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            body.setAttribute('data-theme', newTheme);
            
            const icon = document.getElementById('themeIcon');
            icon.className = newTheme === 'light' ? 'fas fa-moon' : 'fas fa-sun';
            
            localStorage.setItem('theme', newTheme);
            updateCharts();
        }
        
        // Load saved theme
        const savedTheme = localStorage.getItem('theme') || 'light';
        document.body.setAttribute('data-theme', savedTheme);
        if (savedTheme === 'dark') {
            document.getElementById('themeIcon').className = 'fas fa-sun';
        }
        
        // Chart colors based on theme
        function getChartColors() {
            const isDark = document.body.getAttribute('data-theme') === 'dark';
            return {
                primary: '#667eea',
                secondary: '#764ba2',
                success: '#38ef7d',
                text: isDark ? '#f5f7fa' : '#333',
                grid: isDark ? '#0f3460' : '#e0e0e0'
            };
        }
        
        // Create Charts
        let vitalsChart, appointmentsChart;
        
        function createCharts() {
            const colors = getChartColors();
            
            // Vitals Chart
            const vitalsCtx = document.getElementById('vitalsChart').getContext('2d');
            vitalsChart = new Chart(vitalsCtx, {
                type: 'line',
                data: {
                    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                    datasets: [{
                        label: 'Heart Rate (bpm)',
                        data: [72, 75, 70, 73, 71, 74, 72],
                        borderColor: colors.primary,
                        backgroundColor: colors.primary + '20',
                        tension: 0.4,
                        fill: true
                    }, {
                        label: 'Blood Pressure (sys)',
                        data: [120, 118, 122, 119, 121, 120, 119],
                        borderColor: colors.success,
                        backgroundColor: colors.success + '20',
                        tension: 0.4,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { labels: { color: colors.text } }
                    },
                    scales: {
                        y: {
                            beginAtZero: false,
                            ticks: { color: colors.text },
                            grid: { color: colors.grid }
                        },
                        x: {
                            ticks: { color: colors.text },
                            grid: { color: colors.grid }
                        }
                    }
                }
            });
            
            // Appointments Chart
            const appointmentsCtx = document.getElementById('appointmentsChart').getContext('2d');
            appointmentsChart = new Chart(appointmentsCtx, {
                type: 'doughnut',
                data: {
                    labels: ['Completed', 'Upcoming', 'Pending'],
                    datasets: [{
                        data: [{{ total_appointments }}, 2, 1],
                        backgroundColor: [colors.success, colors.primary, colors.secondary],
                        borderWidth: 0
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: { color: colors.text, padding: 15 }
                        }
                    }
                }
            });
        }
        
        function updateCharts() {
            if (vitalsChart) vitalsChart.destroy();
            if (appointmentsChart) appointmentsChart.destroy();
            createCharts();
        }
        
        // Initialize charts
        createCharts();
        
        // Animate health score
        let score = 0;
        const target = 95;
        const scoreElement = document.getElementById('healthScore');
        const duration = 2000;
        const increment = target / (duration / 16);
        
        function animateScore() {
            if (score < target) {
                score += increment;
                scoreElement.textContent = Math.round(score);
                requestAnimationFrame(animateScore);
            } else {
                scoreElement.textContent = target;
            }
        }
        
        animateScore();
    </script>
</body>
</html>
'''

# Files Upload Page
FILES_HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Files - AI Healthcare Chatbot</title>
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
        
        .nav-links { display: flex; gap: 5px; }
        .nav-links a {
            color: white;
            text-decoration: none;
            padding: 10px 20px;
            border-radius: 10px;
            transition: all 0.3s;
        }
        .nav-links a:hover { background: rgba(255,255,255,0.2); }
        
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
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .page-header h1 { font-size: 2.5em; }
        
        .upload-btn {
            background: white;
            color: #667eea;
            padding: 15px 30px;
            border: none;
            border-radius: 10px;
            font-size: 1.1em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .upload-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        .upload-section {
            background: white;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            display: none;
        }
        
        .upload-section.active { display: block; }
        
        .upload-area {
            border: 3px dashed #667eea;
            border-radius: 15px;
            padding: 40px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .upload-area:hover {
            background: #f8f9ff;
            border-color: #764ba2;
        }
        
        .upload-area i {
            font-size: 3em;
            color: #667eea;
            margin-bottom: 15px;
        }
        
        .files-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 20px;
        }
        
        .file-card {
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            transition: all 0.3s;
            text-align: center;
        }
        
        .file-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
        }
        
        .file-icon {
            font-size: 3em;
            margin-bottom: 15px;
        }
        
        .file-icon.pdf { color: #e74c3c; }
        .file-icon.image { color: #3498db; }
        .file-icon.doc { color: #2980b9; }
        
        .file-name {
            font-weight: 600;
            margin-bottom: 10px;
            word-break: break-all;
        }
        
        .file-date {
            color: #999;
            font-size: 0.9em;
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
                <a href="/files"><i class="fas fa-file-medical"></i> Files</a>
                <a href="/logout"><i class="fas fa-sign-out-alt"></i> Logout</a>
            </div>
        </div>
    </nav>
    
    <div class="container">
        <div class="page-header">
            <h1><i class="fas fa-folder-open"></i> My Medical Files</h1>
            <button class="upload-btn" onclick="toggleUpload()">
                <i class="fas fa-plus"></i> Upload File
            </button>
        </div>
        
        <div class="upload-section" id="uploadSection">
            <h2 style="margin-bottom: 20px;"><i class="fas fa-cloud-upload-alt"></i> Upload New File</h2>
            <form id="uploadForm" enctype="multipart/form-data">
                <div class="upload-area" onclick="document.getElementById('fileInput').click()">
                    <i class="fas fa-cloud-upload-alt"></i>
                    <h3>Click to upload or drag and drop</h3>
                    <p>PDF, PNG, JPG, DOC (Max 16MB)</p>
                </div>
                <input type="file" id="fileInput" style="display:none" accept=".pdf,.png,.jpg,.jpeg,.doc,.docx">
                <input type="text" id="description" placeholder="File description (optional)" style="width:100%; padding:15px; margin-top:15px; border:2px solid #e0e0e0; border-radius:10px; font-size:1em;">
                <button type="submit" class="upload-btn" style="margin-top:15px; width:100%;">
                    <i class="fas fa-upload"></i> Upload File
                </button>
            </form>
        </div>
        
        <div class="files-grid">
            {% if files %}
                {% for file in files %}
                <div class="file-card">
                    <div class="file-icon {% if 'pdf' in file[2] %}pdf{% elif 'image' in file[2] %}image{% else %}doc{% endif %}">
                        <i class="fas fa-file-{% if 'pdf' in file[2] %}pdf{% elif 'image' in file[2] %}image{% else %}word{% endif %}"></i>
                    </div>
                    <div class="file-name">{{ file[1] }}</div>
                    <div class="file-date">{{ file[4] }}</div>
                    {% if file[3] %}
                    <p style="color:#666; font-size:0.9em; margin-top:10px;">{{ file[3] }}</p>
                    {% endif %}
                </div>
                {% endfor %}
            {% else %}
                <div style="grid-column: 1/-1; text-align:center; padding:60px; color:#999;">
                    <i class="fas fa-folder-open" style="font-size:4em; margin-bottom:20px; opacity:0.3;"></i>
                    <p style="font-size:1.2em;">No files uploaded yet</p>
                </div>
            {% endif %}
        </div>
    </div>
    
    <script>
        function toggleUpload() {
            document.getElementById('uploadSection').classList.toggle('active');
        }
        
        document.getElementById('uploadForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const fileInput = document.getElementById('fileInput');
            const description = document.getElementById('description').value;
            
            if (!fileInput.files[0]) {
                alert('Please select a file');
                return;
            }
            
            const formData = new FormData();
            formData.append('file', fileInput.files[0]);
            formData.append('description', description);
            
            try {
                const response = await fetch('/upload', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                if (data.success) {
                    alert('File uploaded successfully!');
                    location.reload();
                } else {
                    alert(data.message);
                }
            } catch (error) {
                alert('Upload failed. Please try again.');
            }
        });
    </script>
</body>
</html>
'''
