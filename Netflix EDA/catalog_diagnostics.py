from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


# 1. Carregamento dos dados
BASE_DIR = Path(__file__).resolve().parent
data_path = BASE_DIR / "Dataset" / "netflix_titles.csv"
images_dir = BASE_DIR / "images"
images_dir.mkdir(exist_ok=True)

if not data_path.exists():
    raise FileNotFoundError(f"Arquivo não encontrado em: {data_path}")

df = pd.read_csv(data_path)
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

# Medidas de Tendência Central e Dispersão (apenas filmes, em minutos)
duracao_filmes = df.loc[df["type"] == "Movie", "duration_int"].dropna()

media = duracao_filmes.mean()
mediana = duracao_filmes.median()
moda = duracao_filmes.mode()
desvio_padrao = duracao_filmes.std()
minimo = duracao_filmes.min()
maximo = duracao_filmes.max()

print("\nMedidas de Tendência Central (Filmes em minutos):")
print(f"Média: {media:.2f}")
print(f"Mediana: {mediana:.2f}")
print(f"Moda: {moda.tolist()}")
print(f"Mín / Máx: {minimo} / {maximo}")

print(f"\nMedida de Dispersão (Desvio Padrão): {desvio_padrao:.2f}")

lancamentos_por_ano = (
    df["release_year"]
    .value_counts()
    .sort_index()
)


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
plt.savefig(images_dir / "releases_by_year.png", dpi=150)
plt.show()

# Histograma de duração dos filmes
plt.figure(figsize=(10,5))
plt.hist(duracao_filmes, bins=range(0, 330, 10), color="steelblue", edgecolor="white")
plt.axvline(media, color="red", linestyle="--", linewidth=1.8, label=f"Média: {media:.1f} min")

plt.title("Distribuição da Duração dos Filmes na Netflix")
plt.xlabel("Duração (minutos)")
plt.ylabel("Quantidade de Filmes")
plt.legend()
plt.grid(axis="y", linestyle = "--", alpha=0.7)
plt.tight_layout()
plt.savefig(images_dir / "movies_duration_hist.png", dpi=150)
plt.show()

