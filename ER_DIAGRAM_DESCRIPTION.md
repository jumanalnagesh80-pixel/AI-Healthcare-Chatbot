# ENTITY RELATIONSHIP DIAGRAM
## AI Healthcare Chatbot Database Schema

### ER DIAGRAM DESCRIPTION

This document describes the complete Entity-Relationship diagram for the AI Healthcare Chatbot database. The database contains 13 tables with multiple relationships.

---

## ENTITIES AND ATTRIBUTES

### 1. USERS
**Primary Key:** user_id (INTEGER, AUTO_INCREMENT)

**Attributes:**
- user_id: INTEGER PRIMARY KEY AUTO_INCREMENT
- username: TEXT NOT NULL UNIQUE
- password_hash: TEXT NOT NULL
- email: TEXT
- role: TEXT NOT NULL DEFAULT 'patient' (Values: 'admin', 'patient')
- full_name: TEXT
- is_active: INTEGER DEFAULT 1 (1=Active, 0=Inactive)
- created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- last_login: TIMESTAMP

**Relationships:**
- One-to-One with PATIENTS (user_id)
- One-to-Many with ACTIVITY_LOG (user_id)
- One-to-One with DOCTORS (user_id)

---

### 2. PATIENTS
**Primary Key:** patient_id (INTEGER, AUTO_INCREMENT)

