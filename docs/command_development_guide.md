# Telegram Userbot Command Development Guide
# Telegram Userbot Komut Geliştirme Rehberi

## English Guide

### 1. Basic Command Structure
Every command file must follow this basic structure:
```python
async def command(event, args):
    """
    Command: your_command_name
    Description: Brief description of what your command does
    Usage: 
        !your_command_name [argument1] [argument2] - Description
        !your_command_name [optional_arg] - Another usage example
    """
    # Your code here
    return {
        "prefix": "your_command_name",
        "return": "Your response message"
    }
```

### 2. Important Components

#### 2.1 Command Function
- Must be named `command`
- Must be `async`
- Takes two parameters:
  - `event`: Contains message and chat information
  - `args`: List of command arguments

#### 2.2 Docstring
- Must include:
  - Command name
  - Description
  - Usage examples
- Will be used by the help system

#### 2.3 Return Value
Must return a dictionary with:
- `prefix`: Command name (for logging)
- `return`: Response message to send

### 3. Best Practices

#### 3.1 Language Support
Use the language manager for all user-facing messages:
```python
from utils.language import get_lang_manager

lang_manager = get_lang_manager()
message = lang_manager.get_text("your_command.message_key")
```

#### 3.2 Error Handling
Always use try-except blocks:
```python
try:
    # Your code here
except Exception as e:
    return {
        "prefix": "your_command_name",
        "return": f"Error: {str(e)}"
    }
```

#### 3.3 Logging
Use the logger for debugging:
```python
import logging
logger = logging.getLogger('your_command_name')
logger.info("Operation completed")
logger.error("An error occurred")
```

### 4. Example Command
Here's a complete example of a simple command:
```python
import logging
from utils.language import get_lang_manager

logger = logging.getLogger('greet')

async def command(event, args):
    """
    Command: greet
    Description: Greets a user
    Usage: 
        !greet - Greets you
        !greet [name] - Greets the specified person
    """
    try:
        lang_manager = get_lang_manager()
        
        if args:
            name = ' '.join(args)
            return {
                "prefix": "greet",
                "return": lang_manager.get_text("greet.with_name", name=name)
            }
        
        return {
            "prefix": "greet",
            "return": lang_manager.get_text("greet.default")
        }
    except Exception as e:
        logger.error(f"Error in greet command: {str(e)}")
        return {
            "prefix": "greet",
            "return": f"Error: {str(e)}"
        }
```

### 5. Security Guidelines
1. Never use `eval` or `exec`
2. Validate all user inputs
3. Be careful with file operations
4. Don't expose sensitive information
5. Use secure API endpoints (https)

---

## Türkçe Rehber

### 1. Temel Komut Yapısı
Her komut dosyası bu temel yapıyı takip etmelidir:
```python
async def command(event, args):
    """
    Command: komut_adınız
    Description: Komutunuzun kısa açıklaması
    Usage: 
        !komut_adınız [parametre1] [parametre2] - Açıklama
        !komut_adınız [opsiyonel_parametre] - Başka bir kullanım örneği
    """
    # Kodunuz buraya
    return {
        "prefix": "komut_adınız",
        "return": "Yanıt mesajınız"
    }
```

### 2. Önemli Bileşenler

#### 2.1 Komut Fonksiyonu
- İsmi `command` olmalı
- `async` olmalı
- İki parametre alır:
  - `event`: Mesaj ve sohbet bilgilerini içerir
  - `args`: Komut parametrelerinin listesi

#### 2.2 Docstring (Belgelendirme)
Şunları içermelidir:
- Komut adı
- Açıklama
- Kullanım örnekleri
- Yardım sistemi tarafından kullanılır

#### 2.3 Dönüş Değeri
Şu anahtarları içeren bir sözlük döndürmelidir:
- `prefix`: Komut adı (loglama için)
- `return`: Gönderilecek yanıt mesajı

### 3. En İyi Uygulamalar

#### 3.1 Dil Desteği
Kullanıcıya gösterilecek tüm mesajlar için dil yöneticisini kullanın:
```python
from utils.language import get_lang_manager

lang_manager = get_lang_manager()
mesaj = lang_manager.get_text("komutunuz.mesaj_anahtari")
```

#### 3.2 Hata Yönetimi
Her zaman try-except blokları kullanın:
```python
try:
    # Kodunuz buraya
except Exception as e:
    return {
        "prefix": "komut_adınız",
        "return": f"Hata: {str(e)}"
    }
```

#### 3.3 Loglama
Hata ayıklama için logger kullanın:
```python
import logging
logger = logging.getLogger('komut_adınız')
logger.info("İşlem tamamlandı")
logger.error("Bir hata oluştu")
```

### 4. Örnek Komut
İşte basit bir komutun tam örneği:
```python
import logging
from utils.language import get_lang_manager

logger = logging.getLogger('selam')

async def command(event, args):
    """
    Command: selam
    Description: Kullanıcıyı selamlar
    Usage: 
        !selam - Sizi selamlar
        !selam [isim] - Belirtilen kişiyi selamlar
    """
    try:
        lang_manager = get_lang_manager()
        
        if args:
            isim = ' '.join(args)
            return {
                "prefix": "selam",
                "return": lang_manager.get_text("selam.isimli", isim=isim)
            }
        
        return {
            "prefix": "selam",
            "return": lang_manager.get_text("selam.varsayilan")
        }
    except Exception as e:
        logger.error(f"Selam komutunda hata: {str(e)}")
        return {
            "prefix": "selam",
            "return": f"Hata: {str(e)}"
        }
```

### 5. Güvenlik Yönergeleri
1. Asla `eval` veya `exec` kullanmayın
2. Tüm kullanıcı girdilerini doğrulayın
3. Dosya işlemlerinde dikkatli olun
4. Hassas bilgileri açığa çıkarmayın
5. Güvenli API uç noktaları kullanın (https)

### 6. Önemli Notlar
1. Her komut tek bir işlevi yerine getirmeli
2. Kodunuzu iyi belgeleyin
3. Hata mesajları açık ve anlaşılır olmalı
4. Performans için asenkron işlemleri kullanın
5. Dil dosyalarına yeni metinleri eklemeyi unutmayın
