"""
Enhanced Medical Knowledge Base for HealthAI
Comprehensive medical information for AI responses
"""

# Expanded Symptom Database
SYMPTOMS_DATABASE = {
    # Critical Symptoms - Require Immediate Attention
    'chest pain': {
        'severity': 'critical',
        'conditions': ['Heart Attack', 'Angina', 'Pulmonary Embolism', 'Aortic Dissection'],
        'description': 'Discomfort, pressure, or pain in the chest area',
        'advice': '⚠️ **MEDICAL EMERGENCY!** Call 911 immediately! This could be a heart attack. Do not drive yourself to the hospital.',
        'red_flags': ['Pain spreading to arm/jaw', 'Shortness of breath', 'Nausea', 'Sweating', 'Dizziness'],
        'when_to_call_911': 'Immediately if experiencing chest pain',
        'diagnostic_tests': ['ECG', 'Cardiac enzymes', 'Chest X-ray', 'CT scan']
    },
    'difficulty breathing': {
        'severity': 'critical',
        'conditions': ['Asthma attack', 'Heart failure', 'Pneumonia', 'Pulmonary embolism', 'COVID-19'],
        'description': 'Feeling unable to get enough air, labored breathing',
        'advice': '⚠️ **SEEK IMMEDIATE MEDICAL ATTENTION!** Call 911 if severe. This is a medical emergency.',
        'red_flags': ['Blue lips/face', 'Chest pain', 'Confusion', 'Unable to speak full sentences'],
        'when_to_call_911': 'Severe difficulty breathing, especially with chest pain or confusion',
        'home_care': 'Sit upright, stay calm, use inhaler if prescribed'
    },
    'severe bleeding': {
        'severity': 'critical',
        'conditions': ['Trauma', 'Internal bleeding', 'Blood clotting disorder'],
        'description': 'Heavy blood loss that doesn\'t stop with pressure',
        'advice': '⚠️ **CALL 911 IMMEDIATELY!** Apply direct pressure. Lie down and elevate the bleeding area if possible.',
        'red_flags': ['Bleeding that won\'t stop after 10 minutes of pressure', 'Blood spurting', 'Deep wounds'],
        'when_to_call_911': 'Any severe or uncontrolled bleeding',
        'first_aid': 'Apply direct pressure with clean cloth, elevate if possible'
    },
    
    # High Priority Symptoms
    'severe headache': {
        'severity': 'high',
        'conditions': ['Migraine', 'Meningitis', 'Brain hemorrhage', 'Stroke'],
        'description': 'Sudden, intense headache unlike normal headaches',
        'advice': 'Seek immediate medical attention if this is the "worst headache of your life" or comes with fever, stiff neck, confusion, or vision changes.',
        'red_flags': ['Sudden onset', 'Stiff neck', 'Fever', 'Confusion', 'Vision problems', 'Weakness'],
        'when_to_see_doctor': 'Within 1 hour if severe with red flags',
        'home_care': 'Rest in dark, quiet room. Cold compress. Stay hydrated.'
    },
    'high fever': {
        'severity': 'high',
        'conditions': ['Severe infection', 'COVID-19', 'Flu', 'Sepsis'],
        'description': 'Temperature above 103°F (39.4°C)',
        'advice': 'See a doctor if fever is over 103°F, lasts more than 3 days, or comes with severe symptoms.',
        'red_flags': ['Confusion', 'Difficulty breathing', 'Severe headache', 'Rash', 'Persistent vomiting'],
        'when_to_see_doctor': 'Same day if over 103°F or with concerning symptoms',
        'home_care': 'Rest, hydrate, acetaminophen/ibuprofen, cool compress'
    },
    
    # Moderate Priority Symptoms  
    'fever': {
        'severity': 'moderate',
        'conditions': ['Flu', 'COVID-19', 'Common cold', 'Infection'],
        'description': 'Elevated body temperature (100.4°F - 103°F / 38°C - 39.4°C)',
        'advice': 'Rest, stay hydrated, and monitor temperature. See doctor if fever persists for 3+ days or exceeds 103°F.',
        'red_flags': ['Over 103°F', 'Lasts more than 3 days', 'With rash', 'With confusion'],
        'when_to_see_doctor': 'If persists 3+ days or exceeds 103°F',
        'home_care': 'Rest, fluids (water, broth), acetaminophen or ibuprofen, light clothing, room temperature environment',
        'prevention': 'Wash hands frequently, stay away from sick people, get vaccinated'
    },
    'cough': {
        'severity': 'low-moderate',
        'conditions': ['Common cold', 'Bronchitis', 'Allergies', 'COVID-19', 'Pneumonia'],
        'description': 'Reflex to clear airways of mucus or irritants',
        'advice': 'Usually resolves in 2-3 weeks. See doctor if persistent, with blood, or accompanied by fever and shortness of breath.',
        'red_flags': ['Blood in cough', 'High fever', 'Difficulty breathing', 'Weight loss', 'Lasts over 3 weeks'],
        'when_to_see_doctor': 'If lasts over 2 weeks, bloody, or with severe symptoms',
        'home_care': 'Honey (for adults), plenty of fluids, humidifier, avoid irritants, rest',
        'prevention': 'Avoid smoking, wash hands, stay away from sick people'
    },
    'headache': {
        'severity': 'low-moderate',
        'conditions': ['Tension headache', 'Migraine', 'Dehydration', 'Stress', 'Sinusitis'],
        'description': 'Pain or discomfort in the head or face region',
        'advice': 'Rest in a quiet, dark room. Try over-the-counter pain relief. See doctor if severe, frequent, or unusual.',
        'red_flags': ['Sudden and severe', 'With fever and stiff neck', 'After head injury', 'With vision changes', 'Worst ever experienced'],
        'when_to_see_doctor': 'If severe, frequent, or with concerning symptoms',
        'home_care': 'Rest, hydration, OTC pain relievers (ibuprofen, acetaminophen), cold/hot compress, dark quiet room',
        'prevention': 'Regular sleep, hydration, stress management, avoid triggers'
    },
    'nausea': {
        'severity': 'moderate',
        'conditions': ['Gastroenteritis', 'Food poisoning', 'Migraine', 'Pregnancy', 'Motion sickness'],
        'description': 'Feeling of wanting to vomit, upset stomach',
        'advice': 'Sip clear fluids, eat bland foods (BRAT diet). See doctor if persistent, with severe pain, or signs of dehydration.',
        'red_flags': ['Severe abdominal pain', 'Blood in vomit', 'Signs of dehydration', 'Lasts over 48 hours'],
        'when_to_see_doctor': 'If persistent over 48 hours or with severe symptoms',
        'home_care': 'Clear liquids, BRAT diet (banana, rice, applesauce, toast), ginger, rest, avoid solid foods initially',
        'prevention': 'Food safety, hand washing, avoid triggers'
    },
    'fatigue': {
        'severity': 'low',
        'conditions': ['Anemia', 'Depression', 'Thyroid problems', 'Sleep disorders', 'Chronic fatigue syndrome'],
        'description': 'Persistent tiredness not relieved by rest',
        'advice': 'Ensure adequate sleep (7-9 hours), healthy diet, regular exercise. See doctor if persistent despite lifestyle changes.',
        'red_flags': ['Sudden onset', 'With weight loss', 'With fever', 'Severe and unrelenting'],
        'when_to_see_doctor': 'If persistent for weeks despite good sleep and diet',
        'home_care': 'Prioritize sleep, balanced diet, regular exercise, stress management, limit caffeine',
        'prevention': 'Regular sleep schedule, balanced diet, exercise, stress management'
    },
    'dizziness': {
        'severity': 'moderate',
        'conditions': ['Vertigo', 'Dehydration', 'Low blood pressure', 'Inner ear problem', 'Medication side effect'],
        'description': 'Feeling lightheaded, unsteady, or spinning sensation',
        'advice': 'Sit or lie down immediately. Stay hydrated. See doctor if frequent, severe, or with other concerning symptoms.',
        'red_flags': ['With chest pain', 'Severe headache', 'Double vision', 'Slurred speech', 'Numbness'],
        'when_to_see_doctor': 'If frequent, severe, or with concerning symptoms',
        'home_care': 'Sit/lie down, stay hydrated, avoid sudden movements, avoid driving',
        'prevention': 'Stay hydrated, rise slowly from sitting/lying, avoid alcohol'
    },
    'sore throat': {
        'severity': 'low',
        'conditions': ['Viral infection', 'Strep throat', 'Allergies', 'Dry air'],
        'description': 'Pain, scratchiness, or irritation of the throat',
        'advice': 'Rest, warm liquids, throat lozenges. See doctor if severe, persistent, or with high fever.',
        'red_flags': ['Difficulty breathing/swallowing', 'High fever', 'Rash', 'Joint pain', 'Lasts over a week'],
        'when_to_see_doctor': 'If severe, with high fever, or lasts over a week',
        'home_care': 'Warm liquids (tea with honey), salt water gargle, throat lozenges, humidifier, rest',
        'prevention': 'Hand washing, avoid sick people, don\'t share utensils'
    }
}

