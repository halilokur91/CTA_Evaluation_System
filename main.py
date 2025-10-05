"""
CTA (Common Turkic Alphabet) Evaluation System
Desktop Application for Academic Research

This application evaluates the phonetic representation of
the Common Turkic Alphabet within an LLM-supported framework.
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import threading
from datetime import datetime
import os
import sys
import re

# Fix Windows UTF-8 encoding issues for console output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        # Python < 3.7
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Import modules
from modules.transliterator import TransliteratorEngine
from modules.risk_analyzer import RiskAnalyzer
from modules.cognate_aligner import CognateAligner
from modules.report_generator import ReportGenerator
from modules.llm_interface import LLMInterface
from modules.pce_analyzer import PCEAnalyzer

# Safe print function for debugging with special characters
def safe_print(message):
    """Safely print debug messages with Unicode characters"""
    try:
        print(message)
    except UnicodeEncodeError:
        # Fallback: print without special characters
        print(message.encode('ascii', 'replace').decode('ascii'))

class CTAEvaluationApp:
    def __init__(self):
        # Main window settings - Academic Light Theme
        ctk.set_appearance_mode("light")  
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.title("🔤 CTA Evaluation System - Academic Research Tool")
        self.root.geometry("1500x1000")
        self.root.minsize(1300, 900)
        
        # Professional colors suitable for academic papers
        self.colors = {
            'primary': "#1e40af",      # Academic blue
            'primary_hover': "#1d4ed8", 
            'secondary': "#6366f1",    # Indigo
            'success': "#059669",      # Emerald
            'warning': "#d97706",      # Orange
            'danger': "#dc2626",       # Red
            'info': "#0284c7",         # Sky blue
            'light_bg': "#f8fafc",     # Very light gray
            'card_bg': "#ffffff",      # Pure white
            'text_primary': "#1f2937", # Dark gray
            'text_secondary': "#6b7280", # Medium gray
            'border_light': "#e5e7eb", # Light border
            'accent_bg': "#f1f5f9"     # Light accent
        }
        
        # Initialize modules
        self.llm_interface = LLMInterface()
        self.transliterator = TransliteratorEngine(self.llm_interface)
        self.risk_analyzer = RiskAnalyzer(self.llm_interface)
        self.cognate_aligner = CognateAligner(self.llm_interface)
        self.report_generator = ReportGenerator()
        self.pce_analyzer = PCEAnalyzer(self.llm_interface)
        
        # Create UI components
        self.setup_ui()
        
        # Load settings from existing config
        self.load_existing_settings()
        
        # To store results
        self.results = {
            'transliteration': None,
            'risk_analysis': None,
            'cognate_alignment': None,
            'pce_analysis': None
        }
    
    def setup_ui(self):
        """Create main interface - Modern design"""
        # Main title - Academic header
        title_frame = ctk.CTkFrame(
            self.root, 
            height=100,
            corner_radius=12,
            fg_color=self.colors['light_bg'],
            border_width=2,
            border_color=self.colors['border_light']
        )
        title_frame.pack(fill="x", padx=25, pady=15)
        title_frame.pack_propagate(False)
        
        # Main title
        title_label = ctk.CTkLabel(
            title_frame, 
            text="📚 CTA (Common Turkic Alphabet) Evaluation System",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.colors['primary']
        )
        title_label.pack(pady=(15, 5))
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            title_frame,
            text="For Academic Research • LLM-Supported Analysis • Phonetic Evaluation Platform",
            font=ctk.CTkFont(size=14),
            text_color=self.colors['text_secondary']
        )
        subtitle_label.pack(pady=(0, 15))
        
        # Main content container - Modern card design
        main_container = ctk.CTkFrame(
            self.root,
            corner_radius=20,
            fg_color="transparent"
        )
        main_container.pack(fill="both", expand=True, padx=25, pady=(0, 25))
        
        # Tab system - Academic tab design
        self.notebook = ctk.CTkTabview(
            main_container,
            corner_radius=12,
            border_width=1,
            border_color=self.colors['border_light'],
            segmented_button_fg_color=self.colors['accent_bg'],
            segmented_button_selected_color=self.colors['primary'],
            segmented_button_selected_hover_color=self.colors['primary_hover'],
            text_color=self.colors['text_primary'],
            text_color_disabled=self.colors['text_secondary']
        )
        self.notebook.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Create tabs
        self.create_module_introduction_tab()
        self.create_transliteration_tab()
        self.create_risk_analysis_tab()
        self.create_cognate_alignment_tab()
        self.create_pce_analysis_tab()
        self.create_reports_tab()
        self.create_settings_tab()
    
    def create_module_introduction_tab(self):
        """Module introduction tab - Modern card layout"""
        tab = self.notebook.add("📚 Module Introduction")
        
        # Main scroll frame - Modern styling
        main_scroll = ctk.CTkScrollableFrame(
            tab,
            corner_radius=12,
            scrollbar_button_color=self.colors['primary'],
            scrollbar_button_hover_color=self.colors['primary_hover']
        )
        main_scroll.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Hero section - Academic welcome card
        hero_card = ctk.CTkFrame(
            main_scroll,
            corner_radius=12,
            fg_color=self.colors['accent_bg'],
            border_width=2,
            border_color=self.colors['primary'],
            height=120
        )
        hero_card.pack(fill="x", pady=(0, 25))
        hero_card.pack_propagate(False)
        
        hero_title = ctk.CTkLabel(
            hero_card, 
            text="📚 CTA Evaluation System",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.colors['primary']
        )
        hero_title.pack(pady=(20, 5))
        
        hero_subtitle = ctk.CTkLabel(
            hero_card,
            text="Evaluate the phonetic representation of the Common Turkic Alphabet to academic standards with 6 main modules",
            font=ctk.CTkFont(size=16),
            text_color=self.colors['text_secondary'],
            wraplength=700
        )
        hero_subtitle.pack(pady=(0, 20))
        
        # Module 1: Transliteration Engine
        self._create_module_section(main_scroll, "🔄 1. Transliteration Engine", self.colors['info'], """
PURPOSE: Converts from different Turkic language alphabets to CTA.

FEATURES:
• Supports 6 different source languages: Turkish, Uzbek Latin, Kazakh Cyrillic, Azerbaijani Latin, Turkmen Latin, Kyrgyz Cyrillic
• Systematic conversion with predefined mapping rules
• Focuses on 5 new CTA letters: x, ə→ä, q, ñ, û
• JSON schema validation and character filtering
• Statistical analysis and usage reports

TECHNICAL DETAILS:
• LLM-based prompt engineering
• Phonetic context analysis
• Morphophonological environment consideration
• Idempotency control
• Quality assurance mechanisms

USE CASES:
• Text standardization between Turkic languages
• Academic research and corpus creation
• Multilingual document processing
• Phonetic writing system analysis""")
        
        # Module 2: Risk Analyzer
        self._create_module_section(main_scroll, "⚠️ 2. Phonetic Risk Analyzer", self.colors['warning'], """
PURPOSE: Detects phonetic ambiguities and confusions in CTA text.

FEATURES:
• Performs risk analysis of new CTA letters (x, ə, q, ñ, û)
• Language-dependent confusion detection
• Confidence scores (0.0-1.0) and severity grading (low/medium/high)
• Recognizes cross-linguistic confusion patterns
• Includes morphophonological environment analysis

ANALYSIS CRITERIA:
• x: uvular vs. velar fricative confusion
• ə→ä: open/front vowel confusions (with e/a)
• q: velar vs. uvular stop confusion (with k)
• ñ: nasal confusion (ng↔ñ transitions)
• û: length marker deficiency/excess

OUTPUT FORMAT:
• Detailed risk table
• Statistical summary
• Most problematic letters list
• Language coverage analysis""")
        
        # Module 3: Cognate Aligner
        self._create_module_section(main_scroll, "🔗 3. Cognate Aligner", self.colors['success'], """
PURPOSE: Aligns cognate words from different Turkic languages in CTA and performs similarity analysis.

FEATURES:
• Supports 11 Turkic languages (tr, az, uz, kk, ky, tk, tt, ba, cv, sah, ug)
• Phonetic similarity grouping after CTA normalization
• 3 similarity levels: HIGH (systematic sound correspondence), MEDIUM (possible cognate), LOW (distant relationship)
• Systematic sound change recognition (k~q, sh~ş, e~ä, etc.)
• Morphological analysis (root + suffix separation)

WORKING PRINCIPLE:
1. Transliterate each candidate word to CTA
2. Group by phonetic similarity level
3. Identify systematic sound correspondences
4. Provide confidence scores and rationales
5. Perform root analysis (if possible)

USE SCENARIOS:
• Etymological research
• Comparative linguistics studies
• Inter-Turkic language dictionary development
• Detection of phonetic change patterns""")
        
        # Module 4: Report Generator
        self._create_module_section(main_scroll, "📊 4. Report Generator", self.colors['secondary'], """
PURPOSE: Generates comprehensive and visualized reports from all analysis results.

FEATURES:
• Comprehensive analysis report generation
• Statistical visualizations (matplotlib/seaborn)
• Risk heat maps
• Similarity distribution charts
• New letter usage analysis
• Multiple format support (PDF, Excel, JSON, CSV)

REPORT TYPES:
• Executive Summary
• Detailed transliteration analysis
• Phonetic risk assessment
• Cognate alignment results
• Comprehensive analysis of new letters (x, ə, q, ñ, û)
• Methodology explanations

VISUALIZATIONS:
• Risk heat map (letters × languages)
• Similarity distribution pie chart
• Confidence scores histogram
• New letter usage bar chart""")
        
        # Module 5: LLM Interface
        self._create_module_section(main_scroll, "🤖 5. LLM Interface", self.colors['primary'], """
