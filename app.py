import streamlit as st
import pandas as pd
from fpdf import FPDF
import os

# 1. Configuração da página e Estilo Customizado
st.set_page_config(page_title="SaaS Fiscal Elton", page_icon="💰", layout="wide")

# CSS para mudar a cor do botão e headers
st.markdown("""
    <style>
    .stButton>button {
        background-color: #003366;
        color: white;
        border-radius: 10px;
    }
    h1, h2, h3 {
        color: #003366;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Função para gerar o PDF Profissional
def gerar_pdf(dados):
    pdf = FPDF()
    pdf.add_page()
    
    diretorio_root = os.path.dirname(os.path.abspath(__file__))
    caminho_da_logo = os.path.join(diretorio_root, "logo.png")
    
    if os.path.exists(caminho_da_logo):
        pdf.image(caminho_da_logo, 10, 8, 33)
        pdf.ln(20)

    pdf.set_font("helvetica", "B", 20)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 15, "PLANEJAMENTO FISCAL E PREVIDENCIÁRIO", align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    
    pdf.set_font("helvetica", "", 12)
    pdf.set_text_color(0, 0, 0)
    
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(100, 10, "Descrição dos Valores", border=1, fill=True)
    pdf.cell(90, 10, "Valor Estimado", border=1, fill=True, new_x="LMARGIN", new_y="NEXT")
    
    itens = [
        ("Setor", dados['categoria']),
        ("Faturamento Bruto", f"R$ {dados['valor_bruto']:,.2f}"),
        ("Alíquota IVA", f"{dados['aliquota']}%"),
        ("Retenção IVA", f"R$ {dados['imposto']:,.2f}"),
        ("Contribuição INSS", f"R$ {dados['inss']:,.2f}")
    ]
    
    for item, valor in itens:
        pdf.cell(100, 10, item, border=1)
        pdf.cell(90, 10, valor, border=1, new_x="LMARGIN", new_y="NEXT")
    
    pdf.ln(10)
    pdf.set_font("helvetica", "B", 14)
    pdf.set_text_color(46, 125, 50)
    pdf.cell(0, 10, f"SALDO LÍQUIDO FINAL: R$ {dados['valor_liquido']:,.2f}", align='R')
    
    return pdf.output()

# 3. Interface Visual
diretorio_root = os.path.dirname(os.path.abspath(__file__))
caminho_da_logo = os.path.join(diretorio_root, "logo.png")

col_logo, col_titulo = st.columns([1, 4])
with col_logo:
    if os.path.exists(caminho_da_logo):
        st.image(caminho_da_logo, width=120)
with col_titulo:
    st.title("Simulador Fiscal & Previdenciário 2026")
    st.write("Análise completa de recebíveis para Profissionais Autônomos.")

st.divider()

# Colunas de entrada
c1, c2 = st.columns(2)
with c1:
    st.subheader("📝 Configurações")
    valor_venda = st.number_input("Valor total do serviço (R$)", min_value=0.0, value=10000.0)
    categoria = st.selectbox("Área de Atuação", ["Engenharia", "Advocacia", "Arquitetura", "Tecnologia", "Saúde"])
    aliquota = st.slider("Alíquota IVA prevista (%)", 25.0, 30.0, 27.5)
    
    calc_inss = st.checkbox("Deseja calcular INSS (Autônomo)?", value=True)
    inss = (valor_venda * 0.11) if calc_inss else 0.0 # Exemplo de 11%

valor_imposto = valor_venda * (aliquota / 100)
valor_liquido = valor_venda - valor_imposto - inss

with c2:
    st.subheader("💰 Resultado Detalhado")
    st.metric("Líquido na Conta", f"R$ {valor_liquido:,.2f}")
    
    # Gráfico de pizza para melhor visualização
    df_pizza = pd.DataFrame({
        'Categoria': ['Líquido', 'IVA (Imposto)', 'INSS'],
        'Valor': [valor_liquido, valor_imposto, inss]
    })
    st.bar_chart(df_pizza, x='Categoria', y='Valor', color=['#2ecc71', '#e74c3c', '#f1c40f'])

st.divider()

# 4. Dados e Botão
dados_relatorio = {
    "categoria": categoria,
    "valor_bruto": valor_venda,
    "imposto": valor_imposto,
    "inss": inss,
    "valor_liquido": valor_liquido,
    "aliquota": aliquota
}

st.subheader("📄 Exportação")
if st.button("Gerar Planejamento em PDF"):
    pdf_res = gerar_pdf(dados_relatorio)
    st.download_button(
        label="📥 Baixar agora",
        data=bytes(pdf_res),
        file_name="Planejamento_Completo_2026.pdf",
        mime="application/pdf"
    )

st.sidebar.markdown("---")
st.sidebar.info("Este simulador considera o Split Payment da Reforma Tributária.")