# Comprehensive Medication Database
MEDICATIONS_DATABASE = {
    # Pain Relievers & Anti-inflammatories
    'acetaminophen': {
        'brand_names': ['Tylenol', 'Panadol'],
        'category': 'Pain reliever / Fever reducer',
        'uses': ['Pain relief', 'Fever reduction', 'Headache', 'Muscle aches'],
        'how_it_works': 'Reduces pain signals in the brain and regulates body temperature',
        'dosage': 'Adults: 325-650mg every 4-6 hours, max 3000mg/day',
        'side_effects': ['Rare at normal doses', 'Liver damage with overdose'],
        'warnings': ['Do not exceed recommended dose', 'Avoid with alcohol', 'Check for acetaminophen in other medications'],
        'interactions': ['Alcohol (liver damage risk)', 'Warfarin (increased bleeding risk)'],
        'tips': 'Gentler on stomach than NSAIDs. Safe during pregnancy when used as directed.'
    },
    'ibuprofen': {
        'brand_names': ['Advil', 'Motrin'],
        'category': 'NSAID (Pain reliever / Anti-inflammatory)',
        'uses': ['Pain relief', 'Fever reduction', 'Inflammation', 'Arthritis'],
        'how_it_works': 'Blocks production of prostaglandins that cause pain and inflammation',
        'dosage': 'Adults: 200-400mg every 4-6 hours, max 1200mg/day (OTC)',
        'side_effects': ['Stomach upset', 'Heartburn', 'Dizziness', 'Rarely: ulcers, kidney problems'],
        'warnings': ['Take with food', 'Avoid if history of ulcers', 'Caution with heart disease', 'Not recommended during pregnancy'],
        'interactions': ['Aspirin', 'Blood thinners', 'ACE inhibitors', 'Diuretics'],
        'tips': 'Take with food or milk to reduce stomach upset. More effective for inflammation than acetaminophen.'
    },
    'aspirin': {
        'brand_names': ['Bayer', 'Bufferin', 'Ecotrin'],
        'category': 'NSAID (Pain reliever / Blood thinner)',
        'uses': ['Pain relief', 'Fever reduction', 'Heart attack prevention', 'Stroke prevention'],
        'how_it_works': 'Reduces pain/inflammation and prevents blood clots',
        'dosage': 'Pain: 325-650mg every 4 hours. Heart protection: 81-325mg daily (doctor prescribed)',
        'side_effects': ['Stomach upset', 'Bleeding risk', 'Heartburn', 'Ringing in ears (high doses)'],
        'warnings': ['Not for children (Reye\'s syndrome risk)', 'Bleeding risk', 'Take with food', 'Tell doctor before surgery'],
        'interactions': ['Blood thinners', 'NSAIDs', 'Corticosteroids', 'Alcohol'],
        'tips': 'Low-dose aspirin for heart protection should be taken daily as prescribed. Never stop suddenly without consulting doctor.'
    },
    
    # Blood Pressure Medications
    'lisinopril': {
        'brand_names': ['Prinivil', 'Zestril'],
        'category': 'ACE Inhibitor (Blood pressure medication)',
        'uses': ['High blood pressure', 'Heart failure', 'Post-heart attack'],
        'how_it_works': 'Relaxes blood vessels by blocking ACE enzyme',
        'dosage': 'Usually 10-40mg once daily (doctor prescribed)',
        'side_effects': ['Dry cough', 'Dizziness', 'Fatigue', 'Rarely: angioedema'],
        'warnings': ['Do not use during pregnancy', 'Monitor kidney function', 'Can cause high potassium'],
        'interactions': ['Potassium supplements', 'NSAIDs', 'Diuretics'],
        'tips': 'Take at same time daily. May take 2-4 weeks for full effect. Stand slowly to avoid dizziness.'
    },
    'amlodipine': {
        'brand_names': ['Norvasc'],
        'category': 'Calcium Channel Blocker (Blood pressure medication)',
        'uses': ['High blood pressure', 'Angina', 'Coronary artery disease'],
        'how_it_works': 'Relaxes blood vessels and improves blood flow',
        'dosage': 'Usually 5-10mg once daily',
        'side_effects': ['Swelling of ankles/feet', 'Dizziness', 'Flushing', 'Fatigue'],
        'warnings': ['May cause swelling', 'Avoid grapefruit juice'],
        'interactions': ['Grapefruit juice', 'Simvastatin (high doses)'],
        'tips': 'Can be taken with or without food. Report excessive swelling to doctor.'
    },
    
    # Diabetes Medications
    'metformin': {
        'brand_names': ['Glucophage', 'Fortamet'],
        'category': 'Diabetes medication (Biguanide)',
        'uses': ['Type 2 diabetes', 'Pre-diabetes', 'PCOS'],
        'how_it_works': 'Reduces glucose production in liver and improves insulin sensitivity',
        'dosage': 'Starting: 500mg once or twice daily with meals, gradually increase',
        'side_effects': ['Diarrhea', 'Nausea', 'Stomach upset', 'Vitamin B12 deficiency (long-term)'],
        'warnings': ['Take with food', 'Stop before contrast dye procedures', 'Monitor kidney function'],
        'interactions': ['Alcohol (lactic acidosis risk)', 'Contrast dye'],
        'tips': 'Take with meals to reduce stomach upset. Extended-release version causes less GI upset.'
    },
    
    # Cholesterol Medications
    'atorvastatin': {
        'brand_names': ['Lipitor'],
        'category': 'Statin (Cholesterol-lowering medication)',
        'uses': ['High cholesterol', 'Heart disease prevention'],
        'how_it_works': 'Blocks enzyme needed to produce cholesterol in liver',
        'dosage': 'Usually 10-80mg once daily',
        'side_effects': ['Muscle aches', 'Liver enzyme elevation', 'Rarely: rhabdomyolysis'],
        'warnings': ['Avoid during pregnancy', 'Monitor liver function', 'Report muscle pain/weakness'],
        'interactions': ['Grapefruit juice (large amounts)', 'Some antibiotics'],
        'tips': 'Can take any time of day with or without food. Report unexplained muscle pain immediately.'
    },
    
    # Stomach Acid Reducers
    'omeprazole': {
        'brand_names': ['Prilosec'],
        'category': 'Proton Pump Inhibitor (Acid reducer)',
        'uses': ['GERD', 'Ulcers', 'Heartburn', 'Zollinger-Ellison syndrome'],
        'how_it_works': 'Reduces stomach acid production',
        'dosage': 'Usually 20-40mg once daily before meal',
        'side_effects': ['Headache', 'Diarrhea', 'Nausea', 'Long-term: bone fracture risk, B12 deficiency'],
        'warnings': ['Long-term use concerns', 'May mask stomach cancer symptoms'],
        'interactions': ['Clopidogrel (reduced effectiveness)', 'Some antifungals'],
        'tips': 'Take 30-60 minutes before first meal of day. May take several days for full effect.'
    },
    
    # Antibiotics
    'amoxicillin': {
        'brand_names': ['Amoxil', 'Trimox'],
        'category': 'Antibiotic (Penicillin)',
        'uses': ['Bacterial infections', 'Strep throat', 'Ear infections', 'Urinary tract infections'],
        'how_it_works': 'Kills bacteria by interfering with cell wall formation',
        'dosage': 'Varies by infection, usually 250-500mg every 8 hours',
        'side_effects': ['Diarrhea', 'Nausea', 'Rash', 'Rarely: severe allergic reaction'],
        'warnings': ['Complete full course', 'Allergic reactions possible', 'May reduce birth control effectiveness'],
        'interactions': ['Birth control pills', 'Methotrexate'],
        'tips': 'Take with or without food. Complete entire course even if feeling better. Probiotics may help prevent diarrhea.'
    }
}

