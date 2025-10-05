"""
Cognate Aligner
Aligns cognate words from different Turkic languages in CTA
"""

from typing import Dict, Any, List, Tuple
from .llm_interface import LLMInterface

class CognateAligner:
    def __init__(self, llm_interface: LLMInterface):
        self.llm = llm_interface
        self.system_prompt = self._create_system_prompt()
        self.supported_languages = {
            'tr': 'Turkish',
            'az': 'Azerbaijani',
            'uz': 'Uzbek',
            'kk': 'Kazakh',
            'ky': 'Kyrgyz',
            'tk': 'Turkmen',
            'tt': 'Tatar',
            'ba': 'Bashkir',
            'cv': 'Chuvash',
            'sah': 'Sakha',
            'ug': 'Uyghur'
        }
    
    def _create_system_prompt(self) -> str:
        """Create system prompt for cognate alignment"""
        return """ROLE: You align potential cognates across Turkic languages AFTER CTA transliteration.

PROCESS:
1) Transliterate each candidate word into CTA using the same mapping rules as the transliteration engine
2) Group words by phonetic similarity levels: "high" | "medium" | "low"  
3) Add brief rationale explaining the relationship (shared root, systematic sound change, etc.)

SIMILARITY CRITERIA:
- HIGH: Clear cognates with systematic sound correspondences (e.g., tr:şehir ~ uz:şahar, shared root with regular sh~ş)
- MEDIUM: Probable cognates with some sound changes or semantic drift (e.g., related roots but different suffixes)
- LOW: Possible distant relationships or borrowings (similar function/meaning but unclear etymology)

SOUND CHANGE PATTERNS TO RECOGNIZE:
- Consonant shifts: k~q (front/back), g~ğ, sh~ş, ch~ç, x~h
- Vowel changes: e~ä, o~ò, u~ü, ı~i (vowel harmony effects)
- Length variations: û marker differences
- Nasal variations: n~ñ (ng realization)

OUTPUT FORMAT (JSON only):
{
  "groups": [
    {
      "similarity": "high|medium|low",
      "items": [
        {"lang": "language_code", "original": "original_word", "ota": "ota_form"}
      ],
      "rationale": "TÜRKÇE açıklama - ses değişimleri ve ilişkiler",
      "confidence": 0.0-1.0,
      "root_analysis": "TÜRKÇE kök analizi - ortak köken açıklaması"
    }
  ],
  "statistics": {
    "total_words": number,
    "groups_found": number,
    "average_group_size": number
  }
}

CRITICAL LANGUAGE REQUIREMENT:
- Write ALL rationale and root_analysis in TURKISH
- Use Turkish linguistic terminology
- Example rationale: "Ortak Türkçe kök, sistematik ses uyuşması (sh↔ş)"
- Example root_analysis: "Proto-Türkçe *su kökünden"

IMPORTANT:
- Apply CTA transliteration rules consistently
- Focus on systematic sound correspondences, not surface similarity
- Consider morphological structure (root + suffixes)
- Be conservative with HIGH similarity ratings
- Explain your reasoning clearly in Turkish"""
    
    def align_cognates(self, candidates_input: str) -> Dict[str, Any]:
        """
        Align cognate candidates
        
        Args:
            candidates_input: Format: "lang_code:word" on each line
            
        Returns:
            Alignment results
        """
        # Parse input text
        candidates = self._parse_candidates(candidates_input)
        
        if not candidates:
            return {
                "groups": [],
                "error": "No valid candidate words found. Format: 'language_code:word' (e.g.: tr:şehir)",
                "input": candidates_input
            }
        
        # Create user prompt
        user_prompt = self._create_user_prompt(candidates)
        
        try:
            # Make LLM call
            response = self.llm.call_llm(
                system_prompt=self.system_prompt,
                user_prompt=user_prompt,
                temperature=0.3,  # For creative but consistent analysis
                max_tokens=3000
            )
            
            # Parse JSON
            result = self.llm.parse_json_response(response["content"])
            
            # If LLM returned single group, put in groups array
            if 'similarity' in result and 'groups' not in result:
                # LLM returned as single group, convert to array
                result = {
                    "groups": [result],
                    "statistics": {
                        "total_words": len(candidates),
                        "groups_found": 1,
                        "average_group_size": len(result.get('items', []))
                    }
                }
            
            # Validate and enrich results
            validated_result = self._validate_and_enrich_result(result, candidates)
            
            # Add LLM metadata
            validated_result["llm_metadata"] = {
                "model": response.get("model"),
                "usage": response.get("usage"),
                "response_time": response.get("response_time")
            }
            
            return validated_result
            
        except Exception as e:
            return {
                "groups": [],
                "error": f"Cognate alignment error: {str(e)}",
                "candidates": candidates
            }
    
    def _parse_candidates(self, input_text: str) -> List[Dict[str, str]]:
        """Parse candidate word input"""
        candidates = []
        lines = input_text.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line or ':' not in line:
                continue
            
            try:
                lang_code, word = line.split(':', 1)
                lang_code = lang_code.strip().lower()
                word = word.strip()
                
                if lang_code and word:
                    candidates.append({
                        "lang": lang_code,
                        "original": word,
                        "language_name": self.supported_languages.get(lang_code, lang_code.upper())
                    })
            except ValueError:
                continue
        
        return candidates
    
    def _create_user_prompt(self, candidates: List[Dict[str, str]]) -> str:
        """Create user prompt"""
        candidates_text = "\n".join([
            f"- {c['lang']}: {c['original']} ({c['language_name']})"
            for c in candidates
        ])
        
        return f"""CANDIDATE WORDS:
{candidates_text}

TASK:
1) Transliterate each word according to CTA rules
2) Group by phonetic similarity after CTA normalization
3) Identify systematic sound correspondences
4) Provide confidence scores and rationales

FOCUS POINTS:
- Systematic sound changes (k~q, sh~ş, etc.)
- Morphological analysis (root + affixes)
- Semantic relationships
- Historical sound correspondences

CRITICAL: Write ALL "rationale" and "root_analysis" fields in TURKISH!
Examples:
- rationale: "Ortak Türkçe kök, sistematik ses uyuşması (sh↔ş)"
- root_analysis: "Proto-Türkçe *su kökünden türemiş"

Return result in specified JSON format - with TURKISH explanations."""
    
    def _validate_and_enrich_result(self, result: Dict[str, Any], 
                                  original_candidates: List[Dict[str, str]]) -> Dict[str, Any]:
        """Validate and enrich results"""
        try:
            # Check basic structure
            if "groups" not in result:
                result["groups"] = []
            
            validated_groups = []
            total_words = 0
            
            for group in result["groups"]:
                validated_group = self._validate_group(group)
                if validated_group:
                    validated_groups.append(validated_group)
                    total_words += len(validated_group["items"])
            
            result["groups"] = validated_groups
            
            # Calculate statistics
            statistics = self._calculate_alignment_statistics(validated_groups, original_candidates)
            result["statistics"] = statistics
            
            # Add summary analysis
            result["summary"] = self._generate_alignment_summary(validated_groups, statistics)
            
            return result
            
        except Exception as e:
            return {
                "groups": [],
                "error": f"Result validation error: {str(e)}",
                "original_result": result
            }
    
    def _validate_group(self, group: Dict[str, Any]) -> Dict[str, Any]:
        """Validate group object"""
        try:
            # Check required fields
            required_fields = ["similarity", "items", "rationale"]
            for field in required_fields:
                if field not in group:
                    return None
            
            # Check similarity value
            if group["similarity"] not in ["high", "medium", "low"]:
                group["similarity"] = "medium"
            
            # Validate items list
            validated_items = []
            for item in group["items"]:
                if isinstance(item, dict) and "lang" in item and "original" in item:
                    # If no CTA field, leave empty
                    if "ota" not in item:
                        item["ota"] = item["original"]  # Fallback
                    validated_items.append(item)
            
            if len(validated_items) < 2:  # Must have at least 2 words
                return None
            
            group["items"] = validated_items
            
            # Add confidence field (if missing)
            if "confidence" not in group:
                # Default confidence based on similarity
                confidence_map = {"high": 0.8, "medium": 0.6, "low": 0.4}
                group["confidence"] = confidence_map.get(group["similarity"], 0.5)
            
            # Add root analysis field (if missing)
            if "root_analysis" not in group:
                group["root_analysis"] = "Root analysis not provided"
            
            return group
            
        except Exception:
            return None
    
    def _calculate_alignment_statistics(self, groups: List[Dict[str, Any]], 
                                      original_candidates: List[Dict[str, str]]) -> Dict[str, Any]:
        """Hizalama istatistiklerini hesapla"""
        stats = {
            "total_input_words": len(original_candidates),
            "total_aligned_words": 0,
            "groups_found": len(groups),
            "average_group_size": 0,
            "similarity_distribution": {"high": 0, "medium": 0, "low": 0},
            "language_coverage": set(),
            "average_confidence": 0.0,
            "alignment_rate": 0.0
        }
        
        if not groups:
            return stats
        
        total_confidence = 0
        total_words = 0
        
        for group in groups:
            # Grup büyüklüğü
            group_size = len(group.get("items", []))
            total_words += group_size
            
            # Similarity dağılımı
            similarity = group.get("similarity", "medium")
            stats["similarity_distribution"][similarity] += 1
            
            # Confidence ortalaması
            confidence = group.get("confidence", 0.5)
            total_confidence += confidence
            
            # Dil kapsamı
            for item in group.get("items", []):
                lang = item.get("lang", "")
                if lang:
                    stats["language_coverage"].add(lang)
        
        stats["total_aligned_words"] = total_words
        stats["average_group_size"] = total_words / len(groups) if groups else 0
        stats["average_confidence"] = total_confidence / len(groups) if groups else 0
        stats["alignment_rate"] = total_words / len(original_candidates) if original_candidates else 0
        stats["language_coverage"] = list(stats["language_coverage"])
        
        return stats
    
    def _generate_alignment_summary(self, groups: List[Dict[str, Any]], 
                                  statistics: Dict[str, Any]) -> str:
        """Hizalama özeti oluştur"""
        if not groups:
            return "Hiçbir kognat hizalaması bulunamadı."
        
        summary = f"Kognat Hizalama Özeti:\n"
        summary += f"- {statistics['groups_found']} grup bulundu\n"
        summary += f"- Toplam {statistics['total_aligned_words']} kelime hizalandı\n"
        summary += f"- Ortalama grup büyüklüğü: {statistics['average_group_size']:.1f}\n"
        summary += f"- Hizalama oranı: {statistics['alignment_rate']:.1%}\n"
        summary += f"- Ortalama güven skoru: {statistics['average_confidence']:.2f}\n"
        
        # Similarity dağılımı
        dist = statistics['similarity_distribution']
        summary += f"- Yüksek benzerlik: {dist['high']} grup\n"
        summary += f"- Orta benzerlik: {dist['medium']} grup\n"
        summary += f"- Düşük benzerlik: {dist['low']} grup\n"
        
        # Dil kapsamı
        languages = statistics['language_coverage']
        summary += f"- Kapsanan diller: {', '.join(languages)}\n"
        
        return summary
    
    def batch_align(self, candidate_lists: List[str]) -> List[Dict[str, Any]]:
        """
        Toplu kognat hizalama
        
        Args:
            candidate_lists: Aday kelime listelerinin listesi
            
        Returns:
            Hizalama sonuçları listesi
        """
        results = []
        for candidates in candidate_lists:
            result = self.align_cognates(candidates)
            results.append(result)
        
        return results
    
    def export_alignment_table(self, alignment_result: Dict[str, Any]) -> str:
        """
        Hizalama sonucunu tablo formatında dışa aktar
        
        Args:
            alignment_result: align_cognates() sonucu
            
        Returns:
            Tablo formatında metin
        """
        if 'error' in alignment_result:
            return f"Hata: {alignment_result['error']}"
        
        groups = alignment_result.get('groups', [])
        if not groups:
            return "Hiçbir grup bulunamadı."
        
        table = "KOGNAT HİZALAMA TABLOSU\n"
        table += "=" * 80 + "\n\n"
        
        for i, group in enumerate(groups, 1):
            similarity = group.get('similarity', 'bilinmiyor').upper()
            confidence = group.get('confidence', 0.0)
            rationale = group.get('rationale', '')
            
            table += f"GRUP {i} - Benzerlik: {similarity} (Güven: {confidence:.2f})\n"
            table += f"Gerekçe: {rationale}\n"
            table += "-" * 60 + "\n"
            
            for item in group.get('items', []):
                lang = item.get('lang', '').upper()
                original = item.get('original', '')
                ota = item.get('ota', '')
                table += f"{lang:>4}: {original:<15} → CTA: {ota}\n"
            
            table += "\n"
        
        return table
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Desteklenen dilleri getir"""
        return self.supported_languages.copy()