PURPOSE: Provides secure and efficient interaction with OpenAI API.

FEATURES:
• OpenAI GPT-4/3.5-turbo support
• Smart JSON parsing (error tolerant)
• CTA character set validation
• Token usage tracking and optimization
• Response time measurement
• Error handling and retry

SECURITY:
• Secure API key storage
• Rate limiting protection
• Input validation
• Output sanitization
• Error handling

PERFORMANCE:
• Intelligent prompt engineering
• Context window optimization
• Batch processing support
• Response caching (future)
• Token usage analytics

JSON PARSING:
• Regex-based fallback parsing
• Multiple format support (array/object)
• Prefix/suffix cleaning
• Error-tolerant extraction""")
        
        # Module 6: PCE Analyzer
        self._create_module_section(main_scroll, "📊 6. PCE (Phonetic Correspondence Effectiveness) Analyzer", self.colors['warning'], """
PURPOSE: Objectively measures and compares the phonetic representation of writing systems.

FEATURES:
• UPC (Unique Phoneme Count) - Calculate unique phoneme count
• TPC (Total Phoneme Count) - Total phoneme count analysis
• ALC (Average Letter Count) - Average letter count calculation
• Weighted PCE and Logarithmic PCE calculation methods
• Original vs CTA comparative analysis
• 18-19% improvement rates (weighted method)
• 11-12% improvement rates (logarithmic method)

CALCULATION METHODS:
• Weighted PCE: (UPC/TPC) × ALC × Scaling Factor
• Logarithmic PCE: log(UPC) + log(ALC) + Constant
• Improvement Rate: ((CTA_PCE - Original_PCE) / Original_PCE) × 100

ACADEMIC VALUE:
• Objective writing system evaluation
• G2P model-independent analysis
• Multilingual comparison capability
• Scientific basis for writing reforms
• Phonetic effectiveness measurement for NLP applications

USE CASES:
• Writing system reform evaluation
• Phonetic representation effectiveness measurement
• Academic research and paper writing
• Language technology development
• Multilingual educational material design""")
        
        # System Architecture
        self._create_module_section(main_scroll, "🏗️ System Architecture", self.colors['danger'], """
GENERAL FLOW:
1. User input → Transliteration Engine → CTA text
2. CTA text → Risk Analyzer → Phonetic risk report
3. Candidate words → Cognate Aligner → Similarity groups
4. All results → Report Generator → Comprehensive analysis

INTER-MODULE COMMUNICATION:
• Each module uses LLM Interface
• JSON-based data exchange
• Standardized error handling
• Metadata and statistics sharing

QUALITY ASSURANCE:
• Input/output validation in each module
• JSON schema control in LLM responses
• Character set filtering
• Statistical consistency checks