# Health Tips by Category
HEALTH_TIPS_COMPREHENSIVE = {
    'nutrition': [
        'Eat 5-9 servings of fruits and vegetables daily for optimal nutrition',
        'Choose whole grains over refined grains for better fiber intake',
        'Include lean protein sources like fish, chicken, beans, and legumes',
        'Limit processed foods high in sodium, sugar, and unhealthy fats',
        'Stay hydrated by drinking at least 8 glasses of water daily',
        'Practice portion control using smaller plates and mindful eating',
        'Include healthy fats from nuts, avocados, and olive oil',
        'Eat breakfast to kickstart your metabolism',
        'Limit added sugars to less than 25g daily',
        'Cook at home more often to control ingredients and portions'
    ],
    'exercise': [
        'Aim for 150 minutes of moderate aerobic activity weekly',
        'Include strength training exercises at least 2 days per week',
        'Take breaks to stand and stretch if you sit for long periods',
        'Find activities you enjoy to make exercise sustainable',
        'Start slowly and gradually increase intensity to avoid injury',
        'Warm up before and cool down after exercise',
        'Mix cardio, strength, and flexibility training for balance',
        'Exercise with a friend for motivation and accountability',
        'Set realistic fitness goals and track your progress',
        'Listen to your body and rest when needed'
    ],
    'sleep': [
        'Maintain a consistent sleep schedule, even on weekends',
        'Aim for 7-9 hours of quality sleep each night',
        'Create a relaxing bedtime routine to wind down',
        'Keep your bedroom cool, dark, and quiet',
        'Avoid screens 1 hour before bedtime (blue light disrupts sleep)',
        'Limit caffeine after 2 PM and avoid alcohol before bed',
        'Exercise regularly, but not close to bedtime',
        'Manage stress through relaxation techniques',
        'Avoid large meals and excessive fluids before bed',
        'Consider white noise or relaxation apps if needed'
    ],
    'mental_health': [
        'Practice mindfulness or meditation for 10-15 minutes daily',
        'Maintain social connections and meaningful relationships',
        'Seek professional help if experiencing persistent sadness or anxiety',
        'Practice gratitude by noting 3 things you\'re thankful for daily',
        'Limit social media use to reduce comparison and anxiety',
        'Set healthy boundaries in relationships and at work',
        'Engage in hobbies and activities you enjoy',
        'Practice self-compassion and avoid negative self-talk',
        'Take regular breaks from work and technology',
        'Consider therapy or counseling as preventive mental healthcare'
    ],
    'preventive_care': [
        'Schedule annual physical exams and health screenings',
        'Stay up-to-date with recommended vaccinations',
        'Practice good hand hygiene to prevent infections',
        'Use sunscreen daily to prevent skin damage and cancer',
        'Know your family medical history and share with your doctor',
        'Quit smoking and avoid secondhand smoke exposure',
        'Limit alcohol consumption to moderate levels',
        'Maintain a healthy weight through diet and exercise',
        'Monitor your blood pressure, cholesterol, and blood sugar',
        'Practice safe sex and get regular STI screenings if sexually active'
    ],
    'chronic_disease': [
        'Take medications exactly as prescribed by your doctor',
        'Keep a symptom journal to track patterns and triggers',
        'Attend all scheduled follow-up appointments',
        'Learn about your condition and treatment options',
        'Build a support network of family, friends, and support groups',
        'Make lifestyle modifications recommended by your healthcare team',
        'Communicate openly with your healthcare providers',
        'Create an emergency action plan for your condition',
        'Monitor relevant health metrics (blood pressure, glucose, etc.)',
        'Stay positive and focus on what you can control'
    ]
}

