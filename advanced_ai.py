"""
Advanced AI Features for Healthcare Chatbot
Medical report analysis, pattern recognition, and intelligent diagnosis
"""

from typing import Dict, List, Tuple
import re
from datetime import datetime
import json


class MedicalAIAssistant:
    """Advanced AI for medical analysis and diagnosis support"""
    
    def __init__(self):
        """Initialize AI assistant with medical knowledge base"""
        self.disease_patterns = self._load_disease_patterns()
        self.symptom_combinations = self._load_symptom_combinations()
        self.critical_symptoms = self._load_critical_symptoms()
    
    def _load_disease_patterns(self) -> Dict:
        """Load disease pattern recognition data"""
        return {
            "diabetes": {
                "symptoms": ["increased thirst", "frequent urination", "fatigue", "blurred vision", "slow healing"],
                "risk_factors": ["obesity", "family history", "age > 45", "sedentary lifestyle"],
                "severity": "chronic",
                "specialist": "Endocrinology"
            },
            "hypertension": {
                "symptoms": ["headaches", "dizziness", "chest pain", "shortness of breath"],
                "risk_factors": ["high salt diet", "stress", "obesity", "family history"],
                "severity": "chronic",
                "specialist": "Cardiology"
            },
            "covid-19": {
                "symptoms": ["fever", "cough", "loss of taste", "loss of smell", "fatigue", "difficulty breathing"],
                "risk_factors": ["exposure", "crowded places", "no vaccination"],
                "severity": "acute",
                "specialist": "Infectious Disease"
            },
            "asthma": {
                "symptoms": ["wheezing", "shortness of breath", "chest tightness", "coughing"],
                "risk_factors": ["allergies", "family history", "pollution exposure"],
                "severity": "chronic",
                "specialist": "Pulmonology"
            },
            "migraine": {
                "symptoms": ["severe headache", "nausea", "sensitivity to light", "visual disturbances"],
                "risk_factors": ["stress", "lack of sleep", "certain foods", "hormonal changes"],
                "severity": "episodic",
                "specialist": "Neurology"
            }
        }
    
    def _load_symptom_combinations(self) -> Dict:
        """Load dangerous symptom combinations"""
        return {
            "heart_attack": ["chest pain", "shortness of breath", "arm pain", "sweating", "nausea"],
            "stroke": ["sudden weakness", "facial drooping", "speech difficulty", "confusion", "severe headache"],
            "sepsis": ["high fever", "rapid heart rate", "confusion", "difficulty breathing", "extreme pain"],
            "anaphylaxis": ["difficulty breathing", "swelling", "rash", "rapid pulse", "dizziness"]
        }
    
    def _load_critical_symptoms(self) -> List[str]:
        """Load critical symptoms requiring immediate attention"""
        return [
            "chest pain", "difficulty breathing", "severe bleeding", "loss of consciousness",
            "severe head injury", "stroke symptoms", "heart attack symptoms",
            "severe allergic reaction", "severe burns", "suicidal thoughts"
        ]
    
    def analyze_symptoms(self, symptoms: List[str], patient_history: Dict = None) -> Dict:
        """
        Advanced symptom analysis with pattern recognition
        Returns diagnosis suggestions, severity, and recommendations
        """
        symptoms_lower = [s.lower() for s in symptoms]
        
        # Check for critical symptoms first
        critical_check = self._check_critical_symptoms(symptoms_lower)
        if critical_check["is_critical"]:
            return critical_check
        
        # Check for dangerous combinations
        dangerous_check = self._check_dangerous_combinations(symptoms_lower)
        if dangerous_check["is_dangerous"]:
            return dangerous_check
        
        # Pattern matching for diseases
        possible_conditions = self._match_disease_patterns(symptoms_lower, patient_history)
        
        # Calculate severity
        severity = self._calculate_severity(symptoms_lower, possible_conditions)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(possible_conditions, severity)
        
        return {
            "is_critical": False,
            "is_dangerous": False,
            "severity": severity,
            "possible_conditions": possible_conditions,
            "recommendations": recommendations,
            "specialist_referral": self._get_specialist_referral(possible_conditions),
            "confidence": self._calculate_confidence(symptoms_lower, possible_conditions),
            "follow_up_questions": self._generate_follow_up_questions(possible_conditions)
        }
    
    def _check_critical_symptoms(self, symptoms: List[str]) -> Dict:
        """Check for critical symptoms requiring immediate attention"""
        critical_found = [s for s in symptoms if any(crit in s for crit in self.critical_symptoms)]
        
        if critical_found:
            return {
                "is_critical": True,
                "severity": "EMERGENCY",
                "critical_symptoms": critical_found,
                "action": "CALL 911 IMMEDIATELY",
                "message": "⚠️ MEDICAL EMERGENCY DETECTED! Call 911 or go to the nearest emergency room immediately!"
            }
        
        return {"is_critical": False}
    
    def _check_dangerous_combinations(self, symptoms: List[str]) -> Dict:
        """Check for dangerous symptom combinations"""
        for condition, combo_symptoms in self.symptom_combinations.items():
            matches = sum(1 for s in symptoms if any(cs in s for cs in combo_symptoms))
            
            if matches >= 3:  # 3 or more matching symptoms
                return {
                    "is_dangerous": True,
                    "severity": "HIGH",
                    "possible_emergency": condition,
                    "matching_symptoms": matches,
                    "action": "Seek immediate medical attention",
                    "message": f"⚠️ Symptoms match pattern for {condition}. Seek immediate medical care!"
                }
        
        return {"is_dangerous": False}
    
    def _match_disease_patterns(self, symptoms: List[str], patient_history: Dict = None) -> List[Dict]:
        """Match symptoms against disease patterns"""
        matches = []
        
        for disease, data in self.disease_patterns.items():
            symptom_matches = sum(1 for s in symptoms if any(ds in s for ds in data["symptoms"]))
            
            if symptom_matches > 0:
                confidence = (symptom_matches / len(data["symptoms"])) * 100
                
                # Adjust confidence based on patient history
                if patient_history:
                    if "chronic_conditions" in patient_history:
                        if disease in patient_history["chronic_conditions"].lower():
                            confidence += 20
                    
                    if "allergies" in patient_history:
                        if disease in patient_history["allergies"].lower():
                            confidence += 15
                
                matches.append({
                    "condition": disease,
                    "confidence": min(confidence, 100),
                    "matching_symptoms": symptom_matches,
                    "total_symptoms": len(data["symptoms"]),
                    "severity": data["severity"],
                    "specialist": data["specialist"]
                })
        
        # Sort by confidence
        matches.sort(key=lambda x: x["confidence"], reverse=True)
        return matches[:5]  # Top 5 matches
    
    def _calculate_severity(self, symptoms: List[str], conditions: List[Dict]) -> str:
        """Calculate overall severity level"""
        if not conditions:
            if len(symptoms) >= 5:
                return "MODERATE"
            return "MILD"
        
        highest_severity = conditions[0]["severity"]
        confidence = conditions[0]["confidence"]
        
        if confidence >= 70 and highest_severity == "chronic":
            return "MODERATE"
        elif len(symptoms) >= 4:
            return "MODERATE"
        
        return "MILD"
    
    def _generate_recommendations(self, conditions: List[Dict], severity: str) -> List[str]:
        """Generate health recommendations based on analysis"""
        recommendations = []
        
        if severity == "EMERGENCY":
            recommendations.append("🚨 Call 911 immediately")
            recommendations.append("🏥 Go to nearest emergency room")
            return recommendations
        
        if severity == "HIGH":
            recommendations.append("⚠️ Seek medical attention within 24 hours")
            recommendations.append("📞 Call your doctor today")
        elif severity == "MODERATE":
            recommendations.append("📅 Schedule appointment within 3-5 days")
            recommendations.append("📊 Monitor symptoms closely")
        else:
            recommendations.append("🏠 Rest and home care")
            recommendations.append("💧 Stay hydrated")
            recommendations.append("🌡️ Monitor symptoms for 48 hours")
        
        if conditions:
            top_condition = conditions[0]
            recommendations.append(f"🏥 Consider consulting: {top_condition['specialist']}")
        
        recommendations.append("📝 Keep a symptom diary")
        recommendations.append("🔔 Set up follow-up reminder")
        
        return recommendations
    
    def _get_specialist_referral(self, conditions: List[Dict]) -> str:
        """Get specialist referral recommendation"""
        if not conditions:
            return "General Medicine"
        return conditions[0]["specialist"]
    
    def _calculate_confidence(self, symptoms: List[str], conditions: List[Dict]) -> int:
        """Calculate overall confidence in diagnosis"""
        if not conditions:
            return 30
        
        if len(symptoms) >= 4 and conditions[0]["confidence"] >= 60:
            return min(85, conditions[0]["confidence"])
        
        return int(conditions[0]["confidence"])
    
    def _generate_follow_up_questions(self, conditions: List[Dict]) -> List[str]:
        """Generate follow-up questions for better diagnosis"""
        questions = [
            "How long have you had these symptoms?",
            "Have symptoms worsened or improved recently?",
            "Are you currently taking any medications?",
            "Do you have any known allergies?"
        ]
        
        if conditions:
            condition = conditions[0]["condition"]
            if condition == "diabetes":
                questions.extend([
                    "Have you noticed increased thirst or urination?",
                    "Do you have a family history of diabetes?"
                ])
            elif condition == "hypertension":
                questions.extend([
                    "Have you checked your blood pressure recently?",
                    "Do you experience dizziness or headaches?"
                ])
        
        return questions
    
    def analyze_medical_report(self, report_text: str) -> Dict:
        """
        Analyze medical report text and extract key information
        """
        analysis = {
            "report_type": self._detect_report_type(report_text),
            "abnormal_values": self._find_abnormal_values(report_text),
            "key_findings": self._extract_key_findings(report_text),
            "recommendations": [],
            "severity": "Normal"
        }
        
        if analysis["abnormal_values"]:
            analysis["severity"] = "Abnormal"
            analysis["recommendations"].append("Consult with your doctor about abnormal values")
        
        return analysis
    
    def _detect_report_type(self, text: str) -> str:
        """Detect type of medical report"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["blood test", "cbc", "hemoglobin", "wbc"]):
            return "Blood Test"
        elif any(word in text_lower for word in ["x-ray", "ct scan", "mri", "ultrasound"]):
            return "Imaging Report"
        elif any(word in text_lower for word in ["glucose", "a1c", "insulin"]):
            return "Diabetes Panel"
        elif any(word in text_lower for word in ["cholesterol", "lipid", "hdl", "ldl"]):
            return "Lipid Profile"
        else:
            return "General Report"
    
    def _find_abnormal_values(self, text: str) -> List[Dict]:
        """Find abnormal values in report"""
        abnormal = []
        
        # Look for patterns like "High", "Low", "Abnormal"
        lines = text.split('\n')
        for line in lines:
            if any(word in line.lower() for word in ["high", "low", "abnormal", "critical"]):
                abnormal.append({
                    "finding": line.strip(),
                    "status": "Abnormal"
                })
        
        return abnormal
    
    def _extract_key_findings(self, text: str) -> List[str]:
        """Extract key findings from report"""
        findings = []
        
        # Extract lines with medical terms
        medical_terms = ["diagnosis", "impression", "conclusion", "findings", "result"]
        lines = text.split('\n')
        
        for line in lines:
            if any(term in line.lower() for term in medical_terms):
                findings.append(line.strip())
        
        return findings[:5]  # Top 5 findings


# Global instance
medical_ai = MedicalAIAssistant()
