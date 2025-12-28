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

st.info("💡 **Dica de Negócio:** Com a Reforma, o imposto é retido na hora (Split Payment). Este SaaS ajuda você a planejar o seu preço de venda para não ficar no prejuízo.")