# First Aid Basics
FIRST_AID_GUIDE = {
    'cuts_scrapes': {
        'steps': [
            'Wash hands thoroughly',
            'Stop bleeding by applying gentle pressure with clean cloth',
            'Clean wound with water (soap if available)',
            'Apply antibiotic ointment',
            'Cover with sterile bandage',
            'Change bandage daily and watch for infection signs'
        ],
        'when_to_see_doctor': 'Deep, gaping, or won\'t stop bleeding after 10 min'
    },
    'burns': {
        'steps': [
            'First-degree: Run cool (not cold) water over burn for 10-20 minutes',
            'Gently pat dry with clean cloth',
            'Apply aloe vera or burn ointment',
            'Cover loosely with sterile gauze',
            'Take OTC pain reliever if needed'
        ],
        'when_to_see_doctor': 'Second or third degree, larger than 3 inches, on face/hands/joints'
    },
    'nosebleed': {
        'steps': [
            'Sit upright and lean slightly forward',
            'Pinch soft part of nose for 10 minutes',
            'Breathe through mouth',
            'Apply cold compress to bridge of nose',
            'Avoid blowing nose for several hours'
        ],
        'when_to_see_doctor': 'Doesn\'t stop after 20 minutes, frequent nosebleeds, after head injury'
    },
    'choking': {
        'steps': [
            'Encourage coughing if person can cough/speak',
            'Heimlich maneuver if can\'t breathe/speak',
            'Call 911 if unconscious',
            'Start CPR if trained and person becomes unconscious'
        ],
        'when_to_call_911': 'Person can\'t breathe, speak, or becomes unconscious'
    }
}

