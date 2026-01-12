import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
import plotly.express as px
import plotly.graph_objects as go

# הגדרות עמוד
st.set_page_config(
    page_title="ניהול משכנתא חכם",
    layout="wide",
    initial_sidebar_state="expanded"
)

# עיצוב CSS מינימליסטי ובנקאי
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: #f5f7fa;
    }

    /* הגדרות עמוד */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 1rem;
        max-width: 1400px;
    }

    /* עיצוב כרטיסי מדדים - מינימליסטי */
    [data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e8ecef;
        padding: 24px;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 13px;
        font-weight: 500;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 28px;
        font-weight: 600;
        color: #1f2937;
    }
    
    /* סרגל צד נקי */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-left: 1px solid #e8ecef;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        padding: 0.5rem 0;
    }

    /* כפתורי ניווט בסרגל צד - מיושרים לשמאל */
    [data-testid="stSidebar"] .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: transparent;
        color: #6b7280;
        border: none;
        height: 42px;
        font-weight: 500;
        font-size: 14px;
        transition: all 0.2s;
        text-align: left;
        padding-left: 16px;
        justify-content: flex-start;
    }
    
    .st-emotion-cache-1lads1q {
        display: flex;
        -webkit-box-align: center;
        align-items: center;
        -webkit-box-pack: center;
        justify-content: left;
        width: 100%;
    }
    
    .stButton>button:hover {
        background-color: #f3f4f6;
        color: #1f2937;
    }
    
    .stButton>button:active,
    .stButton>button:focus {
        background-color: #2563eb !important;
        color: white !important;
        box-shadow: none !important;
    }

    /* כותרות נקיות */
    h1 {
        font-weight: 700;
        color: #111827;
        font-size: 32px;
        margin-bottom: 0.5rem;
    }
    
    h2 {
        font-weight: 600;
        color: #374151;
        font-size: 20px;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    h3 {
        font-weight: 600;
        color: #4b5563;
        font-size: 16px;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background-color: #2563eb;
    }
    
    /* הסתרת אלמנטים מיותרים */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* טבלאות נקיות */
    [data-testid="stDataFrame"] {
        border: 1px solid #e8ecef;
        border-radius: 8px;
    }
    
    /* מרווחים */
    .element-container {
        margin-bottom: 0rem;
    }
    
    /* תפריט ניווט מותאם אישית */
    .nav-button {
        display: block;
        padding: 12px 16px;
        margin: 6px 0;
        border-radius: 8px;
        text-decoration: none;
        color: #6b7280;
        font-weight: 500;
        font-size: 14px;
        transition: all 0.2s;
        cursor: pointer;
        border: none;
        background: transparent;
        text-align: left;
        width: 100%;
    }
    
    .nav-button:hover {
        background-color: #f3f4f6;
        color: #1f2937;
    }
    
    .nav-button.active {
        background-color: #eff6ff;
        color: #2563eb;
        font-weight: 600;
    }
    
    /* הסתרת radio buttons מקוריים */
    [data-testid="stSidebar"] .row-widget.stRadio > div > label > div:first-child {
        display: none;
    }
    
    [data-testid="stSidebar"] .row-widget.stRadio > div {
        gap: 4px;
    }
    
    [data-testid="stSidebar"] .row-widget.stRadio > div > label {
        background-color: transparent;
        padding: 12px 16px;
        border-radius: 8px;
        border: none;
        transition: all 0.2s;
        font-size: 14px;
        font-weight: 500;
        color: #6b7280;
        cursor: pointer;
    }
    
    [data-testid="stSidebar"] .row-widget.stRadio > div > label:hover {
        background-color: #f3f4f6;
        color: #1f2937;
    }
    
    [data-testid="stSidebar"] .row-widget.stRadio > div > label[aria-checked="true"] {
        background-color: #2563eb;
        color: white;
        font-weight: 600;
    }
    
    /* Divider */
    hr {
        margin: 2rem 0;
        border: none;
        border-top: 1px solid #e8ecef;
    }
    </style>
    """, unsafe_allow_html=True)

DATA_FILE = "mortgage_data.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            df = pd.read_csv(DATA_FILE)
            df["date"] = pd.to_datetime(df["date"])
            return df.sort_values("date")
        except:
            return pd.DataFrame(columns=["date", "remaining", "payment"])
    else:
        return pd.DataFrame(columns=["date", "remaining", "payment"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

df = load_data()

# --- חישובי דאטה מתקדמים ---
if not df.empty and len(df) > 0:
    df_sorted = df.sort_values("date").reset_index(drop=True)
    
    df_sorted["principal_paid"] = df_sorted["remaining"].shift(1) - df_sorted["remaining"]
    df_sorted["principal_paid"] = df_sorted["principal_paid"].fillna(0)
    
    df_sorted["interest_paid"] = df_sorted["payment"] - df_sorted["principal_paid"]
    df_sorted["interest_paid"] = df_sorted["interest_paid"].clip(lower=0)
    
    df_sorted["interest_rate_monthly"] = (df_sorted["interest_paid"] / df_sorted["remaining"].shift(1) * 100)
    
    last_remaining = df_sorted["remaining"].iloc[-1]
    total_paid = df_sorted["payment"].sum()
    total_interest = df_sorted["interest_paid"].sum()
    total_principal = df_sorted["principal_paid"].sum()
    
    last_payment = df_sorted["payment"].iloc[-1]
    last_principal = df_sorted["principal_paid"].iloc[-1]
    last_interest = df_sorted["interest_paid"].iloc[-1]
    last_interest_rate = df_sorted["interest_rate_monthly"].iloc[-1] if pd.notna(df_sorted["interest_rate_monthly"].iloc[-1]) else 0
    
    avg_payment = df_sorted["payment"].mean()
    avg_principal = df_sorted["principal_paid"].mean()
    avg_interest = df_sorted["interest_paid"].mean()
    avg_interest_rate = df_sorted["interest_rate_monthly"].mean()
    
    if avg_principal > 0:
        months_left = last_remaining / avg_principal
        estimated_end_date = df_sorted["date"].iloc[-1] + timedelta(days=30 * months_left)
        total_remaining_interest = (last_remaining * (avg_interest_rate / 100)) * months_left / 2
        total_future_cost = last_remaining + total_remaining_interest
    else:
        months_left = 0
        estimated_end_date = None
        total_remaining_interest = 0
        total_future_cost = last_remaining
    
    if len(df_sorted) > 1:
        initial_loan = df_sorted["remaining"].iloc[0] + df_sorted["principal_paid"].iloc[1:].sum()
    else:
        initial_loan = last_remaining + total_principal
    
    progress = min(1.0, max(0.0, (total_principal / initial_loan))) if initial_loan > 0 else 0
    
    if len(df_sorted) > 1:
        prev_payment = df_sorted["payment"].iloc[-2]
        prev_principal = df_sorted["principal_paid"].iloc[-2]
        prev_interest = df_sorted["interest_paid"].iloc[-2]
        
        payment_change = last_payment - prev_payment
        principal_change = last_principal - prev_principal
        interest_change = last_interest - prev_interest
    else:
        payment_change = principal_change = interest_change = 0
        
else:
    last_remaining = total_paid = months_left = progress = 0
    total_interest = total_principal = 0
    last_payment = last_principal = last_interest = last_interest_rate = 0
    avg_payment = avg_principal = avg_interest = avg_interest_rate = 0
    payment_change = principal_change = interest_change = 0
    estimated_end_date = None
    total_future_cost = 0
    initial_loan = 0
    df_sorted = df

# -----------------------------------------------------------
# סרגל צד
# -----------------------------------------------------------
with st.sidebar:
    st.markdown("### 🏦 ניהול משכנתא")
    st.markdown("---")
    
    # תפריט ניווט מותאם אישית עם HTML/CSS
    menu_items = [
        ("📊 סקירה כללית", "overview"),
        ("💳 ניתוח מפורט", "analysis"),
        ("➕ תשלום חדש", "payment"),
        ("⚙️ הגדרות", "settings")
    ]
    
    # יצירת session state אם לא קיים
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "overview"
    
    st.markdown("**ניווט**")
    
    # יצירת כפתורים מותאמים אישית
    for label, page_id in menu_items:
        if st.button(label, key=f"nav_{page_id}", use_container_width=True):
            st.session_state.current_page = page_id
            st.rerun()
    
    # מיפוי בין page_id לתצוגה
    page_mapping = {
        "overview": "📊 סקירה כללית",
        "analysis": "💳 ניתוח מפורט",
        "payment": "➕ תשלום חדש",
        "settings": "⚙️ הגדרות"
    }
    
    menu_choice = page_mapping.get(st.session_state.current_page, "📊 סקירה כללית")
    
    st.markdown("---")
    
    if not df.empty:
        st.markdown("**סיכום מהיר**")
        st.metric("יתרה", f"₪{last_remaining:,.0f}", label_visibility="collapsed")
        st.caption(f"שולם עד כה: ₪{total_paid:,.0f}")
        st.caption(f"התקדמות: {progress:.0%}")

# -----------------------------------------------------------
# תוכן ראשי
# -----------------------------------------------------------

# כותרת מינימליסטית
st.markdown("# Dashboard")
st.caption(f"עדכון אחרון: {datetime.now().strftime('%d.%m.%Y')}")

# -----------------------------------------------------------
# עמוד סקירה כללית
# -----------------------------------------------------------
if menu_choice == "📊 סקירה כללית":
    
    # שורת מדדים עיקרית
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("יתרה נוכחית", f"₪{last_remaining:,.0f}")
    
    with col2:
        st.metric("ירידת חוב החודש", f"₪{last_principal:,.0f}" if last_principal > 0 else "---")
    
    with col3:
        st.metric("ריבית ששולמה החודש", f"₪{last_interest:,.0f}" if last_interest > 0 else "---")
    
    with col4:
        st.metric("חודשים לסיום", f"{months_left:.0f}" if months_left > 0 else "---")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if df.empty:
        st.info("👋 התחל על ידי הוספת תשלום ראשון בלשונית 'תשלום חדש'")
    else:
        # שני גרפים זה לצד זה - קומפקטיים
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### היסטוריית חוב")
            fig1 = px.area(
                df_sorted, 
                x="date", 
                y="remaining",
                color_discrete_sequence=["#2563eb"]
            )
            fig1.update_layout(
                plot_bgcolor="white",
                paper_bgcolor="white",
                margin=dict(l=0, r=0, t=5, b=0),
                xaxis_title="",
                yaxis_title="",
                height=200,
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor="#f3f4f6")
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            st.markdown("### חלוקת תשלומים")
            fig2 = go.Figure()
            fig2.add_trace(go.Bar(
                x=df_sorted["date"], 
                y=df_sorted["principal_paid"], 
                name="קרן",
                marker_color="#10b981"
            ))
            fig2.add_trace(go.Bar(
                x=df_sorted["date"], 
                y=df_sorted["interest_paid"], 
                name="ריבית",
                marker_color="#ef4444"
            ))
            fig2.update_layout(
                barmode='stack',
                plot_bgcolor="white",
                paper_bgcolor="white",
                margin=dict(l=0, r=0, t=5, b=0),
                xaxis_title="",
                yaxis_title="",
                height=200,
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor="#f3f4f6")
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        # טבלה קומפקטית מתחת
        st.markdown("### תשלומים אחרונים")
        display_df = df_sorted[["date", "payment", "principal_paid", "interest_paid", "remaining"]].copy()
        display_df["date"] = display_df["date"].dt.strftime("%m/%Y")
        display_df = display_df.rename(columns={
            "date": "תאריך",
            "payment": "תשלום",
            "principal_paid": "קרן",
            "interest_paid": "ריבית",
            "remaining": "יתרה"
        })
        st.dataframe(
            display_df.iloc[::-1].head(5), 
            hide_index=True, 
            use_container_width=True
        )

# -----------------------------------------------------------
# עמוד ניתוח מפורט
# -----------------------------------------------------------
elif menu_choice == "💳 ניתוח מפורט":
    
    if df.empty:
        st.info("👋 אין מספיק נתונים לניתוח. הוסף תשלומים כדי לראות תובנות.")
    else:
        
        # החודש האחרון
        st.markdown("### התשלום האחרון")
        c1, c2, c3, c4 = st.columns(4)
        
        c1.metric(
            "תשלום כולל", 
            f"₪{last_payment:,.0f}",
            delta=f"{payment_change:,.0f}" if payment_change != 0 else None
        )
        c2.metric(
            "קרן", 
            f"₪{last_principal:,.0f}",
            delta=f"{principal_change:,.0f}" if principal_change != 0 else None
        )
        c3.metric(
            "ריבית", 
            f"₪{last_interest:,.0f}",
            delta=f"{interest_change:,.0f}" if interest_change != 0 else None,
            delta_color="inverse"
        )
        c4.metric(
            "יחס קרן/תשלום", 
            f"{(last_principal/last_payment*100):.0f}%" if last_payment > 0 else "---"
        )
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # ממוצעים
        st.markdown("### ממוצעים")
        c1, c2, c3, c4 = st.columns(4)
        
        c1.metric("תשלום ממוצע", f"₪{avg_payment:,.0f}")
        c2.metric("קרן ממוצעת", f"₪{avg_principal:,.0f}")
        c3.metric("ריבית ממוצעת", f"₪{avg_interest:,.0f}")
        c4.metric("ריבית חודשית", f"{avg_interest_rate:.2f}%")
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # סיכום כולל
        st.markdown("### סיכום כולל")
        c1, c2, c3, c4 = st.columns(4)
        
        c1.metric("סך תשלומים", f"₪{total_paid:,.0f}")
        c2.metric("סך קרן", f"₪{total_principal:,.0f}")
        c3.metric("סך ריבית", f"₪{total_interest:,.0f}")
        c4.metric("% ריבית", f"{(total_interest/total_paid*100):.1f}%" if total_paid > 0 else "---")
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # תחזיות
        st.markdown("### תחזית")
        c1, c2, c3, c4 = st.columns(4)
        
        c1.metric("חודשים נותרים", f"{months_left:.0f}" if months_left > 0 else "---")
        c2.metric(
            "תאריך סיום משוער", 
            estimated_end_date.strftime("%m/%Y") if estimated_end_date else "---"
        )
        c3.metric("ריבית עתידית", f"₪{total_remaining_interest:,.0f}")
        c4.metric("עלות כוללת משוערת", f"₪{(total_paid + total_future_cost):,.0f}")
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # תובנות
        st.markdown("### תובנות")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if last_principal > avg_principal * 1.1 and len(df_sorted) > 3:
                st.success(f"✓ התשלום לקרן החודש היה {((last_principal/avg_principal - 1)*100):.0f}% מעל הממוצע")
            elif last_principal < avg_principal * 0.9 and len(df_sorted) > 3:
                st.warning(f"התשלום לקרן החודש היה {((1 - last_principal/avg_principal)*100):.0f}% מתחת לממוצע")
            else:
                st.info("התשלום לקרן בטווח הממוצע")
        
        with col2:
            annual_rate = avg_interest_rate * 12 if avg_interest_rate > 0 else 0
            st.info(f"הריבית השנתית האפקטיבית: **{annual_rate:.2f}%**")

# -----------------------------------------------------------
# עמוד תשלום חדש
# -----------------------------------------------------------
elif menu_choice == "➕ תשלום חדש":
    
    st.markdown("### הוסף תשלום חדש")
    st.caption("הזן את פרטי התשלום החודשי האחרון")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.form("input_form", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            d = st.date_input("תאריך", datetime.now())
        
        with col2:
            r = st.number_input("יתרה נוכחית (₪)", min_value=0.0, step=1000.0)
        
        with col3:
            p = st.number_input("סכום ששולם (₪)", min_value=0.0, step=100.0)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            submit = st.form_submit_button("💾 שמור", use_container_width=True)
        
        if submit:
            if r > 0 and p > 0:
                new_row = pd.DataFrame([{
                    "date": pd.to_datetime(d), 
                    "remaining": r, 
                    "payment": p
                }])
                df = pd.concat([df, new_row], ignore_index=True)
                save_data(df)
                st.success("✓ התשלום נשמר בהצלחה")
                st.rerun()
            else:
                st.error("אנא מלא את כל השדות")

# -----------------------------------------------------------
# עמוד הגדרות
# -----------------------------------------------------------
elif menu_choice == "⚙️ הגדרות":
    
    st.markdown("### ניהול נתונים")
    st.caption("ערוך או מחק רשומות קיימות")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if df.empty:
        st.info("אין נתונים להצגה")
    else:
        edited = st.data_editor(
            df.sort_values("date", ascending=False),
            column_config={
                "date": st.column_config.DateColumn("תאריך", format="DD/MM/YYYY"),
                "remaining": st.column_config.NumberColumn("יתרה (₪)", format="₪%.0f"),
                "payment": st.column_config.NumberColumn("תשלום (₪)", format="₪%.0f")
            },
            use_container_width=True,
            num_rows="dynamic",
            hide_index=True
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button("💾 שמור שינויים", use_container_width=True):
                save_data(edited)
                st.success("✓ השינויים נשמרו")
                st.rerun()