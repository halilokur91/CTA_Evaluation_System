"""
Phonetic Risk Analyzer
Detects ambiguities and confusions in CTA text
"""

from typing import Dict, Any, List
from .llm_interface import LLMInterface

class RiskAnalyzer:
    def __init__(self, llm_interface: LLMInterface):
        self.llm = llm_interface
        self.system_prompt = self._create_system_prompt()
        self.new_letters = ['x', 'X', 'ə', 'Ə', 'ä', 'Ä', 'q', 'Q', 'ñ', 'Ñ', 'û', 'Û', 'ò', 'Ò']
    
    def _create_system_prompt(self) -> str:
        """Create system prompt for risk analysis"""
        return """ROLE: You are a phonetic risk analyzer for CTA-normalized text.
TASK: Report ambiguities specifically for x, ə, q, ñ, û (also consider ò, ğ, ä/ö/ü when relevant).

ANALYSIS FOCUS:
- x: uvular fricative vs. velar fricative vs. /h/ (Azeri/Turkmen/Arabic origin)
- ə→ä: open/front vowel confusion with e/a (dialectal/L1 influence)  
- q: velar vs. uvular stop confusion with k (back vowel context expected)
- ñ: nasal confusion - often not shown in Turkish orthography; ng↔ñ transitions
- û: length marker - missing/exaggerated length (morpheme boundary artifacts)
- ò: rounded back vowel (Uzbek o') vs. regular o
- ğ: soft g vs. fricative variants
- ä/ö/ü: front vowel confusions in different Turkic languages

For each potential risk, provide:
{
  "letter": "character in question",
  "possible_confusions": ["list", "of", "alternatives"],
  "languages": ["affected", "language", "codes"],
  "examples": ["example", "words", "showing", "confusion"],
  "confidence": 0.0-1.0,
  "context": "brief explanation of when/why confusion occurs",
  "severity": "low|medium|high"
}

OUTPUT: JSON array of risk objects only. No additional text.
Write "context" field explanations in Turkish.

IMPORTANT GUIDELINES:
- Only report actual phonetic ambiguities, not spelling variations
- Focus on cross-linguistic confusion patterns
- Consider morphophonological environments
- Rate confidence based on frequency and systematicity of confusion
- Severity: high=frequent systematic confusion, medium=context-dependent, low=rare/marginal
- Write context explanations in Turkish (e.g., "Kalın k ile normal k karışımı")"""
    
    def analyze_risks(self, ota_text: str) -> Dict[str, Any]:
        """
        Analyze phonetic risks in CTA text
        
        Args:
            ota_text: CTA text to be analyzed
            
        Returns:
            Risk analysis results (dict with 'risks', 'statistics', 'llm_metadata')
        """
        if not ota_text.strip():
            return {
                "risks": [],
                "error": "Empty text - CTA text is required for risk analysis"
            }
        
        # Detect new letters in text
        found_letters = self._find_new_letters(ota_text)
        
        if not found_letters:
            return {
                "risks": [{
                    "letter": "none",
                    "possible_confusions": [],
                    "languages": [],
                    "examples": [],
                    "confidence": 1.0,
                    "context": "No new CTA letters found in text",
                    "severity": "low"
                }],
                "statistics": {
                    "total_risks": 0,
                    "new_letters_count": 0
                },
                "llm_metadata": {}
            }
        
        # Create user prompt
        user_prompt = f"""CTA_TEXT:
"{ota_text}"

DETECTED_NEW_LETTERS: {', '.join(found_letters)}

TASK:
Analyze the phonetic risks and potential confusions for the new CTA letters found in this text. 
Focus particularly on: {', '.join(found_letters)}

Consider:
1. Cross-linguistic confusion patterns
2. Morphophonological environments  
3. Dialectal variations
4. L1 transfer effects
5. Systematic vs. sporadic confusions

Return JSON array of risk analysis objects as specified in the system prompt."""
        
        try:
            # Make LLM call
            response = self.llm.call_llm(
                system_prompt=self.system_prompt,
                user_prompt=user_prompt,
                temperature=0.2,  # Low temperature for consistent analysis
                max_tokens=2000
            )
            
            # Parse JSON
            risks = self.llm.parse_json_response(response["content"])
            
            # If single object returned, make it a list
            if isinstance(risks, dict):
                risks = [risks]
            
            # Validate and enrich results
            validated_risks = []
            for risk in risks:
                validated_risk = self._validate_and_enrich_risk(risk, ota_text)
                if validated_risk:
                    validated_risks.append(validated_risk)
            
            # Add statistics
            analysis_stats = self._calculate_risk_statistics(validated_risks, ota_text)
            
            return {
                "risks": validated_risks,
                "statistics": analysis_stats,
                "llm_metadata": {
                    "model": response.get("model"),
                    "usage": response.get("usage"),
                    "response_time": response.get("response_time")
                }
            }
            
        except Exception as e:
            return {
                "risks": [],
                "error": f"Risk analysis error: {str(e)}",
                "input_text": ota_text
            }
    
    def _find_new_letters(self, text: str) -> List[str]:
        """Find new CTA letters in text"""
        found = []
        for letter in self.new_letters:
            if letter in text:
                found.append(letter)
        return list(set(found))  # Remove duplicates
    
    def _validate_and_enrich_risk(self, risk: Dict[str, Any], text: str) -> Dict[str, Any]:
        """Validate and enrich risk object"""
        try:
            # Check required fields
            required_fields = ['letter', 'possible_confusions', 'languages', 'examples', 'confidence']
            for field in required_fields:
                if field not in risk:
                    return None
            
            # Validate data types
            if not isinstance(risk['possible_confusions'], list):
                risk['possible_confusions'] = [str(risk['possible_confusions'])]
            
            if not isinstance(risk['languages'], list):
                risk['languages'] = [str(risk['languages'])]
            
            if not isinstance(risk['examples'], list):
                risk['examples'] = [str(risk['examples'])]
            
            # Normalize confidence value
            try:
                confidence = float(risk['confidence'])
                risk['confidence'] = max(0.0, min(1.0, confidence))
            except (ValueError, TypeError):
                risk['confidence'] = 0.5
            
            # Check severity field
            if 'severity' not in risk or risk['severity'] not in ['low', 'medium', 'high']:
                risk['severity'] = 'medium'
            
            # Add context field (if missing)
            if 'context' not in risk:
                risk['context'] = f"Phonetic ambiguity for letter '{risk['letter']}'"
            
            # Calculate frequency in text
            letter_count = text.count(risk['letter'].lower()) + text.count(risk['letter'].upper())
            risk['frequency_in_text'] = letter_count
            
            return risk
            
        except Exception:
            return None
    
    def _calculate_risk_statistics(self, risks: List[Dict[str, Any]], text: str) -> Dict[str, Any]:
        """Calculate risk statistics"""
        if not risks:
            return {"total_risks": 0}
        
        stats = {
            "total_risks": len(risks),
            "severity_distribution": {"low": 0, "medium": 0, "high": 0},
            "average_confidence": 0.0,
            "most_problematic_letters": [],
            "language_coverage": set(),
            "total_new_letters_in_text": 0
        }
        
        total_confidence = 0
        letter_risk_count = {}
        
        for risk in risks:
            # Severity distribution
            severity = risk.get('severity', 'medium')
            stats["severity_distribution"][severity] += 1
            
            # Average confidence
            confidence = risk.get('confidence', 0.5)
            total_confidence += confidence
            
            # Risk count by letter
            letter = risk.get('letter', '')
            letter_risk_count[letter] = letter_risk_count.get(letter, 0) + 1
            
            # Language coverage
            languages = risk.get('languages', [])
            stats["language_coverage"].update(languages)
            
            # Frequency in text
            stats["total_new_letters_in_text"] += risk.get('frequency_in_text', 0)
        
        # Average confidence
        stats["average_confidence"] = total_confidence / len(risks)
        
        # Most problematic letters
        stats["most_problematic_letters"] = sorted(
            letter_risk_count.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:3]
        
        # Convert language coverage to list
        stats["language_coverage"] = list(stats["language_coverage"])
        
        return stats
    
    def batch_analyze(self, texts: List[str]) -> List[Dict[str, Any]]:
        """
        Batch risk analysis
        
        Args:
            texts: List of texts to be analyzed
            
        Returns:
            List of risk analysis results
        """
        results = []
        for text in texts:
            result = self.analyze_risks(text)
            results.append(result)
        
        return results
    
    def generate_risk_summary(self, analysis_result: Dict[str, Any]) -> str:
        """
        Generate risk analysis summary
        
        Args:
            analysis_result: Result from analyze_risks()
            
        Returns:
            Summary text
        """
        if 'error' in analysis_result:
            return f"Risk analysis error: {analysis_result['error']}"
        
        risks = analysis_result.get('risks', [])
        stats = analysis_result.get('statistics', {})
        
        if not risks:
            return "No risks detected in text."
        
        summary = f"Risk Analysis Summary:\n"
        summary += f"- Total risk count: {stats.get('total_risks', 0)}\n"
        summary += f"- Average confidence score: {stats.get('average_confidence', 0):.2f}\n"
        
        severity_dist = stats.get('severity_distribution', {})
        summary += f"- High risk: {severity_dist.get('high', 0)}\n"
        summary += f"- Medium risk: {severity_dist.get('medium', 0)}\n"
        summary += f"- Low risk: {severity_dist.get('low', 0)}\n"
        
        problematic = stats.get('most_problematic_letters', [])
        if problematic:
            summary += f"- Most problematic letters: {', '.join([f'{letter}({count})' for letter, count in problematic])}\n"
        
        languages = stats.get('language_coverage', [])
        if languages:
            summary += f"- Affected languages: {', '.join(languages)}\n"
        
        return summary
