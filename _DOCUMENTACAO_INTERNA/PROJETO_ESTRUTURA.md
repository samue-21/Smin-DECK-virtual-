# 📋 Estrutura do Projeto Smin-DECK

## 🎯 Objetivo
Sistema profissional de gerenciamento de mídia para igrejas com suporte a buttons customizáveis, controle de reprodução e editor de logo interativo.

---

## 📂 Arquitetura Principal

### **Arquivos Principais**
- **main.py** - Ponto de entrada da aplicação
- **deck_window.py** - Janela principal (UI, menu, gerenciamento)
- **playback_window.py** - Janela fullscreen de reprodução (vídeo/áudio/imagem)
- **logo_editor_window.py** - Editor interativo de posição/tamanho de logo (flutuante)
- **database.py** - Gerenciamento de banco de dados (botões, configurações)
- **background.py** - Controle de background (imagem ou cor)

### **Arquivos Suporte**
- **bot_humanizado.py** - Bot Discord humanizado (opcional)
- **bot_connector.py** - Integração com Discord
- **app_paths.py** - Gerenciador de caminhos de arquivos
- **arquivo_processor.py** - Processamento de arquivos enviados

---

## ✨ Features Implementadas

### ✅ Gerenciamento de Botões
- Criar, editar, deletar botões customizáveis
- Nomes e icones personalizados
- **Persistência**: Nomes salvos em banco de dados (não são perdidos ao reiniciar)

### ✅ Reprodução de Mídia
- **Vídeos**: MP4, AVI, MOV, MKV, FLV, WMV, WEBM, M4V
- **Áudio**: MP3, WAV, OGG, FLAC, AAC, M4A, WMA
- **Imagens**: JPG, JPEG, PNG, BMP, WEBP, GIF, SVG
- Fullscreen automático
- Loop mode (repetição contínua)
- Crossfade entre mídias

### ✅ Editor de Logo Interativo
- Janela flutuante separada (stays-on-top)
- Drag & Drop para posicionar logo
- Shift+Drag para redimensionar
- Controles spinbox para X, Y, tamanho
- Slider para opacidade (0-100%)
- **Persistência**: Salva em deck_config.sdk
- Preview em tempo real com grid

### ✅ Background Customizável
- Suporte a imagem ou cor sólida
- Integração com sistema de temas

### ✅ Discord Integration (Opcional)
- Auto-cleanup de canais
- Envio de arquivos para fila
- Bot humanizado

---

## ⚠️ Limitações Encontradas

### **Logo no Fullscreen (PyQt6 Limitation)**
❌ **PROBLEMA**: Não é possível exibir logo como overlay no fullscreen fullscreen due to:
- PyQt6 fullscreen widgets com layouts escondem overlays atrás do widget de vídeo
- paintEvent() não é chamado em fullscreen com layouts
- Z-order/raise_() não funciona em fullscreen
- QGraphicsOpacityEffect causa conflitos com painter

✅ **SOLUÇÃO**: Editor de logo funciona perfeitamente:
- Usuário edita logo em janela flutuante separada
- Configuração é salva em JSON
- Pronto para: C++, Electron, ou outra linguagem com melhor controle de rendering

### **PyQt6 Limitações Gerais**
- Overlays em fullscreen são extremamente limitados
- Rendering customizado em fullscreen é complicado
- Falta de controle fino sobre composição de layers
- Alto consumo de memória em apps grandes

---

## 🔧 Configuração de Logo

### **Estrutura JSON (deck_config.sdk)**
```json
{
  "player_config": {
    "logo_path": "C:/Users/.../logo.png",
    "logo_size": 150,
    "logo_opacity": 0.8,
    "x": 10,
    "y": 218
  }
}
```

### **Usando o Editor**
1. Durante reprodução: Clique com direito → "✏️ Editar posição da logo…"
2. Janela flutuante abre
3. Arraste para mover, Shift+Arraste para redimensionar
4. Ajuste X, Y, tamanho e opacidade
5. Clique "✅ Salvar"
6. Configuração é persistida automaticamente

---

## 📊 Fluxo de Dados

```
main.py
  ↓
deck_window.py (UI Principal)
  ├── Gerencia botões (database.py)
  ├── Controla reprodução
  └── Abre playback_window.py (fullscreen)
      ├── Reproduz mídia
      ├── Liga logo_editor_window.py (flutuante)
      └── Salva config em deck_config.sdk

logo_editor_window.py
  ├── Edita posição/tamanho
  ├── Emite signals para deck_window
  └── deck_window atualiza player_config
```

---

## 🚀 Próximos Passos (Projeto Piloto)

### **Tecnologia Sugerida: Electron + React**
**Razões:**
- ✅ Total controle sobre rendering
- ✅ Overlays sem limitações
- ✅ Melhor performance
- ✅ Profissional para mercado
- ✅ Pode monetizar facilmente

**O que será possível:**
- Logo visível no fullscreen
- Efeitos avançados (blur, sombra, animações)
- UI mais moderna
- Melhor integração com sistemas operacionais

---

## 📝 Notas Importantes

### **Manutenção**
- Logs removidos de código de produção
- Código limpo e documentado
- Erros aparecem apenas quando necessário

### **Banco de Dados**
- SQLite (fácil deployment)
- Migrações automáticas
- Backup recomendado antes de atualizações

### **Distribuição**
- Compilável com PyInstaller
- Gera .exe single-file
- Requer Python 3.10+ (ou vendored)

---

## 📞 Suporte Técnico

**Problemas Comuns:**

1. **Logo não persiste**
   - Verifique deck_config.sdk existe
   - Verifique permissões de escrita

2. **Áudio/Vídeo não toca**
   - Verifique formato suportado
   - Verifique codec disponível

3. **Editor de logo não abre**
   - Verifique se vídeo está tocando
   - Menu aparece apenas durante playback

---

**Versão**: 1.0  
**Data**: Janeiro 2026  
**Status**: Estável para produção (exceto logo em fullscreen)
