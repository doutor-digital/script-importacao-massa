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
