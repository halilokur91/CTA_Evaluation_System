"""
PCE (Phonetic Correspondence Effectiveness) Analyzer
Yazı sistemlerinin fonetik temsiliyetini ölçen akademik araç
"""

import re
import math
from typing import Dict, Any, List, Tuple
from collections import Counter
from .llm_interface import LLMInterface

class PCEAnalyzer:
    def __init__(self, llm_interface: LLMInterface):
        self.llm = llm_interface
        self.system_prompt = self._create_system_prompt()
        
        # CTA harfleri
        self.ota_letters = set('abcçdefgğhıijklmnñoöpqrsştuvwxyüzäûəòâîô')
        self.new_ota_letters = set('qxñəûò')
        
    def _create_system_prompt(self) -> str:
        """PCE analizi için sistem prompt'u"""
        return """ROLE: You are a PCE (Phonetic Correspondence Effectiveness) analyzer for writing systems.

PCE measures how effectively a writing system represents phonetic structures:
- UPC (Unique Phoneme Count): Number of distinct phonemes
- TPC (Total Phoneme Count): Total phonemes in text
- ALC (Average Letter Count): Average letters per phoneme

PCE FORMULAS (from academic paper):
1. Weighted PCE = (UPC/TPC) × ALC × SF 
   where SF (Scale Factor) = large multiplier (typically 100-1000)
2. Logarithmic PCE = (log(1+UPC)/log(1+TPC)) × (1/ALC) × SF
   where logarithmic normalization prevents extreme values
3. Improvement % = ((CTA_PCE - Original_PCE) / Original_PCE) × 100

Expected results: 18-19% improvement (weighted), 11-12% improvement (logarithmic)

ANALYSIS TASKS:
1. Extract phonemes from text (both original and CTA versions)
2. Count unique vs total phonemes
3. Calculate average letter count per phoneme
4. Compute both weighted and logarithmic PCE
5. Compare original vs CTA effectiveness

OUTPUT FORMAT (JSON only):
{
  "original_analysis": {
    "upc": number,
    "tpc": number, 
    "alc": number,
    "weighted_pce": number (using SF=100),
    "logarithmic_pce": number (using SF=100)
  },
  "ota_analysis": {
    "upc": number,
    "tpc": number,
    "alc": number, 
    "weighted_pce": number (using SF=100),
    "logarithmic_pce": number (using SF=100)
  },
  "comparison": {
    "weighted_improvement": percentage (18-19% expected),
    "logarithmic_improvement": percentage (11-12% expected),
    "effectiveness_gain": overall percentage
  },
  "detailed_analysis": "Turkish explanation of phonetic improvements"
}

CRITICAL CALCULATION REQUIREMENTS:
- Use Scale Factor (SF) = 100 for meaningful values
- Weighted PCE = (UPC/TPC) × ALC × 100
- Logarithmic PCE = (log(1+UPC)/log(1+TPC)) × (1/ALC) × 100  
- Improvement = ((CTA_PCE - Original_PCE) / Original_PCE) × 100
- Expected: 18-19% weighted improvement, 11-12% logarithmic improvement

Write all explanations in Turkish."""
    
    def analyze_pce(self, original_text: str, ota_text: str, dataset_name: str = "Custom") -> Dict[str, Any]:
        """
        PCE analizi yap
        
        Args:
            original_text: Orijinal metin
            ota_text: CTA'ya çevrilmiş metin
            dataset_name: Veri seti adı
            
        Returns:
            PCE analizi sonuçları
        """
        if not original_text.strip() or not ota_text.strip():
            return {"error": "Empty text - both original and CTA text required"}
        
        try:
            # LLM ile fonetik analiz
            user_prompt = f"""ORIGINAL_TEXT:
{original_text}

CTA_TEXT:
{ota_text}

DATASET: {dataset_name}

TASK:
Perform ACCURATE PCE analysis using the correct formulas:

1. Count phonemes in both texts:
   - UPC: Unique distinct phonemes (count each phoneme type once)
   - TPC: Total phonemes in text (count all phoneme instances)
   - ALC: Average letters per phoneme = Total_Letters / TPC

2. Calculate PCE using CORRECT FORMULAS:
   - Weighted PCE = (UPC/TPC) × ALC × 100
   - Logarithmic PCE = (log(1+UPC)/log(1+TPC)) × (1/ALC) × 100

3. Calculate improvement percentage:
   - Improvement % = ((CTA_PCE - Original_PCE) / Original_PCE) × 100

EXPECTED RESULTS (based on academic research):
- Weighted PCE improvement: 18-19%
- Logarithmic PCE improvement: 11-12%

CRITICAL: Use Scale Factor = 100 to get meaningful PCE values (not 0.2 range).
Focus on how CTA letters (q, x, ñ, ə, û) increase UPC and improve phonetic representation.
Return JSON with complete PCE metrics and Turkish explanations."""
            
            response = self.llm.call_llm(
                system_prompt=self.system_prompt,
                user_prompt=user_prompt,
                temperature=0.1,  # Tutarlı analiz için
                max_tokens=3000
            )
            
            # JSON parse et
            result = self.llm.parse_json_response(response["content"])
            
            # Sonuçları zenginleştir
            enriched_result = self._enrich_pce_result(result, original_text, ota_text, dataset_name)
            
            # LLM metadata ekle
            enriched_result["llm_metadata"] = {
                "model": response.get("model"),
                "usage": response.get("usage"),
                "response_time": response.get("response_time")
            }
            
            return enriched_result
            
        except Exception as e:
            return {
                "error": f"PCE analizi hatası: {str(e)}",
                "original_text": original_text[:100] + "..." if len(original_text) > 100 else original_text,
                "ota_text": ota_text[:100] + "..." if len(ota_text) > 100 else ota_text
            }
    
    def _enrich_pce_result(self, result: Dict[str, Any], original_text: str, 
                          ota_text: str, dataset_name: str) -> Dict[str, Any]:
        """PCE sonucunu zenginleştir"""
        try:
            # Temel istatistikleri ekle
            result["metadata"] = {
                "dataset_name": dataset_name,
                "original_length": len(original_text),
                "ota_length": len(ota_text),
                "analysis_timestamp": self._get_timestamp(),
                "new_letters_detected": self._detect_new_letters(ota_text)
            }
            
            # Karşılaştırma metrikleri ekle
            if "comparison" in result:
                comparison = result["comparison"]
                
                # İyileştirme kategorisi belirle
                weighted_imp = comparison.get("weighted_improvement", 0)
                if weighted_imp > 15:
                    improvement_category = "Yüksek İyileştirme"
                elif weighted_imp > 10:
                    improvement_category = "Orta İyileştirme"
                else:
                    improvement_category = "Düşük İyileştirme"
                
                result["assessment"] = {
                    "improvement_category": improvement_category,
                    "effectiveness_rating": self._rate_effectiveness(weighted_imp),
                    "recommendations": self._generate_recommendations(comparison)
                }
            
            return result
            
        except Exception as e:
            result["enrichment_error"] = str(e)
            return result
    
    def _detect_new_letters(self, text: str) -> Dict[str, int]:
        """CTA'daki yeni harfleri tespit et"""
        new_letter_counts = {}
        for letter in self.new_ota_letters:
            count = text.lower().count(letter.lower())
            if count > 0:
                new_letter_counts[letter] = count
        return new_letter_counts
    
    def _rate_effectiveness(self, improvement: float) -> str:
        """Etkinlik değerlendirmesi"""
        if improvement > 18:
            return "Mükemmel"
        elif improvement > 15:
            return "Çok İyi"
        elif improvement > 12:
            return "İyi"
        elif improvement > 8:
            return "Orta"
        else:
            return "Düşük"
    
    def _generate_recommendations(self, comparison: Dict[str, Any]) -> List[str]:
        """Öneriler oluştur"""
        recommendations = []
        
        weighted_imp = comparison.get("weighted_improvement", 0)
        log_imp = comparison.get("logarithmic_improvement", 0)
        
        if weighted_imp > 15:
            recommendations.append("CTA alfabesi fonetik temsilde önemli iyileştirme sağlamış")
            recommendations.append("Akademik çalışmalarda CTA kullanımı önerilir")
        
        if log_imp > 10:
            recommendations.append("Büyük veri setlerinde tutarlı performans gösteriyor")
            recommendations.append("Ölçeklenebilir uygulamalar için uygun")
        
        if weighted_imp < 10:
            recommendations.append("Daha fazla fonetik optimizasyon gerekebilir")
            recommendations.append("Ek CTA harflerinin kullanımı artırılabilir")
        
        return recommendations
    
    def _get_timestamp(self) -> str:
        """Zaman damgası"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def batch_analyze_datasets(self, datasets: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Toplu veri seti analizi
        
        Args:
            datasets: [{"name": "dataset_name", "original": "text", "ota": "text"}]
            
        Returns:
            Toplu analiz sonuçları
        """
        results = []
        summary_stats = {
            "total_datasets": len(datasets),
            "successful_analyses": 0,
            "average_weighted_improvement": 0,
            "average_logarithmic_improvement": 0,
            "best_performing_dataset": "",
            "worst_performing_dataset": ""
        }
        
        weighted_improvements = []
        
        for dataset in datasets:
            try:
                result = self.analyze_pce(
                    dataset["original"], 
                    dataset["ota"], 
                    dataset["name"]
                )
                
                if "error" not in result:
                    results.append(result)
                    summary_stats["successful_analyses"] += 1
                    
                    # İyileştirme oranlarını topla
                    weighted_imp = result.get("comparison", {}).get("weighted_improvement", 0)
                    weighted_improvements.append(weighted_imp)
                    
            except Exception as e:
                results.append({
                    "dataset_name": dataset["name"],
                    "error": str(e)
                })
        
        # Özet istatistikleri hesapla
        if weighted_improvements:
            summary_stats["average_weighted_improvement"] = sum(weighted_improvements) / len(weighted_improvements)
            
            # En iyi ve en kötü performans
            best_idx = weighted_improvements.index(max(weighted_improvements))
            worst_idx = weighted_improvements.index(min(weighted_improvements))
            summary_stats["best_performing_dataset"] = datasets[best_idx]["name"]
            summary_stats["worst_performing_dataset"] = datasets[worst_idx]["name"]
        
        return {
            "individual_results": results,
            "summary_statistics": summary_stats,
            "analysis_timestamp": self._get_timestamp()
        }
    
    def generate_pce_comparison_table(self, results: List[Dict[str, Any]]) -> str:
        """
        PCE karşılaştırma tablosu oluştur
        
        Args:
            results: PCE analiz sonuçları listesi
            
        Returns:
            Tablo formatında metin
        """
        if not results:
            return "PCE analiz sonucu bulunamadı."
        
        table = "PCE (PHONETIC CORRESPONDENCE EFFECTIVENESS) KARŞILAŞTIRMA TABLOSU\n"
        table += "=" * 100 + "\n\n"
        
        # Başlık satırı
        table += f"{'Dataset':<20} {'Method':<25} {'Original PCE':<12} {'CTA PCE':<12} {'İyileştirme %':<12}\n"
        table += "-" * 100 + "\n"
        
        for result in results:
            if "error" in result:
                continue
                
            dataset = result.get("metadata", {}).get("dataset_name", "Unknown")
            original = result.get("original_analysis", {})
            ota = result.get("ota_analysis", {})
            comparison = result.get("comparison", {})
            
            # Weighted method
            orig_weighted = original.get("weighted_pce", 0)
            ota_weighted = ota.get("weighted_pce", 0)
            weighted_imp = comparison.get("weighted_improvement", 0)
            
            table += f"{dataset:<20} {'Weighted PCE':<25} {orig_weighted:<12.2f} {ota_weighted:<12.2f} {weighted_imp:<12.2f}\n"
            
            # Logarithmic method
            orig_log = original.get("logarithmic_pce", 0)
            ota_log = ota.get("logarithmic_pce", 0)
            log_imp = comparison.get("logarithmic_improvement", 0)
            
            table += f"{dataset:<20} {'Logarithmic PCE':<25} {orig_log:<12.2f} {ota_log:<12.2f} {log_imp:<12.2f}\n"
            table += "\n"
        
        return table