# When to See a Doctor vs ER
CARE_GUIDELINES = {
    'call_911': [
        'Chest pain or pressure',
        'Difficulty breathing or shortness of breath',
        'Sudden severe headache (worst ever)',
        'Slurred speech, drooping face, arm weakness (stroke signs)',
        'Heavy bleeding that won\'t stop',
        'Severe allergic reaction',
        'Major trauma or injury',
        'Choking',
        'Unconscious or unresponsive',
        'Severe burns',
        'Poisoning',
        'Thoughts of self-harm'
    ],
    'go_to_er': [
        'High fever (over 103°F) with confusion',
        'Severe abdominal pain',
        'Vomiting blood',
        'Severe head injury',
        'Possible broken bone',
        'Deep cuts requiring stitches',
        'Eye injuries',
        'Severe asthma attack not responding to inhaler'
    ],
    'urgent_care': [
        'Minor fractures or sprains',
        'Cuts that may need stitches (not severe)',
        'Moderate burns',
        'Moderate fever',
        'Ear or sinus infections',
        'Urinary tract infections',
        'Minor allergic reactions',
        'Flu symptoms'
    ],
    'schedule_appointment': [
        'Persistent cough or cold',
        'Mild rash',
        'Minor aches and pains',
        'Routine checkups',
        'Follow-up care',
        'Medication refills',
        'Chronic condition management',
        'Preventive care and screenings'
    ]
}

def get_symptom_info(symptom_name):
    """Get detailed information about a symptom"""
    symptom_lower = symptom_name.lower()
    for key, value in SYMPTOMS_DATABASE.items():
        if key in symptom_lower or symptom_lower in key:
            return value
    return None

def get_medication_info(medication_name):
    """Get detailed information about a medication"""
    med_lower = medication_name.lower()
    for key, value in MEDICATIONS_DATABASE.items():
        if key in med_lower or med_lower in key:
            return value
        # Check brand names
        if 'brand_names' in value:
            for brand in value['brand_names']:
                if brand.lower() in med_lower:
                    return value
    return None

def get_health_tips(category=None, count=5):
    """Get health tips by category"""
    import random
    
    if category and category in HEALTH_TIPS_COMPREHENSIVE:
        return random.sample(HEALTH_TIPS_COMPREHENSIVE[category], min(count, len(HEALTH_TIPS_COMPREHENSIVE[category])))
    
    # Return random tips from all categories
    all_tips = []
    for tips in HEALTH_TIPS_COMPREHENSIVE.values():
        all_tips.extend(tips)
    return random.sample(all_tips, min(count, len(all_tips)))