ACADEMIC STANDARDS:
• Reproducible results
• Detailed methodology documentation
• Statistical significance testing
• Error rate analysis
• Confidence interval reporting""")
    
    def _create_module_section(self, parent, title, color, content):
        """Create module section - Modern card design"""
        # Academic card container
        card_frame = ctk.CTkFrame(
            parent,
            corner_radius=12,
            fg_color=self.colors['card_bg'],
            border_width=2,
            border_color=color
        )
        card_frame.pack(fill="x", pady=(0, 20), padx=5)
        
        # Header with colored accent
        header_frame = ctk.CTkFrame(
            card_frame,
            corner_radius=10,
            fg_color=color,
            height=50
        )
        header_frame.pack(fill="x", padx=15, pady=15)
        header_frame.pack_propagate(False)
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text=title,
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="white"
        )
        title_label.pack(pady=12)
        
        # Content area
        content_frame = ctk.CTkFrame(
            card_frame,
            corner_radius=10,
            fg_color="transparent"
        )
        content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Content text
        content_label = ctk.CTkLabel(
            content_frame,
            text=content.strip(),
            font=ctk.CTkFont(size=12),
            wraplength=900,
            justify="left",
            anchor="nw",
            text_color=self.colors['text_primary']
        )
        content_label.pack(pady=10, fill="both", expand=True)
    
    def create_transliteration_tab(self):
        """Transliteration tab - Modern dual panel design"""
        tab = self.notebook.add("🔄 Transliteration")
        
        # Ana container
        main_container = ctk.CTkFrame(tab, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Sol panel - Giriş (Modern card design)
        left_panel = ctk.CTkFrame(
            main_container,
            corner_radius=15,
            fg_color=self.colors['card_bg']
        )
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Sol panel başlığı
        left_header = ctk.CTkFrame(
            left_panel,
            corner_radius=12,
            fg_color=self.colors['info'],
            height=60
        )
        left_header.pack(fill="x", padx=20, pady=20)
        left_header.pack_propagate(False)
        
        ctk.CTkLabel(
            left_header,
            text="📝 Source Text",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        ).pack(pady=15)
        
        # Language selection - Modern card
        lang_card = ctk.CTkFrame(left_panel, corner_radius=10)
        lang_card.pack(fill="x", padx=20, pady=(0, 15))
        
        lang_label = ctk.CTkLabel(
            lang_card,
            text="🌍 Select Source Language:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        lang_label.pack(pady=(15, 10))
        
        self.source_lang = ctk.CTkOptionMenu(
            lang_card,
            values=["Turkish", "Uzbek Latin", "Kazakh Cyrillic", "Azerbaijani Latin", "Turkmen Latin", "Kyrgyz Cyrillic"],
            width=300,
            height=35,
            corner_radius=8,
            font=ctk.CTkFont(size=13),
            dropdown_font=ctk.CTkFont(size=12)
        )
        self.source_lang.pack(pady=(0, 15))
        
        # Text input area
        text_label = ctk.CTkLabel(
            left_panel,
            text="✍️ Write your text here:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        text_label.pack(pady=(0, 10), padx=20, anchor="w")
        
        self.input_text = ctk.CTkTextbox(
            left_panel,
            height=200,
            corner_radius=10,
            font=ctk.CTkFont(size=13),
            border_width=2,
            border_color=self.colors['info']
        )
        # Metin alanı - responsive
        self.input_text.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        
        # BUTONLAR - SABİT BOTTOM AREA
        button_area = ctk.CTkFrame(left_panel, fg_color="transparent")
        button_area.pack(fill="x", side="bottom", padx=20, pady=(0, 20))
        
        # Butonları ortalamak için wrapper
        button_wrapper = ctk.CTkFrame(button_area, fg_color="transparent")
        button_wrapper.pack(anchor="center")
        
        # Load from file button
        self.load_btn = ctk.CTkButton(
            button_wrapper,
            text="📁 LOAD FROM FILE",
            command=self.load_text_file,
            width=190,
            height=45,
            corner_radius=10,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#6366f1",
            hover_color="#4f46e5",
            text_color="white"
        )
        self.load_btn.pack(side="left", padx=(0, 15))
        
        # Translitere et butonu
        self.process_btn = ctk.CTkButton(
            button_wrapper,
            text="🚀 TRANSLITERATE",
            command=self.run_transliteration,
            width=190,
            height=45,
            corner_radius=10,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#22c55e",
            hover_color="#16a34a",
            text_color="white"
        )
        self.process_btn.pack(side="right", padx=(15, 0))
        
        # Sağ panel - Çıkış (Modern card design)
        right_panel = ctk.CTkFrame(
            main_container,
            corner_radius=15,
            fg_color=self.colors['card_bg']
        )
        right_panel.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Sağ panel başlığı
        right_header = ctk.CTkFrame(
            right_panel,
            corner_radius=12,
            fg_color=self.colors['primary'],
            height=60
        )
        right_header.pack(fill="x", padx=20, pady=20)
        right_header.pack_propagate(False)
        
        ctk.CTkLabel(
            right_header,
            text="🎯 CTA Output",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        ).pack(pady=15)
        
        # Result area
        result_label = ctk.CTkLabel(
            right_panel,
            text="📄 Transliteration Result:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        result_label.pack(pady=(0, 10), padx=20, anchor="w")
        
        self.transliteration_result = ctk.CTkTextbox(
            right_panel,
            height=250,
            corner_radius=10,
            font=ctk.CTkFont(size=13),
            border_width=2,
            border_color=self.colors['primary']
        )
        self.transliteration_result.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        
        # Notlar alanı
        notes_label = ctk.CTkLabel(
            right_panel,
            text="📝 Notes and Explanations:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        notes_label.pack(pady=(0, 10), padx=20, anchor="w")
        
        self.transliteration_notes = ctk.CTkTextbox(
            right_panel,
            height=120,
            corner_radius=10,
            font=ctk.CTkFont(size=12),
            border_width=1,
            border_color=self.colors['secondary']
        )
        self.transliteration_notes.pack(fill="x", padx=20, pady=(0, 15))
        
        # Kaydet butonu
        save_btn = ctk.CTkButton(
            right_panel,
            text="💾 Save Result",
            command=self.save_transliteration_result,
            width=200,
            height=40,
            corner_radius=10,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=self.colors['warning'],
            hover_color=("#b45309")
        )
        save_btn.pack(pady=(0, 20))
    
    def create_risk_analysis_tab(self):
        """Risk analysis tab - Modern design"""
        tab = self.notebook.add("⚠️ Phonetic Risk Analysis")
        
        # Ana container
        main_container = ctk.CTkFrame(tab, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Üst panel - Giriş (Modern card design)
        input_card = ctk.CTkFrame(
            main_container,
            corner_radius=15,
            fg_color=self.colors['card_bg'],
            height=250
        )
        input_card.pack(fill="x", pady=(0, 15))
        input_card.pack_propagate(False)
        
        # Başlık
        input_header = ctk.CTkFrame(
            input_card,
            corner_radius=12,
            fg_color=self.colors['warning'],
            height=55
        )
        input_header.pack(fill="x", padx=20, pady=20)
        input_header.pack_propagate(False)
        
        ctk.CTkLabel(
            input_header,
            text="⚠️ CTA Text Risk Analysis",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        ).pack(pady=12)
        
        # Text input area
        input_label = ctk.CTkLabel(
            input_card,
            text="📝 Enter CTA text to analyze:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        input_label.pack(pady=(0, 10), padx=20, anchor="w")
        
        # Input ve buton container
        input_container = ctk.CTkFrame(input_card, fg_color="transparent")
        input_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.risk_input_text = ctk.CTkTextbox(
            input_container,
            height=120,
            corner_radius=10,
            font=ctk.CTkFont(size=13),
            border_width=2,
            border_color=self.colors['warning']
        )
        self.risk_input_text.pack(fill="both", expand=True, side="left", padx=(0, 15))
        
        # Analysis button - Vertical on the right
        analyze_btn = ctk.CTkButton(
            input_container,
            text="🔍\nRun\nRisk\nAnalysis",
            command=self.run_risk_analysis,
            width=100,
            height=120,
            corner_radius=10,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=self.colors['danger'],
            hover_color=("#b91c1c")
        )
        analyze_btn.pack(side="right", fill="y")
        
        # Bottom panel - Results (Modern table design)
        results_card = ctk.CTkFrame(
            main_container,
            corner_radius=15,
            fg_color=self.colors['card_bg']
        )
        results_card.pack(fill="both", expand=True)
        
        # Results header
        results_header = ctk.CTkFrame(
            results_card,
            corner_radius=12,
            fg_color=self.colors['danger'],
            height=55
        )
        results_header.pack(fill="x", padx=20, pady=20)
        results_header.pack_propagate(False)
        
        ctk.CTkLabel(
            results_header,
            text="📊 Risk Analysis Results",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        ).pack(pady=12)
        
        # Treeview için akademik container
        tree_container = ctk.CTkFrame(
            results_card,
            corner_radius=8,
            fg_color=self.colors['accent_bg'],
            border_width=1,
            border_color=self.colors['border_light']
        )
        tree_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Treeview için sonuçlar tablosu
        columns = ("Letter", "Confusions", "Languages", "Example", "Confidence")
        self.risk_tree = ttk.Treeview(
            tree_container, 
            columns=columns, 
            show="headings", 
            height=15
        )
        
        # Column styling
        for col in columns:
            self.risk_tree.heading(col, text=col)
            self.risk_tree.column(col, width=150, anchor="center")
        
        # Modern scrollbar
        risk_scrollbar = ttk.Scrollbar(
            tree_container, 
            orient="vertical", 
            command=self.risk_tree.yview
        )
        self.risk_tree.configure(yscrollcommand=risk_scrollbar.set)
        
        # Pack treeview ve scrollbar
        self.risk_tree.pack(side="left", fill="both", expand=True, padx=15, pady=15)
        risk_scrollbar.pack(side="right", fill="y", padx=(0, 15), pady=15)
    
    def create_cognate_alignment_tab(self):
        """Cognate alignment tab - Modern dual panel design"""
        tab = self.notebook.add("🔗 Cognate Alignment")
        
        # Ana container
        main_container = ctk.CTkFrame(tab, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Sol panel - Giriş (Modern card design)
        left_panel = ctk.CTkFrame(
            main_container,
            corner_radius=15,
            fg_color=self.colors['card_bg']
        )
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Sol panel başlığı
        left_header = ctk.CTkFrame(
            left_panel,
            corner_radius=12,
            fg_color=self.colors['success'],
            height=60
        )
        left_header.pack(fill="x", padx=20, pady=20)
        left_header.pack_propagate(False)
        
        ctk.CTkLabel(
            left_header,
            text="📝 Candidate Words",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        ).pack(pady=15)
        
        # Short format explanation
        format_label = ctk.CTkLabel(
            left_panel,
            text="📋 Format: language_code:word (tr:şehir, az:şəhər)",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=self.colors['text_secondary']
        )
        format_label.pack(pady=(0, 10), padx=20)
        
        # Kelime giriş alanı
        input_label = ctk.CTkLabel(
            left_panel,
            text="✍️ Enter candidate words:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        input_label.pack(pady=(0, 10), padx=20, anchor="w")
        
        self.cognate_input = ctk.CTkTextbox(
            left_panel,
            height=200,
            corner_radius=10,
            font=ctk.CTkFont(size=13),
            border_width=2,
            border_color=self.colors['success']
        )
        self.cognate_input.pack(fill="x", padx=20, pady=(0, 5))
        
        # SABİT BUTON ALANI - TAM EKRANDA DA GÖRÜNÜR
        fixed_button_area = ctk.CTkFrame(left_panel, height=140, fg_color="transparent")
        fixed_button_area.pack(fill="x", side="bottom", padx=10, pady=10)
        fixed_button_area.pack_propagate(False)
        
        # Ana buton
        self.cognate_analyze_btn = ctk.CTkButton(
            fixed_button_area,
            text="🚀 START COGNATE ANALYSIS",
            command=self.run_cognate_alignment,
            width=380,
            height=55,
            corner_radius=12,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#dc2626",
            hover_color="#b91c1c",
            text_color="white"
        )
        self.cognate_analyze_btn.pack(pady=(10, 5))
        
        # İkinci buton
        self.cognate_analyze_btn2 = ctk.CTkButton(
            fixed_button_area,
            text="🔍 TRANSLATE AND ANALYZE",
            command=self.run_cognate_alignment,
            width=380,
            height=45,
            corner_radius=10,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#7c3aed",
            hover_color="#6d28d9",
            text_color="white"
        )
        self.cognate_analyze_btn2.pack(pady=(5, 10))
        
        # Sağ panel - Sonuçlar (Modern card design)
        right_panel = ctk.CTkFrame(
            main_container,
            corner_radius=15,
            fg_color=self.colors['card_bg']
        )
        right_panel.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Sağ panel başlığı
        right_header = ctk.CTkFrame(
            right_panel,
            corner_radius=12,
            fg_color=self.colors['info'],
            height=60
        )
        right_header.pack(fill="x", padx=20, pady=20)
        right_header.pack_propagate(False)
        
        ctk.CTkLabel(
            right_header,
            text="📊 Alignment Results",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        ).pack(pady=15)
        
        # Sonuçlar alanı
        results_label = ctk.CTkLabel(
            right_panel,
            text="📄 Similarity Groups and Analysis:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        results_label.pack(pady=(0, 10), padx=20, anchor="w")
        
        self.cognate_results = ctk.CTkTextbox(
            right_panel,
            height=500,
            corner_radius=10,
            font=ctk.CTkFont(size=12),
            border_width=2,
            border_color=self.colors['info']
        )
        self.cognate_results.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    def create_pce_analysis_tab(self):
        """PCE (Phonetic Correspondence Effectiveness) analysis tab"""
        tab = self.notebook.add("📊 PCE Analysis")
        
        # Ana container
        main_container = ctk.CTkFrame(tab, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Üst panel - Giriş (sabit yükseklik)
        input_panel = ctk.CTkFrame(
            main_container,
            corner_radius=15,
            fg_color=self.colors['card_bg'],
            height=250
        )
        input_panel.pack(fill="x", pady=(0, 10))
        input_panel.pack_propagate(False)
        
        # Başlık
        input_header = ctk.CTkFrame(
            input_panel,
            corner_radius=12,
            fg_color=self.colors['info'],
            height=55
        )
        input_header.pack(fill="x", padx=20, pady=20)
        input_header.pack_propagate(False)
        
        ctk.CTkLabel(
            input_header,
            text="📊 PCE (Phonetic Correspondence Effectiveness) Analysis",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        ).pack(pady=12)
        
        # İçerik container
        content_container = ctk.CTkFrame(input_panel, fg_color="transparent")
        content_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Sol taraf - Orijinal metin
        left_input = ctk.CTkFrame(content_container, fg_color="transparent")
        left_input.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        orig_label = ctk.CTkLabel(
            left_input,
            text="📝 Original Text:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        orig_label.pack(pady=(0, 10), anchor="w")
        
        self.pce_original_text = ctk.CTkTextbox(
            left_input,
            height=120,
            corner_radius=10,
            font=ctk.CTkFont(size=12),
            border_width=2,
            border_color=self.colors['secondary']
        )
        self.pce_original_text.pack(fill="x")
        
        # Sağ taraf - CTA metin
        right_input = ctk.CTkFrame(content_container, fg_color="transparent")
        right_input.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        ota_label = ctk.CTkLabel(
            right_input,
            text="🔤 CTA Text:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        ota_label.pack(pady=(0, 10), anchor="w")
        
        self.pce_ota_text = ctk.CTkTextbox(
            right_input,
            height=120,
            corner_radius=10,
            font=ctk.CTkFont(size=12),
            border_width=2,
            border_color=self.colors['primary']
        )
        self.pce_ota_text.pack(fill="x")
        
        # Orta panel - Kontroller (küçültüldü)
        control_panel = ctk.CTkFrame(
            main_container,
            corner_radius=15,
            fg_color=self.colors['card_bg'],
            height=80
        )
        control_panel.pack(fill="x", pady=(0, 10))
        control_panel.pack_propagate(False)
        
        # Dataset adı ve buton
        control_content = ctk.CTkFrame(control_panel, fg_color="transparent")
        control_content.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Sol taraf - Dataset adı
        left_control = ctk.CTkFrame(control_content, fg_color="transparent")
        left_control.pack(side="left", fill="both", expand=True, padx=(0, 15))
        
        dataset_label = ctk.CTkLabel(
            left_control,
            text="📋 Dataset:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        dataset_label.pack(pady=(5, 2), anchor="w")
        
        self.pce_dataset_name = ctk.CTkEntry(
            left_control,
            width=250,
            height=30,
            corner_radius=8,
            font=ctk.CTkFont(size=12),
            placeholder_text="TTC4900, Custom_Dataset"
        )
        self.pce_dataset_name.pack(anchor="w")
        
        # Sağ taraf - Analiz butonu
        right_control = ctk.CTkFrame(control_content, fg_color="transparent")
        right_control.pack(side="right", fill="y")
        
        pce_btn = ctk.CTkButton(
            right_control,
            text="🔬 RUN PCE ANALYSIS",
            command=self.run_pce_analysis,
            width=180,
            height=50,
            corner_radius=10,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=self.colors['warning'],
            hover_color=("#b45309"),
            text_color="white"
        )
        pce_btn.pack(pady=10)
        
        # Alt panel - Sonuçlar
        results_panel = ctk.CTkFrame(
            main_container,
            corner_radius=15,
            fg_color=self.colors['card_bg']
        )
        results_panel.pack(fill="both", expand=True)
        
        # Results header (küçültüldü)
        results_header = ctk.CTkFrame(
            results_panel,
            corner_radius=12,
            fg_color=self.colors['warning'],
            height=45
        )
        results_header.pack(fill="x", padx=20, pady=15)
        results_header.pack_propagate(False)
        
        ctk.CTkLabel(
            results_header,
            text="📈 PCE Analysis Results",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="white"
        ).pack(pady=10)
        
        # Sonuçlar alanı - MUTLAKA GÖRÜNÜR
        self.pce_results = ctk.CTkTextbox(
            results_panel,
            height=400,
            corner_radius=10,
            font=ctk.CTkFont(size=11),
            border_width=2,
            border_color=self.colors['warning']
        )
        self.pce_results.pack(fill="both", expand=True, padx=20, pady=(0, 15))
    
    def create_reports_tab(self):
        """Reports tab - Modern design"""
        tab = self.notebook.add("📊 Reports")
        
        # Ana container
        main_container = ctk.CTkFrame(tab, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Üst panel - Rapor seçimi ve butonları
        control_panel = ctk.CTkFrame(
            main_container,
            corner_radius=15,
            fg_color=self.colors['card_bg'],
            height=200
        )
        control_panel.pack(fill="x", pady=(0, 15))
        control_panel.pack_propagate(False)
        
        # Başlık
        control_header = ctk.CTkFrame(
            control_panel,
            corner_radius=12,
            fg_color=self.colors['secondary'],
            height=55
        )
        control_header.pack(fill="x", padx=20, pady=20)
        control_header.pack_propagate(False)
        
        ctk.CTkLabel(
            control_header,
            text="📊 Report Generation Center",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        ).pack(pady=12)
        
        # İçerik container
        control_content = ctk.CTkFrame(control_panel, fg_color="transparent")
        control_content.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Sol taraf - Rapor türü seçimi
        left_control = ctk.CTkFrame(control_content, fg_color="transparent")
        left_control.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        type_label = ctk.CTkLabel(
            left_control,
            text="📋 Select Report Type:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        type_label.pack(pady=(10, 10), anchor="w")
        
        self.report_type = ctk.CTkOptionMenu(
            left_control,
            values=["Comprehensive Analysis Report", "Transliteration Summary", "Risk Analysis Details", "Cognate Alignment Report"],
            width=300,
            height=35,
            corner_radius=8,
            font=ctk.CTkFont(size=13)
        )
        self.report_type.pack(pady=(0, 10), anchor="w")
        
        # Sağ taraf - Butonlar
        right_control = ctk.CTkFrame(control_content, fg_color="transparent")
        right_control.pack(side="right", fill="y")
        
        button_label = ctk.CTkLabel(
            right_control,
            text="🎯 Report Format:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        button_label.pack(pady=(10, 10))
        
        # Buton container
        button_grid = ctk.CTkFrame(right_control, fg_color="transparent")
        button_grid.pack()
        
        pdf_btn = ctk.CTkButton(
            button_grid,
            text="📄 PDF",
            command=self.generate_pdf_report,
            width=100,
            height=35,
            corner_radius=8,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=self.colors['danger'],
            hover_color=("#b91c1c")
        )
        pdf_btn.pack(side="left", padx=(0, 8))
        
        excel_btn = ctk.CTkButton(
            button_grid,
            text="📈 Excel",
            command=self.generate_excel_report,
            width=100,
            height=35,
            corner_radius=8,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=self.colors['success'],
            hover_color=("#047857")
        )
        excel_btn.pack(side="left", padx=4)
        
        json_btn = ctk.CTkButton(
            button_grid,
            text="📦 JSON",
            command=self.export_json,
            width=100,
            height=35,
            corner_radius=8,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=self.colors['info'],
            hover_color=("#0369a1")
        )
        json_btn.pack(side="left", padx=(8, 0))
        
        # Alt panel - Rapor önizleme
        preview_panel = ctk.CTkFrame(
            main_container,
            corner_radius=15,
            fg_color=self.colors['card_bg']
        )
        preview_panel.pack(fill="both", expand=True)
        
        # Önizleme başlığı
        preview_header = ctk.CTkFrame(
            preview_panel,
            corner_radius=12,
            fg_color=self.colors['primary'],
            height=55
        )
        preview_header.pack(fill="x", padx=20, pady=20)
        preview_header.pack_propagate(False)
        
        ctk.CTkLabel(
            preview_header,
            text="👁️ Report Preview",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        ).pack(pady=12)
        
        # Önizleme alanı
        self.report_preview = ctk.CTkTextbox(
            preview_panel,
            corner_radius=10,
            font=ctk.CTkFont(size=12),
            border_width=2,
            border_color=self.colors['primary']
        )
        self.report_preview.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    def create_settings_tab(self):
        """Settings tab - Modern design"""
        tab = self.notebook.add("⚙️ Settings")
        
        # Ana container
        main_container = ctk.CTkFrame(tab, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Left panel - LLM Settings
        settings_panel = ctk.CTkFrame(
            main_container,
            corner_radius=15,
            fg_color=self.colors['card_bg']
        )
        settings_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # LLM Settings header
        llm_header = ctk.CTkFrame(
            settings_panel,
            corner_radius=12,
            fg_color=self.colors['primary'],
            height=60
        )
        llm_header.pack(fill="x", padx=20, pady=20)
        llm_header.pack_propagate(False)
        
        ctk.CTkLabel(
            llm_header,
            text="🤖 LLM Settings",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        ).pack(pady=15)
        
        # API Key bölümü
        api_section = ctk.CTkFrame(settings_panel, corner_radius=10)
        api_section.pack(fill="x", padx=20, pady=(0, 15))
        
        api_label = ctk.CTkLabel(
            api_section,
            text="🔑 OpenAI API Key:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        api_label.pack(pady=(15, 10), anchor="w", padx=20)
        
        self.api_key_entry = ctk.CTkEntry(
            api_section,
            width=450,
            height=35,
            show="*",
            corner_radius=8,
            font=ctk.CTkFont(size=13),
            placeholder_text="sk-..."
        )
        self.api_key_entry.pack(pady=(0, 15), padx=20)
        
        # Model seçimi bölümü
        model_section = ctk.CTkFrame(settings_panel, corner_radius=10)
        model_section.pack(fill="x", padx=20, pady=(0, 15))
        
        model_label = ctk.CTkLabel(
            model_section,
            text="🧠 GPT Model Selection:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        model_label.pack(pady=(15, 10), anchor="w", padx=20)
        
        # Model bilgi kartı
        model_info_card = ctk.CTkFrame(
            model_section,
            corner_radius=8,
            fg_color=self.colors['info']
        )
        model_info_card.pack(fill="x", padx=20, pady=(0, 10))
        
        model_info_text = """💡 RECOMMENDED: gpt-4o (latest, fast and high performance)
