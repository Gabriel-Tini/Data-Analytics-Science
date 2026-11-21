from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


# 1. Carregamento dos dados
data_path = Path("Dataset/netflix_titles.csv")
df = pd.read_csv(data_path) 

if data_path.exists():
    print("Arquivo carregado com sucesso!")


# 2. Visualização geral dos dados
print(f'\nPrimeiras linhas do DataFrame:\n{df.head()}')  # Exibir as primeiras linhas do DataFrame
print('\nInformações gerais do DataFrame:')
df.info()  # Exibir informações gerais sobre o DataFrame, incluindo tipos de dados e contagem de valores não nulos
print(f'\nForma do DataFrame (linhas, colunas):\n{df.shape}')  # Exibir a forma do DataFrame (número de linhas e colunas)
print(f'\nEstatísticas descritivas:\n{df.describe().round(2)}')  # Exibir estatísticas descritivas das colunas numéricas
print(f'\nValores nulos por coluna:\n{df.isnull().sum()}')  # Exibir a contagem de valores nulos em cada coluna

# 3. Tratamento das colunas de data
df[["duration_int", "duration_type"]] = df["duration"].str.split(" ", n=1, expand=True) # Separando a coluna "duration" em duas colunas: "duration_int" (parte numérica) e "duration_type" (parte textual)
df["duration_int"] = pd.to_numeric(df["duration_int"], errors="coerce").astype("Int64") #Convertendo a coluna "duration_int" para o tipo inteiro, tratando valores não numéricos como NaN
df["duration_type"] = df["duration_type"].replace({"Season": "Seasons"}) #Padroniza Season e Seasons em uma categoria

print("\nAmostra de duration, duration_int e duration_type:")
print(df[["duration", "duration_int", "duration_type"]].head())

print("\nCategorias em duration_type:")
print(df["duration_type"].value_counts(dropna=False))

#Medidas de Tendência Central 
coluna = "duration_int"

media = df[coluna].mean()
mediana = df[coluna].median()
moda = df[coluna].mode()

duracao_filmes = df.loc[df["type"] == "Movie", "duration_int"].dropna()

#Medida de Dispersão
desvio_padrao = df[coluna].std()

print("\nMedidas de Tendência Central:")
print(f"Média: {media:.2f}")
print(f"Mediana: {mediana:.2f}")
print(f"Moda: {moda.tolist()}")

print(f"\nMedida de Dispersão: {desvio_padrao:.2f}")

lancamentos_por_ano = (
    df["release_year"]
    .value_counts()
    .sort_index()
)
media_filmes = duracao_filmes.mean()
mediana_filmes = duracao_filmes.median()


# 4. Visualização Gráfica

# Evolução de lançamentos por ano
plt.figure(figsize=(8, 4))
plt.bar(lancamentos_por_ano.index, lancamentos_por_ano.values, color='darkblue')
plt.title("Evolução de Lançamentos por ano")
plt.xlabel('Ano de Lançamento')
plt.ylabel('Quantidade de Títulos')
plt.xticks(range(1920, 2025, 10), rotation = 45)
plt.grid(axis="y", linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig("images/releases_by_year.png", dpi=150)
plt.show()

# Histograma de duração dos filmes
plt.figure(figsize=(10,5))
plt.hist(duracao_filmes, bins=range(0, 300, 10), color="steelblue", edgecolor="white")
plt.axvline(media_filmes, color="red", linestyle="--", linewidth=1.8, label=f"Média: {media_filmes:.1f}min")

plt.title("Distribuição da Duração dos Filmes na Netflix")
plt.xlabel("Duração (minutos)")
plt.ylabel("Quantidade de Filmes")
plt.legend()
plt.grid(axis="y", linestyle = "--", alpha=0.7)
plt.tight_layout()
plt.savefig("images/movies_duration_hist.png", dpi=150)
plt.show()

