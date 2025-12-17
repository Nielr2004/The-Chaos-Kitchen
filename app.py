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
st.set_page_config(page_title="The Chaos Kitchen", page_icon="🤪", layout="wide")

# 2. UI POLISH (REFINED POP ART THEME)
st.markdown("""
<style>
    /* 1. Main Background: Funky Purple Gradient */
    .stApp {
        background: linear-gradient(135deg, #8E2DE2 0%, #4A00E0 100%);
        color: #fff;
    }
    
    .block-container { padding-top: 2rem; }
    
    /* 2. Headers: Comic Style */
    h1 {
        font-family: 'Comic Sans MS', 'Chalkboard SE', sans-serif !important; 
        color: #FFD700;
        text-shadow: 4px 4px 0px #000000;
        transform: rotate(-1deg);
        font-weight: 900 !important;
        font-size: 3.5rem !important;
    }
    h3 { color: #fff; text-shadow: 2px 2px 0px #000; }
    
    /* 3. CUSTOM METRIC CSS */
    .pop-metric-container {
        text-align: center;
        margin-bottom: 20px;
    }
    .pop-metric-label {
        color: #000000;
        font-family: 'Arial Black', sans-serif;
        font-weight: 900;
        font-size: 14px;
        text-transform: uppercase;
        margin-bottom: 5px;
        text-shadow: 1px 1px 0px #fff; 
        letter-spacing: 1px;
    }
    .pop-metric-box {
        background-color: #FFFFFF;
        border: 3px solid #000000;
        box-shadow: 6px 6px 0px #000000;
        border-radius: 12px;
        padding: 15px;
        font-family: 'Courier New', monospace;
        font-weight: 900;
        font-size: 28px; /* Adjusted for better fit */
        color: #000000;
        transition: transform 0.2s;
    }
    .pop-metric-box:hover {
        transform: translate(-3px, -3px);
        box-shadow: 9px 9px 0px #000000;
        background-color: #FFD700;
    }
    
    /* 4. TABS */
    .stTabs [data-baseweb="tab-list"] { gap: 15px; border: none; }
    .stTabs [data-baseweb="tab"] {
        background-color: #222;
        color: #fff;
        border-radius: 8px;
        border: 2px solid #fff;
        font-weight: bold;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FF4B4B;
        color: #fff;
        border-color: #000;
        box-shadow: 4px 4px 0px #000;
        transform: translateY(-2px);
    }
    
    /* 5. SIDEBAR */
    section[data-testid="stSidebar"] {
        background-color: #FFD700;
        border-right: 5px solid #000;
    }
    section[data-testid="stSidebar"] h1 { color: #000 !important; text-shadow: none; }
    section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] label {
        color: #000 !important;
        font-weight: 800;
    }
    
    /* Alert Box */
    .pop-alert {
        padding: 15px;
        border: 3px solid black;
        border-radius: 10px;
        margin-bottom: 10px;
        font-weight: bold;
        color: black;
        box-shadow: 4px 4px 0px rgba(0,0,0,0.5);
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
def display_pop_metric(label, value):
    st.markdown(f"""
    <div class="pop-metric-container">
        <div class="pop-metric-label">{label}</div>
        <div class="pop-metric-box">{value}</div>
    </div>
    """, unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🎛️ Controls")
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
    st.title("The Chaos Kitchen 🌪️")
    st.markdown("**Where algorithms cook dinner and the rules don't matter.**")

# --- CUSTOM METRICS SECTION ---
m1, m2, m3, m4 = st.columns(4)
with m1: display_pop_metric("Recipes Analyzed", len(recipes))
with m2: display_pop_metric("Ingredients", len(G.nodes))
with m3: display_pop_metric("Flavor Gangs", len(communities))
with m4: display_pop_metric("Chaos Level", f"{random.randint(80, 100)}%")

st.write("")

# TABS
tab_net, tab_judge, tab_insight = st.tabs(["🕸️ The Blob", "⚖️ AI Judge", "🧠 The Why"])

with tab_net:
    st.markdown("### 🕸️ Ingredient Network")
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
    st.markdown("### ⚖️ Judgement Day")
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
            st.markdown("#### 📝 Verdict:")
            if weird_score > 30:
                st.markdown(f'<div class="pop-alert" style="background-color:#FF4B4B;">🤮 CRIMINAL OFFENSE<br><span style="font-weight:normal; font-size:14px;">The food police have been dispatched.</span></div>', unsafe_allow_html=True)
            elif not connected:
                st.markdown(f'<div class="pop-alert" style="background-color:#FFD700;">🤨 SUSPICIOUS<br><span style="font-weight:normal; font-size:14px;">These ingredients have absolutely no chemistry.</span></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="pop-alert" style="background-color:#00FF00;">👨‍🍳 SURPRISINGLY LEGAL<br><span style="font-weight:normal; font-size:14px;">The algorithms allow this. Proceed.</span></div>', unsafe_allow_html=True)

            # Radar Chart
            st.markdown("#### 🧬 Flavor DNA")
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
    st.markdown("### 🧠 The Flavor Gangs")
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
                <div style="background-color: {color}; padding: 15px; border: 3px solid black; border-radius: 10px; margin-bottom: 15px; box-shadow: 4px 4px 0px #000;">
                    <h3 style="margin:0; color:black; text-shadow:none;">{gang_name}</h3>
                    <p style="margin:0; color:black; font-weight:bold;">{', '.join(members)}</p>
                </div>
                """, unsafe_allow_html=True)
            
    st.markdown("---")
    st.markdown("### 🤝 Strongest Friendships")
    
    edge_data = []
    for u, v, data in G.edges(data=True):
        weight = data.get('weight', 1) 
        edge_data.append({"Ingredient A": u, "Ingredient B": v, "Bond Strength": weight})
    
    if edge_data:
        df = pd.DataFrame(edge_data).sort_values("Bond Strength", ascending=False).head(5)
        st.table(df)