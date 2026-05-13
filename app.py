import streamlit as st
import pandas as pd
from datetime import date

# --- Page Config ---
st.set_page_config(page_title="UniFind", page_icon="🔍")

# --- CSS (Waisa hi look jaisa aapka original tha) ---
st.markdown("""
<style>
    .stApp { background-color: #f5f5f3; }
    .badge { padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 500; }
    .badge-lost { background: #FAECE7; color: #993C1D; }
    .badge-found { background: #E1F5EE; color: #0F6E56; }
    div[data-testid="stMetricValue"] { font-size: 24px; }
</style>
""", unsafe_allow_html=True)

# --- Database Initialization (Fix for the error) ---
if 'items' not in st.session_state:
    st.session_state.items = [
        {'id':1,'type':'found','title':'Blue water bottle','category':'Accessories','location':'Cafeteria','date':'2025-05-10','desc':'Blue Nalgene bottle with stickers.','contact':'sara@uni.edu','contactName':'Sara'},
        {'id':2,'type':'found','title':'Airpods Pro case','category':'Electronics','location':'Library','date':'2025-05-11','desc':'White case.','contact':'ali@uni.edu','contactName':'Ali'},
        {'id':3,'type':'lost','title':'Black wallet','category':'Accessories','location':'Parking lot B','date':'2025-05-09','desc':'Leather wallet with ID.','contact':'tariq@uni.edu','contactName':'Tariq'},
        {'id':4,'type':'found','title':'Student ID card','category':'ID/Card','location':'Main gate','date':'2025-05-12','desc':'CS dept ID.','contact':'guard@uni.edu','contactName':'Security'},
        {'id':5,'type':'lost','title':'Grey hoodie','category':'Clothing','location':'Gym','date':'2025-05-08','desc':'University logo.','contact':'hamza@uni.edu','contactName':'Hamza'},
        {'id':6,'type':'found','title':'House keys','category':'Keys','location':'Block D','date':'2025-05-12','desc':'Red keychain.','contact':'office@uni.edu','contactName':'Admin'}
    ]

# --- Functions ---
def render_card(item):
    badge_style = "badge-lost" if item['type'] == 'lost' else "badge-found"
    with st.container(border=True):
        col1, col2 = st.columns([3, 1])
        col1.markdown(f"**{item['title']}**")
        col2.markdown(f'<span class="badge {badge_style}">{item["type"].capitalize()}</span>', unsafe_allow_html=True)
        st.caption(f"📍 {item['location']} | 🏷️ {item['category']} | 📅 {item['date']}")
        st.write(item['desc'])
        if st.button(f"Contact {item['contactName']}", key=f"btn_{item['id']}"):
            st.success(f"Contact details: {item['contact']}")

# --- UI Layout ---
tab_home, tab_browse, tab_lost, tab_found = st.tabs(["🏠 Home", "🔎 Browse", "😞 Lost", "😊 Found"])

# --- TAB: HOME ---
with tab_home:
    st.title("🔍 UniFind")
    # Stats Row (Yahan error aa raha tha, ab fixed hai)
    l_count = len([i for i in st.session_state.items if i['type'] == 'lost'])
    f_count = len([i for i in st.session_state.items if i['type'] == 'found'])
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Lost Items", l_count)
    c2.metric("Found Items", f_count)
    c3.metric("Total Items", len(st.session_state.items))
    
    st.markdown("### Recent Items")
    for item in reversed(st.session_state.items[-4:]):
        render_card(item)

# --- TAB: BROWSE ---
with tab_browse:
    st.subheader("Browse Items")
    q = st.text_input("Search items...", placeholder="Search by name or location")
    col_f1, col_f2 = st.columns(2)
    t_filter = col_f1.selectbox("Filter Type", ["All", "lost", "found"])
    c_filter = col_f2.selectbox("Filter Category", ["All", "Electronics", "Clothing", "Accessories", "Books", "Keys", "ID/Card", "Bag", "Other"])
    
    filtered = st.session_state.items
    if q: filtered = [i for i in filtered if q.lower() in i['title'].lower() or q.lower() in i['desc'].lower()]
    if t_filter != "All": filtered = [i for i in filtered if i['type'] == t_filter]
    if c_filter != "All": filtered = [i for i in filtered if i['category'] == c_filter]
    
    for item in reversed(filtered):
        render_card(item)

# --- TAB: POST LOST ---
with tab_lost:
    st.subheader("Report Lost Item")
    with st.form("lost_form", clear_on_submit=True):
        name = st.text_input("Item Name *")
        cat = st.selectbox("Category *", ["Electronics", "Clothing", "Accessories", "Books", "Keys", "ID/Card", "Bag", "Other"])
        loc = st.text_input("Last Seen Location")
        dt = st.date_input("Date Lost")
        desc = st.text_area("Description")
        cname = st.text_input("Your Name")
        cont = st.text_input("Contact Info")
        
        # Live matching logic (Similar to your bulb panel)
        matches = [i for i in st.session_state.items if i['type'] == 'found' and (name.lower() in i['title'].lower() if name else False)]
        if matches:
            st.info(f"💡 We found {len(matches)} matching found items! Check the Browse tab.")
            
        if st.form_submit_button("Submit"):
            if name and cat:
                st.session_state.items.append({'id': len(st.session_state.items)+1, 'type':'lost', 'title':name, 'category':cat, 'location':loc, 'date':str(dt), 'desc':desc, 'contact':cont, 'contactName':cname})
                st.success("Posted!")
                st.rerun()

# --- TAB: POST FOUND ---
with tab_found:
    st.subheader("Report Found Item")
    with st.form("found_form", clear_on_submit=True):
        name_f = st.text_input("Item Name *")
        cat_f = st.selectbox("Category *", ["Electronics", "Clothing", "Accessories", "Books", "Keys", "ID/Card", "Bag", "Other"])
        loc_f = st.text_input("Found Location")
        dt_f = st.date_input("Date Found")
        desc_f = st.text_area("Description")
        cname_f = st.text_input("Your Name")
        cont_f = st.text_input("Contact Info")
        
        if st.form_submit_button("Submit"):
            if name_f and cat_f:
                st.session_state.items.append({'id': len(st.session_state.items)+1, 'type':'found', 'title':name_f, 'category':cat_f, 'location':loc_f, 'date':str(dt_f), 'desc':desc_f, 'contact':cont_f, 'contactName':cname_f})
                st.success("Posted!")
                st.rerun()
