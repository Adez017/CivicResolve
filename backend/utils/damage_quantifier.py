"""
Computer Vision Damage Quantification Module
Analyzes civic issue photos using AI to measure damage and estimate repair costs.

Usage:
    from backend.utils.damage_quantifier import DamageQuantifier
    
    quantifier = DamageQuantifier()
    result = quantifier.quantify_damage("path/to/image.jpg", "pothole")
    print(result['summary'])
"""

import os
import json
import base64
from pathlib import Path

# Try to import Google Generative AI
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


class RepairCalculator:
    """Calculates repair materials and costs based on damage measurements."""
    
    # Material costs in INR (Indian Rupees) - approximate rates
    MATERIAL_COSTS = {
        'cement_per_bag': 350,       # 50kg bag
        'asphalt_per_kg': 15,
        'gravel_per_bag': 200,       # 50kg bag
        'paint_per_liter': 250,
        'brick_per_piece': 8,
        'sand_per_bag': 100,         # 50kg bag
    }
    
    # Labor costs in INR per hour
    LABOR_RATES = {
        'pothole': 200,
        'garbage': 150,
        'infrastructure': 250,
        'general': 180
    }
    
    # Equipment rental per day
    EQUIPMENT_COSTS = {
        'road_repair_kit': 500,
        'garbage_truck': 2000,
        'scaffolding': 800,
        'power_tools': 400,
    }
    
    @classmethod
    def calculate_pothole_repair(cls, area_sqm: float, depth_cm: float) -> dict:
        """Calculate materials needed for pothole repair."""
        volume_liters = area_sqm * (depth_cm / 100) * 1000
        
        # Material calculations
        cement_bags = max(1, int(volume_liters / 40) + 1)  # ~40L per bag coverage
        gravel_bags = max(1, int(volume_liters / 50) + 1)
        asphalt_kg = volume_liters * 0.8  # Approximate density
        
        materials = [
            f"{cement_bags} bag{'s' if cement_bags > 1 else ''} cement ({cement_bags * 50}kg)",
            f"{gravel_bags} bag{'s' if gravel_bags > 1 else ''} gravel ({gravel_bags * 50}kg)",
        ]
        
        # For larger potholes, add asphalt
        if area_sqm > 0.5:
            materials.append(f"{int(asphalt_kg)}kg asphalt mix")
        
        labor_hours = max(1, int(area_sqm * 2) + 1)
        
        material_cost = (cement_bags * cls.MATERIAL_COSTS['cement_per_bag'] + 
                        gravel_bags * cls.MATERIAL_COSTS['gravel_per_bag'] +
                        (asphalt_kg * cls.MATERIAL_COSTS['asphalt_per_kg'] if area_sqm > 0.5 else 0))
        
        labor_cost = labor_hours * cls.LABOR_RATES['pothole']
        equipment_cost = cls.EQUIPMENT_COSTS['road_repair_kit']
        
        total_min = int(material_cost + labor_cost)
        total_max = int(total_min * 1.4)  # 40% buffer for contingencies
        
        return {
            'materials': materials,
            'equipment': ['Basic road repair kit', 'Safety barriers'],
            'labor_hours': labor_hours,
            'cost_range': {'min': total_min, 'max': total_max, 'currency': 'INR'}
        }
    
    @classmethod
    def calculate_garbage_cleanup(cls, volume_cubic_m: float, weight_kg: float) -> dict:
        """Calculate resources needed for garbage cleanup."""
        # Truck capacity ~5 cubic meters or ~2000kg
        trucks_needed = max(1, int(max(volume_cubic_m / 5, weight_kg / 2000) + 0.5))
        workers_needed = max(2, int(weight_kg / 200))
        labor_hours = max(1, int(weight_kg / 100))
        
        labor_cost = labor_hours * workers_needed * cls.LABOR_RATES['garbage']
        truck_cost = trucks_needed * cls.EQUIPMENT_COSTS['garbage_truck']
        
        total_min = int(labor_cost + truck_cost)
        total_max = int(total_min * 1.3)
        
        return {
            'materials': [
                f"{trucks_needed} garbage truck{'s' if trucks_needed > 1 else ''} needed",
                f"{workers_needed} workers required",
                "Industrial garbage bags",
                "Protective gear"
            ],
            'equipment': ['Garbage truck', 'Loading equipment'],
            'labor_hours': labor_hours,
            'cost_range': {'min': total_min, 'max': total_max, 'currency': 'INR'}
        }
    
    @classmethod
    def calculate_infrastructure_repair(cls, crack_length_m: float, affected_area_sqm: float, 
                                        damage_type: str = 'crack') -> dict:
        """Calculate materials for infrastructure repair."""
        materials = []
        
        if damage_type in ['crack', 'wall']:
            cement_bags = max(1, int(crack_length_m / 5) + 1)
            paint_liters = max(1, int(affected_area_sqm / 10) + 1)
            materials = [
                f"{cement_bags} bag{'s' if cement_bags > 1 else ''} cement ({cement_bags * 50}kg)",
                f"{paint_liters} liter{'s' if paint_liters > 1 else ''} paint",
                "Crack filler/sealant",
                "Primer"
            ]
            material_cost = (cement_bags * cls.MATERIAL_COSTS['cement_per_bag'] + 
                           paint_liters * cls.MATERIAL_COSTS['paint_per_liter'])
        else:
            bricks = int(affected_area_sqm * 50)  # ~50 bricks per sqm
            cement_bags = max(1, int(affected_area_sqm / 2) + 1)
            materials = [
                f"{bricks} bricks",
                f"{cement_bags} bag{'s' if cement_bags > 1 else ''} cement",
                "Sand and mortar mix"
            ]
            material_cost = (bricks * cls.MATERIAL_COSTS['brick_per_piece'] + 
                           cement_bags * cls.MATERIAL_COSTS['cement_per_bag'])
        
        labor_hours = max(2, int(affected_area_sqm) + int(crack_length_m))
        labor_cost = labor_hours * cls.LABOR_RATES['infrastructure']
        
        total_min = int(material_cost + labor_cost)
        total_max = int(total_min * 1.5)
        
        return {
            'materials': materials,
            'equipment': ['Scaffolding (if needed)', 'Power tools', 'Safety equipment'],
            'labor_hours': labor_hours,
            'cost_range': {'min': total_min, 'max': total_max, 'currency': 'INR'}
        }


