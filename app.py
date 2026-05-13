import streamlit as st
import pandas as pd
from datetime import date

# --- Page Config ---
st.set_page_config(page_title="UniFind", page_icon="🔍", layout="centered")

# --- Custom CSS for Styling ---
st.markdown("""
    <style>
    .main { background-color: #f5f5f3; }
    .stButton>button { border-radius: 8px; }
    .stat-card {
        background: #f0f0ee;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
    }
    .badge {
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: bold;
    }
    .badge-lost { background: #FAECE7; color: #993C1D; }
    .badge-found { background: #E1F5EE; color: #0F6E56; }
    </style>
""", unsafe_allow_html=True)

# --- Initialize Session State (The "Database") ---
if 'items' not in st.session_state:
    st.session_state.items = [
        {'id':1,'type':'found','title':'Blue water bottle','category':'Accessories','location':'Cafeteria','date':'2025-05-10','desc':'Blue Nalgene bottle with stickers on it.','contact':'sara@uni.edu','contactName':'Sara'},
        {'id':2,'type':'found','title':'Airpods Pro case','category':'Electronics','location':'Library 2nd floor','date':'2025-05-11','desc':'White Airpods Pro case, no earbuds inside.','contact':'ali@uni.edu','contactName':'Ali'},
        {'id':3,'type':'lost','title':'Black wallet','category':'Accessories','location':'Parking lot B','date':'2025-05-09','desc':'Black leather wallet, has student ID inside.','contact':'tariq@uni.edu','contactName':'Tariq'},
        {'id':4,'type':'found','title':'Student ID card','category':'ID/Card','location':'Main gate','date':'2025-05-12','desc':'Student ID belonging to someone from CS dept.','contact':'guard@uni.edu','contactName':'Security desk'},
        {'id':5,'type':'lost','title':'Grey hoodie','category':'Clothing','location':'Gym changing room','date':'2025-05-08','desc':'Grey medium hoodie with university logo.','contact':'hamza@uni.edu','contactName':'Hamza'},
        {'id':6,'type':'found','title':'House keys','category':'Keys','location':'Block D corridor','date':'2025-05-12','desc':'A bunch of 3 keys on a red keychain.','contact':'office@uni.edu','contactName':'Admin office'},
    ]

# --- Helper: Render Item Card ---
def render_item_card(item):
    badge_class = "badge-lost" if item['type'] == 'lost' else "badge-found"
    with st.container(border=True):
        col1, col2 = st.columns([3, 1])
        col1.subheader(item['title'])
        col2.markdown(f'<span class="badge {badge_class}">{item["type"].upper()}</span>', unsafe_allow_html=True)
        
        st.caption(f"📍 {item['location']} | 📁 {item['category']} | 📅 {item['date']}")
        st.write(item['desc'])
        
        if st.button(f"Contact {item['contactName']}", key=f"btn_{item['id']}"):
            st.info(f"Contact: {item['contact']} (Message feature simulated)")

# --- Navigation ---
tabs = st.tabs(["🏠 Home", "🔍 Browse", "😞 Post Lost", "😊 Post Found"])

# --- TAB 1: HOME ---
with tabs[0]:
    st.title("🔍 UniFind")
    
    # Stats Row
    lost_count = len([i for i in st.session_state.items if i['type'] == 'lost'])
    found_count = len([i for i in st.session_state.items if i['type'] == 'found'])
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Lost Items", lost_count)
    c2.metric("Found Items", found_count)
    c3.metric("Total Posts", len(st.session_state.items))
    
    st.divider()
    
    col_l, col_r = st.columns(2)
    with col_l:
        st.subheader("Recent Lost Items")
        lost_items = [i for i in st.session_state.items if i['type'] == 'lost'][-2:]
        for item in reversed(lost_items):
            render_item_card(item)
            
    with col_r:
        st.subheader("Recent Found Items")
        found_items = [i for i in st.session_state.items if i['type'] == 'found'][-2:]
        for item in reversed(found_items):
            render_item_card(item)

# --- TAB 2: BROWSE ---
with tabs[1]:
    st.header("Browse All Items")
    
    s_col1, s_col2, s_col3 = st.columns([2, 1, 1])
    search_query = s_col1.text_input("Search items...", placeholder="e.g. Wallet")
    filter_type = s_col2.selectbox("Type", ["All", "lost", "found"])
    filter_cat = s_col3.selectbox("Category", ["All", "Electronics", "Clothing", "Accessories", "Books", "Keys", "ID/Card", "Bag", "Other"])
    
    filtered = st.session_state.items
    if search_query:
        filtered = [i for i in filtered if search_query.lower() in i['title'].lower() or search_query.lower() in i['desc'].lower()]
    if filter_type != "All":
        filtered = [i for i in filtered if i['type'] == filter_type]
    if filter_cat != "All":
        filtered = [i for i in filtered if i['category'] == filter_cat]
        
    if not filtered:
        st.warning("No items match your search.")
    else:
        for item in reversed(filtered):
            render_item_card(item)

# --- TAB 3: POST LOST ---
with tabs[2]:
    st.header("Report a Lost Item")
    with st.form("lost_form", clear_on_submit=True):
        l_name = st.text_input("Item Name *")
        l_cat = st.selectbox("Category *", ["Electronics", "Clothing", "Accessories", "Books", "Keys", "ID/Card", "Bag", "Other"])
        l_loc = st.text_input("Last seen location")
        l_date = st.date_input("Date lost", value=date.today())
        l_desc = st.text_area("Description")
        l_cname = st.text_input("Your Name")
        l_contact = st.text_input("Contact (Email/Phone)")
        
        # Matching Logic (Automatic check)
        matches = [i for i in st.session_state.items if i['type'] == 'found' and 
                  (l_name.lower() in i['title'].lower() if l_name else False or i['category'] == l_cat)]
        
        if l_name and matches:
            st.info(f"💡 We found {len(matches)} similar item(s) already reported as found! Check the Browse tab.")

        submitted = st.form_submit_button("Submit Lost Report")
        if submitted:
            if not l_name:
                st.error("Please enter an item name.")
            else:
                new_item = {
                    'id': len(st.session_state.items) + 1,
                    'type': 'lost', 'title': l_name, 'category': l_cat,
                    'location': l_loc, 'date': str(l_date), 'desc': l_desc,
                    'contact': l_contact, 'contactName': l_cname
                }
                st.session_state.items.append(new_item)
                st.success("Lost report submitted!")
                st.rerun()

# --- TAB 4: POST FOUND ---
with tabs[3]:
    st.header("Report a Found Item")
    with st.form("found_form", clear_on_submit=True):
        f_name = st.text_input("Item Name *")
        f_cat = st.selectbox("Category *", ["Electronics", "Clothing", "Accessories", "Books", "Keys", "ID/Card", "Bag", "Other"])
        f_loc = st.text_input("Found at location")
        f_date = st.date_input("Date found", value=date.today())
        f_desc = st.text_area("Description")
        f_cname = st.text_input("Your Name")
        f_contact = st.text_input("Contact (Email/Phone)")
        
        submitted = st.form_submit_button("Submit Found Report")
        if submitted:
            if not f_name:
                st.error("Please enter an item name.")
            else:
                new_item = {
                    'id': len(st.session_state.items) + 1,
                    'type': 'found', 'title': f_name, 'category': f_cat,
                    'location': f_loc, 'date': str(f_date), 'desc': f_desc,
                    'contact': f_contact, 'contactName': f_cname
                }
                st.session_state.items.append(new_item)
                st.success("Found report submitted!")
                st.rerun()