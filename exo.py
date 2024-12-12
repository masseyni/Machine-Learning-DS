import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px

# Charger ou générer les données si le fichier n'existe pas
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

    weather_data["Temperature_F"] = weather_data["Temperature"] * 9 / 5 + 32
    weather_data["Is_Hot"] = (weather_data["Temperature"] > 25).astype(int)

    weather_data = weather_data.sort_values(by="Date").reset_index(drop=True)
    weather_data.to_csv("weather_data_1000.csv", index=False)
    return weather_data

# Vérifier l'existence du fichier CSV
if os.path.exists("weather_data_1000.csv"):
    data = pd.read_csv("weather_data_1000.csv")
    print("Le fichier a été chargé avec succès.")
else:
    print("Le fichier n'existe pas. Génération du fichier...")
    data = generate_weather_data()  # Générer le dataset si le fichier n'existe pas

# Etape 1: Préparer les données pour une analyse mensuelle
# Transformez la colonne Date en mois
data['Date'] = pd.to_datetime(data['Date'])
data['Month'] = data['Date'].dt.month

# Regrouper les données pour calculer la température moyenne, les précipitations totales et l'humidité moyenne par mois
monthly_data = data.groupby('Month').agg(
    Temperature_mean=('Temperature', 'mean'),
    Precipitation_total=('Precipitation', 'sum'),
    Humidity_mean=('Humidity', 'mean')
).reset_index()

# Afficher les résultats mensuels
print(monthly_data)

# Questions intermédiaires :
# Quels sont les mois avec les précipitations les plus élevées ?
# on peut citer les 3 derniers mois de l'annee

max_precipitation_month = monthly_data.loc[monthly_data['Precipitation_total'].idxmax()]
print(f"Le mois avec les précipitations les plus élevées est : {max_precipitation_month['Month']} avec {max_precipitation_month['Precipitation_total']} mm.")

# Y a-t-il une différence notable entre les mois en termes d'humidité ?
#on peut dire que les 6 derniers mois sont plus humide que les 6 premiers
humidity_diff = monthly_data['Humidity_mean'].max() - monthly_data['Humidity_mean'].min()
print(f"La différence d'humidité entre le mois le plus humide et le plus sec est de : {humidity_diff}.")

# Etape 2: Créer une courbe pour les températures mensuelles
plt.figure(figsize=(10, 6))
plt.plot(monthly_data['Month'], monthly_data['Temperature_mean'], marker='o', color='tab:orange')
plt.title('Température Moyenne Mensuelle', fontsize=16)
plt.xlabel('Mois', fontsize=12)
plt.ylabel('Température Moyenne (°C)', fontsize=12)
plt.xticks(monthly_data['Month'])
plt.grid(True)
plt.show()

# Questions intermédiaires :
# Pendant quels mois la température est-elle la plus élevée ?
# La temperature est ^lus elevee au mois d'Avril
max_temp_month = monthly_data.loc[monthly_data['Temperature_mean'].idxmax()]
print(f"Le mois avec la température la plus élevée est : {max_temp_month['Month']} avec {max_temp_month['Temperature_mean']}°C.")

# Etape 3: Visualiser les précipitations mensuelles avec un histogramme
plt.figure(figsize=(10, 6))
sns.barplot(x='Month', y='Precipitation_total', data=monthly_data, palette='Blues')
plt.title('Précipitations Totales Mensuelles', fontsize=16)
plt.xlabel('Mois', fontsize=12)
plt.ylabel('Précipitations Totales (mm)', fontsize=12)
plt.xticks(monthly_data['Month'])
plt.show()

# Questions intermédiaires :
# Quels mois ont les précipitations les plus importantes ?

max_precip_month = monthly_data.loc[monthly_data['Precipitation_total'].idxmax()]
print(f"Le mois avec les précipitations les plus importantes est : {max_precip_month['Month']} avec {max_precip_month['Precipitation_total']} mm.")

# Etape 4: Créer un tableau de bord interactif avec Plotly
# Courbe des températures mensuelles
fig_temp = go.Figure()
fig_temp.add_trace(go.Scatter(x=monthly_data['Month'], y=monthly_data['Temperature_mean'], mode='lines+markers', name='Température Moyenne', line=dict(color='orange')))

# Histogramme des précipitations mensuelles
fig_precip = go.Figure()
fig_precip.add_trace(go.Bar(x=monthly_data['Month'], y=monthly_data['Precipitation_total'], name='Précipitations Totales', marker=dict(color='blue')))

# Créer un tableau de bord interactif combinant les deux graphiques
fig_dashboard = go.Figure()

# Ajouter les deux graphiques dans un seul tableau de bord
fig_dashboard.add_trace(go.Scatter(x=monthly_data['Month'], y=monthly_data['Temperature_mean'], mode='lines+markers', name='Température Moyenne', line=dict(color='orange')))
fig_dashboard.add_trace(go.Bar(x=monthly_data['Month'], y=monthly_data['Precipitation_total'], name='Précipitations Totales', marker=dict(color='blue')))

fig_dashboard.update_layout(
    title="Tableau de Bord Interactif des Températures et Précipitations Mensuelles",
    xaxis_title="Mois",
    yaxis_title="Valeurs",
    barmode='overlay',
    template="plotly_dark"
)

fig_dashboard.show()

# Questions intermédiaires :
# Quels mois présentent à la fois des températures élevées et de fortes précipitations ?
# on peut voir que le 4e mois nous avons une temperature ainsi qu'une precipitation assez elevee

# Les mois les plus secs (faibles précipitations) sont-ils aussi les plus froids ?
#Non car on constate que le mois de juin a la plus petite precipitation alors que la temperature reste elevee 
