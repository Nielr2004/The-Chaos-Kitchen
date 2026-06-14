import streamlit as st
import pandas as pd
import networkx as nx
from networkx.algorithms import community
from pyvis.network import Network
import streamlit.components.v1 as components
import itertools
from collections import Counter
import random
import plotly.graph_objects as go

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="The Chaos Kitchen", page_icon="⚗️", layout="wide")

# 2. UI POLISH (UNIQUE HIGH-IMPACT DESIGN)
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    /* Bold Neon Background */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1a3e 50%, #2d0a4e 100%);
        background-attachment: fixed;
        color: #f8f9fa;
    }
    
    .block-container { 
        padding-top: 2rem;
        padding-left: 2.5rem;
        padding-right: 2.5rem;
        max-width: 1400px;
    }
    
    /* Bold Headers with Glow */
    h1 {
        background: linear-gradient(120deg, #ff006e, #8338ec, #3a86ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 900 !important;
        font-size: 3.5rem !important;
        margin-bottom: 0.5rem !important;
        letter-spacing: -1px;
        text-shadow: 0 0 30px rgba(255, 0, 110, 0.3);
    }
    
    h2 {
        color: #3a86ff;
        font-weight: 700 !important;
        font-size: 2rem !important;
        margin-top: 2rem !important;
        margin-bottom: 1.5rem !important;
        border-left: 4px solid #ff006e;
        padding-left: 15px;
    }
    
    h3 { 
        color: #ff006e;
        font-weight: 700 !important;
        font-size: 1.4rem !important;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    h4 {
        color: #8338ec;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }
    
    /* Subtitles */
    .stMarkdown > p {
        font-size: 1.05rem;
        line-height: 1.7;
        color: #b0b9ff;
    }
    
    .stCaption {
        color: #a0aeff !important;
        font-size: 0.95rem !important;
        font-style: italic;
    }
    
    /* NEON METRICS CARDS */
    .metric-container {
        background: linear-gradient(135deg, rgba(255, 0, 110, 0.1), rgba(58, 134, 255, 0.1));
        border: 2px solid rgba(255, 0, 110, 0.4);
        border-radius: 16px;
        padding: 25px;
        text-align: center;
        backdrop-filter: blur(15px);
        transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
        box-shadow: 0 8px 32px rgba(255, 0, 110, 0.15);
        position: relative;
        overflow: hidden;
    }
    
    .metric-container::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255, 0, 110, 0.15), transparent);
        animation: pulse-glow 4s ease-in-out infinite;
    }
    
    @keyframes pulse-glow {
        0%, 100% { transform: translate(0, 0); opacity: 0.5; }
        50% { transform: translate(10px, 10px); opacity: 1; }
    }
    
    .metric-container:hover {
        background: linear-gradient(135deg, rgba(255, 0, 110, 0.2), rgba(58, 134, 255, 0.2));
        border-color: rgba(255, 0, 110, 0.8);
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 12px 48px rgba(255, 0, 110, 0.3);
    }
    
    .metric-label {
        color: #b0b9ff;
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 12px;
        position: relative;
        z-index: 1;
    }
    
    .metric-value {
        color: #ffffff;
        font-size: 2.5rem;
        font-weight: 900;
        font-family: 'Courier New', monospace;
        background: linear-gradient(120deg, #ff006e, #3a86ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        position: relative;
        z-index: 1;
    }
    
    .metric-icon {
        font-size: 2.2rem;
        margin-bottom: 10px;
        background: linear-gradient(120deg, #ff006e, #8338ec);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: float 3s ease-in-out infinite;
        position: relative;
        z-index: 1;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    /* TABS */
    .stTabs [data-baseweb="tab-list"] { 
        gap: 12px;
        border: none;
        background: rgba(255, 0, 110, 0.05);
        border-radius: 12px;
        padding: 8px;
        border: 1px solid rgba(255, 0, 110, 0.2);
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: #a0aeff;
        border-radius: 10px;
        border: 1px solid transparent;
        font-weight: 700;
        padding: 12px 24px;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.95rem;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(255, 0, 110, 0.1);
        color: #ff006e;
        border-color: rgba(255, 0, 110, 0.4);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(255, 0, 110, 0.2), rgba(58, 134, 255, 0.2));
        color: #ff006e;
        border-color: rgba(255, 0, 110, 0.6);
        box-shadow: 0 0 20px rgba(255, 0, 110, 0.2);
    }
    
    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(51, 30, 80, 0.6) 0%, rgba(26, 26, 62, 0.8) 100%);
        border-right: 2px solid rgba(255, 0, 110, 0.3);
    }
    
    section[data-testid="stSidebar"] h1 { 
        color: #ff006e !important;
        font-size: 1.7rem !important;
        font-weight: 900;
        text-transform: uppercase;
    }
    
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] label {
        color: #b0b9ff !important;
        font-weight: 600;
    }
    
    /* INPUTS */
    .stSlider > div > div > div > div,
    .stRadio > div > div,
    .stMultiSelect > div > div {
        color: #b0b9ff;
    }
    
    /* BUTTONS */
    .stButton > button {
        background: linear-gradient(135deg, rgba(255, 0, 110, 0.2), rgba(58, 134, 255, 0.2));
        color: #ff006e;
        border: 2px solid rgba(255, 0, 110, 0.5);
        border-radius: 10px;
        font-weight: 700;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, rgba(255, 0, 110, 0.3), rgba(58, 134, 255, 0.3));
        border-color: rgba(255, 0, 110, 0.8);
        transform: translateY(-4px);
        box-shadow: 0 8px 20px rgba(255, 0, 110, 0.3);
    }
    
    /* STATUS ALERTS */
    .status-alert {
        padding: 20px;
        border-radius: 12px;
        margin: 16px 0;
        font-weight: 600;
        border-left: 5px solid;
        backdrop-filter: blur(15px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
        font-size: 1.05rem;
    }
    
    .status-success {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.2), rgba(34, 197, 94, 0.05));
        border-left-color: #22c55e;
        color: #4ade80;
    }
    
    .status-warning {
        background: linear-gradient(135deg, rgba(251, 146, 60, 0.2), rgba(251, 146, 60, 0.05));
        border-left-color: #fb923c;
        color: #fdba74;
    }
    
    .status-error {
        background: linear-gradient(135deg, rgba(255, 0, 110, 0.2), rgba(255, 0, 110, 0.05));
        border-left-color: #ff006e;
        color: #ff4081;
    }
    
    /* GANG/COMMUNITY CARDS */
    .gang-card {
        background: linear-gradient(135deg, rgba(255, 0, 110, 0.12), rgba(58, 134, 255, 0.12));
        border: 2px solid rgba(255, 0, 110, 0.3);
        border-radius: 14px;
        padding: 22px;
        margin-bottom: 18px;
        backdrop-filter: blur(15px);
        transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
        box-shadow: 0 8px 32px rgba(255, 0, 110, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .gang-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        transition: left 0.5s ease;
    }
    
    .gang-card:hover::before {
        left: 100%;
    }
    
    .gang-card:hover {
        background: linear-gradient(135deg, rgba(255, 0, 110, 0.2), rgba(58, 134, 255, 0.2));
        border-color: rgba(255, 0, 110, 0.6);
        transform: translateY(-6px);
        box-shadow: 0 12px 48px rgba(255, 0, 110, 0.2);
    }
    
    .gang-title {
        color: #ff006e;
        font-weight: 900;
        font-size: 1.3rem;
        margin-bottom: 10px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .gang-members {
        color: #a0aeff;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    /* DATA TABLE */
    .stDataFrame {
        background: rgba(26, 26, 62, 0.6) !important;
    }
    
    /* DIVIDER */
    hr {
        border-top: 2px solid rgba(255, 0, 110, 0.3) !important;
        margin: 2.5rem 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. DATA ENGINE
@st.cache_data
def load_data(limit=300, diet="All"):
    try:
        ingredients_pool = {
            "Italian": ["Tomato", "Basil", "Mozzarella", "Pasta", "Garlic", "Olive Oil", "Oregano", "Parmesan", "Pancetta"],
            "Mexican": ["Corn", "Beans", "Avocado", "Chili", "Lime", "Cilantro", "Tortilla", "Cumin", "Salsa", "Chicken"],
            "Asian": ["Soy Sauce", "Ginger", "Rice", "Sesame Oil", "Scallions", "Tofu", "Garlic", "Chili", "Miso", "Shrimp"],
            "American": ["Beef", "Cheese", "Potato", "Butter", "Bread", "Milk", "Bacon", "Onion", "BBQ Sauce", "Steak"],
            "Indian": ["Garam Masala", "Turmeric", "Paneer", "Lentils", "Ghee", "Ginger", "Cumin", "Chili", "Yogurt", "Spinach"],
            "Chaos": ["Chocolate", "Pickles", "Peanut Butter", "Kimchi", "Honey", "Coffee", "Vanilla", "Mint"]
        }
        
        # Helper to map ingredient back to likely cuisine for auto-naming
        ing_to_cuisine = {}
        for cuisine, items in ingredients_pool.items():
            for item in items:
                ing_to_cuisine[item] = cuisine

        flavor_db = {
            "Chili": [5, 10, 0, 2, 3], "Garlic": [8, 4, 0, 0, 1], "Lime": [2, 0, 3, 5, 0],
            "Chocolate": [1, 0, 10, 8, 2], "Pickles": [4, 2, 1, 10, 8], "Honey": [0, 0, 10, 2, 0],
            "Soy Sauce": [10, 0, 2, 1, 0], "Bacon": [10, 0, 3, 1, 9], "Cheese": [8, 0, 1, 2, 4],
            "Tomato": [6, 0, 4, 0, 2], "Beef": [10, 0, 0, 0, 6], "Chicken": [8, 0, 0, 0, 5],
            "Corn": [3, 0, 6, 0, 7], "Mint": [0, 2, 2, 8, 0], "Peanut Butter": [6, 0, 7, 5, 1]
        }
        
        non_veg = ["Beef", "Bacon", "Chicken", "Pancetta", "Shrimp", "Steak", "Pork"]
        
        data = []
        cuisine_list = list(ingredients_pool.keys())
        
        for i in range(limit):
            cuisine = random.choice(cuisine_list)
            base = random.sample(ingredients_pool[cuisine], k=random.randint(3, 5))
            
            if random.random() < 0.3:
                chaos_ing = random.choice(ingredients_pool["Chaos"])
                if chaos_ing not in base:
                    base.append(chaos_ing)
            
            is_veg = not any(i in non_veg for i in base)
            if diet == "Vegetarian" and not is_veg: continue
            
            data.append({"ingredients": base, "cuisine": cuisine})
            
        return data, flavor_db, ing_to_cuisine
    except Exception: return [], {}, {}

# Helper Function for Custom Metrics
def display_pop_metric(label, icon, value):
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-icon">{icon}</div>
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)

# Sidebar
st.sidebar.title("⚙️ Controls")
st.sidebar.caption("Adjust the Chaos Matrix")
limit = st.sidebar.slider("Dataset Size", 50, 600, 250)
diet_mode = st.sidebar.radio("Diet Mode", ["All", "Vegetarian"])

# Load Data
recipes, flavor_db, ing_to_cuisine = load_data(limit, diet_mode)

# 4. GRAPH LOGIC
G = nx.Graph()
for r in recipes:
    for u, v in itertools.combinations(r['ingredients'], 2):
        if G.has_edge(u, v): 
            G[u][v]['weight'] = G[u][v].get('weight', 0) + 1
        else: 
            G.add_edge(u, v, weight=1)

threshold = 2 if len(recipes) > 100 else 1
G.remove_edges_from([(u, v) for u, v, d in G.edges(data=True) if d.get('weight', 0) < threshold])
G.remove_nodes_from([n for n, d in G.degree() if d == 0])

try:
    communities = list(community.greedy_modularity_communities(G))
except:
    communities = []

colors = ["#FF00CC", "#00FFFF", "#FFFF00", "#00FF00", "#FF4500", "#9900FF"]
node_colors = {}
node_group = {}

# --- SMART GANG NAMING ---
community_names = {}
for i, comm in enumerate(communities):
    c = colors[i % len(colors)]
    
    # Analyze dominant cuisine in this cluster
    cuisines_in_cluster = [ing_to_cuisine.get(node, "Unknown") for node in comm]
    most_common = Counter(cuisines_in_cluster).most_common(1)
    
    if most_common:
        dominant_cuisine = most_common[0][0]
        if dominant_cuisine == "Chaos": gang_label = "The Weirdos"
        elif dominant_cuisine == "Italian": gang_label = "The Mob"
        elif dominant_cuisine == "Mexican": gang_label = "Cartel"
        elif dominant_cuisine == "Asian": gang_label = "The Dynasty"
        elif dominant_cuisine == "American": gang_label = "Freedom Fighters"
        elif dominant_cuisine == "Indian": gang_label = "Spice Squad"
        else: gang_label = f"Gang #{i+1}"
    else:
        gang_label = f"Gang #{i+1}"
        
    community_names[i] = gang_label

    for node in comm:
        node_colors[node] = c
        node_group[node] = gang_label
        G.nodes[node]['color'] = c
        G.nodes[node]['size'] = 15 + (G.degree[node] * 2)
        G.nodes[node]['title'] = f"{node} | {gang_label}"
        G.nodes[node]['label'] = node

# 5. MAIN DASHBOARD
c1, c2 = st.columns([3, 1])
with c1:
    st.markdown("# <i class='fas fa-flask-vial'></i> The Chaos Kitchen", unsafe_allow_html=True)
    st.markdown("*Where algorithms cook dinner and the rules don't matter.*")

# --- CUSTOM METRICS SECTION ---
m1, m2, m3, m4 = st.columns(4)
with m1: display_pop_metric("Recipes Analyzed", '<i class="fas fa-utensils"></i>', len(recipes))
with m2: display_pop_metric("Ingredients", '<i class="fas fa-leaf"></i>', len(G.nodes))
with m3: display_pop_metric("Flavor Gangs", '<i class="fas fa-users"></i>', len(communities))
with m4: display_pop_metric("Chaos Level", '<i class="fas fa-fire"></i>', f"{random.randint(80, 100)}%")

st.write("")

# TABS
tab_net, tab_judge, tab_insight = st.tabs(["Network", "Judge", "Insights"])

with tab_net:
    st.markdown("### <i class='fas fa-network-wired'></i> Ingredient Network", unsafe_allow_html=True)
    st.caption("Ingredients that appear in recipes together are connected. Colors represent communities.")
    
    net = Network(height="600px", width="100%", bgcolor="#111", font_color="white", cdn_resources='in_line')
    net.from_nx(G)
    # Refined Physics: Improved stabilization
    net.force_atlas_2based(gravity=-80, central_gravity=0.005, spring_length=120, spring_strength=0.08, damping=0.4)
    
    try:
        html = net.generate_html()
        components.html(html, height=620)
    except Exception as e:
        st.error(f"Graph Error: {e}")

with tab_judge:
    st.markdown("### <i class='fas fa-scale-balanced'></i> Judgment Day", unsafe_allow_html=True)
    st.write("Select ingredients to create a dish. The AI will rate your sanity.")
    
    col_in, col_out = st.columns(2)
    with col_in:
        my_ings = st.multiselect("Your Basket:", sorted(list(G.nodes)), max_selections=5)
    
    with col_out:
        if my_ings:
            weird_score = sum([20 for i in my_ings if i in ["Chocolate", "Pickles", "Kimchi", "Mint", "Coffee"]])
            
            connected = True
            if len(my_ings) > 1:
                try:
                    if not nx.has_path(G, my_ings[0], my_ings[1]): connected = False
                except: connected = False

            # Verdict Visuals
            st.markdown("#### <i class='fas fa-file-lines'></i> Verdict", unsafe_allow_html=True)
            if weird_score > 30:
                st.markdown(f'<div class="status-alert status-error"><i class="fas fa-skull-crossbones"></i> CRIMINAL OFFENSE<br><span style="font-size:14px;">The food police have been dispatched.</span></div>', unsafe_allow_html=True)
            elif not connected:
                st.markdown(f'<div class="status-alert status-warning"><i class="fas fa-triangle-exclamation"></i> SUSPICIOUS<br><span style="font-size:14px;">These ingredients have absolutely no chemistry.</span></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="status-alert status-success"><i class="fas fa-check-circle"></i> SURPRISINGLY LEGAL<br><span style="font-size:14px;">The algorithms allow this. Proceed.</span></div>', unsafe_allow_html=True)

            # Radar Chart
            st.markdown("#### <i class='fas fa-dna'></i> Flavor DNA", unsafe_allow_html=True)
            profile = [0, 0, 0, 0, 0]
            c = 0
            for i in my_ings:
                p = flavor_db.get(i, [3, 1, 1, 1, 1]) 
                profile = [x+y for x,y in zip(profile, p)]
                c += 1
            
            if c > 0:
                profile = [x/c for x in profile]
                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(
                    r=profile, 
                    theta=['Savory', 'Spicy', 'Sweet', 'Weird', 'Crunch'], 
                    fill='toself',
                    line_color='#FF00CC', 
                    fillcolor='rgba(255, 0, 204, 0.3)'
                ))
                fig.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 10]), bgcolor='#fff'),
                    showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='black', family="Courier New", size=14),
                    margin=dict(l=40, r=40, t=20, b=20)
                )
                st.plotly_chart(fig, use_container_width=True)

