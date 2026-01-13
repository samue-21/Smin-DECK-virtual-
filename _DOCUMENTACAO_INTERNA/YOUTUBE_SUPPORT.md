# YouTube Support - SminDeck

## Funcionalidade Implementada

Agora você pode adicionar vídeos do YouTube diretamente ao SminDeck! Quando clica no botão, o vídeo será aberto em fullscreen no seu navegador padrão.

## Como Usar

### 1. Adicionando uma URL do YouTube

#### Método 1: Via Diálogo de Seleção de Mídia
1. Clique em um botão para associar uma mídia
2. Na janela que aparece, vá para a aba **"📺 YouTube"**
3. Cole a URL do YouTube no campo de entrada
4. A URL será validada automaticamente (você verá ✅ quando for válida)
5. Clique em **OK** para salvar

#### Método 2: Dragging & Dropping
Você pode arrastar e soltar um arquivo (arquivo local) como já fazia antes. Para YouTube, use o método acima.

### 2. Formatos de URL Suportados

Todas as variações de URL do YouTube são suportadas:

- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/embed/VIDEO_ID`
- `youtube.com/watch?v=VIDEO_ID` (sem https)

Com parâmetros adicionais:
- `https://www.youtube.com/watch?v=VIDEO_ID&t=10s` (tempo específico)

### 3. Reproduzindo o Vídeo

1. Clique no botão que tem uma URL do YouTube associada
2. O vídeo abrirá automaticamente em fullscreen no seu navegador padrão
3. O vídeo iniciará com autoplay ativado

### 4. Salvamento de Configuração

Quando você fecha o SminDeck, todas as URLs do YouTube são automaticamente salvas no arquivo `deck_config.sdk`. Quando você reabre a aplicação, as URLs continuam associadas aos botões.

## Detalhes Técnicos

- **Detecção de URL**: Usa expressões regulares (regex) para validar URLs do YouTube
- **Extração de ID**: Extrai automaticamente o ID do vídeo da URL
- **Abertura em Fullscreen**: Abre a URL em fullscreen usando o navegador padrão do sistema
- **Autoplay**: O vídeo começa a reproduzir automaticamente

## Recursos Visuais

- **Ícone do Botão**: Quando uma URL do YouTube é adicionada, o botão exibe "📺 YouTube"
- **Validação em Tempo Real**: Conforme você digita a URL, o sistema valida e mostra:
  - ✅ URL válida (com a URL truncada)
  - ❌ URL inválida (se não for reconhecida como YouTube)

## Possíveis Melhorias Futuras

- Suporte a reprodução dentro da aplicação (sem abrir navegador)
- Download de vídeos usando yt-dlp
- Previsualização de thumbnail do vídeo
- Suporte a playlists do YouTube
- Controle de reprodução (pause, skip, etc.) dentro da aplicação

## Troubleshooting

### "URL inválida do YouTube"
- Verifique se a URL é do YouTube (youtube.com ou youtu.be)
- Copie a URL completa da barra de endereço do navegador
- Tente novamente

### Vídeo não abre
- Verifique se seu navegador padrão está configurado
- Verifique sua conexão com a internet
- Tente abrir a URL manualmente no seu navegador

### Configuração não é salva
- Certifique-se de que a pasta contém o arquivo `deck_config.sdk`
- Verifique permissões de escrita na pasta do SminDeck

---

**Versão**: 0.1.2+YouTube  
**Data**: Janeiro 2026
