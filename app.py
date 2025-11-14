"""
Application Streamlit pour l'application sportive
Lancez avec : streamlit run app.py
"""
import streamlit as st
import requests
from datetime import date, datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Configuration de la page
st.set_page_config(
    page_title="Application Sportive",
    page_icon="🏃",
    layout="wide",
    initial_sidebar_state="expanded"
)

# URL de l'API (à adapter selon votre configuration)
API_URL = "http://localhost:8000/api"

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .success-msg {
        padding: 1rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        color: #155724;
    }
    .error-msg {
        padding: 1rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        color: #721c24;
    }
</style>
""", unsafe_allow_html=True)

# ========== GESTION DE SESSION ==========

def init_session():
    """Initialise les variables de session"""
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None

def login(pseudo, mdp):
    """Connexion d'un utilisateur"""
    try:
        response = requests.post(
            f"{API_URL}/utilisateurs/connexion",
            json={"pseudo": pseudo, "mdp": mdp}
        )
        if response.status_code == 200:
            user = response.json()
            st.session_state.user = user
            st.session_state.user_id = user['id']
            return True, "Connexion réussie !"
        else:
            return False, "Identifiants incorrects"
    except Exception as e:
        return False, f"Erreur : {str(e)}"

def logout():
    """Déconnexion"""
    st.session_state.user = None
    st.session_state.user_id = None

def register(nom, prenom, age, pseudo, mail, mdp, taille=None, poids=None):
    """Inscription d'un nouvel utilisateur"""
    try:
        data = {
            "nom": nom,
            "prenom": prenom,
            "age": age,
            "pseudo": pseudo,
            "mail": mail,
            "mdp": mdp
        }
        if taille:
            data["taille"] = taille
        if poids:
            data["poids"] = poids
            
        response = requests.post(
            f"{API_URL}/utilisateurs/inscription",
            json=data
        )
        if response.status_code == 201:
            return True, "Inscription réussie ! Vous pouvez vous connecter."
        else:
            error = response.json().get('detail', 'Erreur lors de l\'inscription')
            return False, error
    except Exception as e:
        return False, f"Erreur : {str(e)}"

# ========== FONCTIONS API ==========

def get_activites(user_id, type_sport=None, limit=50):
    """Récupère les activités d'un utilisateur"""
    try:
        params = {"limit": limit}
        if type_sport:
            params["type_sport"] = type_sport
        
        response = requests.get(
            f"{API_URL}/activites/utilisateur/{user_id}",
            params=params
        )
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

def creer_activite_manuelle(user_id, nom, type_sport, date_activite, duree_minutes, 
                           description="", d_plus=0, calories=0, distance=0):
    """Crée une activité manuellement"""
    try:
        response = requests.post(
            f"{API_URL}/activites",
            json={
                "utilisateur_id": user_id,
                "nom": nom,
                "type_sport": type_sport,
                "date_activite": date_activite.isoformat(),
                "duree_activite": duree_minutes * 60,  # Conversion en secondes
                "description": description,
                "d_plus": d_plus,
                "calories": calories,
                "distance": distance
            }
        )
        return response.status_code == 201, response.json()
    except Exception as e:
        return False, str(e)

def upload_gpx(user_id, nom, type_sport, description, gpx_file):
    """Upload un fichier GPX"""
    try:
        files = {"gpx": gpx_file}
        data = {
            "utilisateur_id": user_id,
            "nom": nom,
            "type_sport": type_sport,
            "description": description
        }
        response = requests.post(
            f"{API_URL}/activites/gpx",
            data=data,
            files=files
        )
        return response.status_code == 201, response.json()
    except Exception as e:
        return False, str(e)

def get_statistiques_completes(user_id, sections="resume,hebdo,sports,tableau_bord"):
    """Récupère les statistiques complètes"""
    try:
        response = requests.get(
            f"{API_URL}/statistiques/{user_id}/complet",
            params={"sections": sections}
        )
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def get_fil_actualite(user_id, nb_jours=7, limite=50):
    """Récupère le fil d'actualité"""
    try:
        response = requests.get(
            f"{API_URL}/fil/{user_id}",
            params={"nb_jours": nb_jours, "limite": limite}
        )
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

def liker_activite(user_id, activite_id):
    """Like une activité"""
    try:
        response = requests.post(
            f"{API_URL}/interactions/activites/{activite_id}/like/{user_id}"
        )
        return response.status_code == 200
    except:
        return False

def unliker_activite(user_id, activite_id):
    """Unlike une activité"""
    try:
        response = requests.delete(
            f"{API_URL}/interactions/activites/{activite_id}/like/{user_id}"
        )
        return response.status_code == 200
    except:
        return False