• gpt-4o-mini: More economical, fast alternative  • gpt-4-turbo: High performance
• gpt-3.5-turbo: Most economical option"""
        
        model_info_label = ctk.CTkLabel(
            model_info_card,
            text=model_info_text,
            font=ctk.CTkFont(size=11),
            justify="left",
            text_color="white",
            wraplength=400
        )
        model_info_label.pack(pady=10, padx=15)
        
        self.model_selection = ctk.CTkOptionMenu(
            model_section,
            values=[
                "gpt-4o",                    # Latest GPT-4 Omni model
                "gpt-4o-mini",               # Faster and more economical GPT-4o
                "gpt-4-turbo",               # GPT-4 Turbo (2024)
                "gpt-4-turbo-preview",       # GPT-4 Turbo Preview
                "gpt-4",                     # Standard GPT-4
                "gpt-4-32k",                 # GPT-4 32k context
                "gpt-3.5-turbo",             # GPT-3.5 Turbo (most economical)
                "gpt-3.5-turbo-16k",         # GPT-3.5 Turbo 16k context
                "gpt-3.5-turbo-1106",        # GPT-3.5 Turbo (November 2023)
                "gpt-4-1106-preview",        # GPT-4 Turbo (November 2023)
                "gpt-4-vision-preview"       # GPT-4 Vision (visual analysis)
            ],
            width=450,
            height=35,
            corner_radius=8,
            font=ctk.CTkFont(size=13)
        )
        self.model_selection.pack(pady=(0, 15), padx=20)
        self.model_selection.set("gpt-4o")  # Default selection
        
        # Kaydet butonu
        save_btn = ctk.CTkButton(
            settings_panel,
            text="💾 Save Settings",
            command=self.save_settings,
            width=200,
            height=45,
            corner_radius=10,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=self.colors['success'],
            hover_color=("#047857")
        )
        save_btn.pack(pady=20)
        
        # Mevcut ayarları yükle (eğer bekleyen değerler varsa)
        self.load_pending_settings()
        
        # Right panel - Application Information
        info_panel = ctk.CTkFrame(
            main_container,
            corner_radius=15,
            fg_color=self.colors['card_bg']
        )
        info_panel.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Bilgi başlığı
        info_header = ctk.CTkFrame(
            info_panel,
            corner_radius=12,
            fg_color=self.colors['secondary'],
            height=60
        )
        info_header.pack(fill="x", padx=20, pady=20)
        info_header.pack_propagate(False)
        
        ctk.CTkLabel(
            info_header,
            text="ℹ️ Application Information",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        ).pack(pady=15)
        
        # Bilgi kartları
        version_card = ctk.CTkFrame(info_panel, corner_radius=10)
        version_card.pack(fill="x", padx=20, pady=(0, 15))
        
        version_label = ctk.CTkLabel(
            version_card,
            text="🚀 CTA Evaluation System v1.0",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.colors['primary']
        )
        version_label.pack(pady=(15, 5))
        
        subtitle_label = ctk.CTkLabel(
            version_card,
            text="For Academic Research",
            font=ctk.CTkFont(size=12),
            text_color=self.colors['text_secondary']
        )
        subtitle_label.pack(pady=(0, 15))
        
        # Özellikler kartı
        features_card = ctk.CTkFrame(info_panel, corner_radius=10)
        features_card.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        features_text = """
