# 🚀 Script de Importação em Massa e Cruzamento de Dados

Este projeto contém um conjunto de scripts para automatizar a conversão e o cruzamento de relatórios de clínicas/unidades de saúde.

O objetivo principal é transformar planilhas brutas do sistema em listas de contatos qualificadas para ações de recuperação de pacientes, incluindo:

- Follow-up
- Remarcações
- Resgate de avaliações não convertidas em tratamentos

---

# 🛠️ Arquitetura do Projeto

O fluxo de trabalho é dividido em duas etapas principais:

## 1. Conversão de Arquivos — `converter.ps1` (PowerShell)

Responsável por:

- Abrir arquivos `.xls` com o Microsoft Excel em segundo plano
- Converter para `.csv` em padrão **UTF-8 com separador `;`**
- Excluir automaticamente os arquivos `.xls` após a conversão

---

## 2. Cruzamento de Dados — `script.py` (Python)

Responsável por:

- Ler os arquivos `.csv`
- Limpar e padronizar os dados
- Cruzar as tabelas operacionais com a base de cadastro
- Recuperar números de telefone (celular) dos pacientes

---

# 📋 Pré-requisitos

Para executar a automação, você precisa ter:

- **Sistema Operacional:** Windows (devido ao COM Object do Excel)
- **Microsoft Excel instalado**
- **Python 3.x** instalado e no PATH
- **Biblioteca Pandas**

Instalação do pandas:

```bash
pip install pandas
```

---

# ⚙️ Como Usar

## Passo 1 — Preparação dos Arquivos

Coloque na pasta do projeto os relatórios exportados com os nomes **exatos** abaixo:

cadastro.xls
tratamentos.xls
desmarcados.xls
nao-compareceu.xls
avaliacoes.xls

> ⚠️ Os nomes precisam ser exatamente iguais para o script funcionar corretamente.

---

## Passo 2 — Configuração do Caminho

No arquivo `converter.ps1`, ajuste o diretório:

```powershell
$pasta = "C:\Users\douto\Downloads\script-importacao-massa"
```

Substitua pelo caminho real da sua máquina.

---

## Passo 3 — Conversão (XLS → CSV)

Execute o script PowerShell:

- Clique com o botão direito em `converter.ps1`
- Selecione **Executar com PowerShell**

O script irá:

- Converter automaticamente todos os arquivos `.xls` para `.csv`
- Excluir os arquivos `.xls` originais

---

## Passo 4 — Cruzamento de Dados (Python)

Abra o terminal na pasta do projeto e execute:

```bash
python script.py
```

O sistema solicitará o nome da unidade/pasta (exemplo: `Balsas` ou `Acailandia`).

O script irá:

- Criar a pasta automaticamente
- Processar os dados
- Gerar os arquivos finais

---

# 📊 Arquivos Finais Gerados

O script produz três listas estratégicas:

## 1. `1_FINAL_NAO_COMPARECEU.csv`
Pacientes que agendaram, mas não compareceram.

---

## 2. `2_FINAL_DESMARCADOS.csv`
Pacientes que desmarcaram ativamente a consulta.

---

## 3. `3_FINAL_AVALIACOES_NAO_FECHADAS.csv`
Pacientes que realizaram avaliação, mas **não iniciaram tratamento**.

> Este é o arquivo de maior valor comercial.

---

# 📈 Resultado no Console

Ao final da execução, será exibido um resumo com:

- Total de pacientes recuperados
- Quantidade de pacientes com telefone válido

---

# 🔍 Regras de Tratamento de Dados

O script Python aplica automaticamente:

- Padronização de textos em **maiúsculas**
- Remoção de espaços extras
- Tratamento de linhas inválidas (`on_bad_lines='skip'`)
- Cruzamento pelo campo **PACIENTE**

---

# ⚠️ Observações Importantes

- O script depende da consistência dos nomes das colunas
- Pequenas variações nos relatórios podem impactar o cruzamento
- Recomenda-se validar os arquivos `.csv` antes do processamento

---

# 🧩 Melhorias Futuras

Possíveis evoluções do projeto:

- Interface gráfica para execução
- Detecção automática de colunas
- Integração com API de WhatsApp
- Dashboard de métricas de recuperação

---

# 👨‍💻 Autor

Automação desenvolvida para recuperação e reativação de pacientes em clínicas de saúde.
