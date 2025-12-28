import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="SaaS Fiscal Autônomo", page_icon="📊")

st.title("🛡️ Simulador de Sobrevivência: Reforma 2026")
st.markdown("""
Esta ferramenta ajuda o autônomo a entender o **Split Payment** e o impacto do **IBS/CBS**.
""")

# Barra lateral para configurações
st.sidebar.header("Configurações Fiscais")
aliquota_iva = st.sidebar.slider("Alíquota Estimada IVA Dual (%)", 20.0, 30.0, 27.5)

# Área principal
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        valor_venda = st.number_input("Valor do seu Serviço (R$)", min_value=0.0, value=1000.0)
        categoria = st.selectbox("Categoria", ["Serviços Técnicos", "Consultoria", "Comércio", "Educação"])

    # Cálculos
    valor_imposto = valor_venda * (aliquota_iva / 100)
    valor_liquido = valor_venda - valor_imposto

    with col2:
        st.metric("Você recebe (Líquido)", f"R$ {valor_liquido:.2f}")
        st.metric("Retenção Automática", f"R$ {valor_imposto:.2f}", delta="-IVA", delta_color="inverse")

# Gráfico simples de impacto
st.subheader("Análise de Recebimento")
dados_grafico = pd.DataFrame({
    'Tipo': ['Seu Bolso', 'Governo (IBS/CBS)'],
    'Valor': [valor_liquido, valor_imposto]
})
st.bar_chart(data=dados_grafico, x='Tipo', y='Valor')

st.info("💡 **Dica de Negócio:** Com a Reforma, o imposto é retido na hora (Split Payment). Este SaaS ajuda você a planejar o seu preço de venda para não ficar no prejuízo.")from fpdf import FPDF
import streamlit as st

# Função para criar o PDF
def gerar_pdf(dados):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(40, 10, "Relatório de Planejamento Fiscal 2026")
    pdf.ln(20)
    
    pdf.set_font("Arial", "", 12)
    pdf.cell(40, 10, f"Categoria de Serviço: {dados['categoria']}")
    pdf.ln(10)
    pdf.cell(40, 10, f"Valor Bruto: R$ {dados['valor_bruto']:.2f}")
    pdf.ln(10)
    pdf.cell(40, 10, f"Imposto Retido (IBS/CBS): R$ {dados['imposto']:.2f}")
    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(40, 10, f"Valor Líquido na Conta: R$ {dados['valor_liquido']:.2f}")
    
    return pdf.output(dest='S').encode('latin-1')

# --- DENTRO DO SEU CÓDIGO APP.PY (Onde aparecem os resultados) ---

# Prepare os dados para o PDF
dados_para_relatorio = {
    "categoria": categoria,
    "valor_bruto": valor_venda,
    "imposto": valor_imposto,
    "valor_liquido": valor_liquido
}

# Botão de Download
pdf_bytes = gerar_pdf(dados_para_relatorio)
st.download_button(
    label="📥 Baixar Planejamento em PDF",
    data=pdf_bytes,
    file_name="planejamento_fiscal.pdf",
    mime="application/pdf"
)