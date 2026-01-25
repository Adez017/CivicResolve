import streamlit as st
import requests
import pandas as pd
import time

# CONFIG
API_URL = "http://localhost:5000/api"
IMG_URL = "http://localhost:5000/data/images"

st.set_page_config(page_title="CivicResolve Secure", layout="wide", page_icon="🔐")

# --- AUTHENTICATION LOGIC ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['role'] = None
    st.session_state['username'] = None

def login():
    st.title("🔐 System Login")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login", use_container_width=True)
            
            if submit:
                # HARDCODED CREDENTIALS (For Demo)
                if username == "admin" and password == "admin123":
                    st.session_state['logged_in'] = True
                    st.session_state['role'] = "Admin"
                    st.session_state['username'] = "Administrator"
                    st.rerun()
                    
                elif username == "worker" and password == "fixit":
                    st.session_state['logged_in'] = True
                    st.session_state['role'] = "Worker"
                    st.session_state['username'] = "worker_01"
                    st.rerun()
                    
                elif username == "cam" and password == "smartcity":
                    st.session_state['logged_in'] = True
                    st.session_state['role'] = "Camera"
                    st.session_state['username'] = "CAM_SECTOR_4"
                    st.rerun()
                    
                else:
                    st.error("❌ Invalid Username or Password")

def logout():
    st.session_state['logged_in'] = False
    st.session_state['role'] = None
    st.rerun()

# --- SHOW LOGIN IF NOT LOGGED IN ---
if not st.session_state['logged_in']:
    login()
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.write(f"👤 **{st.session_state['username']}**")
    st.write(f"🔑 Role: {st.session_state['role']}")
    st.markdown("---")
    if st.button("Logout", use_container_width=True):
        logout()

