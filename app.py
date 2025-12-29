import streamlit as st
import pandas as pd
from fpdf import FPDF
import os

# 1. Configuração da página e Estilo
st.set_page_config(page_title="Simulador Fiscal", page_icon="💰", layout="wide")

st.markdown("""
    <style>
    .stButton>button {
        background-color: #003366;
        color: white;
        border-radius: 10px;
        width: 100%;
    }
    h1, h2, h3 {
        color: #003366;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f1f1f1;
        color: #555;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        border-top: 1px solid #ddd;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Função para gerar o PDF
def gerar_pdf(dados):
    pdf = FPDF()
    pdf.add_page()
    
    diretorio_root = os.path.dirname(os.path.abspath(__file__))
    caminho_logo = os.path.join(diretorio_root, "logo.png")
    
    if os.path.exists(caminho_logo):
        pdf.image(caminho_logo, 10, 8, 33)
        pdf.ln(20)

    pdf.set_font("helvetica", "B", 20)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 15, "PLANEJAMENTO FISCAL E PREVIDENCIÁRIO", align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    
    pdf.set_font("helvetica", "", 12)
    pdf.set_text_color(0, 0, 0)
    
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(100, 10, "Descricao", border=1, fill=True)
    pdf.cell(90, 10, "Valor Estimado", border=1, fill=True, new_x="LMARGIN", new_y="NEXT")
    
    itens = [
        ("Setor", dados['categoria']),
        ("Faturamento Bruto", f"R$ {dados['valor_bruto']:,.2f}"),
        ("Retencao IVA (2026)", f"R$ {dados['imposto']:,.2f}"),
        ("Contribuicao INSS", f"R$ {dados['inss']:,.2f}")
    ]
    
    for item, valor in itens:
        pdf.cell(100, 10, item, border=1)
        pdf.cell(90, 10, valor, border=1, new_x="LMARGIN", new_y="NEXT")
    
    pdf.ln(10)
    pdf.set_font("helvetica", "B", 14)
    pdf.set_text_color(46, 125, 50)
    pdf.cell(0, 10, f"SALDO LIQUIDO FINAL: R$ {dados['valor_liquido']:,.2f}", align='R')
    
    return pdf.output()

# 3. Interface Visual
diretorio_root = os.path.dirname(os.path.abspath(__file__))
caminho_logo = os.path.join(diretorio_root, "logo.png")

col_logo, col_titulo = st.columns([1, 4])
with col_logo:
    if os.path.exists(caminho_logo):
        st.image(caminho_logo, width=120)
with col_titulo:
    # NOME ALTERADO AQUI
    st.title("Simulador Fiscal")
    st.write("Estratégia e Inteligência Tributária para o seu negócio.")

st.divider()

c1, c2 = st.columns(2)
with c1:
    st.subheader("📝 Parâmetros")
    valor_venda = st.number_input("Valor do Serviço (R$)", min_value=0.0, value=10000.0)
    categoria = st.selectbox("Área", ["Tecnologia", "Consultoria", "Engenharia", "Saúde"])
    aliquota = st.slider("Alíquota IVA (%)", 25.0, 30.0, 27.5)
    
    calc_inss = st.checkbox("Calcular INSS Autônomo (11%)", value=True)
    inss = (valor_venda * 0.11) if calc_inss else 0.0

valor_imposto = valor_venda * (aliquota / 100)
valor_liquido = valor_venda - valor_imposto - inss

with c2:
    st.subheader("💰 Resumo Financeiro")
    st.metric("Líquido Estimado", f"R$ {valor_liquido:,.2f}")
    
    df_chart = pd.DataFrame({
        'Categoria': ['Líquido', 'IVA', 'INSS'],
        'Valor': [valor_liquido, valor_imposto, inss]
    })
    st.bar_chart(df_chart, x='Categoria', y='Valor', color='Categoria')

st.divider()

# 4. Exportação e Rodapé
st.subheader("📄 Gerar Documento Profissional")
dados_relatorio = {
    "categoria": categoria,
    "valor_bruto": valor_venda,
    "imposto": valor_imposto,
    "inss": inss,
    "valor_liquido": valor_liquido,
    "aliquota": aliquota
}

if st.button("Gerar Relatório de Planejamento"):
    pdf_res = gerar_pdf(dados_relatorio)
    st.download_button(
        label="📥 Clique aqui para baixar o PDF",
        data=bytes(pdf_res),
        file_name="Planejamento_Fiscal.pdf",
        mime="application/pdf"
    )

# RODAPÉ
st.markdown("""
    <div class="footer">
        <p>© 2025 Simulador Fiscal | Planejamento Tributário 2026</p>
    </div>
    """, unsafe_allow_html=True)