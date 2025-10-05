"""
LLM Interface Modülü
OpenAI API ile etkileşim sağlar
"""

import openai
import json
import os
from typing import Dict, Any, List, Optional
import time

class LLMInterface:
    def __init__(self):
        self.api_key = None
        self.model = "gpt-4"
        self.client = None
        
        # Config dosyasından API key'i al
        try:
            import config
            if hasattr(config, 'OPENAI_API_KEY') and config.OPENAI_API_KEY:
                self.set_api_key(config.OPENAI_API_KEY)
            if hasattr(config, 'OPENAI_MODEL'):
                self.model = config.OPENAI_MODEL
        except ImportError:
            pass
        
        # Çevre değişkeninden API key'i al (yedek)
        if not self.api_key and os.getenv('OPENAI_API_KEY'):
            self.set_api_key(os.getenv('OPENAI_API_KEY'))
    
    def set_api_key(self, api_key: str):
        """API key'i ayarla"""
        self.api_key = api_key
        self.client = openai.OpenAI(api_key=api_key)
    
    def set_model(self, model: str):
        """Model'i ayarla"""
        self.model = model
    
    def call_llm(self, system_prompt: str, user_prompt: str, 
                 temperature: float = 0.3, max_tokens: int = 2000) -> Dict[str, Any]:
        """
        LLM'e çağrı yap
        
        Args:
            system_prompt: Sistem talimatları
            user_prompt: Kullanıcı girişi
            temperature: Yaratıcılık seviyesi
            max_tokens: Maksimum token sayısı
            
        Returns:
            LLM yanıtı ve metadata
        """
        if not self.client:
            raise ValueError("API key ayarlanmamış. Lütfen ayarlar sekmesinden API key'inizi girin.")
        
        try:
            start_time = time.time()
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            end_time = time.time()
            
            result = {
                "content": response.choices[0].message.content,
                "model": response.model,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                },
                "response_time": end_time - start_time,
                "timestamp": time.time()
            }
            
            return result
            
        except Exception as e:
            raise Exception(f"LLM çağrısı başarısız: {str(e)}")
    
    def parse_json_response(self, response_content: str) -> Dict[str, Any]:
        """
        LLM yanıtından JSON'ı parse et
        
        Args:
            response_content: LLM'den gelen yanıt
            
        Returns:
            Parse edilmiş JSON
        """
        try:
            # JSON'ı bul ve parse et
            content = response_content.strip()
            
            # Bazen LLM ekstra açıklama ekler, sadece JSON kısmını al
            if '```json' in content:
                content = content.split('```json')[1].split('```')[0]
            elif content.startswith('```'):
                content = content.split('```')[1].split('```')[0]
            elif 'OUTPUT:' in content:
                # "OUTPUT:" prefix'ini kaldır
                content = content.replace('OUTPUT:', '').strip()
            elif 'OUTPUT_TEXT:' in content:
                # "OUTPUT_TEXT:" prefix'ini kaldır ve JSON kısmını bul
                content = content.replace('OUTPUT_TEXT:', '').strip()
            
            # JSON kısmını bul - { ile başlayan satırı ara
            lines = content.split('\n')
            json_started = False
            json_lines = []
            
            for line in lines:
                line = line.strip()
                if line.startswith('{'):
                    json_started = True
                
                if json_started:
                    json_lines.append(line)
                    if line.endswith('}') and line.count('{') <= line.count('}'):
                        break
            
            if json_lines:
                content = '\n'.join(json_lines)
            
            # Son temizlik
            content = content.strip()
            
            # JSON parse et - array veya object olabilir
            content = content.strip()
            
            # Eğer array ise
            if content.startswith('[') and content.endswith(']'):
                return json.loads(content)
            # Eğer object ise  
            elif content.startswith('{') and content.endswith('}'):
                return json.loads(content)
            else:
                # JSON kısmını bul
                import re
                # Array pattern
                array_match = re.search(r'\[.*?\]', content, re.DOTALL)
                if array_match:
                    return json.loads(array_match.group())
                
                # Object pattern
                obj_match = re.search(r'\{.*?\}', content, re.DOTALL)
                if obj_match:
                    return json.loads(obj_match.group())
                
                # Son çare - content'i direkt parse et
                return json.loads(content)
            
        except json.JSONDecodeError as e:
            # Son çare regex parsing
            import re
            
            # Array pattern (risk analizi için)
            array_pattern = r'\[\s*\{.*?\}\s*(?:,\s*\{.*?\}\s*)*\]'
            array_match = re.search(array_pattern, response_content, re.DOTALL)
            if array_match:
                try:
                    clean_json = array_match.group().strip()
                    return json.loads(clean_json)
                except:
                    pass
            
            # Object pattern (transliterasyon için)
            obj_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
            obj_match = re.search(obj_pattern, response_content, re.DOTALL)
            if obj_match:
                try:
                    clean_json = obj_match.group().strip()
                    return json.loads(clean_json)
                except:
                    pass
            
            raise ValueError(f"JSON parse hatası: {str(e)}\nİçerik: {response_content}")
    
    def validate_ota_characters(self, text: str) -> tuple:
        """
        CTA karakter setini doğrula
        
        Args:
            text: Kontrol edilecek metin
            
        Returns:
            tuple: (geçerli_mi, geçersiz_karakterler)
        """
        allowed_chars = set(
            "abcçdefgğhıijklmnñoòöpqrsştuüvwxyzäûəâîô" +
            "ABCÇDEFGĞHIİJKLMNÑOÒÖPQRSŞTUÜVWXYZÄÛƏÂÎÔ" +
            " .,:;!?()-[]{}\"'0123456789\n\r\t''"
        )
        
        invalid_chars = []
        for char in text:
            if char not in allowed_chars:
                if char not in invalid_chars:
                    invalid_chars.append(char)
        
        return len(invalid_chars) == 0, invalid_chars
    
    def check_idempotency(self, input_text: str, output_text: str, 
                         mapping_rules: Dict[str, str]) -> bool:
        """
        İdempotentlik kontrolü yap
        
        Args:
            input_text: Giriş metni
            output_text: Çıkış metni
            mapping_rules: Eşleme kuralları
            
        Returns:
            İdempotent mi?
        """
        # Basit kontrol: aynı girdi tekrar çevrildiğinde aynı çıktı vermeli
        # Bu gerçek implementasyonda daha karmaşık olacak
        return True  # Şimdilik True döndür