def ajouter_commentaire(user_id, activite_id, contenu):
    """Ajoute un commentaire"""
    try:
        response = requests.post(
            f"{API_URL}/interactions/activites/{activite_id}/commentaires/{user_id}",
            json={"contenu": contenu}
        )
        return response.status_code == 201
    except:
        return False

def get_commentaires(activite_id):
    """Récupère les commentaires d'une activité"""
    try:
        response = requests.get(
            f"{API_URL}/interactions/activites/{activite_id}/commentaires"
        )
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

# ========== PAGES ==========

def page_connexion():
    """Page de connexion/inscription"""
    st.markdown('<p class="main-header">🏃 Application Sportive</p>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔐 Connexion", "📝 Inscription"])
    
    with tab1:
        st.subheader("Connexion")
        with st.form("login_form"):
            pseudo = st.text_input("Pseudo")
            mdp = st.text_input("Mot de passe", type="password")
            submit = st.form_submit_button("Se connecter")
            
            if submit:
                if pseudo and mdp:
                    success, message = login(pseudo, mdp)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.warning("Veuillez remplir tous les champs")
    
    with tab2:
        st.subheader("Inscription")
        with st.form("register_form"):
            col1, col2 = st.columns(2)
            with col1:
                nom = st.text_input("Nom")
                prenom = st.text_input("Prénom")
                age = st.number_input("Âge", min_value=13, max_value=120, value=25)
                pseudo = st.text_input("Pseudo (unique)")
            
            with col2:
                mail = st.text_input("Email")
                mdp = st.text_input("Mot de passe", type="password")
                taille = st.number_input("Taille (cm)", min_value=100, max_value=250, value=170)
                poids = st.number_input("Poids (kg)", min_value=30, max_value=200, value=70)
            
            submit = st.form_submit_button("S'inscrire")
            
            if submit:
                if all([nom, prenom, pseudo, mail, mdp]):
                    success, message = register(nom, prenom, age, pseudo, mail, mdp, taille, poids)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
                else:
                    st.warning("Veuillez remplir tous les champs obligatoires")

def page_dashboard():
    """Tableau de bord principal"""
    user = st.session_state.user
    user_id = st.session_state.user_id
    
    # Header
    col1, col2, col3 = st.columns([2, 3, 1])
    with col1:
        st.title(f"👋 Bonjour {user['prenom']} !")
    with col3:
        if st.button("🚪 Déconnexion"):
            logout()
            st.rerun()
    
    st.divider()
    
    # Récupérer les stats
    stats = get_statistiques_completes(user_id)
    
    if stats and 'tableau_bord' in stats:
        tb = stats['tableau_bord']
        
        # Métriques principales
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total activités",
                tb['activites']['total'],
                f"+{tb['activites']['7_derniers_jours']} (7j)"
            )
        
        with col2:
            st.metric(
                "Total heures",
                f"{tb['heures']['total']:.1f}h",
                f"+{tb['heures']['semaine_en_cours']:.1f}h (semaine)"
            )
        
        with col3:
            st.metric(
                "Total km",
                f"{tb['kilometres']['total']:.1f} km",
                f"+{tb['kilometres']['semaine']:.1f} km (semaine)"
            )
        
        with col4:
            st.metric(
                "Sport favori",
                tb.get('sport_favori', 'N/A'),
                f"{tb['jours_actif']} jours actif"
            )
        
        st.divider()
        
        # Graphiques
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Activités par semaine")
            if 'hebdomadaire' in stats:
                hebdo = stats['hebdomadaire']
                weeks = list(hebdo['activites_par_semaine'].keys())
                
                # Préparer les données pour le graphique
                data = []
                for week in weeks:
                    sports = hebdo['activites_par_semaine'][week]
                    for sport, count in sports.items():
                        data.append({
                            'Semaine': week,
                            'Sport': sport,
                            'Activités': count
                        })
                
                if data:
                    df = pd.DataFrame(data)
                    fig = px.bar(df, x='Semaine', y='Activités', color='Sport',
                                title="Nombre d'activités par semaine")
                    st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🎯 Répartition par sport")
            if 'par_sport' in stats:
                sports_data = stats['par_sport']['statistiques']
                sports = list(sports_data.keys())
                values = [sports_data[s]['nombre_activites'] for s in sports]
                
                fig = px.pie(names=sports, values=values, title="Activités par sport")
                st.plotly_chart(fig, use_container_width=True)