🎯 CORE FEATURES:
• 🔄 Transliteration focused on x, ə, q, ñ, û letters
• ⚠️ Phonetic ambiguity/risk detection  
• 🔗 Cognate alignment and similarity analysis
• 📊 Comprehensive reporting system

🌍 SUPPORTED LANGUAGES:
• Turkish, Uzbek Latin, Kazakh Cyrillic
• Azerbaijani Latin, Turkmen Latin, Kyrgyz Cyrillic

🤖 TECHNICAL FEATURES:
• LLM-supported analysis
• OpenAI GPT-4/3.5 integration
• Modern interface design
• JSON/PDF/Excel report support

📝 DEVELOPER: Academic Research Team
📄 LICENSE: MIT License
        """
        
        features_label = ctk.CTkLabel(
            features_card,
            text=features_text.strip(),
            font=ctk.CTkFont(size=11),
            justify="left",
            anchor="nw",
            wraplength=350
        )
        features_label.pack(pady=15, padx=20, fill="both", expand=True)
    
    # Event handler metodları
    def load_text_file(self):
        """Load text file"""
        file_path = filedialog.askopenfilename(
            title="Select Text File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.input_text.delete("1.0", tk.END)
                    self.input_text.insert("1.0", content)
            except Exception as e:
                messagebox.showerror("Error", f"File could not be loaded: {str(e)}")
    
    def run_transliteration(self):
        """Transliterasyon işlemini çalıştır"""
        input_text = self.input_text.get("1.0", tk.END).strip()
        if not input_text:
            messagebox.showwarning("⚠️ Missing Information", "📝 Please enter the text to be transliterated.\n\n💡 Tip: Write your text in the left panel text area or load from file.")
            return
        
        source_lang = self.source_lang.get()
        
        # Threading ile UI donmasını engelle
        def transliterate():
            try:
                print(f"DEBUG: Transliterasyon baslıyor - Dil: {source_lang}, Metin uzunlugu: {len(input_text)}")
                
                # API key kontrolü
                if not self.llm_interface.api_key:
                    error_result = {"ok": False, "error": "API anahtarı ayarlanmamış!"}
                    self.root.after(0, lambda: self.update_transliteration_ui(error_result))
                    return
                
                result = self.transliterator.transliterate(input_text, source_lang)
                print(f"DEBUG: Transliterasyon tamamlandi - OK: {result.get('ok', False)}")
                
                self.results['transliteration'] = result
                
                # UI'yi güncelle
                self.root.after(0, lambda: self.update_transliteration_ui(result))
                
            except Exception as e:
                print(f"DEBUG: Transliterasyon hatasi: {str(e)}")
                error_result = {"ok": False, "error": str(e)}
                self.root.after(0, lambda: self.update_transliteration_ui(error_result))
        
        threading.Thread(target=transliterate, daemon=True).start()
        
        # Modern loading göstergesi
        self.transliteration_result.delete("1.0", tk.END)
        loading_text = """🔄 Starting Transliteration Process...

⏳ Please wait, process in progress:
• 🤖 Connecting to LLM
• 📝 Analyzing text  
• 🔄 Performing CTA conversion
• ✨ Preparing results

