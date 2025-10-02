import streamlit as st
import qrcode
from io import BytesIO
import base64
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import anthropic

# Page configuration
st.set_page_config(
    page_title="Smart Medication Education Platform",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #e3f2fd 0%, #bbdefb 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-top: 1rem;
    }
    .info-box {
        padding: 1rem;
        border-radius: 10px;
        background-color: #f0f8ff;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
    }
    .success-box {
        padding: 1rem;
        border-radius: 10px;
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'patient_data' not in st.session_state:
    st.session_state.patient_data = []
if 'survey_responses' not in st.session_state:
    st.session_state.survey_responses = []
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""

# Sidebar Configuration
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/pill.png", width=80)
    st.title("🏥 Navigation")
    
    # API Key Configuration
    st.markdown("---")
    st.subheader("🔑 API Configuration")
    api_key = st.text_input(
        "Enter Claude API Key",
        type="password",
        value=st.session_state.api_key,
        help="Get your API key from console.anthropic.com"
    )
    if api_key:
        st.session_state.api_key = api_key
        st.success("✅ API Key Configured")
    
    st.markdown("---")
    
    # Navigation Menu
    page = st.radio(
        "Select Module:",
        [
            "🏠 Home",
            "📋 Research Overview",
            "🔗 QR Code Generator",
            "🤖 AI Medication Chatbot",
            "📊 Patient Survey",
            "📈 Data Analytics",
            "👥 Patient Management",
            "ℹ️ About"
        ]
    )
    
    st.markdown("---")
    st.info("""
    **Quick Guide:**
    - Generate QR codes for medications
    - Chat with AI for medication info
    - Collect patient feedback
    - Analyze research data
    """)

# Helper Functions
def generate_qr_code(data):
    """Generate QR code from data"""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

def get_image_download_link(img_buffer, filename):
    """Generate download link for QR code"""
    b64 = base64.b64encode(img_buffer.getvalue()).decode()
    return f'<a href="data:image/png;base64,{b64}" download="{filename}">📥 Download QR Code</a>'

def chat_with_claude(message, api_key):
    """Send message to Claude API"""
    try:
        client = anthropic.Anthropic(api_key=api_key)
        
        system_prompt = """You are a knowledgeable pharmacy assistant specializing in patient medication education. 
        Provide clear, accurate, and patient-friendly information about medications, including:
        - How to take the medication
        - Common side effects
        - Important warnings
        - Drug interactions
        - Storage instructions
        
        Always remind patients to consult their healthcare provider for personalized advice."""
        
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=system_prompt,
            messages=[
                {"role": "user", "content": message}
            ]
        )
        
        return response.content[0].text
    except Exception as e:
        return f"Error: {str(e)}. Please check your API key and try again."

