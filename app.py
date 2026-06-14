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

# 2. UI POLISH (MODERN OPTIMIZED THEME)
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #f8f9fa;
    }
    
    .block-container { 
        padding-top: 1.5rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    
    /* Headers */
    h1 {
        color: #ffffff;
        font-weight: 700 !important;
        font-size: 2.8rem !important;
        margin-bottom: 0.5rem !important;
        letter-spacing: -0.5px;
    }
    
    h2 {
        color: #ffffff;
        font-weight: 600 !important;
        font-size: 1.8rem !important;
        margin-top: 1.5rem !important;
        margin-bottom: 1rem !important;
    }
    
    h3 { 
        color: #e8eef7;
        font-weight: 600 !important;
        font-size: 1.3rem !important;
    }
    
    /* Subtitles and captions */
    .stMarkdown > p {
        font-size: 1rem;
        line-height: 1.6;
        color: #e8eef7;
    }
    
    .stCaption {
        color: #b0bae8 !important;
        font-size: 0.95rem !important;
    }
    
    /* METRICS CARDS */
    .metric-container {
        background: rgba(255, 255, 255, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.25);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .metric-container:hover {
        background: rgba(255, 255, 255, 0.18);
        border-color: rgba(255, 255, 255, 0.35);
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
    }
    
    .metric-label {
        color: #b0bae8;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    
    .metric-value {
        color: #ffffff;
        font-size: 2rem;
        font-weight: 700;
        font-family: 'Courier New', monospace;
    }
    
    .metric-icon {
        font-size: 1.8rem;
        margin-bottom: 8px;
        color: #a0d8ff;
    }
    
    /* TABS */
    .stTabs [data-baseweb="tab-list"] { 
        gap: 8px;
        border: none;
        background: rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        padding: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: #b0bae8;
        border-radius: 8px;
        border: none;
        font-weight: 600;
        padding: 12px 20px;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(255, 255, 255, 0.08);
        color: #ffffff;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: rgba(255, 255, 255, 0.2);
        color: #ffffff;
        border-color: transparent;
        box-shadow: none;
    }
    
    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.03) 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.15);
    }
    
    section[data-testid="stSidebar"] h1 { 
        color: #ffffff !important;
        font-size: 1.6rem !important;
        font-weight: 700;
    }
    
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] label {
        color: #e8eef7 !important;
        font-weight: 500;
    }
    
    /* INPUT CONTROLS */
    .stSlider > div > div > div > div,
    .stRadio > div > div,
    .stMultiSelect > div > div {
        color: #ffffff;
    }
    
    .stSlider [data-testid="stSliderTickBarMin"],
    .stSlider [data-testid="stSliderTickBarMax"] {
        color: #b0bae8 !important;
    }
    
    /* BUTTONS */
    .stButton > button {
        background-color: rgba(255, 255, 255, 0.15);
        color: #ffffff;
        border: 1px solid rgba(255, 255, 255, 0.25);
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: rgba(255, 255, 255, 0.25);
        border-color: rgba(255, 255, 255, 0.4);
        transform: translateY(-2px);
    }
    
    /* STATUS ALERTS */
    .status-alert {
        padding: 16px;
        border-radius: 10px;
        margin: 12px 0;
        font-weight: 500;
        border-left: 4px solid;
        backdrop-filter: blur(10px);
    }
    
    .status-success {
        background-color: rgba(34, 197, 94, 0.15);
        border-left-color: #22c55e;
        color: #86efac;
    }
    
    .status-warning {
        background-color: rgba(251, 146, 60, 0.15);
        border-left-color: #fb923c;
        color: #fed7aa;
    }
    
    .status-error {
        background-color: rgba(239, 68, 68, 0.15);
        border-left-color: #ef4444;
        color: #fca5a5;
    }
    
    /* GANG/COMMUNITY CARDS */
    .gang-card {
        background: rgba(255, 255, 255, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .gang-card:hover {
        background: rgba(255, 255, 255, 0.18);
        border-color: rgba(255, 255, 255, 0.3);
        transform: translateY(-4px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }
    
    .gang-title {
        color: #ffffff;
        font-weight: 700;
        font-size: 1.2rem;
        margin-bottom: 8px;
    }
    
    .gang-members {
        color: #b0bae8;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    
    /* DATA TABLE */
    .stDataFrame {
        background: rgba(255, 255, 255, 0.08) !important;
    }
    
    .stDataFrame [data-testid="dataframe"] {
        color: #ffffff;
    }
    
    /* DIVIDER */
    hr {
        border-top: 1px solid rgba(255, 255, 255, 0.15) !important;
        margin: 2rem 0 !important;
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