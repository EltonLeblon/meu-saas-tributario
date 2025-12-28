import streamlit as st
import pandas as pd
from fpdf import FPDF

# 1. Configuração da página
st.set_page_config(page_title="SaaS Fiscal 2026", page_icon="📈", layout="wide")

# 2. Função para gerar o PDF atualizada (Sem avisos de erro)
def gerar_pdf(dados):
    pdf = FPDF()
    pdf.add_page()
    
    # Cabeçalho
    pdf.set_font("helvetica", "B", 20)
    pdf.set_text_color(33, 150, 243) # Azul profissional
    pdf.cell(0, 15, "Planejamento Fiscal: Reforma 2026", align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    
    # Corpo do Relatório
    pdf.set_font("helvetica", "", 12)
    pdf.set_text_color(0, 0, 0)
    
    # Criando uma tabela simples
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(95, 10, "Descricao", border=1, fill=True)
    pdf.cell(95, 10, "Valor", border=1, fill=True, new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("helvetica", "", 12)
    itens = [
        ("Categoria", dados['categoria']),
        ("Faturamento Bruto", f"R$ {dados['valor_bruto']:.2f}"),
        ("Imposto Retido (IBS/CBS)", f"R$ {dados['imposto']:.2f}"),
        ("Aliquota Aplicada", f"{dados['aliquota']}%"),
    ]
    
    for item, valor in itens:
        pdf.cell(95, 10, item, border=1)
        pdf.cell(95, 10, valor, border=1, new_x="LMARGIN", new_y="NEXT")
    
    pdf.ln(10)
    pdf.set_font("helvetica", "B", 14)
    pdf.set_text_color(46, 125, 50) # Verde
    pdf.cell(0, 10, f"VALOR LIQUIDO FINAL: R$ {dados['valor_liquido']:.2f}", align='R')
    
    return pdf.output()

# 3. Interface Principal
st.title("🛡️ Simulador de Sobrevivência: Reforma 2026")
st.markdown("---")

# Barra lateral estilizada
with st.sidebar:
    st.header("⚙️ Ajustes Fiscais")
    aliquota_iva = st.slider("Alíquota estimada do IVA (%)", 20.0, 30.0, 27.5)
    st.info("A alíquota padrão prevista é de ~27,5%, mas pode variar conforme o setor.")

# Layout em colunas para métricas
valor_venda = st.number_input("Quanto pretende faturar por serviço (R$)?", min_value=0.0, value=5000.0, step=500.0)
categoria = st.selectbox("Qual o seu setor?", ["Serviços Técnicos", "Consultoria Jurídica/TI", "Comércio Internacional", "Saúde/Educação"])

valor_imposto = valor_venda * (aliquota_iva / 100)
valor_liquido = valor_venda - valor_imposto

st.subheader("📊 Resultados da Simulação")
c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Faturamento Bruto", f"R$ {valor_venda:,.2f}")
with c2:
    st.metric("Imposto (Split Payment)", f"R$ {valor_imposto:,.2f}", delta="-IVA", delta_color="inverse")
with c3:
    st.metric("Líquido Disponível", f"R$ {valor_liquido:,.2f}")

# Gráfico mais detalhado
st.markdown("### 📉 Distribuição do Faturamento")
dados_grafico = pd.DataFrame({
    'Destino': ['Seu Negócio', 'Impostos'],
    'Valor': [valor_liquido, valor_imposto]
})
st.bar_chart(data=dados_grafico, x='Destino', y='Valor', color=["#2ecc71", "#e74c3c"])

st.markdown("---")

# 4. Gerar PDF com o novo formato de bytes
st.subheader("📥 Exportar Planejamento Profissional")
col_btn, col_txt = st.columns([1, 2])

with col_btn:
    dados_relatorio = {
        "categoria": categoria,
        "valor_bruto": valor_venda,
        "imposto": valor_imposto,
        "valor_liquido": valor_liquido,
        "aliquota": aliquota_iva
    }
    
    pdf_bytes = gerar_pdf(dados_relatorio)
    
    st.download_button(
        label="Gerar Relatório PDF",
        data=bytes(pdf_bytes),
        file_name="planejamento_fiscal_v2.pdf",
        mime="application/pdf",
        use_container_width=True
    )

with col_txt:
    st.write("Utilize este documento para justificar o aumento de preços aos seus clientes com base na nova retenção automática.")