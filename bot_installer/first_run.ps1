# Script de Primeira Execução - Configuração do Bot Discord
# Este script roda quando o bot é iniciado pela primeira vez

# Função para pedindo token interativamente
function Get-DiscordToken {
    [System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms') | Out-Null
    [System.Reflection.Assembly]::LoadWithPartialName('System.Drawing') | Out-Null

    $form = New-Object System.Windows.Forms.Form
    $form.Text = 'Configuração do Bot Discord'
    $form.Width = 600
    $form.Height = 350
    $form.StartPosition = 'CenterScreen'
    $form.TopMost = $true

    $label1 = New-Object System.Windows.Forms.Label
    $label1.Text = 'Configure o Token do seu Bot Discord'
    $label1.Location = New-Object System.Drawing.Point(20, 20)
    $label1.Size = New-Object System.Drawing.Size(560, 30)
    $label1.Font = New-Object System.Drawing.Font('Arial', 12, [System.Drawing.FontStyle]::Bold)
    $form.Controls.Add($label1)

    $label2 = New-Object System.Windows.Forms.Label
    $label2.Text = @"
1. Acesse Discord Developer Portal: https://discord.com/developers/applications
2. Selecione seu Bot > Copie o Token (Bot section)
3. Cole o token abaixo:
"@
    $label2.Location = New-Object System.Drawing.Point(20, 60)
    $label2.Size = New-Object System.Drawing.Size(560, 100)
    $form.Controls.Add($label2)

    $textBox = New-Object System.Windows.Forms.TextBox
    $textBox.Location = New-Object System.Drawing.Point(20, 170)
    $textBox.Size = New-Object System.Drawing.Size(560, 30)
    $textBox.Font = New-Object System.Drawing.Font('Courier New', 10)
    $form.Controls.Add($textBox)

    $button = New-Object System.Windows.Forms.Button
    $button.Text = 'Confirmar e Iniciar Bot'
    $button.Location = New-Object System.Drawing.Point(20, 220)
    $button.Size = New-Object System.Drawing.Size(560, 40)
    $button.Font = New-Object System.Drawing.Font('Arial', 11)
    $button.DialogResult = [System.Windows.Forms.DialogResult]::OK
    $form.Controls.Add($button)

    $form.AcceptButton = $button
    $result = $form.ShowDialog()

    return $textBox.Text
}

# Diretório do bot
$BotDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$EnvFile = Join-Path $BotDir ".env"
$DiscordBotExe = Join-Path $BotDir "discord_bot.exe"
$ApiServerExe = Join-Path $BotDir "api_server.exe"

# Verifica se .env existe e se tem token válido
if ((Test-Path $EnvFile) -and ((Get-Content $EnvFile) -match 'DISCORD_TOKEN=.*[a-zA-Z0-9]')) {
    Write-Host "✓ Token já configurado. Iniciando serviços..."
} else {
    Write-Host "Configurando token na primeira execução..."
    $token = Get-DiscordToken
    
    if ($token) {
        # Cria ou atualiza .env
        @"
# Token do Discord Bot
DISCORD_TOKEN=$token
"@ | Out-File -FilePath $EnvFile -Encoding UTF8
        Write-Host "✓ Token salvo com sucesso!"
    } else {
        Write-Host "✗ Token não foi fornecido. Abortando."
        exit 1
    }
}

# Inicia o Discord Bot (sem console)
Write-Host "Iniciando Discord Bot..."
& $DiscordBotExe

# Inicia o API Server (sem console)
Write-Host "Iniciando API Server..."
& $ApiServerExe