# ==========================================
# 1. SMART CAMERA VIEW (Logged in as 'cam')
# ==========================================
if st.session_state['role'] == "Camera":
    st.title("📹 Smart Camera Interface")
    st.info(f"📡 Connected: {st.session_state['username']} | Location: 12.97, 77.59")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Live Feed Injection")
        uploaded_file = st.file_uploader("Upload Frame", type=['jpg', 'png', 'jpeg'])
        
        if uploaded_file and st.button("▶️ Analyze Frame", type="primary"):
            with st.spinner("Processing..."):
                try:
                    # FIX 1: Send filename and type correctly
                    files = {'image': (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    
                    ai_res = requests.post(f"{API_URL}/ai/predict", files=files)
                    
                    if ai_res.status_code == 200:
                        ai_data = ai_res.json()
                        if ai_data['count'] > 0:
                            best = max(ai_data['predictions'], key=lambda x: x['confidence'])
                            issue = best['class']
                            conf = best['confidence']
                            
                            st.error(f"🚨 {issue.upper()} DETECTED! ({conf:.1%})")
                            
                            # Auto-Report Data
                            data = {
                                'type': issue,
                                'lat': 12.9716, 'lng': 77.5946,
                                'address': f"{st.session_state['username']} - Auto Alert"
                            }
                            # Reset file pointer to send again
                            uploaded_file.seek(0)
                            
                            # FIX 2: Send filename correctly for report
                            report_files = {'image': (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                            
                            r = requests.post(f"{API_URL}/citizen/report", files=report_files, data=data)
                            if r.status_code == 201:
                                st.success(f"Ticket #{r.json()['id']} Created Automatically")
                        else:
                            st.success("✅ Frame Clear - No Issues")
                    else:
                        st.error(f"AI Error: {ai_res.text}")
                except Exception as e:
                    st.error(f"Connection Error: {e}")

# ==========================================
# 2. ADMIN VIEW (Logged in as 'admin')
# ==========================================
elif st.session_state['role'] == "Admin":
    st.title("📊 Command Center")
    
    tab1, tab2 = st.tabs(["Dashboard & Assign", "Verification"])
    
    with tab1:
        if st.button("🔄 Refresh Data"): st.rerun()
        
        try:
            res = requests.get(f"{API_URL}/admin/reports")
            if res.status_code == 200:
                data = res.json()
                if data:
                    df = pd.DataFrame(data)
                    
                    # --- FIX: Extract 'address' from nested JSON ---
                    df['address'] = df['location'].apply(lambda x: x.get('address', 'Unknown'))
                    
                    # Metrics
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Pending Alerts", len(df[df['status'] == 'pending']))
                    c2.metric("Resolved", len(df[df['status'] == 'verified']))
                    c3.metric("Total Incidents", len(df))
                    
                    # --- NEW: MAP VISUALIZATION ---
                    st.subheader("📍 Incident Map")
                    # Prepare data for map (Streamlit needs 'lat' and 'lon' columns)
                    map_data = df[['location']].copy()
                    map_data['lat'] = map_data['location'].apply(lambda x: x['lat'])
                    map_data['lon'] = map_data['location'].apply(lambda x: x['lng'])
                    
                    # Draw the map
                    st.map(map_data)
                    # ------------------------------
                    
                    # Display Table
                    st.subheader("📝 Incident List")
                    st.dataframe(
                        df[['id', 'type', 'status', 'address', 'assigned_to']], 
                        use_container_width=True
                    )
                    
                    # Assign Task Section
                    st.subheader("Dispatch Crew")
                    pending = df[df['status'] == 'pending']
                    
                    if not pending.empty:
                        with st.form("assign_form"):
                            c1, c2 = st.columns(2)
                            tid = c1.selectbox("Select Alert ID", pending['id'].tolist())
                            wid = c2.text_input("Worker ID", "worker_01")
                            
                            if st.form_submit_button("Assign Task"):
                                rtype = pending[pending['id'] == tid]['type'].values[0]
                                payload = {"id": int(tid), "type": rtype, "worker_id": wid}
                                
                                r = requests.post(f"{API_URL}/workflow/tasks/assign", json=payload)
                                if r.status_code == 200:
                                    st.success("Assigned successfully!")
                                    time.sleep(1)
                                    st.rerun()
                                else:
                                    st.error(r.text)
                    else:
                        st.info("No pending alerts requiring action.")
                else:
                    st.info("Database is empty. No reports found.")
        except Exception as e: 
            st.error(f"Data Error: {e}")

    with tab2:
        st.subheader("Validate Fixes")
        if st.button("🔄 Refresh List"): st.rerun()
        
        try:
            res = requests.get(f"{API_URL}/admin/reports")
            if res.status_code == 200:
                data = res.json()
                to_verify = [x for x in data if x['status'] == 'completed']
                
                if to_verify:
                    for t in to_verify:
                        with st.expander(f"Review Fix #{t['id']} ({t['type']})", expanded=True):
                            c1, c2 = st.columns(2)
                            c1.image(f"{IMG_URL}/{t['images']['original']}", caption="❌ Issue", use_container_width=True)
                            c2.image(f"{IMG_URL}/{t['images']['resolved']}", caption="✅ Proof", use_container_width=True)
                            
                            if st.button(f"Approve Fix #{t['id']}"):
                                payload = {"id": t['id'], "type": t['type'], "decision": "approve"}
                                requests.post(f"{API_URL}/workflow/verify/verify", json=payload)
                                st.success("Approved and Closed!")
                                time.sleep(1)
                                st.rerun()
                else:
                    st.info("No tasks waiting for verification.")
        except: pass
# ==========================================
# 3. WORKER VIEW (Logged in as 'worker')
# ==========================================
elif st.session_state['role'] == "Worker":
    st.title("👷 Work Orders")
    
    if st.button("🔄 Sync Tasks"):
        try:
            # Fetch tasks for the logged-in worker ID
            wid = st.session_state['username']
            res = requests.get(f"{API_URL}/workflow/worker/my-tasks/{wid}")
            
            if res.status_code == 200:
                tasks = res.json()
                if tasks:
                    for t in tasks:
                        st.markdown("---")
                        st.warning(f"🔧 **Task #{t['id']}**: {t['type'].upper()}")
                        st.write(f"📍 **Location:** {t['location']['address']}")
                        
                        col1, col2 = st.columns(2)
                        col1.image(f"{IMG_URL}/{t['images']['original']}", caption="Issue Photo", width=300)
                        
                        proof = col2.file_uploader(f"Upload Proof #{t['id']}", key=t['id'])
                        
                        if col2.button(f"Mark Complete #{t['id']}"):
                            if proof:
                                # FIX 4: Send filename correctly for proof
                                files = {'image': (proof.name, proof.getvalue(), proof.type)}
                                data = {'id': t['id'], 'type': t['type']}
                                
                                r = requests.post(f"{API_URL}/workflow/worker/complete", files=files, data=data)
                                if r.status_code == 200:
                                    st.success("Job Submitted for Verification!")
                                    time.sleep(1)
                                    st.rerun()
                            else:
                                st.warning("⚠️ Please upload a proof photo first.")
                else:
                    st.success("No active tasks! You are all caught up.")
            else:
                st.error("Could not fetch tasks.")
        except Exception as e:
            st.error(f"Error fetching tasks: {e}")