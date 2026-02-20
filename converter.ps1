# 1. LISTA DE ARQUIVOS (O motor vai processar todos estes nomes)
# Se o nome do arquivo mudar no futuro, basta alterar aqui
$arquivos = @("cadastros", "tratamentos", "desmarcados", "nao-compareceu", "avaliacoes")
$pasta = "C:\Users\douto\Downloads\script-importacao-massa\Arquivos"

Write-Host "Iniciando o Motor Excel em Lote..."
$excel = New-Object -ComObject Excel.Application
$excel.Visible = $false
$excel.DisplayAlerts = $false 

# 2. O LAÇO DE REPETIÇÃO (Loop)
foreach ($nome in $arquivos) {
    $caminhoEntrada = "$pasta\$nome.xls"
    $caminhoSaida = "$pasta\$nome.csv"

    # Verifica se o arquivo .xls existe antes de tentar abrir
    if (Test-Path $caminhoEntrada) {
        Write-Host "-> Processando: $nome.xls..."
        
        $wb = $excel.Workbooks.Open($caminhoEntrada)
        
        # 62 = xlCSVUTF8 | $true = usa separador local (;)
        $wb.SaveAs($caminhoSaida, 62, [Type]::Missing, [Type]::Missing, [Type]::Missing, [Type]::Missing, [Type]::Missing, [Type]::Missing, [Type]::Missing, [Type]::Missing, [Type]::Missing, $true)
        
        $wb.Close($false)
        [System.Runtime.Interopservices.Marshal]::ReleaseComObject($wb) | Out-Null
        
        # Destruição do original
        Remove-Item -Path $caminhoEntrada -Force
        Write-Host "   [OK] Convertido para CSV e .xls destruído."
    } else {
        Write-Host "   [PULADO] Arquivo $nome.xls não encontrado na pasta."
    }
}

# 3. FAXINA FINAL (Só acontece depois que todos os arquivos foram processados)
Write-Host "Fechando o Excel e limpando a memória RAM..."
$excel.Quit()

[System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel) | Out-Null
[System.GC]::Collect()
[System.GC]::WaitForPendingFinalizers()

Write-Host "============================================="
Write-Host "OPERAÇÃO EM LOTE FINALIZADA COM SUCESSO!"
Write-Host "============================================="