This process may take a few seconds..."""
        
        self.transliteration_result.insert("1.0", loading_text)
        
        # Notes alanını da güncelle
        self.transliteration_notes.delete("1.0", tk.END)
        self.transliteration_notes.insert("1.0", "⏳ Process in progress...")
    
    def update_transliteration_ui(self, result):
        """Transliterasyon sonucunu UI'da göster"""
        try:
            print(f"DEBUG: Sonuç geldi: {result}")  # Debug için
            
            # Result areanı temizle
            self.transliteration_result.delete("1.0", tk.END)
            
            # Sonuç var mı kontrol et
            if result.get('ok'):
                output_text = result.get('output_text', 'Çıktı bulunamadı')
                self.transliteration_result.insert("1.0", output_text)
                
                # 🔥 Otomatik olarak Risk Analysis sekmesine kopyala
                self.risk_input_text.delete("1.0", tk.END)
                self.risk_input_text.insert("1.0", output_text)
                
                # 🔥 PCE Analysis sekmesine de kopyala (hem original hem CTA)
                # Original text (kaynak metin)
                original_text = self.input_text.get("1.0", tk.END).strip()
                self.pce_original_text.delete("1.0", tk.END)
                self.pce_original_text.insert("1.0", original_text)
                
                # CTA text (çevrilmiş metin)
                self.pce_ota_text.delete("1.0", tk.END)
                self.pce_ota_text.insert("1.0", output_text)
                
                # Notları güncelle
                self.transliteration_notes.delete("1.0", tk.END)
                notes = result.get('notes', [])
                if notes:
                    notes_text = "\n".join(notes)
                    self.transliteration_notes.insert("1.0", notes_text)
                else:
                    self.transliteration_notes.insert("1.0", "No notes found")
                    
                print(f"DEBUG: UI guncellendi - Cikti uzunlugu: {len(output_text)}")
                safe_print(f"DEBUG: ✅ CTA output otomatik olarak Risk Analysis ve PCE Analysis sekmelerine kopyalandı")
            else:
                error_msg = result.get('error', 'Unknown error')
                self.transliteration_result.insert("1.0", f"Error: {error_msg}")
                self.transliteration_notes.delete("1.0", tk.END)
                self.transliteration_notes.insert("1.0", f"Error occurred: {error_msg}")
                
        except Exception as e:
            safe_print(f"DEBUG: UI update error: {str(e)}")
            self.transliteration_result.delete("1.0", tk.END)
            self.transliteration_result.insert("1.0", f"UI Error: {str(e)}")
            messagebox.showerror("UI Error", f"Error displaying result: {str(e)}")
    
    def run_risk_analysis(self):
        """Risk analizi çalıştır"""
        ota_text = self.risk_input_text.get("1.0", tk.END).strip()
        if not ota_text:
            messagebox.showwarning("⚠️ Missing Information", "📝 Please enter the CTA text to be analyzed.\n\n💡 Tip: First create CTA text from the Transliteration tab or write CTA text directly.")
            return
        
        def analyze():
            try:
                safe_print(f"DEBUG: Risk analizi basliyor - Metin uzunlugu: {len(ota_text)}")
                
                # API key kontrolü
                if not self.llm_interface.api_key:
                    error_result = {"error": "API key not set! Please configure it in Settings tab."}
                    self.root.after(0, lambda: self.update_risk_analysis_ui(error_result))
                    return
                
                result = self.risk_analyzer.analyze_risks(ota_text)
                safe_print(f"DEBUG: Risk analizi tamamlandı - Tip: {type(result).__name__}, Uzunluk: {len(result) if isinstance(result, list) else 'N/A'}")
                
                self.results['risk_analysis'] = result
                
                self.root.after(0, lambda: self.update_risk_analysis_ui(result))
                
            except Exception as e:
                import traceback
                safe_print(f"DEBUG: Risk analizi hatası: {str(e)}")
                safe_print(f"DEBUG: Traceback: {traceback.format_exc()}")
                error_result = {"error": str(e)}
                self.root.after(0, lambda: self.update_risk_analysis_ui(error_result))
        
        threading.Thread(target=analyze, daemon=True).start()
        
        # Modern loading göstergesi ekle
        for item in self.risk_tree.get_children():
            self.risk_tree.delete(item)
        
        # Çoklu loading satırları
        loading_steps = [
            ("🔄 STARTING", "Starting risk analysis...", "LLM", "Setup", "⏳"),
            ("🤖 CONNECTING", "OpenAI API connection...", "GPT", "Connection", "⏳"),
            ("📝 ANALYZING", "Analyzing CTA text...", "Phonetic", "Processing", "⏳"),
            ("⚠️ RISK DETECTION", "Detecting ambiguities...", "x,ə,q,ñ,û", "Scanning", "⏳"),
            ("✨ RESULTS", "Preparing results...", "Table", "Finishing", "⏳")
        ]
        
        for step in loading_steps:
            self.risk_tree.insert("", "end", values=step)
    
    def update_risk_analysis_ui(self, result):
        """Risk analizi sonucunu UI'da göster"""
        try:
            safe_print(f"DEBUG: Risk UI güncelleniyor: {type(result).__name__} - {len(str(result))} chars")
            
            # Mevcut verileri temizle
            for item in self.risk_tree.get_children():
                self.risk_tree.delete(item)
            
            # Result formatını normalize et
            risks = []
            
            # Result bir liste mi, dict mi?
            if isinstance(result, list):
                risks = result  # Direkt liste döndüyse
            elif isinstance(result, dict):
                # Hata kontrolü
                if 'error' in result:
                    error_msg = result['error']
                    self.risk_tree.insert("", "end", values=(
                        "ERROR", error_msg, "", "", "0.00"
                    ))
                    safe_print(f"DEBUG: Risk analizi hatası gösterildi: {error_msg}")
                    return
                # Dict içinde risks anahtarı varsa
                risks = result.get('risks', [])
            else:
                # Beklenmeyen format
                self.risk_tree.insert("", "end", values=(
                    "ERROR", f"Unexpected result type: {type(result).__name__}", "", "", "0.00"
                ))
                return
            
            # Risk yoksa
            if not risks:
                self.risk_tree.insert("", "end", values=(
                    "INFO", "No risks found in text", "", "", "1.00"
                ))
                safe_print("DEBUG: Risk bulunamadı mesajı gösterildi")
                return
            
            # Risk verilerini tabloya ekle
            for risk in risks:
                if isinstance(risk, dict):
                    letter = risk.get('letter', 'unknown')
                    confusions = ', '.join(risk.get('possible_confusions', []))
                    languages = ', '.join(risk.get('languages', []))
                    examples = ', '.join(risk.get('examples', []))
                    confidence = risk.get('confidence', 0)
                    severity = risk.get('severity', 'medium')
                    context = risk.get('context', '')
                    
                    # Confusion text'i oluştur
                    confusion_text = confusions if confusions else context[:50]
                    
                    self.risk_tree.insert("", "end", values=(
                        f"{letter} ({severity})",
                        confusion_text,
                        languages,
                        examples,
                        f"{confidence:.2f}"
                    ))
            
            safe_print(f"DEBUG: {len(risks)} risk UI'da gösterildi")
            
        except Exception as e:
            import traceback
            safe_print(f"DEBUG: Risk UI update error: {str(e)}")
            safe_print(f"DEBUG: Traceback: {traceback.format_exc()}")
            self.risk_tree.insert("", "end", values=(
                "UI ERROR", str(e), "", "", "0.00"
            ))
    
    def run_cognate_alignment(self):
        """Kognat hizalama çalıştır"""
        candidates_text = self.cognate_input.get("1.0", tk.END).strip()
        if not candidates_text:
            messagebox.showwarning("⚠️ Missing Information", "📝 Please enter candidate words.\n\n💡 Format: language_code:word\n📋 Example:\ntr:şehir\naz:xəbər\nuz:qo'shni")
            return
        
        def align():
            try:
                print(f"DEBUG: Kognat hizalama basliyor - Metin uzunlugu: {len(candidates_text)}")
                
                # API key kontrolü
                if not self.llm_interface.api_key:
                    error_result = {"groups": [], "error": "API anahtarı ayarlanmamış!"}
                    self.root.after(0, lambda: self.update_cognate_alignment_ui(error_result))
                    return
                
                result = self.cognate_aligner.align_cognates(candidates_text)
                print(f"DEBUG: Kognat hizalama tamamlandı: {result}")
                
                self.results['cognate_alignment'] = result
                
                self.root.after(0, lambda: self.update_cognate_alignment_ui(result))
            except Exception as e:
                print(f"DEBUG: Kognat hizalama hatası: {str(e)}")
                error_result = {"groups": [], "error": str(e)}
                self.root.after(0, lambda: self.update_cognate_alignment_ui(error_result))
        
        threading.Thread(target=align, daemon=True).start()
        
        # Modern loading göstergesi
        self.cognate_results.delete("1.0", tk.END)
        loading_text = """🔗 Starting Cognate Alignment Process...

⏳ Please wait, analysis in progress:
• 🤖 Connecting to LLM
• 📋 Parsing candidate words
• 🔄 Performing CTA transliteration
• 🔍 Analyzing phonetic similarities
• 📊 Creating similarity groups
• ✨ Formatting results

This process may take longer as it requires 
complex analysis..."""
        
        self.cognate_results.insert("1.0", loading_text)
    
    def update_cognate_alignment_ui(self, result):
        """Kognat hizalama sonucunu UI'da göster - İyileştirilmiş"""
        try:
            self.cognate_results.delete("1.0", tk.END)
            
            # Check if result is valid
            if not isinstance(result, dict):
                error_text = f"❌ UNEXPECTED RESULT TYPE:\nReceived {type(result).__name__} instead of dict\n"
                self.cognate_results.insert("1.0", error_text)
                return
            
            # Error check
            if 'error' in result:
                error_text = f"❌ ERROR OCCURRED:\n{result['error']}\n\n"
                error_text += "💡 Check:\n"
                error_text += "• Is API key correct?\n"
                error_text += "• Is format correct? (tr:şehir)\n"
                error_text += "• Is internet connection available?\n"
                self.cognate_results.insert("1.0", error_text)
                return
            
            # Title
            formatted_result = "🔗 COGNATE ALIGNMENT RESULTS\n" + "="*60 + "\n\n"
            
            # Grupları kontrol et
            groups = result.get('groups', [])
            if not groups:
                formatted_result += "❌ No similarity groups found.\n\n"
                formatted_result += "💡 Suggestions:\n"
                formatted_result += "• Add more candidate words\n"
                formatted_result += "• Try different language combinations\n"
                formatted_result += "• Use real cognate words\n"
                self.cognate_results.insert("1.0", formatted_result)
                return
            
            # Grupları göster
            for i, group in enumerate(groups, 1):
                similarity = group.get('similarity', 'unknown').upper()
                confidence = group.get('confidence', 0.0)
                rationale = group.get('rationale', 'No explanation')
                root_analysis = group.get('root_analysis', '')
                
                # Group header
                formatted_result += f"📊 GROUP {i} - Similarity: {similarity} (Confidence: {confidence:.2f})\n"
                formatted_result += f"🔍 Rationale: {rationale}\n"
                
                if root_analysis:
                    formatted_result += f"🌱 Root Analysis: {root_analysis}\n"
                
                formatted_result += "\n📝 Words:\n"
                
                # Kelimeleri göster
                items = group.get('items', [])
                for item in items:
                    lang = item.get('lang', '').upper()
                    original = item.get('original', '')
                    ota = item.get('ota', '')
                    formatted_result += f"   • {lang}: {original} → CTA: {ota}\n"
                
                formatted_result += "\n" + "─"*50 + "\n\n"
            
            # Add statistics
            stats = result.get('statistics', {})
            if stats:
                formatted_result += "📈 STATISTICS:\n"
                # Doğru field'ları kullan
                total_words = stats.get('total_input_words', stats.get('total_words', 0))
                aligned_words = stats.get('total_aligned_words', 0)
                groups_found = stats.get('groups_found', 0)
                avg_size = stats.get('average_group_size', 0)
                avg_confidence = stats.get('average_confidence', 0)
                alignment_rate = stats.get('alignment_rate', 0)
                
                formatted_result += f"• Total words: {total_words}\n"
                formatted_result += f"• Aligned words: {aligned_words}\n"
                formatted_result += f"• Groups found: {groups_found}\n"
                formatted_result += f"• Average group size: {avg_size:.1f}\n"
                formatted_result += f"• Alignment rate: {alignment_rate:.1%}\n"
                formatted_result += f"• Average confidence: {avg_confidence:.2f}\n"
                
                # Benzerlik dağılımı
                sim_dist = stats.get('similarity_distribution', {})
                if sim_dist:
                    formatted_result += f"• High similarity: {sim_dist.get('high', 0)} groups\n"
                    formatted_result += f"• Medium similarity: {sim_dist.get('medium', 0)} groups\n"
                    formatted_result += f"• Low similarity: {sim_dist.get('low', 0)} groups\n"
            
            self.cognate_results.insert("1.0", formatted_result)
            
        except Exception as e:
            import traceback
            error_text = f"❌ UI UPDATE ERROR:\n{str(e)}\n\n"
            error_text += f"Debug info: {traceback.format_exc()}\n"
            self.cognate_results.insert("1.0", error_text)
            safe_print(f"DEBUG: Cognate UI error: {str(e)}")
    
    def run_pce_analysis(self):
        """PCE analizi çalıştır"""
        original_text = self.pce_original_text.get("1.0", "end").strip()
        ota_text = self.pce_ota_text.get("1.0", "end").strip()
        dataset_name = self.pce_dataset_name.get().strip() or "Custom_Dataset"
        
        if not original_text or not ota_text:
            messagebox.showwarning("⚠️ Missing Information", "📝 Enter both original and CTA text.\n\n💡 Tip: Write original text in the left panel, CTA text in the right panel.")
            return
        
        def analyze():
            try:
                print(f"DEBUG: PCE analizi başlıyor - Dataset: {dataset_name}")
                
                # API key kontrolü
                if not self.llm_interface.api_key:
                    error_result = {"error": "API anahtarı ayarlanmamış!"}
                    self.root.after(0, lambda: self.update_pce_analysis_ui(error_result))
                    return
                
                result = self.pce_analyzer.analyze_pce(original_text, ota_text, dataset_name)
                print(f"DEBUG: PCE analizi tamamlandı: {result}")
                
                self.results['pce_analysis'] = result
                
                self.root.after(0, lambda: self.update_pce_analysis_ui(result))
                
            except Exception as e:
                print(f"DEBUG: PCE analizi hatası: {str(e)}")
                error_result = {"error": str(e)}
                self.root.after(0, lambda: self.update_pce_analysis_ui(error_result))
        
        threading.Thread(target=analyze, daemon=True).start()
        
        # Loading göstergesi
        self.pce_results.delete("1.0", "end")
        loading_text = """🔬 Starting PCE (Phonetic Correspondence Effectiveness) Analysis...

⏳ Please wait, complex phonetic analysis in progress:
• 🤖 Connecting to LLM
• 📝 Original text phoneme analysis
• 🔤 CTA text phoneme analysis  
• 📊 UPC, TPC, ALC calculations
• ⚖️ Weighted PCE calculation
• 📈 Logarithmic PCE calculation
• 📋 Comparative analysis
• ✨ Formatting results

This process may take longer as it requires 
academic-level analysis..."""
        
        self.pce_results.insert("1.0", loading_text)
    
    def update_pce_analysis_ui(self, result):
        """PCE analizi sonucunu UI'da göster"""
        try:
            self.pce_results.delete("1.0", "end")
            
            # Check if result is valid
            if not isinstance(result, dict):
                error_text = f"❌ UNEXPECTED RESULT TYPE:\nReceived {type(result).__name__} instead of dict\n"
                self.pce_results.insert("1.0", error_text)
                return
            
            # Error check
            if 'error' in result:
                error_text = f"❌ PCE ANALYSIS ERROR:\n{result['error']}\n\n"
                error_text += "💡 Check:\n"
                error_text += "• Is API key correct?\n"
                error_text += "• Are both text fields filled?\n"
                error_text += "• Is internet connection available?\n"
                self.pce_results.insert("1.0", error_text)
                return
            
            # Format successful result
            formatted_result = "📊 PCE (PHONETIC CORRESPONDENCE EFFECTIVENESS) ANALYSIS\n" + "="*80 + "\n\n"
            
            # Dataset information
            metadata = result.get("metadata", {})
            formatted_result += f"📋 Dataset: {metadata.get('dataset_name', 'Unknown')}\n"
            formatted_result += f"📏 Original Length: {metadata.get('original_length', 0)} characters\n"
            formatted_result += f"🔤 CTA Length: {metadata.get('ota_length', 0)} characters\n\n"
            
            # Orijinal analiz
            original = result.get("original_analysis", {})
            if original:
                formatted_result += "📝 ORIGINAL TEXT ANALYSIS:\n"
                formatted_result += f"• UPC (Unique Phoneme Count): {original.get('upc', 0)}\n"
                formatted_result += f"• TPC (Total Phoneme Count): {original.get('tpc', 0)}\n"
                formatted_result += f"• ALC (Average Letter Count): {original.get('alc', 0):.2f}\n"
                formatted_result += f"• Weighted PCE: {original.get('weighted_pce', 0):.2f}\n"
                formatted_result += f"• Logarithmic PCE: {original.get('logarithmic_pce', 0):.2f}\n\n"
            
            # CTA analiz
            ota = result.get("ota_analysis", {})
            if ota:
                formatted_result += "🔤 CTA TEXT ANALYSIS:\n"
                formatted_result += f"• UPC (Unique Phoneme Count): {ota.get('upc', 0)}\n"
                formatted_result += f"• TPC (Total Phoneme Count): {ota.get('tpc', 0)}\n"
                formatted_result += f"• ALC (Average Letter Count): {ota.get('alc', 0):.2f}\n"
                formatted_result += f"• Weighted PCE: {ota.get('weighted_pce', 0):.2f}\n"
                formatted_result += f"• Logarithmic PCE: {ota.get('logarithmic_pce', 0):.2f}\n\n"
            
            # Karşılaştırma
            comparison = result.get("comparison", {})
            if comparison:
                formatted_result += "📈 COMPARISON AND IMPROVEMENT:\n"
                weighted_imp = comparison.get("weighted_improvement", 0)
                log_imp = comparison.get("logarithmic_improvement", 0)
                
                formatted_result += f"• Weighted PCE Improvement: %{weighted_imp:.2f}\n"
                formatted_result += f"• Logarithmic PCE Improvement: %{log_imp:.2f}\n"
                formatted_result += f"• Overall Effectiveness Gain: %{comparison.get('effectiveness_gain', 0):.2f}\n\n"
            
            # Değerlendirme
            assessment = result.get("assessment", {})
            if assessment:
                formatted_result += "🎯 ASSESSMENT:\n"
                formatted_result += f"• Improvement Category: {assessment.get('improvement_category', 'Unknown')}\n"
                formatted_result += f"• Effectiveness Rating: {assessment.get('effectiveness_rating', 'Unknown')}\n\n"
                
                recommendations = assessment.get("recommendations", [])
                if recommendations:
                    formatted_result += "💡 RECOMMENDATIONS:\n"
                    for rec in recommendations:
                        formatted_result += f"• {rec}\n"
                    formatted_result += "\n"
            
            # Detailed analysis
            detailed = result.get("detailed_analysis", "")
            if detailed:
                formatted_result += "🔍 DETAILED ANALYSIS:\n"
                formatted_result += f"{detailed}\n\n"
            
            # Yeni harfler
            new_letters = metadata.get("new_letters_detected", {})
            if new_letters:
                formatted_result += "🆕 DETECTED NEW CTA LETTERS:\n"
                for letter, count in new_letters.items():
                    formatted_result += f"• {letter}: used {count} times\n"
            
            self.pce_results.insert("1.0", formatted_result)
            
        except Exception as e:
            import traceback
            error_text = f"❌ UI UPDATE ERROR:\n{str(e)}\n\n"
            error_text += f"Debug info: {traceback.format_exc()}\n"
            self.pce_results.insert("1.0", error_text)
            safe_print(f"DEBUG: PCE UI error: {str(e)}")
    
    def save_transliteration_result(self):
        """Transliterasyon sonucunu kaydet"""
        if not self.results.get('transliteration'):
            messagebox.showwarning("Warning", "No transliteration result to save.")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Save Result",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                if file_path.endswith('.json'):
                    with open(file_path, 'w', encoding='utf-8') as file:
                        json.dump(self.results['transliteration'], file, ensure_ascii=False, indent=2)
                else:
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(self.results['transliteration']['output_text'])
                
                messagebox.showinfo("✅ Success!", f"🎉 Transliteration result saved successfully!\n\n📁 Location: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Save error: {str(e)}")
    
    def generate_pdf_report(self):
        """PDF rapor oluştur"""
        # Analiz verilerini kontrol et
        if not any(self.results.values()):
            messagebox.showwarning("⚠️ No Data", "📊 Run analysis operations first to create report:\n• 🔄 Transliteration\n• ⚠️ Risk Analysis\n• 🔗 Cognate Alignment")
            return
        
        # Dosya kaydetme dialogu
        file_path = filedialog.asksaveasfilename(
            title="Save PDF Report",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                # PDF rapor oluştur
                success = self.report_generator.generate_comprehensive_pdf(
                    transliteration_result=self.results.get('transliteration'),
                    risk_result=self.results.get('risk_analysis'),
                    cognate_result=self.results.get('cognate_alignment'),
                    pce_result=self.results.get('pce_analysis'),
                    output_path=file_path
                )
                
                if success:
                    messagebox.showinfo("✅ Success!", f"🎉 Comprehensive PDF report created successfully!\n\n📁 Location: {file_path}\n📊 Content: All analysis results, charts and statistics")
                else:
                    messagebox.showerror("❌ Error", "PDF report could not be created. Please try again.")
                    
            except Exception as e:
                messagebox.showerror("❌ Error", f"PDF creation error: {str(e)}")
        
        # Rapor önizlemesi göster
        self.show_report_preview()
    
    def show_report_preview(self):
        """Rapor önizlemesi göster"""
        try:
            preview_text = "📊 COMPREHENSIVE CTA EVALUATION REPORT PREVIEW\n" + "="*70 + "\n\n"
            
            # Transliterasyon özeti
            if self.results.get('transliteration'):
                trans = self.results['transliteration']
                preview_text += "🔄 TRANSLITERATION SUMMARY:\n"
                preview_text += f"• Source Language: {trans.get('statistics', {}).get('source_language', 'Unknown')}\n"
                preview_text += f"• Input Length: {trans.get('statistics', {}).get('input_length', 0)} characters\n"
                preview_text += f"• Output Length: {trans.get('statistics', {}).get('output_length', 0)} characters\n"
                new_letters = trans.get('statistics', {}).get('new_letters_used', {})
                if new_letters:
                    preview_text += f"• New Letters Used: {', '.join([f'{k}({v})' for k, v in new_letters.items()])}\n"
                preview_text += "\n"
            
            # Risk analizi özeti
            if self.results.get('risk_analysis'):
                risk = self.results['risk_analysis']
                risks = risk.get('risks', [])
                preview_text += "⚠️ RISK ANALYSIS SUMMARY:\n"
                preview_text += f"• Risks Detected: {len(risks)} items\n"
                if risks:
                    high_risks = [r for r in risks if r.get('severity') == 'high']
                    medium_risks = [r for r in risks if r.get('severity') == 'medium']
                    low_risks = [r for r in risks if r.get('severity') == 'low']
                    preview_text += f"• High Risk: {len(high_risks)}, Medium Risk: {len(medium_risks)}, Low Risk: {len(low_risks)}\n"
                    avg_confidence = sum(r.get('confidence', 0) for r in risks) / len(risks)
                    preview_text += f"• Average Confidence: {avg_confidence:.2f}\n"
                preview_text += "\n"
            
            # Kognat analizi özeti
            if self.results.get('cognate_alignment'):
                cog = self.results['cognate_alignment']
                stats = cog.get('statistics', {})
                preview_text += "🔗 COGNATE ANALYSIS SUMMARY:\n"
                preview_text += f"• Total Words: {stats.get('total_input_words', 0)}\n"
                preview_text += f"• Aligned Words: {stats.get('total_aligned_words', 0)}\n"
                preview_text += f"• Groups Found: {stats.get('groups_found', 0)}\n"
                preview_text += f"• Alignment Rate: {stats.get('alignment_rate', 0):.1%}\n"
                preview_text += "\n"
            
            preview_text += "📋 REPORT CONTENT:\n"
            preview_text += "• Executive Summary\n"
            preview_text += "• Methodology Explanation\n"
            preview_text += "• Detailed Transliteration Analysis\n"
            preview_text += "• Phonetic Risk Assessment\n"
            preview_text += "• Cognate Alignment Results\n"
            preview_text += "• Statistical Charts and Tables\n"
            preview_text += "• Comprehensive Analysis of New Letters (q, x, ñ, ə, û)\n"
            preview_text += "• Results and Recommendations\n\n"
            
            preview_text += "🎯 This report is in professional format ready for use in your academic paper."
            
            self.report_preview.delete("1.0", "end")
            self.report_preview.insert("1.0", preview_text)
            
        except Exception as e:
            self.report_preview.delete("1.0", "end")
            self.report_preview.insert("1.0", f"Preview error: {str(e)}")
    
    def generate_excel_report(self):
        """Excel rapor oluştur"""
        messagebox.showinfo("🚧 Under Development", "📈 Excel report feature will be added soon!\n\n🔜 Available in the next update.")
    
    def export_json(self):
        """JSON olarak dışa aktar"""
        if not any(self.results.values()):
            messagebox.showwarning("⚠️ No Data", "📊 No analysis data found to export.\n\n💡 Tip: Run analysis operations first:\n• 🔄 Transliteration\n• ⚠️ Risk Analysis\n• 🔗 Cognate Alignment")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Export JSON",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                export_data = {
                    'timestamp': datetime.now().isoformat(),
                    'results': self.results
                }
                
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(export_data, file, ensure_ascii=False, indent=2)
                
                messagebox.showinfo("✅ Success!", f"🎉 All analysis data exported to JSON format successfully!\n\n📁 Location: {file_path}\n📊 Content: Transliteration, Risk Analysis, Cognate Alignment")
            except Exception as e:
                messagebox.showerror("Error", f"Export error: {str(e)}")
    
    def save_settings(self):
        """Ayarları kaydet"""
        api_key = self.api_key_entry.get()
        model = self.model_selection.get()
        
        # Eğer maskelenmiş key görünüyorsa, gerçek key'i kullan
        if api_key.startswith("sk-...") and hasattr(self, '_real_api_key'):
            # Kullanıcı key'i değiştirmemişse mevcut key'i kullan
            api_key = self._real_api_key
        elif api_key.startswith("sk-..."):
            messagebox.showwarning("Warning", "Please enter a new API key or change the existing key.")
            return
        
        if api_key and not api_key.startswith("sk-..."):
            # Config dosyasını güncelle
            success = self.update_config_file(api_key, model)
            
            if success:
                # LLM interface'i güncelle
                self.llm_interface.set_api_key(api_key)
                self.llm_interface.set_model(model)
                
                # Gerçek key'i sakla ve UI'da maskelenmiş göster
                self._real_api_key = api_key
                masked_key = "sk-..." + api_key[-4:]
                self.api_key_entry.delete(0, 'end')
                self.api_key_entry.insert(0, masked_key)
                
                messagebox.showinfo("✅ Settings Saved!", "🎉 LLM settings saved successfully!\n\n🤖 Model: " + model + "\n🔑 API Key: Stored securely\n📝 Config file updated")
            else:
                # Sadece bellekte güncelle
                self.llm_interface.set_api_key(api_key)
                self.llm_interface.set_model(model)
                
                # Gerçek key'i sakla ve UI'da maskelenmiş göster
                self._real_api_key = api_key
                masked_key = "sk-..." + api_key[-4:]
                self.api_key_entry.delete(0, 'end')
                self.api_key_entry.insert(0, masked_key)
                
                messagebox.showwarning("Partial Success", "Settings saved in memory but config file could not be updated.")
        else:
            messagebox.showwarning("Warning", "Please enter a valid API key.")
    
    def update_config_file(self, api_key, model):
        """Config dosyasını güncelle"""
        try:
            config_path = "config.py"
            
            # Config dosyası var mı kontrol et
            if not os.path.exists(config_path):
                # Yeni config dosyası oluştur
                config_content = self._create_default_config()
            else:
                # Mevcut config dosyasını oku
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_content = f.read()
            
            # API key'i güncelle
            api_key_pattern = r'OPENAI_API_KEY\s*=\s*["\'][^"\']*["\']'
            new_api_key_line = f'OPENAI_API_KEY = "{api_key}"'
            
            if re.search(api_key_pattern, config_content):
                config_content = re.sub(api_key_pattern, new_api_key_line, config_content)
            else:
                # API key satırı yoksa ekle
                config_content += f"\n{new_api_key_line}\n"
            
            # Model'i güncelle
            model_pattern = r'OPENAI_MODEL\s*=\s*["\'][^"\']*["\']'
            new_model_line = f'OPENAI_MODEL = "{model}"'
            
            if re.search(model_pattern, config_content):
                config_content = re.sub(model_pattern, new_model_line, config_content)
            else:
                # Model satırı yoksa ekle
                config_content += f"{new_model_line}\n"
            
            # Config dosyasını kaydet
            with open(config_path, 'w', encoding='utf-8') as f:
                f.write(config_content)
            
            return True
            
        except Exception as e:
            print(f"Config dosyası güncelleme hatası: {str(e)}")
            return False
    
    def _create_default_config(self):
        """Create default config content"""
        return """# CTA Evaluation System - Configuration File
# Enter your OpenAI API key here

# OpenAI API Settings
OPENAI_API_KEY = ""
OPENAI_MODEL = "gpt-4o"

# Application Settings
APP_DEBUG = False
APP_LOG_LEVEL = "INFO"

# Report Settings
REPORTS_DIR = "reports"
TEMP_DIR = "temp"

# LLM Settings
DEFAULT_TEMPERATURE = 0.3
DEFAULT_MAX_TOKENS = 2000
REQUEST_TIMEOUT = 30

# UI Settings
THEME = "light"
LANGUAGE = "en"
"""
    
    def load_existing_settings(self):
        """Mevcut config dosyasından ayarları yükle ve UI'ya uygula"""
        try:
            # Config dosyasından mevcut değerleri al
            current_api_key = getattr(self.llm_interface, 'api_key', None)
            current_model = getattr(self.llm_interface, 'model', 'gpt-4o')
            
            # UI elementleri henüz oluşturulmadıysa, daha sonra yükle
            if hasattr(self, 'api_key_entry') and hasattr(self, 'model_selection'):
                # API key'i UI'ya yükle (güvenlik için son 4 karakterini göster)
                if current_api_key and len(current_api_key) > 8:
                    masked_key = "sk-..." + current_api_key[-4:]
                    self.api_key_entry.insert(0, masked_key)
                
                # Model seçimini UI'ya yükle
                if current_model:
                    try:
                        self.model_selection.set(current_model)
                    except:
                        pass  # Model listede yoksa varsayılan değerde kalsın
            else:
                # UI henüz hazır değilse, değerleri sakla ve daha sonra uygula
                self._pending_api_key = current_api_key
                self._pending_model = current_model
                
        except Exception as e:
            print(f"Ayarlar yüklenirken hata: {str(e)}")
    
    def load_pending_settings(self):
        """Bekleyen ayarları UI'ya yükle"""
        try:
            # Bekleyen API key varsa yükle
            if hasattr(self, '_pending_api_key') and self._pending_api_key:
                # Güvenlik için maskelenmiş gösterim
                if len(self._pending_api_key) > 8:
                    masked_key = "sk-..." + self._pending_api_key[-4:]
                    self.api_key_entry.delete(0, 'end')
                    self.api_key_entry.insert(0, masked_key)
                    # Gerçek key'i gizli bir attribute'ta sakla
                    self._real_api_key = self._pending_api_key
                
            # Bekleyen model varsa yükle
            if hasattr(self, '_pending_model') and self._pending_model:
                try:
                    self.model_selection.set(self._pending_model)
                except:
                    pass
                    
            # Bekleyen değerleri temizle
            if hasattr(self, '_pending_api_key'):
                delattr(self, '_pending_api_key')
            if hasattr(self, '_pending_model'):
                delattr(self, '_pending_model')
                
        except Exception as e:
            print(f"Bekleyen ayarlar yüklenirken hata: {str(e)}")
    
    def run(self):
        """Uygulamayı çalıştır"""
        self.root.mainloop()

if __name__ == "__main__":
    app = CTAEvaluationApp()
    app.run()
