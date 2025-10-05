"""
Transliteration Engine
Converts from different Turkic language alphabets to CTA
"""

from typing import Dict, Any, List
from .llm_interface import LLMInterface

class TransliteratorEngine:
    def __init__(self, llm_interface: LLMInterface):
        self.llm = llm_interface
        self.mapping_rules = self._load_mapping_rules()
        self.system_prompt = self._create_system_prompt()
    
    def _load_mapping_rules(self) -> Dict[str, Dict[str, str]]:
        """Load mapping rules"""
        return {
            "Turkish": {
                # Turkish already uses Latin alphabet, minimal changes
                # Mappings only for special cases
                "ğ": "ğ", "Ğ": "Ğ",  # Soft g preserved
                "ç": "ç", "Ç": "Ç",  # Ç preserved
                "ş": "ş", "Ş": "Ş",  # Ş preserved
                "ı": "ı", "I": "I",  # Dotted/undotted i preserved
                "i": "i", "İ": "İ",
                "ö": "ö", "Ö": "Ö",  # Ö preserved
                "ü": "ü", "Ü": "Ü",  # Ü preserved
                # Notes on new CTA letters not found in Turkish
                # q, x, ñ, ä, û, ò do not occur naturally in Turkish
            },
            "Uzbek Latin": {
                "sh": "ş", "Sh": "Ş", "SH": "Ş",
                "ch": "ç", "Ch": "Ç", "CH": "Ç",
                "o'": "ò", "O'": "Ò",
                "g'": "ğ", "G'": "Ğ",
                "ng": "ñ", "Ng": "Ñ", "NG": "Ñ",
                "q": "q", "Q": "Q",
                "x": "x", "X": "X"
            },
            "Kazakh Cyrillic": {
                "қ": "q", "Қ": "Q",
                "ғ": "ğ", "Ғ": "Ğ",
                "ң": "ñ", "Ң": "Ñ",
                "ә": "ä", "Ә": "Ä",
                "ө": "ö", "Ө": "Ö",
                "ү": "ü", "Ү": "Ü",
                "ы": "ı", "Ы": "I",
                "і": "i", "І": "I",
                "ш": "ş", "Ш": "Ş",
                "ч": "ç", "Ч": "Ç",
                "х": "x", "Х": "X",
                "а": "a", "А": "A",
                "б": "b", "Б": "B",
                "в": "v", "В": "V",
                "г": "g", "Г": "G",
                "д": "d", "Д": "D",
                "е": "e", "Е": "E",
                "ж": "j", "Ж": "J",
                "з": "z", "З": "Z",
                "й": "y", "Й": "Y",
                "к": "k", "К": "K",
                "л": "l", "Л": "L",
                "м": "m", "М": "M",
                "н": "n", "Н": "N",
                "о": "o", "О": "O",
                "п": "p", "П": "P",
                "р": "r", "Р": "R",
                "с": "s", "С": "S",
                "т": "t", "Т": "T",
                "у": "u", "У": "U",
                "ф": "f", "Ф": "F",
                "ц": "ts", "Ц": "Ts",
                "щ": "şç", "Щ": "Şç",
                "ъ": "", "Ъ": "",
                "ь": "", "Ь": "",
                "э": "e", "Э": "E",
                "ю": "yu", "Ю": "Yu",
                "я": "ya", "Я": "Ya"
            },
            "Azerbaijani Latin": {
                "ə": "ä", "Ə": "Ä",
                "ğ": "ğ", "Ğ": "Ğ",
                "ı": "ı", "I": "I",
                "ö": "ö", "Ö": "Ö",
                "ü": "ü", "Ü": "Ü",
                "ç": "ç", "Ç": "Ç",
                "ş": "ş", "Ş": "Ş",
                "x": "x", "X": "X"
            },
            "Turkmen Latin": {
                "ä": "ä", "Ä": "Ä",
                "ç": "ç", "Ç": "Ç",
                "ž": "j", "Ž": "J",
                "ň": "ñ", "Ň": "Ñ",
                "ö": "ö", "Ö": "Ö",
                "ş": "ş", "Ş": "Ş",
                "ü": "ü", "Ü": "Ü",
                "ý": "y", "Ý": "Y"
            },
            "Kyrgyz Cyrillic": {
                "а": "a", "А": "A",
                "б": "b", "Б": "B",
                "в": "v", "В": "V",
                "г": "g", "Г": "G",
                "д": "d", "Д": "D",
                "е": "e", "Е": "E",
                "ё": "yo", "Ё": "Yo",
                "ж": "j", "Ж": "J",
                "з": "z", "З": "Z",
                "и": "i", "И": "I",
                "й": "y", "Й": "Y",
                "к": "k", "К": "K",
                "л": "l", "Л": "L",
                "м": "m", "М": "M",
                "н": "n", "Н": "N",
                "ң": "ñ", "Ң": "Ñ",
                "о": "o", "О": "O",
                "ө": "ö", "Ө": "Ö",
                "п": "p", "П": "P",
                "р": "r", "Р": "R",
                "с": "s", "С": "S",
                "т": "t", "Т": "T",
                "у": "u", "У": "U",
                "ү": "ü", "Ү": "Ü",
                "ф": "f", "Ф": "F",
                "х": "x", "Х": "X",
                "ц": "ts", "Ц": "Ts",
                "ч": "ç", "Ч": "Ç",
                "ш": "ş", "Ш": "Ş",
                "щ": "şç", "Щ": "Şç",
                "ъ": "", "Ъ": "",
                "ы": "ı", "Ы": "I",
                "ь": "", "Ь": "",
                "э": "e", "Э": "E",
                "ю": "yu", "Ю": "Yu",
                "я": "ya", "Я": "Ya"
            }
        }
    
    def _create_system_prompt(self) -> str:
        """Create system prompt"""
        return """ROLE: You are a transliteration engine for the Common Turkic Alphabet (CTA).

CORE CTA PRINCIPLE:
CTA = Turkish Alphabet (29 letters) + 5 New Letters for pan-Turkic sounds
New letters: q, x, ñ, ə→ä, û

CTA RULES:
1. Turkish (29 letters) preserved: a,b,c,ç,d,e,f,g,ğ,h,ı,i,j,k,l,m,n,o,ö,p,r,s,ş,t,u,ü,v,y,z
2. Apply 5 NEW letters systematically:
   - q: Kalın "K" sesi - kalın ünlülerle birlikte: Qazaq (Kazak), Qırğız (Kırgız)
   - x: Gırtlaksı "H" (hırıltılı, Arapça خ sesi): Xəbər (Haber), Xizmat (Hizmet)
   - ə: Açık/öne yakın "E" (e ile a arası): Ədəbiyyat (Edebiyat), mən, hərkəs
   - ñ: Genizsi "N" (nazal n, İngilizce ng): Teñri (Tengri), Teñiz (Tengiz)
   - û: Uzatmalı "U" (uzun ünlü göstergesi): Sû (uzun su sesi), anlam ayrımı yapar

SYSTEMATIC MAPPING:
# Turkish → CTA  
Turkish IS the base CTA (29 letters preserved) with systematic ə application:
- Apply ə for open/front e sounds: "ben" → "bən", "herkes" → "hərkəs"
- Change loanwords: "haber" → "xabər", "hikaye" → "xikayə" 
- Change ethnic names: "Kazak" → "Qazaq", "Kırgız" → "Qırğız"
- Keep closed e's as "e": "güzel", "gel", "ver" stay unchanged

# Uzbek Latin → CTA  
sh→ş, ch→ç, o'→ò, g'→ğ, ng→ñ, q→q, x→x

# Kazakh Cyrillic → CTA
қ→q, ғ→ğ, ң→ñ, ә→ä, ө→ö, ү→ü, ы→ı, і→i, ш→ş, ч→ç, х→x
Standard Cyrillic: а→a, б→b, в→v, г→g, д→d, е→e, ж→j, з→z, й→y, к→k, л→l, м→m, н→n, о→o, п→p, р→r, с→s, т→t, у→u, ф→f, ц→ts, щ→şç, ю→yu, я→ya

# Azerbaijani Latin → CTA
ə→ä, x→x (preserve other letters)

# Turkmen Latin → CTA  
ä→ä, ň→ñ, ž→j, ý→y

# Kyrgyz Cyrillic → CTA
ң→ñ, ө→ö, ү→ü, ы→ı (+ standard Cyrillic mappings)

OUTPUT FORMAT - CRITICAL:
Return ONLY valid JSON, no additional text before or after:
{"ok": true, "output_text": "transliterated_text", "notes": ["Turkish_notes_here"]}

Do NOT add any explanations, prefixes like "OUTPUT:", "JSON:", or other text outside the JSON.

NOTES REQUIREMENTS:
- Write ALL notes in Turkish
- Explain which new CTA letters were used and why
- Mention systematic sound changes applied
- For Turkish input: "Türkçe metinde CTA fonetik iyileştirmeleri uygulandı: [list changes]" 
- For other languages: "X dilinden CTA'ya çevrildi. Kullanılan yeni harfler: [list]"

TURKISH-SPECIFIC CTA RULES - ULTRA CONSERVATIVE:
For Turkish text, apply ALMOST NO changes - Turkish IS the base CTA language:

1. q (Kalın "k"): Replace "k" with "q" ONLY in ethnic/geographic names
   - "Kazak" → "Qazaq", "Kırgız" → "Qırğız", "Özbekistan" → "Özbəqistan"
   - KEEP ALL other Turkish k's unchanged: "köy", "komşu", "kalem", "halk"
   
2. x (Gırtlaksı "h"): Replace "h" with "x" ONLY in clear Arabic/Persian loanwords  
   - "haber" → "xaber" (news), "hizmet" → "xizmet" (service)
   - KEEP Turkish h's: "hayat", "hava", "hep", "halk" remain unchanged
   
3. ñ (Genizsi "n"): Use VERY RARELY, only in specific Turkic terms
   - "Tanrı" → "Tañrı" (God), "han" → "xañ" (khan)
   - KEEP most n's unchanged
   
4. ə (Açık/ön "e"): Use SELECTIVELY for Turkish open/front e sounds
   - Use ə for open e's in certain contexts: "herkes" → "hərkəs", "derviş" → "dərviş"
   - Common words with ə: "sen" → "sən", "ben" → "bən", "erer" → "ərər"
   - Keep closed e's as "e": "gel", "ver", "güzel" stay unchanged
   
5. û (Uzatmalı "U"): Use for long U sounds and meaning differentiation
   - Long vowels: "su" → "sû" (when emphasized), "dur" → "dûr" (long duration)
   - Meaning differentiation: "su" vs "sû", helps distinguish word meanings

CRITICAL FOR TURKISH: Apply all 5 CTA letters systematically!
q: Kalın K → Qazaq, Qırğız (ethnic names, back vowel contexts)
x: Gırtlaksı H → xabər, xizmət (Arabic loanwords)
ə: Açık E → bən, səni, hərkəs, dərviş, ədəbiyyat (open e sounds)
ñ: Genizsi N → Tañrı, Teñri (Turkic spiritual/nature terms)
û: Uzatmalı U → sû, dûr (long vowels, meaning differentiation)

ALLOWED CTA CHARACTERS:
a b c ç d e f g ğ h ı i j k l m n ñ o ò ö p q r s ş t u ü v w x y z ä û ə â î ô
A B C Ç D E F G Ğ H I İ J K L M N Ñ O Ò Ö P Q R S Ş T U Ü V W X Y Z Ä Û Ə Â Î Ô
(space & standard punctuation: .,:;!?()-[]{}\"'0123456789 and smart quotes '' and circumflex âîô)

PRESERVE:
URLs, emails, @mentions, #hashtags, numbers, dates, currency, code blocks unchanged."""
    
    def transliterate(self, input_text: str, source_language: str) -> Dict[str, Any]:
        """
        Transliterate text to CTA
        
        Args:
            input_text: Text to be converted
            source_language: Source language
            
        Returns:
            Transliteration result
        """
        if not input_text.strip():
            return {"ok": False, "error": "Empty text"}
        
        # Create user prompt
        user_prompt = f"""INPUT_TEXT:
{input_text}

SOURCE_LANGUAGE: {source_language}

TASK:
Transliterate from {source_language} to CTA following these rules:

1. Apply CTA systematic mappings for {source_language}
2. Use new CTA letters (q, x, ñ, ə→ä, û) where phonetically appropriate
3. Preserve Turkish alphabet letters (29 letters) as base
4. Write notes in Turkish explaining changes made

CRITICAL: Return ONLY the JSON object, no additional text:
{{"ok": true, "output_text": "...", "notes": ["Türkçe açıklama..."]}}

FOCUS: Turkish needs MINIMAL changes - it IS the CTA base!
For Turkish: Apply ULTRA CONSERVATIVE approach:

1. q: Kalın "K" for back vowel contexts: "Kazak"→"Qazaq", "Kırgız"→"Qırğız"
2. x: Gırtlaksı "H" for Arabic loanwords: "haber"→"xabər", "hizmet"→"xizmət"  
3. ñ: Genizsi "N" for Turkic terms: "Tanrı"→"Tañrı", "Tengri"→"Teñri"
4. ə: Açık "E" for open e sounds: "herkes"→"hərkəs", "edebiyat"→"ədəbiyyat"
5. û: Uzatmalı "U" for long vowels: "su"→"sû" (when long), meaning differentiation

CORRECT TURKISH EXAMPLES:
- "herkes geldi" → "hərkəs gəldi" (ə for open e's)
- "ben seni seviyorum" → "bən səni seviyorum" (ə for open e's)
- "derviş hikaye anlattı" → "dərviş xikayə anlattı" (ə + x)
- "haber okuyor" → "xabər okuyor" (x + ə)
- "su içiyorum" → "sû içiyorum" (û for long u when emphasized)
- "Tengri" → "Teñri" (ñ for genizsi n)
- "güzel" → "güzel" (keep closed e unchanged)

CRITICAL: Use ə for Turkish open/front e sounds - this is core CTA principle!"""
        
        try:
            # Make LLM call
            response = self.llm.call_llm(
                system_prompt=self.system_prompt,
                user_prompt=user_prompt,
                temperature=0.1,  # Low temperature for consistency
                max_tokens=2000
            )
            
            # Parse JSON
            result = self.llm.parse_json_response(response["content"])
            
            # Quality control
            if result.get("ok") and result.get("output_text"):
                output_text = result["output_text"]
                
                # CTA character validation
                is_valid, invalid_chars = self.llm.validate_ota_characters(output_text)
                if not is_valid:
                    result["notes"] = result.get("notes", [])
                    result["notes"].append(f"Warning: Invalid characters detected: {', '.join(invalid_chars)}")
                
                # Add statistics
                result["statistics"] = {
                    "input_length": len(input_text),
                    "output_length": len(output_text),
                    "source_language": source_language,
                    "new_letters_used": self._count_new_letters(output_text)
                }
                
                # Add LLM metadata
                result["llm_metadata"] = {
                    "model": response.get("model"),
                    "usage": response.get("usage"),
                    "response_time": response.get("response_time")
                }
            
            return result
            
        except Exception as e:
            return {
                "ok": False,
                "error": f"Transliteration error: {str(e)}",
                "input_text": input_text,
                "source_language": source_language
            }
    
    def _count_new_letters(self, text: str) -> Dict[str, int]:
        """Count usage of new letters"""
        new_letters = ['x', 'X', 'ä', 'Ä', 'q', 'Q', 'ñ', 'Ñ', 'û', 'Û', 'ò', 'Ò']
        counts = {}
        
        for letter in new_letters:
            count = text.count(letter)
            if count > 0:
                counts[letter] = count
        
        return counts
    
    def batch_transliterate(self, texts: List[str], source_language: str) -> List[Dict[str, Any]]:
        """
        Batch transliteration
        
        Args:
            texts: List of texts to be converted
            source_language: Source language
            
        Returns:
            List of transliteration results
        """
        results = []
        for text in texts:
            result = self.transliterate(text, source_language)
            results.append(result)
        
        return results
    
    def get_supported_languages(self) -> List[str]:
        """Get supported languages"""
        return list(self.mapping_rules.keys())
