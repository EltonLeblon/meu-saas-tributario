import streamlit as st
import pandas as pd
from fpdf import FPDF
import os

# 1. Configuração da página
st.set_page_config(page_title="SaaS Fiscal Elton", page_icon="💼", layout="wide")

# 2. Função para gerar o PDF Profissional
def gerar_pdf(dados):
    pdf = FPDF()
    pdf.add_page()
    
    # Se a logo existir, coloca no PDF também
    if os.path.exists("logo.png"):
        pdf.image("logo.png", 10, 8, 33)
        pdf.ln(20)

    pdf.set_font("helvetica", "B", 20)
    pdf.set_text_color(0, 51, 102) # Azul Marinho
    pdf.cell(0, 15, "RELATÓRIO DE PLANEJAMENTO FISCAL", align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    
    # Tabela de Dados
    pdf.set_font("helvetica", "", 12)
    pdf.set_text_color(0, 0, 0)
    
    # Cabeçalho da tabela
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(100, 10, "Item de Análise", border=1, fill=True)
    pdf.cell(90, 10, "Valor Estimado", border=1, fill=True, new_x="LMARGIN", new_y="NEXT")
    
    itens = [
        ("Setor de Atuação", dados['categoria']),
        ("Faturamento Bruto", f"R$ {dados['valor_bruto']:,.2f}"),
        ("Alíquota IVA (2026)", f"{dados['aliquota']}%"),
        ("Imposto Retido (Split Payment)", f"R$ {dados['imposto']:,.2f}")
    ]
    
    for item, valor in itens:
        pdf.cell(100, 10, item, border=1)
        pdf.cell(90, 10, valor, border=1, new_x="LMARGIN", new_y="NEXT")
    
    pdf.ln(10)
    pdf.set_font("helvetica", "B", 14)
    pdf.cell(0, 10, f"SALDO LÍQUIDO A RECEBER: R$ {dados['valor_liquido']:,.2f}", align='R')
    
    return pdf.output()

# 3. Interface Visual do Site
# Exibição da Logo no Site
col_logo, col_titulo = st.columns([1, 4])
with col_logo:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=150)
with col_titulo:
    st.title("Simulador Fiscal Inteligente")
    st.write("Prepare o seu negócio para a transição tributária de 2026.")

st.divider()

# Colunas de entrada
c1, c2 = st.columns(2)
with c1:
    st.subheader("📝 Dados do Contrato")
    valor_venda = st.number_input("Valor Bruto do Serviço (R$)", min_value=0.0, value=5000.0)
    categoria = st.selectbox("Tipo de Serviço", ["TI & Software", "Consultoria", "Engenharia", "Marketing"])
    aliquota = st.slider("Alíquota IVA (%)", 25.0, 30.0, 27.5)

valor_imposto = valor_venda * (aliquota / 100)
valor_liquido = valor_venda - valor_imposto

with c2:
    st.subheader("💰 Resumo Financeiro")
    st.metric("Receita Líquida", f"R$ {valor_liquido:,.2f}", help="Valor que sobrará após a retenção automática.")
    st.progress(valor_liquido/valor_venda)
    st.caption(f"O governo reterá R$ {valor_imposto:,.2f} automaticamente via Split Payment.")

# Botão de Download Grande
st.divider()
dados_relatorio = {
    "categoria": categoria,
    "valor_bruto": valor_venda,
    "imposto": valor_imposto,
    "valor_liquido": valor_liquido,
    "aliquota": aliquota
}

if st.button("🚀 Gerar Relatório agora"):
    pdf_res = gerar_pdf(dados_relatorio)
    st.download_button(
        label="✅ Clique aqui para baixar o PDF",
        data=bytes(pdf_res),
        file_name="Planejamento_Fiscal_2026.pdf",
        mime="application/pdf"
    )

st.sidebar.markdown("---")
st.sidebar.write("Desenvolvido por **Elton Leblon**")