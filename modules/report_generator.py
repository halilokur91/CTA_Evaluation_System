"""
Rapor Oluşturucu
CTA analiz sonuçlarından kapsamlı raporlar üretir
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping

class ReportGenerator:
    def __init__(self):
        # Matplotlib için Türkçe font ayarları
        plt.rcParams['font.family'] = ['DejaVu Sans', 'Arial Unicode MS', 'sans-serif']
        plt.rcParams['axes.unicode_minus'] = False
        
        # Seaborn stil ayarları
        sns.set_style("whitegrid")
        sns.set_palette("husl")
    
    def generate_comprehensive_report(self, results: Dict[str, Any]) -> str:
        """
        Kapsamlı analiz raporu oluştur
        
        Args:
            results: Tüm analiz sonuçları
            
        Returns:
            Rapor metni
        """
        report = []
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Başlık
        report.append("=" * 80)
        report.append("CTA (ORTAK TÜRK ALFABESİ) DEĞERLENDİRME RAPORU")
        report.append("=" * 80)
        report.append(f"Rapor Tarihi: {timestamp}")
        report.append("")
        
        # Özet
        report.append("ÖZET")
        report.append("-" * 40)
        report.extend(self._generate_executive_summary(results))
        report.append("")
        
        # Transliterasyon analizi
        if results.get('transliteration'):
            report.append("1. TRANSLİTERASYON ANALİZİ")
            report.append("-" * 40)
            report.extend(self._analyze_transliteration(results['transliteration']))
            report.append("")
        
        # Risk analizi
        if results.get('risk_analysis'):
            report.append("2. FONETİK RİSK ANALİZİ")
            report.append("-" * 40)
            report.extend(self._analyze_risks(results['risk_analysis']))
            report.append("")
        
        # Kognat analizi
        if results.get('cognate_alignment'):
            report.append("3. KOGNAT HİZALAMA ANALİZİ")
            report.append("-" * 40)
            report.extend(self._analyze_cognates(results['cognate_alignment']))
            report.append("")
        
        # Yeni harfler analizi
        report.append("4. YENİ HARFLER (x, ə, q, ñ, û) ANALİZİ")
        report.append("-" * 40)
        report.extend(self._analyze_new_letters(results))
        report.append("")
        
        # Metodoloji
        report.append("5. METODOLOJİ")
        report.append("-" * 40)
        report.extend(self._describe_methodology())
        report.append("")
        
        # Sonuç ve öneriler
        report.append("6. SONUÇ VE ÖNERİLER")
        report.append("-" * 40)
        report.extend(self._generate_conclusions(results))
        
        return "\n".join(report)
    
    def generate_comprehensive_pdf(self, transliteration_result=None, risk_result=None, 
                                 cognate_result=None, pce_result=None, output_path="ota_report.pdf") -> bool:
        """
        Kapsamlı PDF raporu oluştur
        
        Args:
            transliteration_result: Transliterasyon sonuçları
            risk_result: Risk analizi sonuçları  
            cognate_result: Kognat hizalama sonuçları
            output_path: Çıktı dosya yolu
            
        Returns:
            Başarı durumu
        """
        try:
            # PDF doküman oluştur
            doc = SimpleDocTemplate(output_path, pagesize=A4)
            styles = getSampleStyleSheet()
            story = []
            
            # Unicode karakterler için font ayarı
            try:
                # DejaVu Sans font'u kaydet (Unicode desteği için)
                from reportlab.pdfbase.ttfonts import TTFont
                import os
                # Sistem fontlarını dene
                font_paths = [
                    "C:/Windows/Fonts/DejaVuSans.ttf",
                    "C:/Windows/Fonts/arial.ttf",
                    "/System/Library/Fonts/Arial.ttf"  # macOS
                ]
                
                for font_path in font_paths:
                    if os.path.exists(font_path):
                        pdfmetrics.registerFont(TTFont('UnicodeFont', font_path))
                        break
                else:
                    # Varsayılan font kullan
                    pass
            except:
                # Font yüklenemezse varsayılan kullan
                pass
            
            # Özel stiller tanımla (Unicode desteği ile)
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30,
                alignment=1,  # Center
                textColor=colors.HexColor('#1e40af'),
                fontName='Helvetica-Bold'  # Unicode uyumlu
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=16,
                spaceAfter=12,
                textColor=colors.HexColor('#059669'),
                fontName='Helvetica-Bold'
            )
            
            # Normal stil de Unicode uyumlu
            normal_style = ParagraphStyle(
                'CustomNormal',
                parent=styles['Normal'],
                fontName='Helvetica',
                fontSize=12
            )
            
            # Main title
            story.append(Paragraph("CTA (Common Turkic Alphabet) Evaluation Report", title_style))
            story.append(Paragraph(f"Academic Research Report - {datetime.now().strftime('%d/%m/%Y')}", styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Executive Summary
            story.append(Paragraph("Yönetici Özeti", heading_style))
            summary_data = self._generate_pdf_summary(transliteration_result, risk_result, cognate_result, pce_result)
            for line in summary_data:
                # Unicode karakterleri güvenli hale getir
                safe_line = self._make_pdf_safe(line)
                story.append(Paragraph(safe_line, normal_style))
            story.append(Spacer(1, 15))
            
            # Transliterasyon bölümü
            if transliteration_result:
                story.append(Paragraph("1. Transliterasyon Analizi", heading_style))
                trans_data = self._generate_pdf_transliteration(transliteration_result)
                for line in trans_data:
                    safe_line = self._make_pdf_safe(line)
                    story.append(Paragraph(safe_line, normal_style))
                story.append(Spacer(1, 15))
            
            # Risk analizi bölümü
            if risk_result:
                story.append(Paragraph("2. Fonetik Risk Analizi", heading_style))
                risk_data = self._generate_pdf_risks(risk_result)
                for line in risk_data:
                    safe_line = self._make_pdf_safe(line)
                    story.append(Paragraph(safe_line, normal_style))
                story.append(Spacer(1, 15))
                
                # Risk tablosu
                if risk_result.get('risks'):
                    story.append(self._create_risk_table(risk_result['risks']))
                    story.append(Spacer(1, 15))
            
            # Kognat analizi bölümü
            if cognate_result:
                story.append(Paragraph("3. Kognat Hizalama Analizi", heading_style))
                cognate_data = self._generate_pdf_cognates(cognate_result)
                for line in cognate_data:
                    safe_line = self._make_pdf_safe(line)
                    story.append(Paragraph(safe_line, normal_style))
                story.append(Spacer(1, 15))
            
            # PCE analizi bölümü
            if pce_result:
                story.append(Paragraph("4. PCE (Fonetik Uygunluk Etkinliği) Analizi", heading_style))
                pce_data = self._generate_pdf_pce(pce_result)
                for line in pce_data:
                    safe_line = self._make_pdf_safe(line)
                    story.append(Paragraph(safe_line, normal_style))
                story.append(Spacer(1, 15))
            
            # Sonuç ve öneriler
            section_num = 4 + (1 if pce_result else 0)
            story.append(Paragraph(f"{section_num}. Sonuç ve Öneriler", heading_style))
            conclusions = self._generate_pdf_conclusions(transliteration_result, risk_result, cognate_result, pce_result)
            for line in conclusions:
                safe_line = self._make_pdf_safe(line)
                story.append(Paragraph(safe_line, normal_style))
            
            # PDF'i oluştur
            doc.build(story)
            return True
            
        except Exception as e:
            print(f"PDF oluşturma hatası: {str(e)}")
            return False
    
    def _generate_pdf_summary(self, trans_result, risk_result, cognate_result) -> List[str]:
        """Generate PDF summary"""
        summary = []
        summary.append("This report comprehensively evaluates the phonetic representation of the Common Turkic Alphabet (CTA).")
        summary.append("")
        
        if trans_result:
            stats = trans_result.get('statistics', {})
            summary.append(f"• Transliterasyon: {stats.get('source_language', 'Bilinmiyor')} dilinden {stats.get('output_length', 0)} karakter işlendi")
        
        if risk_result:
            risks = risk_result.get('risks', [])
            summary.append(f"• Risk Analizi: {len(risks)} fonetik risk tespit edildi")
            
        if cognate_result:
            stats = cognate_result.get('statistics', {})
            summary.append(f"• Kognat Analizi: {stats.get('total_input_words', 0)} kelime analiz edildi, {stats.get('groups_found', 0)} grup bulundu")
        
        return summary
    
    def _generate_pdf_transliteration(self, result) -> List[str]:
        """PDF için transliterasyon analizi"""
        data = []
        stats = result.get('statistics', {})
        
        data.append(f"Kaynak Dil: {stats.get('source_language', 'Bilinmiyor')}")
        data.append(f"İşlenen Metin Uzunluğu: {stats.get('input_length', 0)} karakter")
        data.append(f"CTA Çıktı Uzunluğu: {stats.get('output_length', 0)} karakter")
        
        new_letters = stats.get('new_letters_used', {})
        if new_letters:
            data.append("Kullanılan Yeni CTA Harfleri:")
            for letter, count in new_letters.items():
                data.append(f"  • {letter}: {count} kez kullanıldı")
        
        notes = result.get('notes', [])
        if notes:
            data.append("Notlar:")
            for note in notes:
                data.append(f"  • {note}")
        
        return data
    
    def _generate_pdf_risks(self, result) -> List[str]:
        """PDF için risk analizi"""
        data = []
        risks = result.get('risks', [])
        stats = result.get('statistics', {})
        
        data.append(f"Toplam Risk Sayısı: {len(risks)}")
        data.append(f"Ortalama Güven Skoru: {stats.get('average_confidence', 0):.2f}")
        
        severity_dist = stats.get('severity_distribution', {})
        data.append(f"Risk Dağılımı: Yüksek {severity_dist.get('high', 0)}, Orta {severity_dist.get('medium', 0)}, Düşük {severity_dist.get('low', 0)}")
        
        return data
    
    def _generate_pdf_cognates(self, result) -> List[str]:
        """PDF için kognat analizi"""
        data = []
        stats = result.get('statistics', {})
        groups = result.get('groups', [])
        
        data.append(f"Toplam Kelime: {stats.get('total_input_words', 0)}")
        data.append(f"Hizalanan Kelime: {stats.get('total_aligned_words', 0)}")
        data.append(f"Bulunan Grup: {stats.get('groups_found', 0)}")
        data.append(f"Hizalama Oranı: {stats.get('alignment_rate', 0):.1%}")
        
        if groups:
            data.append("Benzerlik Grupları:")
            for i, group in enumerate(groups, 1):
                similarity = group.get('similarity', 'bilinmiyor').upper()
                confidence = group.get('confidence', 0)
                rationale = group.get('rationale', '')
                data.append(f"  Grup {i}: {similarity} benzerlik (Güven: {confidence:.2f})")
                data.append(f"    Gerekçe: {rationale}")
        
        return data
    
    def _generate_pdf_pce(self, result) -> List[str]:
        """PDF için PCE analizi"""
        data = []
        metadata = result.get('metadata', {})
        original = result.get('original_analysis', {})
        ota = result.get('ota_analysis', {})
        comparison = result.get('comparison', {})
        
        data.append(f"Veri Seti: {metadata.get('dataset_name', 'Bilinmiyor')}")
        data.append(f"Analiz Edilen Metin: {metadata.get('original_length', 0)} karakter")
        data.append("")
        
        # Orijinal analiz
        if original:
            data.append("Orijinal Metin Analizi:")
            data.append(f"  • UPC (Benzersiz Fonem): {original.get('upc', 0)}")
            data.append(f"  • TPC (Toplam Fonem): {original.get('tpc', 0)}")
            data.append(f"  • ALC (Ortalama Harf): {original.get('alc', 0):.2f}")
            data.append(f"  • Weighted PCE: {original.get('weighted_pce', 0):.2f}")
            data.append(f"  • Logarithmic PCE: {original.get('logarithmic_pce', 0):.2f}")
            data.append("")
        
        # CTA analiz
        if ota:
            data.append("CTA Metin Analizi:")
            data.append(f"  • UPC (Benzersiz Fonem): {ota.get('upc', 0)}")
            data.append(f"  • TPC (Toplam Fonem): {ota.get('tpc', 0)}")
            data.append(f"  • ALC (Ortalama Harf): {ota.get('alc', 0):.2f}")
            data.append(f"  • Weighted PCE: {ota.get('weighted_pce', 0):.2f}")
            data.append(f"  • Logarithmic PCE: {ota.get('logarithmic_pce', 0):.2f}")
            data.append("")
        
        # Karşılaştırma
        if comparison:
            data.append("İyileştirme Oranları:")
            weighted_imp = comparison.get('weighted_improvement', 0)
            log_imp = comparison.get('logarithmic_improvement', 0)
            data.append(f"  • Weighted PCE İyileştirmesi: %{weighted_imp:.2f}")
            data.append(f"  • Logarithmic PCE İyileştirmesi: %{log_imp:.2f}")
            data.append(f"  • Genel Etkinlik Kazancı: %{comparison.get('effectiveness_gain', 0):.2f}")
            data.append("")
        
        # Yeni harfler
        new_letters = metadata.get('new_letters_detected', {})
        if new_letters:
            data.append("Tespit Edilen Yeni CTA Harfleri:")
            for letter, count in new_letters.items():
                # Unicode karakterleri güvenli şekilde encode et
                safe_letter = letter.encode('ascii', 'replace').decode('ascii')
                data.append(f"  • {safe_letter}: {count} kez kullanıldı")
        
        return data
    
    def _generate_pdf_conclusions(self, trans_result, risk_result, cognate_result, pce_result=None) -> List[str]:
        """PDF için sonuç ve öneriler"""
        conclusions = []
        conclusions.append("Bu çalışmada CTA'nın fonetik temsil kapasitesi değerlendirilmiştir.")
        conclusions.append("")
        conclusions.append("Ana Bulgular:")
        
        if trans_result:
            new_letters = trans_result.get('statistics', {}).get('new_letters_used', {})
            if new_letters:
                conclusions.append(f"• Yeni CTA harfleri başarıyla uygulandı: {', '.join(new_letters.keys())}")
        
        if risk_result:
            risks = risk_result.get('risks', [])
            if risks:
                high_risks = [r for r in risks if r.get('severity') == 'high']
                conclusions.append(f"• {len(high_risks)} yüksek riskli fonetik belirsizlik tespit edildi")
        
        if cognate_result:
            stats = cognate_result.get('statistics', {})
            rate = stats.get('alignment_rate', 0)
            conclusions.append(f"• Kognat hizalama oranı: {rate:.1%}")
        
        if pce_result:
            comparison = pce_result.get('comparison', {})
            weighted_imp = comparison.get('weighted_improvement', 0)
            log_imp = comparison.get('logarithmic_improvement', 0)
            conclusions.append(f"• PCE Weighted iyileştirmesi: %{weighted_imp:.2f}")
            conclusions.append(f"• PCE Logarithmic iyileştirmesi: %{log_imp:.2f}")
        
        conclusions.append("")
        conclusions.append("Öneriler:")
        conclusions.append("• CTA'nın standartlaştırılması için daha fazla çalışma gereklidir")
        conclusions.append("• Fonetik risklerin minimize edilmesi için ek kurallar önerilebilir")
        conclusions.append("• Kognat hizalama sonuçları etimolojik araştırmalarda kullanılabilir")
        if pce_result:
            conclusions.append("• PCE metriği yazı sistemi reformları için objektif değerlendirme sağlar")
        
        return conclusions
    
    def _create_risk_table(self, risks) -> Table:
        """Risk tablosu oluştur"""
        data = [['Harf', 'Karışımlar', 'Güven', 'Seviye']]
        
        for risk in risks:
            letter = risk.get('letter', '')
            confusions = ', '.join(risk.get('possible_confusions', []))[:30]
            confidence = f"{risk.get('confidence', 0):.2f}"
            severity = risk.get('severity', '').upper()
            data.append([letter, confusions, confidence, severity])
        
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        return table
    
    def _make_pdf_safe(self, text: str) -> str:
        """PDF için güvenli metin oluştur"""
        # Problemli Unicode karakterleri değiştir
        replacements = {
            'ə': 'e',  # Ters e
            'ñ': 'n',  # Tilde n
            'û': 'u',  # Circumflex u
            'ò': 'o',  # Grave o
            'â': 'a',  # Circumflex a
            'î': 'i',  # Circumflex i
            'ô': 'o'   # Circumflex o
        }
        
        safe_text = text
        for original, replacement in replacements.items():
            safe_text = safe_text.replace(original, replacement)
        
        return safe_text
    
    def _generate_pdf_summary(self, trans_result, risk_result, cognate_result, pce_result=None) -> List[str]:
        """Generate PDF summary"""
        summary = []
        summary.append("This report comprehensively evaluates the phonetic representation of the Common Turkic Alphabet (CTA).")
        summary.append("")
        
        if trans_result:
            stats = trans_result.get('statistics', {})
            summary.append(f"• Transliteration: {stats.get('output_length', 0)} characters processed from {stats.get('source_language', 'Unknown')}")
        
        if risk_result:
            risks = risk_result.get('risks', [])
            summary.append(f"• Risk Analysis: {len(risks)} phonetic risks detected")
            
        if cognate_result:
            stats = cognate_result.get('statistics', {})
            summary.append(f"• Cognate Analysis: {stats.get('total_input_words', 0)} words analyzed, {stats.get('groups_found', 0)} groups found")
        
        if pce_result:
            comparison = pce_result.get('comparison', {})
            weighted_imp = comparison.get('weighted_improvement', 0)
            summary.append(f"• PCE Analysis: {weighted_imp:.2f}% phonetic effectiveness improvement")
        
        return summary
    
    def _generate_executive_summary(self, results: Dict[str, Any]) -> List[str]:
        """Yönetici özeti oluştur"""
        summary = []
        
        # Temel istatistikler
        total_analyses = sum(1 for key in ['transliteration', 'risk_analysis', 'cognate_alignment'] 
                           if results.get(key))
        summary.append(f"Bu rapor {total_analyses} farklı analiz modülünü kapsamaktadır.")
        
        # Transliterasyon özeti
        if results.get('transliteration'):
            trans = results['transliteration']
            if 'statistics' in trans:
                stats = trans['statistics']
                summary.append(f"- Transliterasyon: {stats.get('input_length', 0)} karakter girdi, "
                             f"{stats.get('output_length', 0)} karakter CTA çıktısı")
                
                new_letters = stats.get('new_letters_used', {})
                if new_letters:
                    total_new = sum(new_letters.values())
                    summary.append(f"- Yeni CTA harflerinin toplam kullanımı: {total_new}")
        
        # Risk özeti
        if results.get('risk_analysis'):
            risk = results['risk_analysis']
            if 'statistics' in risk:
                stats = risk['statistics']
                summary.append(f"- Risk analizi: {stats.get('total_risks', 0)} risk tespit edildi")
                
                severity = stats.get('severity_distribution', {})
                high_risk = severity.get('high', 0)
                if high_risk > 0:
                    summary.append(f"- Yüksek riskli durum sayısı: {high_risk}")
        
        # Kognat özeti
        if results.get('cognate_alignment'):
            cog = results['cognate_alignment']
            if 'statistics' in cog:
                stats = cog['statistics']
                summary.append(f"- Kognat hizalama: {stats.get('groups_found', 0)} grup, "
                             f"{stats.get('total_aligned_words', 0)} kelime")
        
        return summary
    
    def _analyze_transliteration(self, trans_result: Dict[str, Any]) -> List[str]:
        """Transliterasyon analizini detaylandır"""
        analysis = []
        
        if 'statistics' in trans_result:
            stats = trans_result['statistics']
            
            analysis.append(f"Kaynak Dil: {stats.get('source_language', 'Bilinmiyor')}")
            analysis.append(f"Girdi Uzunluğu: {stats.get('input_length', 0)} karakter")
            analysis.append(f"Çıktı Uzunluğu: {stats.get('output_length', 0)} karakter")
            
            # Yeni harfler kullanımı
            new_letters = stats.get('new_letters_used', {})
            if new_letters:
                analysis.append("\nYeni Harflerin Kullanımı:")
                for letter, count in sorted(new_letters.items()):
                    analysis.append(f"  {letter}: {count} kez")
            else:
                analysis.append("\nYeni harfler bu metinde kullanılmamış.")
        
        # Notlar
        if trans_result.get('notes'):
            analysis.append("\nNotlar:")
            for note in trans_result['notes']:
                analysis.append(f"  • {note}")
        
        # LLM performansı
        if 'llm_metadata' in trans_result:
            meta = trans_result['llm_metadata']
            analysis.append(f"\nİşlem Süresi: {meta.get('response_time', 0):.2f} saniye")
            if 'usage' in meta:
                usage = meta['usage']
                analysis.append(f"Token Kullanımı: {usage.get('total_tokens', 0)} total")
        
        return analysis
    
    def _analyze_risks(self, risk_result: Dict[str, Any]) -> List[str]:
        """Risk analizini detaylandır"""
        analysis = []
        
        if 'statistics' in risk_result:
            stats = risk_result['statistics']
            
            analysis.append(f"Toplam Risk Sayısı: {stats.get('total_risks', 0)}")
            analysis.append(f"Ortalama Güven Skoru: {stats.get('average_confidence', 0):.2f}")
            
            # Severity dağılımı
            severity = stats.get('severity_distribution', {})
            analysis.append("\nRisk Dağılımı:")
            analysis.append(f"  Yüksek Risk: {severity.get('high', 0)}")
            analysis.append(f"  Orta Risk: {severity.get('medium', 0)}")
            analysis.append(f"  Düşük Risk: {severity.get('low', 0)}")
            
            # En problemli harfler
            problematic = stats.get('most_problematic_letters', [])
            if problematic:
                analysis.append("\nEn Problemli Harfler:")
                for letter, count in problematic:
                    analysis.append(f"  {letter}: {count} risk")
            
            # Etkilenen diller
            languages = stats.get('language_coverage', [])
            if languages:
                analysis.append(f"\nEtkilenen Diller: {', '.join(languages)}")
        
        # Detaylı risk listesi
        risks = risk_result.get('risks', [])
        if risks:
            analysis.append("\nDetaylı Risk Listesi:")
            for i, risk in enumerate(risks[:5], 1):  # İlk 5 riski göster
                analysis.append(f"\n{i}. {risk.get('letter', '')} harfi:")
                analysis.append(f"   Karışımlar: {', '.join(risk.get('possible_confusions', []))}")
                analysis.append(f"   Güven: {risk.get('confidence', 0):.2f}")
                analysis.append(f"   Bağlam: {risk.get('context', '')}")
        
        return analysis
    
    def _analyze_cognates(self, cog_result: Dict[str, Any]) -> List[str]:
        """Kognat analizini detaylandır"""
        analysis = []
        
        if 'statistics' in cog_result:
            stats = cog_result['statistics']
            
            analysis.append(f"Toplam Grup Sayısı: {stats.get('groups_found', 0)}")
            analysis.append(f"Hizalanan Kelime Sayısı: {stats.get('total_aligned_words', 0)}")
            analysis.append(f"Ortalama Grup Büyüklüğü: {stats.get('average_group_size', 0):.1f}")
            analysis.append(f"Hizalama Oranı: {stats.get('alignment_rate', 0):.1%}")
            analysis.append(f"Ortalama Güven Skoru: {stats.get('average_confidence', 0):.2f}")
            
            # Benzerlik dağılımı
            similarity = stats.get('similarity_distribution', {})
            analysis.append("\nBenzerlik Dağılımı:")
            analysis.append(f"  Yüksek Benzerlik: {similarity.get('high', 0)} grup")
            analysis.append(f"  Orta Benzerlik: {similarity.get('medium', 0)} grup")
            analysis.append(f"  Düşük Benzerlik: {similarity.get('low', 0)} grup")
            
            # Dil kapsamı
            languages = stats.get('language_coverage', [])
            if languages:
                analysis.append(f"\nKapsanan Diller: {', '.join(languages)}")
        
        # Örnek gruplar
        groups = cog_result.get('groups', [])
        if groups:
            analysis.append("\nÖrnek Kognat Grupları:")
            for i, group in enumerate(groups[:3], 1):  # İlk 3 grubu göster
                similarity = group.get('similarity', '').upper()
                analysis.append(f"\n{i}. Grup (Benzerlik: {similarity}):")
                analysis.append(f"   Gerekçe: {group.get('rationale', '')}")
                
                for item in group.get('items', []):
                    lang = item.get('lang', '').upper()
                    original = item.get('original', '')
                    ota = item.get('ota', '')
                    analysis.append(f"   {lang}: {original} → {ota}")
        
        return analysis
    
    def _analyze_new_letters(self, results: Dict[str, Any]) -> List[str]:
        """Yeni harflerin kapsamlı analizini yap"""
        analysis = []
        new_letters = ['x', 'X', 'ə', 'Ə', 'ä', 'Ä', 'q', 'Q', 'ñ', 'Ñ', 'û', 'Û', 'ò', 'Ò']
        
        # Kullanım istatistikleri
        usage_stats = {}
        
        # Transliterasyondan kullanım
        if results.get('transliteration', {}).get('statistics', {}).get('new_letters_used'):
            trans_usage = results['transliteration']['statistics']['new_letters_used']
            for letter, count in trans_usage.items():
                usage_stats[letter] = usage_stats.get(letter, 0) + count
        
        # Risk analizinden problemli harfler
        risk_letters = set()
        if results.get('risk_analysis', {}).get('risks'):
            for risk in results['risk_analysis']['risks']:
                letter = risk.get('letter', '')
                if letter in new_letters:
                    risk_letters.add(letter)
        
        analysis.append("Yeni CTA Harflerinin Genel Değerlendirmesi:")
        analysis.append("")
        
        # Her harf için analiz
        letter_info = {
            'q': 'Kalın "k" ayrımı (Kazakça/Kırgızca vb.)',
            'x': 'Gırtlaksı "h" (Azerbaycan/Türkmence kökenli)',
            'ñ': 'Genizsi "n" (Tatar/Türkmen/Özbek "ng")',
            'ə': 'Açık/ön "e" (Azerbaycan vb.)',
            'û': 'Uzunluk işareti (çeşitli Türk dillerinde)',
            'ò': 'Yuvarlak arka ünlü (Özbek o\')',
            'ä': 'Ön ünlü (Almanca ä benzeri)',
            'ğ': 'Yumuşak g (Türkçe ğ)'
        }
        
        for letter_lower in ['q', 'x', 'ñ', 'ä', 'û', 'ò']:
            letter_upper = letter_lower.upper()
            usage_count = usage_stats.get(letter_lower, 0) + usage_stats.get(letter_upper, 0)
            has_risk = letter_lower in risk_letters or letter_upper in risk_letters
            
            analysis.append(f"{letter_lower.upper()}: {letter_info.get(letter_lower, '')}")
            analysis.append(f"   Kullanım: {usage_count} kez")
            analysis.append(f"   Risk durumu: {'Tespit edildi' if has_risk else 'Risk yok'}")
            analysis.append("")
        
        # Genel değerlendirme
        total_usage = sum(usage_stats.values())
        total_risks = len(risk_letters)
        
        analysis.append("Genel Değerlendirme:")
        analysis.append(f"- Toplam yeni harf kullanımı: {total_usage}")
        analysis.append(f"- Risk tespit edilen harf sayısı: {total_risks}")
        
        if total_usage > 0:
            risk_rate = total_risks / len([l for l in new_letters if l.lower() in usage_stats or l.upper() in usage_stats])
            analysis.append(f"- Risk oranı: {risk_rate:.1%}")
        
        return analysis
    
    def _describe_methodology(self) -> List[str]:
        """Metodoloji açıklaması"""
        return [
            "Bu çalışmada LLM destekli bir boru hattı kullanılmıştır:",
            "",
            "1. Transliterasyon Aşaması:",
            "   - Kaynak alfabelerden CTA'ya prompt içi eşleme tabloları",
            "   - Özellikle x, ə, q, ñ, û harflerine odaklanma",
            "   - JSON şema doğrulaması ve karakter filtresi",
            "",
            "2. Fonetik Risk Analizi:",
            "   - LLM tabanlı belirsizlik tespiti",
            "   - Dil-bağımlı karışabilirlik analizi",
            "   - Güven skorları ve severity derecelendirmesi",
            "",
            "3. Kognat Hizalama:",
            "   - CTA normalizasyon sonrası benzerlik gruplandırması",
            "   - Sistematik ses değişimi tanıma",
            "   - Yüksek/orta/düşük benzerlik etiketleme",
            "",
            "4. Kalite Kontrol:",
            "   - İdempotentlik denetimi",
            "   - Yasak karakter filtresi",
            "   - JSON zorunluluğu"
        ]
    
    def _generate_conclusions(self, results: Dict[str, Any]) -> List[str]:
        """Sonuç ve öneriler"""
        conclusions = []
        
        # Transliterasyon başarısı
        if results.get('transliteration'):
            trans = results['transliteration']
            if trans.get('ok'):
                conclusions.append("✓ Transliterasyon işlemi başarıyla tamamlandı")
            else:
                conclusions.append("✗ Transliterasyon işleminde sorunlar tespit edildi")
        
        # Risk durumu
        if results.get('risk_analysis'):
            risk = results['risk_analysis']
            if 'statistics' in risk:
                high_risks = risk['statistics'].get('severity_distribution', {}).get('high', 0)
                if high_risks == 0:
                    conclusions.append("✓ Yüksek riskli fonetik belirsizlik tespit edilmedi")
                else:
                    conclusions.append(f"⚠ {high_risks} yüksek riskli durum tespit edildi")
        
        # Kognat başarısı
        if results.get('cognate_alignment'):
            cog = results['cognate_alignment']
            if 'statistics' in cog:
                alignment_rate = cog['statistics'].get('alignment_rate', 0)
                if alignment_rate > 0.8:
                    conclusions.append("✓ Kognat hizalama başarı oranı yüksek")
                elif alignment_rate > 0.5:
                    conclusions.append("~ Kognat hizalama başarı oranı orta düzeyde")
                else:
                    conclusions.append("⚠ Kognat hizalama başarı oranı düşük")
        
        conclusions.append("")
        conclusions.append("Öneriler:")
        conclusions.append("1. Yeni harflerin (x, ə, q, ñ, û) standardizasyonu devam etmelidir")
        conclusions.append("2. Yüksek riskli durumlar için ek doğrulama mekanizmaları gerekebilir")
        conclusions.append("3. Kognat hizalama algoritması daha fazla dil verisiyle geliştirilmelidir")
        conclusions.append("4. CTA'nın Türk dilleri arası yazı-ses uyumuna katkısı olumludur")
        
        return conclusions
    
    def create_risk_heatmap(self, risk_result: Dict[str, Any]) -> plt.Figure:
        """Risk ısı haritası oluştur"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        risks = risk_result.get('risks', [])
        if not risks:
            ax.text(0.5, 0.5, 'Risk verisi bulunamadı', ha='center', va='center')
            return fig
        
        # Veri hazırlama
        letters = []
        languages = []
        confidence_scores = []
        
        for risk in risks:
            letter = risk.get('letter', '')
            risk_languages = risk.get('languages', [])
            confidence = risk.get('confidence', 0.5)
            
            for lang in risk_languages:
                letters.append(letter)
                languages.append(lang)
                confidence_scores.append(1 - confidence)  # Risk = 1 - confidence
        
        if not letters:
            ax.text(0.5, 0.5, 'Görselleştirilebilir risk verisi yok', ha='center', va='center')
            return fig
        
        # DataFrame oluştur
        df = pd.DataFrame({
            'Letter': letters,
            'Language': languages,
            'Risk': confidence_scores
        })
        
        # Pivot tablo oluştur
        pivot_df = df.pivot_table(values='Risk', index='Letter', columns='Language', aggfunc='mean', fill_value=0)
        
        # Heatmap çiz
        sns.heatmap(pivot_df, annot=True, cmap='Reds', ax=ax, fmt='.2f')
        ax.set_title('Fonetik Risk Isı Haritası\n(Harfler × Diller)', fontsize=14, pad=20)
        ax.set_xlabel('Diller', fontsize=12)
        ax.set_ylabel('CTA Harfleri', fontsize=12)
        
        plt.tight_layout()
        return fig
    
    def create_similarity_distribution(self, cognate_result: Dict[str, Any]) -> plt.Figure:
        """Benzerlik dağılımı grafiği"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        groups = cognate_result.get('groups', [])
        if not groups:
            ax1.text(0.5, 0.5, 'Kognat verisi bulunamadı', ha='center', va='center')
            ax2.text(0.5, 0.5, 'Kognat verisi bulunamadı', ha='center', va='center')
            return fig
        
        # Benzerlik dağılımı
        similarities = [group.get('similarity', 'medium') for group in groups]
        similarity_counts = pd.Series(similarities).value_counts()
        
        colors = {'high': '#2ecc71', 'medium': '#f39c12', 'low': '#e74c3c'}
        similarity_colors = [colors.get(sim, '#95a5a6') for sim in similarity_counts.index]
        
        ax1.pie(similarity_counts.values, labels=similarity_counts.index, autopct='%1.1f%%', 
                colors=similarity_colors, startangle=90)
        ax1.set_title('Kognat Benzerlik Dağılımı', fontsize=12)
        
        # Güven skorları dağılımı
        confidences = [group.get('confidence', 0.5) for group in groups]
        ax2.hist(confidences, bins=10, alpha=0.7, color='skyblue', edgecolor='black')
        ax2.set_xlabel('Güven Skoru', fontsize=10)
        ax2.set_ylabel('Grup Sayısı', fontsize=10)
        ax2.set_title('Güven Skorları Dağılımı', fontsize=12)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def create_new_letters_usage(self, results: Dict[str, Any]) -> plt.Figure:
        """Yeni harflerin kullanım grafiği"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Transliterasyon sonuçlarından yeni harf kullanımını al
        usage_data = {}
        if results.get('transliteration', {}).get('statistics', {}).get('new_letters_used'):
            usage_data = results['transliteration']['statistics']['new_letters_used']
        
        if not usage_data:
            ax.text(0.5, 0.5, 'Yeni harf kullanımı tespit edilmedi', ha='center', va='center')
            return fig
        
        # Grafik çiz
        letters = list(usage_data.keys())
        counts = list(usage_data.values())
        
        bars = ax.bar(letters, counts, color='steelblue', alpha=0.7)
        ax.set_xlabel('CTA Yeni Harfleri', fontsize=12)
        ax.set_ylabel('Kullanım Sayısı', fontsize=12)
        ax.set_title('Yeni CTA Harflerinin Kullanım Sıklığı', fontsize=14, pad=20)
        
        # Bar üzerinde değerleri göster
        for bar, count in zip(bars, counts):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                   str(count), ha='center', va='bottom')
        
        ax.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        return fig
    
    def export_to_json(self, results: Dict[str, Any], filepath: str) -> bool:
        """Sonuçları JSON formatında dışa aktar"""
        try:
            export_data = {
                'timestamp': datetime.now().isoformat(),
                'report_version': '1.0',
                'results': results,
                'metadata': {
                    'generator': 'CTA Evaluation System',
                    'export_format': 'JSON'
                }
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"JSON dışa aktarma hatası: {e}")
            return False
    
    def export_to_csv(self, results: Dict[str, Any], filepath: str) -> bool:
        """Risk analizini CSV formatında dışa aktar"""
        try:
            # Risk verilerini CSV için hazırla
            csv_data = []
            
            if results.get('risk_analysis', {}).get('risks'):
                for risk in results['risk_analysis']['risks']:
                    csv_data.append({
                        'Harf': risk.get('letter', ''),
                        'Karışımlar': ', '.join(risk.get('possible_confusions', [])),
                        'Diller': ', '.join(risk.get('languages', [])),
                        'Örnekler': ', '.join(risk.get('examples', [])),
                        'Güven': risk.get('confidence', 0),
                        'Severity': risk.get('severity', ''),
                        'Bağlam': risk.get('context', '')
                    })
            
            if csv_data:
                df = pd.DataFrame(csv_data)
                df.to_csv(filepath, index=False, encoding='utf-8-sig')
                return True
            else:
                return False
                
        except Exception as e:
            print(f"CSV dışa aktarma hatası: {e}")
            return False
