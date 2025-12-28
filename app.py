import streamlit as st
import pandas as pd
from fpdf import FPDF

# 1. Configuração da página
st.set_page_config(page_title="SaaS Fiscal Autônomo", page_icon="📊")

# 2. Função para gerar o PDF (deve ficar no topo)
def gerar_pdf(dados):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Relatorio de Planejamento Fiscal 2026", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Categoria de Servico: {dados['categoria']}", ln=True)
    pdf.cell(0, 10, f"Valor Bruto: R$ {dados['valor_bruto']:.2f}", ln=True)
    pdf.cell(0, 10, f"Imposto Retido (IBS/CBS): R$ {dados['imposto']:.2f}", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"Valor Liquido Estimado: R$ {dados['valor_liquido']:.2f}", ln=True)
    
    # Retorna os bytes do PDF
    return pdf.output()

# 3. Interface Principal
st.title("🛡️ Simulador de Sobrevivência: Reforma 2026")

# Barra lateral
st.sidebar.header("Configurações")
aliquota_iva = st.sidebar.slider("Alíquota IVA (%)", 20.0, 30.0, 27.5)

# Entradas de dados
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

# Gráfico
st.subheader("Análise de Recebimento")
dados_grafico = pd.DataFrame({
    'Tipo': ['Seu Bolso', 'Governo'],
    'Valor': [valor_liquido, valor_imposto]
})
st.bar_chart(data=dados_grafico, x='Tipo', y='Valor')

st.divider() # Linha divisória

# 4. ÁREA DO BOTÃO PDF (Garantindo que apareça)
st.subheader("Gerar Documento Oficial")
try:
    dados_para_relatorio = {
        "categoria": categoria,
        "valor_bruto": valor_venda,
        "imposto": valor_imposto,
        "valor_liquido": valor_liquido
    }
    
    pdf_download = gerar_pdf(dados_para_relatorio)
    
    st.download_button(
        label="📥 Baixar Planejamento em PDF",
        data=pdf_download,
        file_name="planejamento_fiscal_2026.pdf",
        mime="application/pdf"
    )
except Exception as e:
    st.error(f"Erro ao gerar PDF: {e}")

st.info("💡 Dica: Este relatório pode ser usado para negociar seus contratos prevendo a retenção do Split Payment.")