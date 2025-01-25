import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_log(file):
    df = pd.read_csv(file, header=None, names=["timestamp", "ip", "operation", "response_time"])
    return df

def generate_plots(df):
    st.subheader("Gráficos Gerados")

    # a) Pie chart: Percentage of calls per operation
    st.write("a) Porcentagem de chamadas por operação")
    operation_counts = df["operation"].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(operation_counts, labels=operation_counts.index, autopct="%1.1f%%", startangle=90)
    ax1.axis("equal")
    st.pyplot(fig1)

    # b) Horizontal bar chart: Number of requests per IP
    st.write("b) Quantidade de requisições por endereço IP")
    ip_counts = df["ip"].value_counts()
    fig2, ax2 = plt.subplots()
    sns.barplot(x=ip_counts.values, y=ip_counts.index, ax=ax2, orient="h")
    ax2.set_xlabel("Quantidade de Requisições")
    ax2.set_ylabel("Endereço IP")
    st.pyplot(fig2)

    # c) Vertical bar chart: Number of requests per hour of the day
    st.write("c) Quantidade de requisições por horário do dia")
    # Convert Unix timestamp to datetime and extract the hour
    df["hour"] = pd.to_datetime(df["timestamp"], unit="s").dt.hour
    hour_counts = df["hour"].value_counts().sort_index()
    fig3, ax3 = plt.subplots()
    sns.barplot(x=hour_counts.index, y=hour_counts.values, ax=ax3)
    ax3.set_xlabel("Hora do Dia")
    ax3.set_ylabel("Quantidade de Requisições")
    st.pyplot(fig3)

    # d) Scatter plot: Response time vs operation
    st.write("d) Tempo de resposta por operação")
    fig4, ax4 = plt.subplots()
    sns.scatterplot(x=df["operation"], y=df["response_time"], ax=ax4)
    ax4.set_xlabel("Operação")
    ax4.set_ylabel("Tempo de Resposta")
    st.pyplot(fig4)

st.title("Análise de Logs de Requisições")
uploaded_file = st.file_uploader("Carregue o arquivo de log", type=["txt", "csv"])
st.markdown("""
    ### Formato do Arquivo de Log
    O arquivo de log deve ser um arquivo de texto ou CSV com as seguintes colunas separadas por vírgula:
    - **timestamp**: O momento em que a requisição foi recebida, em formato Unix (segundos desde 1º de janeiro de 1970).
    - **ip**: O endereço IP do cliente que fez a requisição.
    - **operation**: O nome da operação realizada (por exemplo, `validate_cpf`, `mul`, `sub`).
    - **response_time**: O tempo (em segundos) que o servidor levou para processar a requisição.

    #### Exemplo de Linha:
    ```
    1737808565.968838, 199.98.50.213, validate_cpf, 0.01
    ```

    #### Exemplo de Arquivo:
    ```
    1737808565.968838, 199.98.50.213, validate_cpf, 0.01
    1737812165.9698384, 121.51.176.72, validate_cpf, 0.01
    1737815765.9708385, 84.212.194.153, mul, 0.02
    1737819365.9708385, 199.98.50.213, sub, 0.015
    ```
    """)


if uploaded_file is not None:
    df = load_log(uploaded_file)
    st.write("Dados do Log:")
    st.write(df)

    st.subheader("IPs Únicos")
    unique_ips = df["ip"].unique()
    st.write(unique_ips)

    generate_plots(df)