with tab_insight:
    st.markdown("### <i class='fas fa-users'></i> The Flavor Gangs", unsafe_allow_html=True)
    st.caption("The AI has mathematically identified these culinary cliques.")
    
    cols = st.columns(3)
    if communities:
        for i, comm in enumerate(communities[:6]):
            col = cols[i % 3]
            with col:
                # Use the Smart Name
                gang_name = community_names.get(i, f"Gang #{i+1}")
                members = list(comm)[:5]
                color = colors[i % len(colors)]
                
                st.markdown(f"""
                <div class="gang-card">
                    <div class="gang-title"><i class="fas fa-circle" style="color: {color}; margin-right: 8px;"></i>{gang_name}</div>
                    <div class="gang-members">{', '.join(members)}</div>
                </div>
                """, unsafe_allow_html=True)
            
    st.markdown("---")
    st.markdown("### <i class='fas fa-handshake'></i> Strongest Friendships", unsafe_allow_html=True)
    
    edge_data = []
    for u, v, data in G.edges(data=True):
        weight = data.get('weight', 1) 
        edge_data.append({"Ingredient A": u, "Ingredient B": v, "Bond Strength": weight})
    
    if edge_data:
        df = pd.DataFrame(edge_data).sort_values("Bond Strength", ascending=False).head(5)
        st.table(df)