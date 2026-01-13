# 🚀 Plano: Projeto Piloto Smin-DECK 2.0

## 📌 Objetivo
Criar versão melhorada com **Electron + React** para superar limitações de PyQt6 e entrar no mercado profissional.

---

## 🎯 Fase 1: Planejamento e Setup (Semana 1)

### **Tecnologias**
```
Frontend: React + TypeScript
Backend: Electron Main Process (Node.js)
Media: electron-media-player ou libvlc.js
Database: SQLite com better-sqlite3
Build: Electron Builder
```

### **Estrutura do Projeto**
```
smin-deck-2.0/
├── public/           # Assets estáticos
├── src/
│   ├── main/        # Electron Main (backend)
│   ├── renderer/    # React App (frontend)
│   └── shared/      # Tipos compartilhados
├── package.json
└── electron-builder.json
```

### **Vantagens vs PyQt6**
| Feature | PyQt6 | Electron+React |
|---------|-------|-----------------|
| Logo Overlay | ❌ Impossível | ✅ Fácil |
| Efeitos (blur, shadow) | ⚠️ Complicado | ✅ CSS simples |
| UI Customização | ⚠️ Limitado | ✅ Total |
| Performance | ✅ Rápido | ✅ Rápido |
| Tamanho .exe | 100MB+ | 150-200MB |
| RAM mínima | 100MB | 150MB |
| Comunidade | Pequena | Gigante |
| Monetização | Complicado | Fácil |

---

## 📋 Fase 2: MVP (Prototipagem Rápida)

### **Feature Set Mínimo**
1. ✅ Player simples (vídeo/áudio)
2. ✅ Logo overlay (funcional!)
3. ✅ Editor de logo interativo
4. ✅ Botões customizáveis
5. ✅ Database (SQLite)

### **O que NÃO incluir no MVP**
- ❌ Discord integration (Fase 3)
- ❌ Themes customizados (Fase 4)
- ❌ Multi-monitor (Fase 3)
- ❌ Streaming integration (Futuro)

### **Timeline Estimada**
- Setup: 2-3 dias
- Player: 3-4 dias
- Logo editor: 2-3 dias
- Buttons: 2-3 dias
- Database: 1-2 dias
- **Total: 2-3 semanas**

---

## 🔧 Fase 3: Features Avançadas

### **Primeira onda**
- [ ] Discord bot integration
- [ ] Multi-screen support
- [ ] Themes customizados
- [ ] Efeitos visuais (blur, shadow, glow)
- [ ] Animações de transição

### **Segunda onda**
- [ ] Suporte a plugins
- [ ] Recording de reprodução
- [ ] Streaming ao vivo (OBS integration)
- [ ] Analytics básico
- [ ] Auto-update

---

## 💰 Fase 4: Monetização

### **Modelos Sugeridos**
1. **Versão Gratuita + Pro**
   - Gratuita: 2 botões, sem logo
   - Pro: Ilimitado, com logo, $10-20/mês

2. **One-time Purchase**
   - $50-100 (melhor para igrejas)

3. **Subscription + Support**
   - $15/mês + suporte técnico

### **O que cobrar**
- ✅ Logo animated
- ✅ Filtros de vídeo
- ✅ Cloud sync
- ✅ Priority support
- ✅ Custom themes
- ✅ API access

---

## 📊 Comparação: Smin-DECK vs Smin-DECK 2.0

### **Atual (PyQt6)**
```
✅ Funcional
✅ Leve
✅ Estável
❌ Logo não aparece (fullscreen)
❌ UI básica
❌ Difícil de monetizar
❌ Comunidade pequena
❌ Extensibilidade limitada
```

### **Novo (Electron+React)**
```
✅ Logo funciona perfeitamente
✅ UI moderna/profissional
✅ Fácil de monetizar
✅ Comunidade gigante
✅ Extensível com plugins
✅ Atualizações automáticas
✅ Melhor experiência mobile (desktop)
⚠️ Consome mais RAM
⚠️ .exe um pouco maior
```

---

## 🎨 UI/UX Improvements

### **Atual**
- Interface desktop clássica
- Menu simples
- Logo editável mas não visível

### **Novo**
- Drag-and-drop intuitivo
- Dark mode nativo
- Logo visible in real-time
- Animations suaves
- Mobile-responsive (para settings)
- Atalhos de teclado customizáveis
- Preview ao vivo do layout

---

## 💾 Dados e Migração

### **Do PyQt6 para Electron**
```python
# Export de deck_config.sdk (JSON)
{
  "buttons": [...],
  "player_config": {...},
  "logo_config": {...}
}

# Importar direto no Electron
// No Electron, mesmo formato JSON
```

**Processo:**
1. Export: `python export_config.py` → config.json
2. Manual import: Copiar arquivo para Electron app
3. **Ou**: Criar ferramenta de migração automática

---

## 🗺️ Roadmap

```
Semana 1-3: MVP (Player + Logo)
    ↓
Semana 4-5: Features Avançadas
    ↓
Semana 6: Testing & Bug Fixes
    ↓
Semana 7: Packaging & Distribution
    ↓
Semana 8+: Monetização & Marketing
```

---

## 📝 Próximas Ações

### **Agora (Setup Inicial)**
1. [ ] Criar novo projeto Electron
2. [ ] Setup React + TypeScript
3. [ ] Estrutura de pasta
4. [ ] CI/CD básico

### **Protótipo (2 semanas)**
1. [ ] Player funcional
2. [ ] Logo overlay visível
3. [ ] Editor interativo de logo
4. [ ] Persistência de config

### **MVP (1 semana)**
1. [ ] Botões funcionais
2. [ ] Database integrado
3. [ ] Packaging .exe
4. [ ] Testes básicos

---

## ❓ Decisões Importantes

**Antes de começar, defina:**

1. **Monetização desde o início?**
   - Sim: Incluir sistema de licenças no MVP
   - Não: Adicionar depois

2. **Suporte a Mac/Linux?**
   - Sim: +30% de tempo desenvolvimento
   - Não: Apenas Windows

3. **Streaming integration?**
   - Sim: Use FFmpeg
   - Não: Media nativo apenas

4. **Plugins/Extensões?**
   - Sim: Arquitetura plugin desde o início
   - Não: App monolítico

---

## 📚 Recursos Úteis

### **Documentação**
- Electron: https://www.electronjs.org/docs
- React: https://react.dev
- Tauri (alternativa): https://tauri.app

### **Libraries Recomendadas**
- `electron-builder` - Packaging
- `react-router` - Navegação
- `sqlite3` / `better-sqlite3` - Database
- `electron-updater` - Auto updates
- `framer-motion` - Animações

---

## ✅ Checklist de Decisão

Antes de iniciar, confirme:

- [ ] Electron + React aprovados?
- [ ] Monetização definida?
- [ ] Timeline realista?
- [ ] Timeline realista?
- [ ] Manter PyQt6 em paralelo?
- [ ] Equipe pronta?

---

**Próxima Reunião**: Discutir decisões acima e começar setup do projeto piloto!