def page_activites():
    """Page des activités"""
    user_id = st.session_state.user_id
    
    st.title("📋 Mes Activités")
    
    # Onglets
    tab1, tab2, tab3 = st.tabs(["📝 Nouvelle activité", "📤 Upload GPX", "📊 Liste"])
    
    with tab1:
        st.subheader("Créer une activité manuellement")
        
        with st.form("create_activity"):
            col1, col2 = st.columns(2)
            
            with col1:
                nom = st.text_input("Nom de l'activité")
                type_sport = st.selectbox("Sport", 
                    ["Course", "Vélo", "Natation", "Marche", "Randonnée", "Autre"])
                date_activite = st.date_input("Date", value=date.today())
                duree = st.number_input("Durée (minutes)", min_value=1, value=60)
            
            with col2:
                distance = st.number_input("Distance (km)", min_value=0.0, value=0.0, step=0.1)
                d_plus = st.number_input("Dénivelé+ (m)", min_value=0, value=0)
                calories = st.number_input("Calories", min_value=0, value=0)
                description = st.text_area("Description")
            
            submit = st.form_submit_button("✅ Créer l'activité")
            
            if submit:
                if nom and type_sport:
                    success, result = creer_activite_manuelle(
                        user_id, nom, type_sport, date_activite, duree,
                        description, d_plus, calories, distance
                    )
                    if success:
                        st.success("✅ Activité créée avec succès !")
                        st.rerun()
                    else:
                        st.error(f"❌ Erreur : {result}")
                else:
                    st.warning("Veuillez remplir les champs obligatoires")
    
    with tab2:
        st.subheader("Upload fichier GPX")
        
        with st.form("upload_gpx"):
            nom = st.text_input("Nom de l'activité")
            type_sport = st.selectbox("Sport", 
                ["Course", "Vélo", "Natation", "Marche", "Randonnée"], key="gpx_sport")
            description = st.text_area("Description", key="gpx_desc")
            gpx_file = st.file_uploader("Fichier GPX", type=['gpx'])
            
            submit = st.form_submit_button("📤 Upload")
            
            if submit:
                if nom and type_sport and gpx_file:
                    success, result = upload_gpx(user_id, nom, type_sport, description, gpx_file)
                    if success:
                        st.success("✅ Activité créée depuis le GPX !")
                        st.json(result)
                        st.rerun()
                    else:
                        st.error(f"❌ Erreur : {result}")
                else:
                    st.warning("Veuillez remplir tous les champs")
    
    with tab3:
        st.subheader("Liste de mes activités")
        
        # Filtres
        col1, col2 = st.columns([1, 3])
        with col1:
            sport_filter = st.selectbox("Filtrer par sport", 
                ["Tous", "Course", "Vélo", "Natation", "Marche", "Randonnée"])
        
        # Récupérer les activités
        filter_sport = None if sport_filter == "Tous" else sport_filter
        activites = get_activites(user_id, type_sport=filter_sport)
        
        if activites:
            st.info(f"📊 {len(activites)} activité(s) trouvée(s)")
            
            for act in activites:
                with st.expander(f"{act['nom']} - {act['type_sport']} - {act['date_activite']}"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write("**Durée:**", f"{act.get('duree_activite', 0) // 60} min")
                        st.write("**Distance:**", f"{act.get('distance', 0):.2f} km")
                    
                    with col2:
                        st.write("**Dénivelé+:**", f"{act.get('d_plus', 0)} m")
                        st.write("**Calories:**", f"{act.get('calories', 0)} kcal")
                    
                    with col3:
                        if act.get('description'):
                            st.write("**Description:**", act['description'])
        else:
            st.info("Aucune activité pour le moment. Créez-en une !")

def page_fil():
    """Page du fil d'actualité"""
    user_id = st.session_state.user_id
    
    st.title("📰 Fil d'actualité")
    
    # Sélection période
    nb_jours = st.selectbox("Période", [7, 14, 30, 90], index=0)
    
    fil = get_fil_actualite(user_id, nb_jours=nb_jours)
    
    if fil:
        st.info(f"📊 {len(fil)} activité(s) dans votre fil")
        
        for item in fil:
            activite = item['activite']
            utilisateur = item['utilisateur']
            nb_likes = item['nb_likes']
            nb_commentaires = item['nb_commentaires']
            user_has_liked = item['user_has_liked']
            
            with st.container():
                st.markdown("---")
                
                # Header
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.subheader(f"🏃 {activite['nom']}")
                    st.caption(f"Par {utilisateur['pseudo']} • {activite['date_activite']}")
                
                # Infos activité
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Sport", activite['type_sport'])
                with col2:
                    st.metric("Durée", f"{activite.get('duree_activite', 0) // 60} min")
                with col3:
                    st.metric("Distance", f"{activite.get('distance', 0):.1f} km")
                with col4:
                    st.metric("D+", f"{activite.get('d_plus', 0)} m")
                
                # Interactions
                col1, col2, col3 = st.columns([1, 1, 4])
                
                with col1:
                    like_emoji = "❤️" if user_has_liked else "🤍"
                    if st.button(f"{like_emoji} {nb_likes}", key=f"like_{activite['id']}"):
                        if user_has_liked:
                            unliker_activite(user_id, activite['id'])
                        else:
                            liker_activite(user_id, activite['id'])
                        st.rerun()
                
                with col2:
                    if st.button(f"💬 {nb_commentaires}", key=f"comment_{activite['id']}"):
                        st.session_state[f"show_comments_{activite['id']}"] = True
                
                # Afficher les commentaires
                if st.session_state.get(f"show_comments_{activite['id']}", False):
                    commentaires = get_commentaires(activite['id'])
                    
                    st.write("**Commentaires:**")
                    for com in commentaires:
                        st.text(f"💬 {com['auteur']['pseudo']}: {com['contenu']}")
                    
                    # Ajouter un commentaire
                    with st.form(f"add_comment_{activite['id']}"):
                        contenu = st.text_input("Ajouter un commentaire")
                        if st.form_submit_button("Envoyer"):
                            if contenu:
                                ajouter_commentaire(user_id, activite['id'], contenu)
                                st.rerun()
    else:
        st.info("Votre fil est vide. Suivez des utilisateurs pour voir leurs activités !")

def page_statistiques():
    """Page des statistiques détaillées"""
    user_id = st.session_state.user_id
    
    st.title("📊 Statistiques détaillées")
    
    stats = get_statistiques_completes(user_id, sections="resume,hebdo,sports,records")
    
    if not stats:
        st.warning("Aucune donnée disponible")
        return
    
    # Résumé global
    if 'resume_global' in stats:
        st.subheader("📈 Résumé global")
        resume = stats['resume_global']
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total activités", resume['nombre_total_activites'])
        col2.metric("Total heures", f"{resume['duree_totale_heures']:.1f}h")
        col3.metric("Total km", f"{resume['distance_totale_km']:.1f} km")
        col4.metric("Total calories", f"{resume['calories_totales']:,}")
        
        st.divider()
    
    # Stats par sport
    if 'par_sport' in stats:
        st.subheader("🏅 Statistiques par sport")
        
        for sport, data in stats['par_sport']['statistiques'].items():
            with st.expander(f"{sport} - {data['nombre_activites']} activités"):
                col1, col2, col3 = st.columns(3)
                col1.metric("Heures totales", f"{data['duree_totale_heures']:.1f}h")
                col2.metric("Distance totale", f"{data['distance_totale_km']:.1f} km")
                col3.metric("Calories", f"{data['calories_totales']:,}")
    
    # Records
    if 'records' in stats:
        st.subheader("🏆 Records personnels")
        
        for sport, records in stats['records'].items():
            with st.expander(f"{sport}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write("**Durée maximale**")
                    st.write(f"{records['duree_maximale']['valeur']:.1f}h")
                    st.caption(records['duree_maximale']['activite'])
                
                with col2:
                    st.write("**Dénivelé maximal**")
                    st.write(f"{records['denivele_maximal']['valeur']} m")
                    st.caption(records['denivele_maximal']['activite'])
                
                with col3:
                    st.write("**Calories maximales**")
                    st.write(f"{records['calories_maximales']['valeur']}")
                    st.caption(records['calories_maximales']['activite'])

# ========== MAIN ==========

def main():
    init_session()
    
    if st.session_state.user is None:
        page_connexion()
    else:
        # Menu latéral
        with st.sidebar:
            st.image("https://img.icons8.com/color/96/000000/running.png", width=100)
            st.title("Navigation")
            
            page = st.radio("", [
                "🏠 Tableau de bord",
                "📋 Mes activités",
                "📰 Fil d'actualité",
                "📊 Statistiques"
            ])
            
            st.divider()
            st.caption(f"Connecté: {st.session_state.user['pseudo']}")
        
        # Afficher la page sélectionnée
        if "Tableau de bord" in page:
            page_dashboard()
        elif "Mes activités" in page:
            page_activites()
        elif "Fil d'actualité" in page:
            page_fil()
        elif "Statistiques" in page:
            page_statistiques()

if __name__ == "__main__":
    main()