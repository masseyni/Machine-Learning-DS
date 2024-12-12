import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Fonction pour générer un jeu de données météo
def generate_weather_data():
    num_rows = 1000
    dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq="H")
    random_dates = np.random.choice(dates, num_rows, replace=True)

    np.random.seed(42)
    temperature = np.round(10 + 15 * np.sin(2 * np.pi * pd.to_datetime(random_dates).dayofyear / 365) + np.random.normal(0, 3, num_rows), 1)
    precipitation = np.random.choice([0, 0, 5, 10, 15, 20], size=num_rows, p=[0.6, 0.2, 0.1, 0.05, 0.03, 0.02])
    humidity = np.round(np.clip(50 + 20 * np.sin(2 * np.pi * pd.to_datetime(random_dates).dayofyear / 365) + np.random.normal(0, 10, num_rows), 30, 100), 1)
    latitude = np.random.uniform(-90, 90, num_rows)
    longitude = np.random.uniform(-180, 180, num_rows)

    weather_data = pd.DataFrame({
        "Date": random_dates,
        "Temperature": temperature,
        "Precipitation": precipitation,
        "Humidity": humidity,
        "Latitude": latitude,
        "Longitude": longitude
    })

    # Ajouter des colonnes dérivées
    weather_data["Temperature_F"] = weather_data["Temperature"] * 9 / 5 + 32
    weather_data["Is_Hot"] = (weather_data["Temperature"] > 25).astype(int)

    weather_data = weather_data.sort_values(by="Date").reset_index(drop=True)

    # Enregistrer dans un fichier CSV
    weather_data.to_csv("weather_data_1000.csv", index=False)
    print("Dataset météo avec 1000 lignes généré et sauvegardé dans 'weather_data_1000.csv'.")
    return weather_data

# Vérifier si le fichier existe avant de tenter de le charger
if os.path.exists("weather_data_1000.csv"):
    data = pd.read_csv("weather_data_1000.csv")
    print("Le fichier a été chargé avec succès.")
else:
    print("Le fichier n'existe pas. Génération du fichier...")
    data = generate_weather_data()  # Appel à la fonction de génération des données

# Étape 1 : Charger le fichier et afficher le nombre de lignes et colonnes
print('Nombre de lignes et colonnes')
print(data.shape)

# Types de données
print('Types de données')
print(data.dtypes)

# Étape 2 : Résumé statistique
print('Résumé statistique')
print(data.describe())

# Les températures max et min
print('Les températures max et min :')
max_temp = data['Temperature'].max()
min_temp = data['Temperature'].min()
print(f"Température minimum : {min_temp}°C")
print(f"Température maximum : {max_temp}°C")

# Étape 3 : Gestion des données manquantes
print('Valeurs manquantes')
print(data.isnull().sum())

# Remplir les valeurs manquantes de température par la moyenne
data['Temperature'] = data['Temperature'].fillna(data['Temperature'].mean())

# Étape 4 : Création d'une nouvelle colonne Temperature_Fahrenheit
data['Temperature_Fahrenheit'] = data['Temperature'] * 9 / 5 + 32

# Étape 5 : Filtrer les jours avec des températures supérieures à 30°C
hot_days = data[data['Temperature'] > 30]
print("\nJours où la température dépasse 30°C")
print(hot_days)

# Étape 6 : Visualisation des températures
plt.figure(figsize=(8, 6))
plt.hist(data['Temperature'], bins=20, color='skyblue', edgecolor='black')
plt.title('Distribution des Températures', fontsize=16)
plt.xlabel('Température (°C)', fontsize=12)
plt.ylabel('Fréquence', fontsize=12)
plt.show()

# Étape 7 : Nuage de points entre Température et Précipitation
sns.scatterplot(x='Temperature', y='Precipitation', data=data)

# Étape 8 : Création d'un graphique temporel pour les températures
data['Date'] = pd.to_datetime(data['Date'])
plt.figure(figsize=(10, 6))
plt.plot(data['Date'], data['Temperature'], label='Température')
plt.title('Variation des Températures au fil du temps', fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Température (°C)', fontsize=12)
plt.xticks(rotation=45)
plt.show()

# Étape 9 : Matrice de corrélation
corr_matrix = data.corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')

data.to_csv("weather_data_transformed.csv", index=False)  # Assurez-vous de sauvegarder le fichier ici
print("Les données transformées ont été sauvegardées dans 'weather_data_transformed.csv'.")

# Vérification des nouvelles colonnes avant l'enregistrement
print("\nVérification des nouvelles colonnes ajoutées :")

# Afficher les premières lignes avec les nouvelles colonnes
print(data[['Temperature_F', 'Is_Hot']].head())  