# Page Routing
if page == "🏠 Home":
    st.markdown('<div class="main-header">💊 Smart Medication Education Platform</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="info-box">
            <h3>🔗 QR Code Technology</h3>
            <p>Replace traditional paper leaflets with scannable QR codes for instant access to medication information.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-box">
            <h3>🤖 AI Chatbot Support</h3>
            <p>Get instant answers to medication questions through our AI-powered chatbot assistant.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="info-box">
            <h3>📊 Research Analytics</h3>
            <p>Track patient engagement, satisfaction, and adherence metrics for research analysis.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.subheader("🎯 Platform Features")
    
    features = {
        "Feature": ["QR Code Generation", "AI Chatbot", "Patient Surveys", "Data Analytics", "Multi-language Support"],
        "Status": ["✅ Active", "✅ Active", "✅ Active", "✅ Active", "🔄 Coming Soon"],
        "Description": [
            "Create custom QR codes for any medication",
            "24/7 AI-powered medication information",
            "Collect patient feedback and satisfaction data",
            "Visualize research data and trends",
            "Support for multiple languages"
        ]
    }
    
    df_features = pd.DataFrame(features)
    st.dataframe(df_features, use_container_width=True, hide_index=True)

elif page == "📋 Research Overview":
    st.markdown('<div class="main-header">📋 Research Project Overview</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ## Title
    **Replacing Traditional Patient Information Leaflets with Smart QR Codes and AI Chatbot Support for Enhanced Medication Education and Adherence**
    
    ---
    
    ### 🎯 Research Objectives
    
    1. **Effectiveness Evaluation**: To evaluate the effectiveness of QR codes and chatbot-assisted platforms in delivering medication information compared to traditional leaflets
    
    2. **Adherence Assessment**: To assess the impact of QR code–chatbot–based education on patient adherence to prescribed medications
    
    3. **Satisfaction Analysis**: To analyze patients' preferences and satisfaction regarding the use of digital education tools
    
    ---
    
    ### ❓ Research Questions
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="info-box">
        <b>Question 1:</b><br>
        Does the use of QR codes and chatbot support improve patient understanding of medication instructions compared to traditional leaflets?
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box">
        <b>Question 2:</b><br>
        Is there a measurable difference in medication adherence among patients using QR code–chatbot education?
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-box">
        <b>Question 3:</b><br>
        What are patients' attitudes and satisfaction levels toward these digital tools?
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box">
        <b>Question 4:</b><br>
        What barriers might hinder the successful adoption of QR codes and chatbots in pharmacies or hospitals?
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.subheader("🔬 Significance of the Study")
    st.write("""
    This study contributes to the modernization of patient education by integrating QR codes and AI-driven chatbot support. 
    It has the potential to:
    - ✅ Improve health outcomes through better adherence
    - ✅ Provide more personalized education
    - ✅ Support healthcare institutions in adopting innovative, patient-centered communication tools
    - ✅ Bridge the digital divide in healthcare education
    """)
    
    st.markdown("---")
    
    st.subheader("📐 Scope and Target Population")
    
    target_populations = pd.DataFrame({
        "Population": ["Elderly Patients", "Chronic Illness", "Low Literacy", "Language Barriers", "Tech-Savvy Youth"],
        "Why Important": [
            "Need larger fonts and simpler explanations",
            "Require continuous medication education",
            "Benefit from audio/visual content",
            "Need multilingual support",
            "Prefer digital interaction"
        ],
        "Expected Benefit": ["High", "High", "Very High", "Very High", "Medium"]
    })
    
    st.dataframe(target_populations, use_container_width=True, hide_index=True)

elif page == "🔗 QR Code Generator":
    st.markdown('<div class="main-header">🔗 QR Code Generator for Medications</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Enter Medication Information")
        
        med_name = st.text_input("💊 Medication Name", placeholder="e.g., Amoxicillin")
        dosage = st.text_input("📏 Dosage", placeholder="e.g., 500mg")
        frequency = st.text_input("⏰ Frequency", placeholder="e.g., Three times daily")
        instructions = st.text_area("📝 Special Instructions", placeholder="Take with food, avoid alcohol")
        
        # Advanced options
        with st.expander("⚙️ Advanced Options"):
            include_chatbot = st.checkbox("Include AI Chatbot Link", value=True)
            custom_url = st.text_input("Custom URL (optional)", placeholder="https://your-med-info.com")
        
        if st.button("🎨 Generate QR Code", type="primary"):
            if med_name and dosage and frequency:
                # Create data for QR code
                qr_data = {
                    "medication": med_name,
                    "dosage": dosage,
                    "frequency": frequency,
                    "instructions": instructions,
                    "generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                if include_chatbot:
                    qr_data["chatbot"] = "enabled"
                
                if custom_url:
                    qr_data["url"] = custom_url
                
                qr_text = json.dumps(qr_data, indent=2)
                
                # Generate QR code
                qr_buffer = generate_qr_code(qr_text)
                
                with col2:
                    st.subheader("Generated QR Code")
                    st.image(qr_buffer, caption=f"QR Code for {med_name}", use_container_width=True)
                    
                    st.markdown(get_image_download_link(qr_buffer, f"{med_name}_QR.png"), unsafe_allow_html=True)
                    
                    st.markdown("""
                    <div class="success-box">
                    ✅ QR Code generated successfully! Patients can scan this code to access medication information instantly.
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.expander("📄 View Encoded Data"):
                        st.json(qr_data)
            else:
                st.error("Please fill in at least Medication Name, Dosage, and Frequency")

elif page == "🤖 AI Medication Chatbot":
    st.markdown('<div class="main-header">🤖 AI Medication Chatbot Assistant</div>', unsafe_allow_html=True)
    
    if not st.session_state.api_key:
        st.warning("⚠️ Please enter your Claude API key in the sidebar to use the chatbot.")
        st.info("👈 Get your API key from: https://console.anthropic.com/")
    else:
        st.markdown("""
        <div class="info-box">
        💬 Ask me anything about medications! I can help with dosage, side effects, interactions, and more.
        <br><br>
        <b>Example questions:</b><br>
        • "What are the side effects of ibuprofen?"<br>
        • "How should I take metformin?"<br>
        • "Can I take aspirin with warfarin?"
        </div>
        """, unsafe_allow_html=True)
        
        # Display chat history
        for chat in st.session_state.chat_history:
            with st.chat_message(chat["role"]):
                st.write(chat["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask about medications..."):
            # Add user message
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)
            
            # Get AI response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = chat_with_claude(prompt, st.session_state.api_key)
                    st.write(response)
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()

elif page == "📊 Patient Survey":
    st.markdown('<div class="main-header">📊 Patient Feedback Survey</div>', unsafe_allow_html=True)
    
    st.write("Help us improve medication education by sharing your experience!")
    
    with st.form("patient_survey"):
        st.subheader("Patient Information")
        
        col1, col2 = st.columns(2)
        with col1:
            patient_id = st.text_input("Patient ID (optional)", placeholder="P001")
            age_group = st.selectbox("Age Group", ["18-30", "31-50", "51-65", "65+"])
            education = st.selectbox("Education Level", ["High School", "Bachelor's", "Master's", "Doctorate", "Other"])
        
        with col2:
            method_used = st.radio("Information Method Used", ["Traditional Leaflet", "QR Code + Chatbot", "Both"])
            tech_comfort = st.slider("Comfort with Technology (1-5)", 1, 5, 3)
        
        st.markdown("---")
        st.subheader("Understanding & Satisfaction")
        
        understanding = st.slider("How well did you understand the medication information? (1-10)", 1, 10, 7)
        satisfaction = st.slider("Overall satisfaction with the information method (1-10)", 1, 10, 7)
        adherence_confidence = st.slider("How confident are you in taking your medication correctly? (1-10)", 1, 10, 7)
        
        st.markdown("---")
        st.subheader("Preferences")
        
        prefer_method = st.radio(
            "Which method do you prefer?",
            ["Traditional Paper Leaflet", "QR Code with Digital Info", "AI Chatbot Support", "Combination of Digital Methods"]
        )
        
        would_recommend = st.radio("Would you recommend the digital method to others?", ["Yes", "No", "Maybe"])
        
        additional_feedback = st.text_area("Additional Comments", placeholder="Share any thoughts or suggestions...")
        
        submitted = st.form_submit_button("Submit Survey", type="primary")
        
        if submitted:
            survey_data = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "patient_id": patient_id or "Anonymous",
                "age_group": age_group,
                "education": education,
                "method_used": method_used,
                "tech_comfort": tech_comfort,
                "understanding": understanding,
                "satisfaction": satisfaction,
                "adherence_confidence": adherence_confidence,
                "prefer_method": prefer_method,
                "would_recommend": would_recommend,
                "feedback": additional_feedback
            }
            
            st.session_state.survey_responses.append(survey_data)
            
            st.markdown("""
            <div class="success-box">
            ✅ Thank you for your feedback! Your response has been recorded.
            </div>
            """, unsafe_allow_html=True)
            
            st.balloons()

elif page == "📈 Data Analytics":
    st.markdown('<div class="main-header">📈 Research Data Analytics</div>', unsafe_allow_html=True)
    
    if len(st.session_state.survey_responses) == 0:
        st.info("📊 No survey data available yet. Collect responses through the Patient Survey module.")
        
        # Sample data for demonstration
        if st.button("Load Sample Data for Demo"):
            sample_data = [
                {"patient_id": "P001", "age_group": "31-50", "method_used": "QR Code + Chatbot", 
                 "understanding": 9, "satisfaction": 8, "adherence_confidence": 9, "tech_comfort": 4,
                 "prefer_method": "AI Chatbot Support", "would_recommend": "Yes"},
                {"patient_id": "P002", "age_group": "65+", "method_used": "Traditional Leaflet",
                 "understanding": 6, "satisfaction": 5, "adherence_confidence": 6, "tech_comfort": 2,
                 "prefer_method": "Traditional Paper Leaflet", "would_recommend": "No"},
                {"patient_id": "P003", "age_group": "18-30", "method_used": "QR Code + Chatbot",
                 "understanding": 10, "satisfaction": 10, "adherence_confidence": 9, "tech_comfort": 5,
                 "prefer_method": "Combination of Digital Methods", "would_recommend": "Yes"},
                {"patient_id": "P004", "age_group": "51-65", "method_used": "Both",
                 "understanding": 8, "satisfaction": 9, "adherence_confidence": 8, "tech_comfort": 3,
                 "prefer_method": "QR Code with Digital Info", "would_recommend": "Yes"},
                {"patient_id": "P005", "age_group": "31-50", "method_used": "QR Code + Chatbot",
                 "understanding": 9, "satisfaction": 9, "adherence_confidence": 10, "tech_comfort": 4,
                 "prefer_method": "AI Chatbot Support", "would_recommend": "Yes"},
            ]
            st.session_state.survey_responses = sample_data
            st.rerun()
    else:
        df = pd.DataFrame(st.session_state.survey_responses)
        
        # Summary Statistics
        st.subheader("📊 Summary Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Responses", len(df))
        with col2:
            st.metric("Avg Understanding", f"{df['understanding'].mean():.1f}/10")
        with col3:
            st.metric("Avg Satisfaction", f"{df['satisfaction'].mean():.1f}/10")
        with col4:
            st.metric("Avg Adherence Confidence", f"{df['adherence_confidence'].mean():.1f}/10")
        
        st.markdown("---")
        
        # Visualizations
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Comparisons", "👥 Demographics", "💬 Preferences", "📥 Export Data"])
        
        with tab1:
            st.subheader("Method Comparison")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Understanding by method
                fig_understanding = px.box(
                    df, x="method_used", y="understanding",
                    title="Understanding Score by Method",
                    color="method_used",
                    labels={"understanding": "Understanding (1-10)", "method_used": "Method Used"}
                )
                st.plotly_chart(fig_understanding, use_container_width=True)
            
            with col2:
                # Satisfaction by method
                fig_satisfaction = px.box(
                    df, x="method_used", y="satisfaction",
                    title="Satisfaction Score by Method",
                    color="method_used",
                    labels={"satisfaction": "Satisfaction (1-10)", "method_used": "Method Used"}
                )
                st.plotly_chart(fig_satisfaction, use_container_width=True)
            
            # Adherence confidence comparison
            fig_adherence = px.violin(
                df, x="method_used", y="adherence_confidence",
                title="Adherence Confidence by Method",
                color="method_used",
                box=True,
                labels={"adherence_confidence": "Adherence Confidence (1-10)", "method_used": "Method Used"}
            )
            st.plotly_chart(fig_adherence, use_container_width=True)
        
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                # Age distribution
                age_counts = df['age_group'].value_counts()
                fig_age = px.pie(values=age_counts.values, names=age_counts.index, 
                                title="Age Group Distribution")
                st.plotly_chart(fig_age, use_container_width=True)
            
            with col2:
                # Tech comfort by age
                fig_tech = px.box(df, x="age_group", y="tech_comfort",
                                 title="Technology Comfort by Age Group",
                                 color="age_group")
                st.plotly_chart(fig_tech, use_container_width=True)
        
        with tab3:
            col1, col2 = st.columns(2)
            
            with col1:
                # Preferred method
                prefer_counts = df['prefer_method'].value_counts()
                fig_prefer = px.bar(x=prefer_counts.index, y=prefer_counts.values,
                                   title="Preferred Information Method",
                                   labels={"x": "Method", "y": "Count"})
                fig_prefer.update_layout(showlegend=False)
                st.plotly_chart(fig_prefer, use_container_width=True)
            
            with col2:
                # Recommendation rate
                recommend_counts = df['would_recommend'].value_counts()
                fig_recommend = px.pie(values=recommend_counts.values, names=recommend_counts.index,
                                      title="Would Recommend Digital Methods?")
                st.plotly_chart(fig_recommend, use_container_width=True)
        
        with tab4:
            st.subheader("Export Research Data")
            
            st.dataframe(df, use_container_width=True)
            
            # Export options
            col1, col2 = st.columns(2)
            
            with col1:
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"survey_data_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            
            with col2:
                json_data = df.to_json(orient="records", indent=2)
                st.download_button(
                    label="📥 Download JSON",
                    data=json_data,
                    file_name=f"survey_data_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json"
                )

elif page == "👥 Patient Management":
    st.markdown('<div class="main-header">👥 Patient Management System</div>', unsafe_allow_html=True)
    
    st.subheader("Register New Patient")
    
    with st.form("patient_registration"):
        col1, col2 = st.columns(2)
        
        with col1:
            patient_name = st.text_input("Patient Name")
            patient_email = st.text_input("Email")
            patient_phone = st.text_input("Phone Number")
        
        with col2:
            patient_age = st.number_input("Age", min_value=1, max_value=120, value=30)
            assigned_method = st.selectbox(
                "Assigned Information Method",
                ["Traditional Leaflet", "QR Code + Chatbot", "Both (Control Group)"]
            )
            enrollment_date = st.date_input("Enrollment Date")
        
        medications = st.text_area("Prescribed Medications", placeholder="List medications separated by commas")
        notes = st.text_area("Additional Notes", placeholder="Any special considerations...")
        
        submitted = st.form_submit_button("Register Patient", type="primary")
        
        if submitted and patient_name:
            patient_data = {
                "id": f"P{len(st.session_state.patient_data) + 1:03d}",
                "name": patient_name,
                "email": patient_email,
                "phone": patient_phone,
                "age": patient_age,
                "method": assigned_method,
                "enrollment_date": str(enrollment_date),
                "medications": medications,
                "notes": notes,
                "registered_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            st.session_state.patient_data.append(patient_data)
            
            st.success(f"✅ Patient registered successfully! ID: {patient_data['id']}")
    
    st.markdown("---")
    
    # Display registered patients
    if st.session_state.patient_data:
        st.subheader("Registered Patients")
        
        patients_df = pd.DataFrame(st.session_state.patient_data)
        st.dataframe(patients_df, use_container_width=True, hide_index=True)
        
        # Export patient data
        csv = patients_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Patient List",
            data=csv,
            file_name=f"patients_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.info("No patients registered yet.")

elif page == "ℹ️ About":
    st.markdown('<div class="main-header">ℹ️ About This Platform</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ## 🎓 Research Project Information
    
    This platform is designed to support PharmD student research on modernizing patient medication education.
    
    ### 🎯 Project Goals
    - Replace traditional paper leaflets with accessible digital solutions
    - Leverage QR codes for instant information access
    - Provide AI-powered chatbot support for personalized medication guidance
    - Collect and analyze patient feedback data
    - Measure impact on medication adherence and understanding
    
    ---
    
    ### 🛠️ Technology Stack
    - **Frontend**: Streamlit (Python)
    - **AI Integration**: Claude API by Anthropic
    - **Data Visualization**: Plotly
    - **QR Code Generation**: python-qrcode library
    
    ---
    
    ### 👨‍💻 For Developers
    
    **Required Libraries:**
    ```python
    pip install streamlit qrcode pillow pandas plotly anthropic
    ```
    
    **Running the App:**
    ```bash
    streamlit run app.py
    ```
    
    ---
    
    ### 📚 Research Team
    - PharmD Students
    - Faculty Advisors
    - Healthcare Technology Partners
    
    ---
    
    ### 📧 Contact & Support
    For technical support or research inquiries, please contact your research supervisor.
    
    ---
    
    ### 📄 License & Ethics
    This platform is developed for educational and research purposes. All patient data is handled according to 
    healthcare privacy regulations and institutional review board (IRB) guidelines.
    """)
    
    st.markdown("---")
    
    st.success("💡 **Tip**: Start by entering your Claude API key in the sidebar to enable the AI chatbot feature.")