class DamageQuantifier:
    """
    AI-powered damage quantification using Google Gemini Vision.
    Analyzes civic issue photos to measure damage and estimate repairs.
    """
    
    SUPPORTED_TYPES = ['pothole', 'garbage', 'infrastructure', 'road_damage', 'wall_crack']
    
    def __init__(self, api_key: str = None):
        """Initialize with optional API key (defaults to GOOGLE_API_KEY env var)."""
        self.api_key = api_key or os.environ.get('GOOGLE_API_KEY')
        self.model = None
        
        if GEMINI_AVAILABLE and self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
            except Exception as e:
                print(f"⚠️ Gemini initialization failed: {e}")
    
    def _encode_image(self, image_path: str) -> dict:
        """Encode image for Gemini API."""
        with open(image_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')
        
        # Determine MIME type
        ext = Path(image_path).suffix.lower()
        mime_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg', 
            '.png': 'image/png',
            '.webp': 'image/webp',
            '.gif': 'image/gif'
        }
        mime_type = mime_types.get(ext, 'image/jpeg')
        
        return {'mime_type': mime_type, 'data': image_data}
    
    def _get_analysis_prompt(self, issue_type: str) -> str:
        """Get specialized prompt based on issue type."""
        base_prompt = """Analyze this image of a civic infrastructure issue and provide precise measurements.
        
You are an expert civil engineer analyzing damage for repair estimation.
Respond ONLY with valid JSON (no markdown, no code blocks, just pure JSON).

"""
        
        if issue_type == 'pothole':
            return base_prompt + """
Analyze this pothole image and estimate:
{
    "detected": true/false,
    "area_sqm": <estimated area in square meters, e.g. 0.5>,
    "depth_cm": <estimated depth in centimeters, e.g. 10>,
    "severity": "minor" | "moderate" | "severe" | "critical",
    "shape": "circular" | "irregular" | "elongated",
    "surface_type": "asphalt" | "concrete" | "mixed",
    "notes": "<any additional observations>"
}

Use visual cues like shadows, surrounding objects (shoes, coins, etc.) for scale estimation.
If no pothole is visible, set detected to false and provide empty values."""

        elif issue_type == 'garbage':
            return base_prompt + """
Analyze this garbage/waste image and estimate:
{
    "detected": true/false,
    "volume_cubic_m": <estimated volume in cubic meters, e.g. 2.0>,
    "weight_kg": <estimated weight in kilograms, e.g. 200>,
    "spread_area_sqm": <area covered in square meters>,
    "waste_type": "organic" | "plastic" | "mixed" | "construction" | "hazardous",
    "severity": "minor" | "moderate" | "severe" | "critical",
    "notes": "<any additional observations>"
}

Estimate based on visible pile size, density of waste, and common reference objects."""

        elif issue_type in ['infrastructure', 'wall_crack', 'road_damage']:
            return base_prompt + """
Analyze this infrastructure damage image and estimate:
{
    "detected": true/false,
    "damage_type": "crack" | "hole" | "erosion" | "collapse" | "surface_damage",
    "crack_length_m": <total length of cracks in meters, if applicable>,
    "affected_area_sqm": <total affected area in square meters>,
    "depth_severity": "surface" | "shallow" | "deep" | "structural",
    "severity": "minor" | "moderate" | "severe" | "critical",
    "structural_risk": true/false,
    "notes": "<any additional observations>"
}

Look for reference objects like bricks, doors, or standard sizes for scale."""

        else:
            return base_prompt + """
Analyze this civic issue image and provide general measurements:
{
    "detected": true/false,
    "issue_type": "<identified issue type>",
    "affected_area_sqm": <estimated affected area>,
    "severity": "minor" | "moderate" | "severe" | "critical",
    "notes": "<description of the issue and any measurements>"
}"""

    def quantify_damage(self, image_path: str, issue_type: str = 'pothole') -> dict:
        """
        Analyze an image and quantify the damage.
        
        Args:
            image_path: Path to the image file
            issue_type: Type of issue ('pothole', 'garbage', 'infrastructure')
            
        Returns:
            dict with damage measurements, repair estimate, and summary
        """
        if not os.path.exists(image_path):
            return {'error': f'Image not found: {image_path}'}
        
        # Normalize issue type
        issue_type = issue_type.lower().strip()
        if issue_type not in self.SUPPORTED_TYPES:
            issue_type = 'pothole'  # Default
        
        # Analyze with AI if available
        if self.model:
            damage_data = self._analyze_with_gemini(image_path, issue_type)
        else:
            # Fallback to mock data for demo/testing
            damage_data = self._get_mock_analysis(issue_type)
            damage_data['_note'] = 'Mock data - Gemini API not configured'
        
        # Calculate repair estimate
        repair_data = self._calculate_repair(damage_data, issue_type)
        
        # Generate summary
        summary = self._generate_summary(damage_data, repair_data, issue_type)
        
        return {
            'damage': damage_data,
            'repair': repair_data,
            'summary': summary,
            'issue_type': issue_type
        }
    
    def _analyze_with_gemini(self, image_path: str, issue_type: str) -> dict:
        """Use Gemini Vision to analyze the image."""
        try:
            image_data = self._encode_image(image_path)
            prompt = self._get_analysis_prompt(issue_type)
            
            response = self.model.generate_content([
                {'mime_type': image_data['mime_type'], 'data': image_data['data']},
                prompt
            ])
            
            # Parse JSON response
            response_text = response.text.strip()
            # Remove any markdown code blocks if present
            if response_text.startswith('```'):
                response_text = response_text.split('\n', 1)[1]
                response_text = response_text.rsplit('```', 1)[0]
            
            return json.loads(response_text)
            
        except json.JSONDecodeError as e:
            return {'error': f'Failed to parse AI response: {e}', 'raw_response': response_text}
        except Exception as e:
            return {'error': f'AI analysis failed: {e}'}
    
    def _get_mock_analysis(self, issue_type: str) -> dict:
        """Return mock data for testing when API is not available."""
        mock_data = {
            'pothole': {
                'detected': True,
                'area_sqm': 0.8,
                'depth_cm': 15,
                'severity': 'moderate',
                'shape': 'irregular',
                'surface_type': 'asphalt',
                'notes': 'Mock data for testing'
            },
            'garbage': {
                'detected': True,
                'volume_cubic_m': 2.5,
                'weight_kg': 200,
                'spread_area_sqm': 5.0,
                'waste_type': 'mixed',
                'severity': 'moderate',
                'notes': 'Mock data for testing'
            },
            'infrastructure': {
                'detected': True,
                'damage_type': 'crack',
                'crack_length_m': 2.5,
                'affected_area_sqm': 3.0,
                'depth_severity': 'surface',
                'severity': 'minor',
                'structural_risk': False,
                'notes': 'Mock data for testing'
            }
        }
        return mock_data.get(issue_type, mock_data['pothole'])
    
    def _calculate_repair(self, damage_data: dict, issue_type: str) -> dict:
        """Calculate repair requirements based on damage data."""
        if damage_data.get('error') or not damage_data.get('detected', True):
            return {'error': 'Cannot calculate repair - no damage detected'}
        
        if issue_type == 'pothole':
            area = damage_data.get('area_sqm', 0.5)
            depth = damage_data.get('depth_cm', 10)
            return RepairCalculator.calculate_pothole_repair(area, depth)
            
        elif issue_type == 'garbage':
            volume = damage_data.get('volume_cubic_m', 1.0)
            weight = damage_data.get('weight_kg', 100)
            return RepairCalculator.calculate_garbage_cleanup(volume, weight)
            
        elif issue_type in ['infrastructure', 'wall_crack', 'road_damage']:
            crack_length = damage_data.get('crack_length_m', 1.0)
            affected_area = damage_data.get('affected_area_sqm', 1.0)
            damage_type = damage_data.get('damage_type', 'crack')
            return RepairCalculator.calculate_infrastructure_repair(
                crack_length, affected_area, damage_type
            )
        
        return {'error': f'Unknown issue type: {issue_type}'}
    
    def _generate_summary(self, damage_data: dict, repair_data: dict, issue_type: str) -> str:
        """Generate human-readable summary."""
        if damage_data.get('error'):
            return f"Analysis failed: {damage_data['error']}"
        
        if not damage_data.get('detected', True):
            return "No damage detected in the image."
        
        # Build damage description
        if issue_type == 'pothole':
            damage_desc = (f"Pothole: {damage_data.get('area_sqm', '?')} sq.m, "
                          f"~{damage_data.get('depth_cm', '?')}cm deep")
        elif issue_type == 'garbage':
            damage_desc = (f"Garbage: ~{damage_data.get('weight_kg', '?')}kg waste, "
                          f"{damage_data.get('volume_cubic_m', '?')} cubic meters")
        else:
            damage_desc = (f"Infrastructure damage: {damage_data.get('crack_length_m', '?')}m crack, "
                          f"{damage_data.get('affected_area_sqm', '?')} sq.m affected")
        
        # Build cost description
        cost = repair_data.get('cost_range', {})
        if cost:
            cost_desc = f"₹{cost.get('min', '?'):,}-{cost.get('max', '?'):,}"
        else:
            cost_desc = "Unable to estimate"
        
        severity = damage_data.get('severity', 'unknown')
        
        return f"{damage_desc}. Severity: {severity}. Estimated repair: {cost_desc}"


# Convenience function for quick analysis
def analyze_civic_issue(image_path: str, issue_type: str = 'pothole', 
                         api_key: str = None) -> dict:
    """
    Quick function to analyze a civic issue image.
    
    Args:
        image_path: Path to the image
        issue_type: 'pothole', 'garbage', or 'infrastructure'
        api_key: Optional Google API key (uses GOOGLE_API_KEY env var if not provided)
        
    Returns:
        dict with damage measurements, repair estimate, and summary
    """
    quantifier = DamageQuantifier(api_key=api_key)
    return quantifier.quantify_damage(image_path, issue_type)


# Singleton instance for reuse
_quantifier_instance = None

def get_quantifier(api_key: str = None) -> DamageQuantifier:
    """Get or create a singleton DamageQuantifier instance."""
    global _quantifier_instance
    if _quantifier_instance is None:
        _quantifier_instance = DamageQuantifier(api_key=api_key)
    return _quantifier_instance
