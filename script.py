import pandas as pd
import os

# === PERGUNTA O NOME DA PASTA (UNIDADE) ===
nome_unidade = input("Digite o nome da unidade/pasta para salvar os resultados (ex: Balsas): ").strip()

# Cria a pasta automaticamente se ela não existir
os.makedirs(nome_unidade, exist_ok=True)
print(f"\n[OK] Os arquivos serão salvos na pasta: {nome_unidade}\n")
# === NOMES DOS ARQUIVOS DE ENTRADA === 
# (Estes arquivos devem estar na mesma pasta onde o script está rodando)
FILE_CADASTRO = 'cadastro.csv'      # Ajuste se o nome for diferente
FILE_NAO_COMPARECEU = 'nao-compareceu.csv'
FILE_DESMARCADOS = 'desmarcados.csv'
FILE_AVALIACOES = 'avaliacoes.csv'         
FILE_TRATAMENTOS = 'tratamentos.csv'       

def limpar_dados(caminho):
    if not os.path.exists(caminho):
        print(f"[ERRO FATAL] O arquivo '{caminho}' não foi encontrado.")
        return None
    
    # Lendo o CSV
    df = pd.read_csv(caminho, sep=';', encoding='utf-8', on_bad_lines='skip')
    
    # Padroniza as colunas
    df.columns = [str(c).strip().upper() for c in df.columns]
    
    # Padroniza os textos (Tudo maiúsculo e sem espaços inúteis)
    cols_texto = df.select_dtypes(include=['object', 'string']).columns
    for col in cols_texto:
        df[col] = df[col].astype(str).str.strip().str.upper()
        
    return df

try:
    print("--- INICIANDO MOTOR DE CRUZAMENTO ---")
    
    print("Carregando Cadastro...")
    df_cad = limpar_dados(FILE_CADASTRO)
    if df_cad is not None:
        df_cad_unico = df_cad.drop_duplicates(subset=['PACIENTE'], keep='last')
    
    print("Carregando Operacional (Faltas/Desmarques)...")
    df_nao_comp = limpar_dados(FILE_NAO_COMPARECEU)
    df_desm = limpar_dados(FILE_DESMARCADOS)
    
    print("Carregando Vendas (Avaliações/Tratamentos)...")
    df_aval = limpar_dados(FILE_AVALIACOES)
    df_trat = limpar_dados(FILE_TRATAMENTOS)

    if all(df is not None for df in [df_cad, df_nao_comp, df_desm, df_aval, df_trat]):
        
        colunas_contato = ['PACIENTE', 'CELULAR']

        # --- LISTA 1: NÃO COMPARECEU ---
        print("\nCruzando: NÃO COMPARECEU...")
        res_nao_comp = pd.merge(df_nao_comp, df_cad_unico[colunas_contato], on='PACIENTE', how='left')
        
        # --- LISTA 2: DESMARCADOS ---
        print("Cruzando: DESMARCADOS...")
        res_desm = pd.merge(df_desm, df_cad_unico[colunas_contato], on='PACIENTE', how='left')

        # --- LISTA 3: AVALIOU, MAS NÃO FECHOU TRATAMENTO ---
        print("Cruzando: AVALIAÇÕES NÃO FECHADAS...")
        df_avaliou_nao_fechou = df_aval[~df_aval['PACIENTE'].isin(df_trat['PACIENTE'])]
        res_aval_perdidas = pd.merge(df_avaliou_nao_fechou, df_cad_unico[colunas_contato], on='PACIENTE', how='left')

        # --- EXPORTAÇÃO (SALVANDO DENTRO DA PASTA ESCOLHIDA) ---
        caminho_1 = os.path.join(nome_unidade, '1_FINAL_NAO_COMPARECEU.csv')
        caminho_2 = os.path.join(nome_unidade, '2_FINAL_DESMARCADOS.csv')
        caminho_3 = os.path.join(nome_unidade, '3_FINAL_AVALIACOES_NAO_FECHADAS.csv')

        res_nao_comp.to_csv(caminho_1, index=False, sep=';', encoding='utf-8-sig')
        res_desm.to_csv(caminho_2, index=False, sep=';', encoding='utf-8-sig')
        res_aval_perdidas.to_csv(caminho_3, index=False, sep=';', encoding='utf-8-sig')
        
        # --- RELATÓRIO ---
        print("\n" + "="*50)
        print(f"MISSÃO CUMPRIDA! ARQUIVOS SALVOS NA PASTA: '{nome_unidade}'")
        print("="*50)
        
        print(f"[A] Lista 'Não Compareceu': {len(res_nao_comp)} clientes.")
        print(f"   - Com Telefone: {res_nao_comp['CELULAR'].notna().sum()}")
        
        print(f"\n[B] Lista 'Desmarcados': {len(res_desm)} clientes.")
        print(f"   - Com Telefone: {res_desm['CELULAR'].notna().sum()}")
        
        print(f"\n[C] Lista 'Avaliaram, Mas Não Compraram' (Follow-up): {len(res_aval_perdidas)} clientes.")
        print(f"   - Com Telefone: {res_aval_perdidas['CELULAR'].notna().sum()}")
        print("="*50)

except Exception as e:
    print(f"\nERRO CRÍTICO DURANTE O PROCESSO: {e}")