**Attributes:**
- patient_id: INTEGER PRIMARY KEY AUTO_INCREMENT
- user_id: INTEGER FOREIGN KEY REFERENCES users(user_id)
- name: TEXT NOT NULL
- age: INTEGER NOT NULL
- gender: TEXT NOT NULL (Values: 'Male', 'Female', 'Other')
- phone: TEXT NOT NULL UNIQUE
- email: TEXT
- address: TEXT
- blood_group: TEXT (Values: 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')
- allergies: TEXT
- chronic_conditions: TEXT
- created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

**Relationships:**
- Many-to-One with USERS (user_id)
- One-to-Many with APPOINTMENTS (patient_id)
- One-to-Many with PRESCRIPTIONS (patient_id)
- One-to-Many with LAB_REPORTS (patient_id)
- One-to-Many with VITAL_SIGNS (patient_id)
- One-to-Many with SYMPTOMS_LOG (patient_id)
- One-to-Many with CHAT_HISTORY (patient_id)
- One-to-Many with CONSULTATIONS (patient_id)
- One-to-Many with INSURANCE (patient_id)
- One-to-Many with EMERGENCY_CONTACTS (patient_id)

---

### 3. APPOINTMENTS
**Primary Key:** appointment_id (INTEGER, AUTO_INCREMENT)

**Attributes:**
- appointment_id: INTEGER PRIMARY KEY AUTO_INCREMENT
- patient_id: INTEGER NOT NULL FOREIGN KEY REFERENCES patients(patient_id)
- patient_name: TEXT NOT NULL
- specialty: TEXT NOT NULL
- appointment_date: DATE NOT NULL
- appointment_time: TEXT NOT NULL
- symptoms: TEXT
- status: TEXT DEFAULT 'Scheduled' (Values: 'Scheduled', 'Completed', 'Cancelled')
- created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

**Relationships:**
- Many-to-One with PATIENTS (patient_id)
- One-to-One with CONSULTATIONS (appointment_id)

---

### 4. PRESCRIPTIONS
**Primary Key:** prescription_id (INTEGER, AUTO_INCREMENT)

**Attributes:**
- prescription_id: INTEGER PRIMARY KEY AUTO_INCREMENT
- patient_id: INTEGER NOT NULL FOREIGN KEY REFERENCES patients(patient_id)
- doctor_name: TEXT NOT NULL
- medication_name: TEXT NOT NULL
- dosage: TEXT NOT NULL
- frequency: TEXT NOT NULL
- duration_days: INTEGER NOT NULL
- instructions: TEXT
- start_date: DATE NOT NULL
- end_date: DATE
- status: TEXT DEFAULT 'Active' (Values: 'Active', 'Completed', 'Expired')
- refills_remaining: INTEGER DEFAULT 0
- side_effects: TEXT
- created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

**Relationships:**
- Many-to-One with PATIENTS (patient_id)

---

### 5. LAB_REPORTS
**Primary Key:** report_id (INTEGER, AUTO_INCREMENT)

**Attributes:**
- report_id: INTEGER PRIMARY KEY AUTO_INCREMENT
- patient_id: INTEGER NOT NULL FOREIGN KEY REFERENCES patients(patient_id)
- report_type: TEXT NOT NULL
- test_name: TEXT NOT NULL
- test_date: DATE NOT NULL
- result_value: TEXT
- normal_range: TEXT
- status: TEXT DEFAULT 'Normal' (Values: 'Normal', 'Abnormal', 'Critical')
- notes: TEXT
- uploaded_by: INTEGER FOREIGN KEY REFERENCES users(user_id)
- file_path: TEXT
- created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

**Relationships:**
- Many-to-One with PATIENTS (patient_id)
- Many-to-One with USERS (uploaded_by)

---

### 6. VITAL_SIGNS
**Primary Key:** vital_id (INTEGER, AUTO_INCREMENT)

**Attributes:**
- vital_id: INTEGER PRIMARY KEY AUTO_INCREMENT
- patient_id: INTEGER NOT NULL FOREIGN KEY REFERENCES patients(patient_id)
- blood_pressure_systolic: INTEGER
- blood_pressure_diastolic: INTEGER
- heart_rate: INTEGER
- temperature: REAL
- oxygen_saturation: INTEGER
- glucose_level: INTEGER
- weight: REAL
- height: REAL
- bmi: REAL
- recorded_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- notes: TEXT

**Relationships:**
- Many-to-One with PATIENTS (patient_id)

---

### 7. SYMPTOMS_LOG
**Primary Key:** log_id (INTEGER, AUTO_INCREMENT)

**Attributes:**
- log_id: INTEGER PRIMARY KEY AUTO_INCREMENT
- patient_id: INTEGER FOREIGN KEY REFERENCES patients(patient_id)
- symptoms: TEXT NOT NULL
- severity: TEXT
- possible_conditions: TEXT
- advice: TEXT
- logged_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

**Relationships:**
- Many-to-One with PATIENTS (patient_id)

---

### 8. CHAT_HISTORY
**Primary Key:** chat_id (INTEGER, AUTO_INCREMENT)

**Attributes:**
- chat_id: INTEGER PRIMARY KEY AUTO_INCREMENT
- session_id: TEXT NOT NULL
- patient_id: INTEGER FOREIGN KEY REFERENCES patients(patient_id)
- message_type: TEXT NOT NULL (Values: 'user', 'bot')
- message: TEXT NOT NULL
- timestamp: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

**Relationships:**
- Many-to-One with PATIENTS (patient_id)

---

### 9. ACTIVITY_LOG
**Primary Key:** activity_id (INTEGER, AUTO_INCREMENT)

**Attributes:**
- activity_id: INTEGER PRIMARY KEY AUTO_INCREMENT
- user_id: INTEGER FOREIGN KEY REFERENCES users(user_id)
- activity_type: TEXT NOT NULL
- description: TEXT NOT NULL
- ip_address: TEXT
- timestamp: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

**Relationships:**
- Many-to-One with USERS (user_id)

---

### 10. CONSULTATIONS
**Primary Key:** consultation_id (INTEGER, AUTO_INCREMENT)

**Attributes:**
- consultation_id: INTEGER PRIMARY KEY AUTO_INCREMENT
- patient_id: INTEGER NOT NULL FOREIGN KEY REFERENCES patients(patient_id)
- doctor_id: INTEGER FOREIGN KEY REFERENCES users(user_id)
- appointment_id: INTEGER FOREIGN KEY REFERENCES appointments(appointment_id)
- consultation_date: DATE NOT NULL
- consultation_time: TEXT NOT NULL
- duration_minutes: INTEGER DEFAULT 30
- meeting_link: TEXT
- status: TEXT DEFAULT 'Scheduled' (Values: 'Scheduled', 'Completed', 'Cancelled')
- notes: TEXT
- recording_path: TEXT
- created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

**Relationships:**
- Many-to-One with PATIENTS (patient_id)
- Many-to-One with DOCTORS (doctor_id)
- One-to-One with APPOINTMENTS (appointment_id)

---

### 11. DOCTORS
**Primary Key:** doctor_id (INTEGER, AUTO_INCREMENT)

**Attributes:**
- doctor_id: INTEGER PRIMARY KEY AUTO_INCREMENT
- user_id: INTEGER FOREIGN KEY REFERENCES users(user_id)
- full_name: TEXT NOT NULL
- specialty: TEXT NOT NULL
- qualification: TEXT NOT NULL
- experience_years: INTEGER
- license_number: TEXT UNIQUE NOT NULL
- phone: TEXT
- email: TEXT
- consultation_fee: REAL
- rating: REAL DEFAULT 0.0
- total_reviews: INTEGER DEFAULT 0
- available_days: TEXT
- bio: TEXT
- profile_image: TEXT
- is_active: INTEGER DEFAULT 1
- created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

**Relationships:**
- One-to-One with USERS (user_id)
- One-to-Many with CONSULTATIONS (doctor_id)

---

### 12. INSURANCE
**Primary Key:** insurance_id (INTEGER, AUTO_INCREMENT)

**Attributes:**
- insurance_id: INTEGER PRIMARY KEY AUTO_INCREMENT
- patient_id: INTEGER NOT NULL FOREIGN KEY REFERENCES patients(patient_id)
- provider_name: TEXT NOT NULL
- policy_number: TEXT NOT NULL
- group_number: TEXT
- coverage_type: TEXT
- start_date: DATE
- end_date: DATE
- status: TEXT DEFAULT 'Active' (Values: 'Active', 'Expired', 'Pending')
- copay_amount: REAL
- deductible: REAL
- notes: TEXT
- created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

**Relationships:**
- Many-to-One with PATIENTS (patient_id)

---

### 13. EMERGENCY_CONTACTS
**Primary Key:** contact_id (INTEGER, AUTO_INCREMENT)

**Attributes:**
- contact_id: INTEGER PRIMARY KEY AUTO_INCREMENT
- patient_id: INTEGER NOT NULL FOREIGN KEY REFERENCES patients(patient_id)
- contact_name: TEXT NOT NULL
- relationship: TEXT NOT NULL
- phone: TEXT NOT NULL
- email: TEXT
- address: TEXT
- is_primary: INTEGER DEFAULT 0 (1=Primary, 0=Secondary)
- created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

**Relationships:**
- Many-to-One with PATIENTS (patient_id)

---

## RELATIONSHIP SUMMARY

### One-to-One Relationships:
1. USERS ←→ PATIENTS (via user_id)
2. USERS ←→ DOCTORS (via user_id)
3. APPOINTMENTS ←→ CONSULTATIONS (via appointment_id)

### One-to-Many Relationships:
1. USERS → ACTIVITY_LOG (one user can have many activity logs)
2. PATIENTS → APPOINTMENTS (one patient can have many appointments)
3. PATIENTS → PRESCRIPTIONS (one patient can have many prescriptions)
4. PATIENTS → LAB_REPORTS (one patient can have many lab reports)
5. PATIENTS → VITAL_SIGNS (one patient can have many vital sign records)
6. PATIENTS → SYMPTOMS_LOG (one patient can have many symptom logs)
7. PATIENTS → CHAT_HISTORY (one patient can have many chat messages)
8. PATIENTS → CONSULTATIONS (one patient can have many consultations)
9. PATIENTS → INSURANCE (one patient can have many insurance records)
10. PATIENTS → EMERGENCY_CONTACTS (one patient can have many emergency contacts)
11. DOCTORS → CONSULTATIONS (one doctor can have many consultations)

### Many-to-Many Relationships:
None (All relationships are one-to-one or one-to-many)

---

## CARDINALITY NOTATION

```
USERS ||--|| PATIENTS : "has"
USERS ||--|| DOCTORS : "is"
USERS ||--o{ ACTIVITY_LOG : "performs"
PATIENTS ||--o{ APPOINTMENTS : "books"
PATIENTS ||--o{ PRESCRIPTIONS : "receives"
PATIENTS ||--o{ LAB_REPORTS : "has"
PATIENTS ||--o{ VITAL_SIGNS : "records"
PATIENTS ||--o{ SYMPTOMS_LOG : "logs"
PATIENTS ||--o{ CHAT_HISTORY : "has"
PATIENTS ||--o{ CONSULTATIONS : "schedules"
PATIENTS ||--o{ INSURANCE : "has"
PATIENTS ||--o{ EMERGENCY_CONTACTS : "has"
DOCTORS ||--o{ CONSULTATIONS : "conducts"
APPOINTMENTS ||--|| CONSULTATIONS : "includes"
```

Legend:
- ||--|| : One-to-One (mandatory both sides)
- ||--o{ : One-to-Many (one mandatory, many optional)

---

## DATABASE NORMALIZATION

The database follows Third Normal Form (3NF):

**First Normal Form (1NF):**
- All tables have primary keys
- All attributes contain atomic values
- No repeating groups

**Second Normal Form (2NF):**
- Meets 1NF requirements
- All non-key attributes fully dependent on primary key
- No partial dependencies

**Third Normal Form (3NF):**
- Meets 2NF requirements
- No transitive dependencies
- All non-key attributes depend only on primary key

---

## REFERENTIAL INTEGRITY CONSTRAINTS

**ON DELETE CASCADE:**
- When a PATIENT is deleted, all related APPOINTMENTS, PRESCRIPTIONS, LAB_REPORTS, VITAL_SIGNS, SYMPTOMS_LOG, CHAT_HISTORY, CONSULTATIONS, INSURANCE, and EMERGENCY_CONTACTS are automatically deleted

**ON DELETE RESTRICT:**
- When a USER is deleted, system checks for related PATIENTS or DOCTORS records
- ACTIVITY_LOG entries preserved for audit

**ON UPDATE CASCADE:**
- Updates to primary keys cascade to foreign keys
- Ensures referential integrity

---

## INDEX STRATEGY

**Primary Indexes:**
- All primary keys automatically indexed

**Foreign Key Indexes:**
- user_id in PATIENTS
- patient_id in all related tables
- doctor_id in CONSULTATIONS
- appointment_id in CONSULTATIONS

**Unique Indexes:**
- username in USERS
- phone in PATIENTS
- license_number in DOCTORS

**Performance Indexes:**
- created_at in all tables (for time-based queries)
- status in APPOINTMENTS, PRESCRIPTIONS, CONSULTATIONS
- specialty in DOCTORS
- test_date in LAB_REPORTS

---

## VISUAL ER DIAGRAM INSTRUCTIONS

To create the ER diagram:

1. **Draw 13 entities (rectangles):**
   - USERS, PATIENTS, APPOINTMENTS, PRESCRIPTIONS
   - LAB_REPORTS, VITAL_SIGNS, SYMPTOMS_LOG, CHAT_HISTORY
   - ACTIVITY_LOG, CONSULTATIONS, DOCTORS, INSURANCE, EMERGENCY_CONTACTS

2. **Connect with relationship lines:**
   - Use crow's foot notation
   - Show cardinality (1:1, 1:M, M:N)
   - Label relationships

3. **Add attributes inside entities:**
   - Underline primary keys
   - Mark foreign keys with (FK)
   - Show data types

4. **Color code:**
   - Core entities: Blue
   - Health record entities: Green
   - System entities: Yellow
   - Doctor-related: Purple

5. **Legend:**
   - Primary Key: Underlined
   - Foreign Key: (FK)
   - Mandatory: Solid line
   - Optional: Dashed line

---

This ER diagram represents a comprehensive healthcare database supporting patient management, medical records, prescriptions, lab results, vital signs monitoring, consultations, and administrative functions.
