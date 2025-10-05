# CTA Evaluation System - User Guide

> **⚡ New User?** Check [QUICKSTART.md](QUICKSTART.md) for the fastest way to get started!

## 📋 Prerequisites

Before using this guide, make sure you have:
- ✅ Installed Python 3.8 or higher
- ✅ Installed all dependencies
- ✅ Obtained an OpenAI API key

**Haven't installed yet?** → See [INSTALLATION.md](INSTALLATION.md) for complete installation instructions.

---

## 🚀 Quick Start

### Launch the Application

```bash
# Activate virtual environment (if using one)
source venv/bin/activate  # Windows: venv\Scripts\activate

# Run the application
python main.py
```

The application window should open with a modern interface.

---

## ⚙️ Initial Configuration

### Setting Up OpenAI API Key
1. Open the application
2. Go to **Settings** tab
3. Enter your OpenAI API key
4. Select a model (recommended: `gpt-4o`)
5. Click "Save Settings" button

### Getting an API Key
1. Go to [OpenAI Platform](https://platform.openai.com)
2. Create an account or log in
3. Create a new key from API Keys section
4. Store the key securely

## 📝 Module Usage

### 1. Transliteration Module

**Purpose**: Translate from different Turkic language alphabets to CTA

**Steps**:
1. Open **Transliteration** tab
2. Select source language:
   - Turkish (already CTA-compatible, minimal changes)
   - Uzbek Latin
   - Kazakh Cyrillic
   - Azerbaijani Latin
   - Turkmen Latin
   - Kyrgyz Cyrillic
3. Enter your text or load a text file with "Load from File"
4. Click "Transliterate" button
5. Review results in right panel
6. Save output with "Save Result"

**Sample Input**:
```
Turkish: Merhaba! Nasılsınız? İyi günler!
Uzbek Latin: Xush kelibsiz! Qanday ahvolingiz?
Kazakh Cyrillic: Қош келдіңіз! Қалай жағдайыңыз?
```

**Expected Output**:
```
CTA: Merhaba! Nasılsınız? İyi günler! (mostly unchanged)
CTA: Xuş kelibsiz! Qanday ahvolingiz?
CTA: Qoş keldiñiz! Qalay jagdayıñız?
```

### 2. Phonetic Risk Analysis

**Purpose**: Detect ambiguities in CTA text

**Steps**:
1. Open **Phonetic Risk Analysis** tab
2. Enter CTA text (you can use transliteration result)
3. Click "Run Risk Analysis" button
4. Review risk table

**Risk Categories**:
- **High Risk**: Systematic confusions, common problems
- **Medium Risk**: Context-dependent confusions
- **Low Risk**: Rare, marginal cases

**Sample Risk Output**:
| Letter | Confusions | Languages | Example | Confidence |
|--------|------------|-----------|---------|------------|
| ñ | ng, n | uz, tr | toñ/tong | 0.74 |
| q | k | kk, ky | qırğız/kırgız | 0.71 |
| x | h, kh | az, tk | xäbär/habar | 0.69 |

### 3. Cognate Alignment

**Purpose**: Align cognate words from different languages

**Steps**:
1. Open **Cognate Alignment** tab
2. Enter words in format: `language_code:word`
3. Click "Run Cognate Analysis" button
4. Review alignment results

**Input Format**:
```
tr:şehir
az:şəhər
uz:shahar
kk:qala
ky:şaar
tk:şäher
```

**Output Example**:
```
HIGH SIMILARITY GROUP:
Rationale: Common root *şäh- + -är/-ir variants
• TR: şehir → CTA: şehir
• AZ: şəhər → CTA: şähär
• UZ: shahar → CTA: şahar
• TK: şäher → CTA: şäher

LOW SIMILARITY GROUP:
Rationale: Different root, functional similarity
• KK: qala → CTA: qala
• KY: şaar → CTA: şaar
```

### 4. PCE Analysis

**Purpose**: Measure and compare phonetic effectiveness of writing systems

**Steps**:
1. Open **PCE Analysis** tab
2. Enter original text in left panel
3. Enter CTA text in right panel
4. Enter dataset name (optional)
5. Click "Run PCE Analysis" button
6. Review comprehensive results

**Output Includes**:
- UPC, TPC, ALC metrics for both texts
- Weighted and Logarithmic PCE calculations
- Improvement percentages
- Assessment and recommendations

### 5. Report Generation

**Purpose**: Generate comprehensive reports in academic format

**Steps**:
1. Open **Reports** tab
2. Select report type:
   - Comprehensive Analysis Report
   - Transliteration Summary
   - Risk Analysis Details
   - Cognate Alignment Report
3. Choose desired format:
   - PDF Report
   - Excel Report
   - JSON Export
4. Review report preview

## 🎯 New CTA Letters Guide

### Letter Definitions
- **q**: Velar "k" - used with back vowels (qara, qış)
- **x**: Uvular "h" - Arabic/Persian origin words (xaber, xerite)
- **ñ**: Nasal "n" - "ng" sound (toñ, qañ)
- **ə→ä**: Open/front "e" - Azerbaijani ə letter (xäbär, gäl)
- **û**: Length marker - indicates long vowel (kûl, bûl)
- **ò**: Rounded back vowel - Uzbek o' letter (qòl, tòrt)

### Usage Examples
```
Turkish: Günaydın! Bugün hava çok güzel. → CTA: Günaydın! Bugün hava çok güzel.
Kazakh: Қайырлы таң! → CTA: Qayırlı tañ!
Uzbek: Xayrli tong! → CTA: Xayrlı toñ!
Azeri: Xeyirli səhər! → CTA: Xeyirli sähär!
Turkmen: Hoş ertir! → CTA: Xoş ertir!
```

### Special Notes for Turkish
- Turkish already uses Latin alphabet, so it's mostly compatible with CTA
- Most text remains unchanged: ç, ğ, ı, i, ö, ş, ü letters are preserved
- q, x, ñ letters are detected in foreign-origin words
- Example: "Qatar'dan gelen eksik haber" → "Qatar'dan gelen eksik haber" (q,x preserved)

## 🔧 Troubleshooting

### Common Errors

**1. API Key Error**
```
Error: "API key not set"
Solution: Enter your OpenAI API key from Settings tab
```

**2. JSON Parse Error**
```
Error: "JSON parse error"
Solution: Check internet connection, verify API limit
```

**3. Empty Result**
```
Error: Empty transliteration result
Solution: Ensure you entered text in a supported language
```

### Performance Tips
- Start with short texts (100-500 characters)
- Keep API limits in mind
- Process large texts in pieces
- Don't forget to save results

### Log Files
```
reports/          # Generated reports
temp/            # Temporary files
logs/            # Error logs (auto-created)
```

## 📊 Data Formats

### JSON Output Example
```json
{
  "transliteration": {
    "ok": true,
    "output_text": "Qayırlı tañ!",
    "notes": ["Kazakh Cyrillic → CTA successful"],
    "statistics": {
      "new_letters_used": {"q": 1, "ñ": 1}
    }
  },
  "risk_analysis": {
    "risks": [
      {
        "letter": "ñ",
        "possible_confusions": ["ng", "n"],
        "languages": ["kk", "uz"],
        "confidence": 0.74,
        "severity": "medium"
      }
    ]
  }
}
```

### CSV Export Format
```csv
Letter,Confusions,Languages,Examples,Confidence,Severity,Context
ñ,"ng, n","kk, uz","toñ, qañ",0.74,medium,"Nasal n confusion"
q,"k","kk, ky","qara, qış",0.71,medium,"Velar k distinction"
```

## 🎓 Academic Usage

### Citation Suggestion
```
CTA Evaluation System (2024). Common Turkic Alphabet Phonetic 
Representation Analysis. Academic Research Tool v1.0.
```

### Publication Preparation
1. Generate comprehensive analysis report
2. Save risk heatmaps
3. Export cognate alignment tables
4. Store raw data in JSON format
5. Copy methodology section from report preview

### Ethical Usage
- Acknowledge LLM usage
- Consider API costs
- Validate and interpret results
- Follow academic integrity principles

## 📞 Support

### Technical Support
- GitHub Issues: Bug reports and feature requests
- Email: For academic collaborations
- Wiki: Detailed documentation

### Community
- Turkic languages research groups
- Linguistics forums
- Academic conferences

---

**Last Updated**: 2024
**Version**: 1.0
**License**: MIT

