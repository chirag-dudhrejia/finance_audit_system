"""
Enterprise-grade theme configuration for Finance Audit System
"""

PRIMARY_COLOR = "#1e3a5f"
SECONDARY_COLOR = "#0d9488"
ACCENT_COLOR = "#3b82f6"
SUCCESS_COLOR = "#10b981"
WARNING_COLOR = "#f59e0b"
ERROR_COLOR = "#ef4444"
INFO_COLOR = "#3b82f6"

BG_PRIMARY = "#f8fafc"
BG_CARD = "#ffffff"
BG_DARK = "#0f172a"
TEXT_PRIMARY = "#1e293b"
TEXT_SECONDARY = "#64748b"
TEXT_MUTED = "#94a3b8"
BORDER_COLOR = "#e2e8f0"
BORDER_RADIUS = "12px"
SHADOW_SM = "0 1px 3px rgba(0,0,0,0.1)"
SHADOW_MD = "0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -2px rgba(0,0,0,0.1)"
SHADOW_LG = "0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -4px rgba(0,0,0,0.1)"

FONT_FAMILY = (
    "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
)

METRIC_COLORS = {
    "income": "#10b981",
    "expenses": "#ef4444",
    "savings": "#3b82f6",
    "neutral": "#64748b",
}

CATEGORY_COLORS = {
    "Food & Dining": "#f59e0b",
    "Transport": "#3b82f6",
    "Shopping": "#ec4899",
    "Entertainment": "#8b5cf6",
    "Bank Transfer": "#06b6d4",
    "Transfer": "#06b6d4",
    "Bills & Utilities": "#ef4444",
    "Rent": "#8b5cf6",
    "Health": "#10b981",
    "Investment": "#3b82f6",
    "Uncategorized": "#94a3b8",
}


def get_css():
    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* {{
    font-family: {FONT_FAMILY};
}}

/* Main background */
.stApp {{
    background-color: {BG_PRIMARY};
}}

/* Sidebar */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
    padding: 1rem;
}}

.st-emotion-cache-zy6yx3 {{
    padding-top: 2rem !important;
}}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {{
    color: white;
}}

[data-testid="stSidebarHeader"] {{
    display: flex !important;
    height: 2rem !important;
    margin-bottom: 0 !important;
}}

[data-testid="stSidebarCollapseButton"] {{
    display: flex !important;
    visibility: visible !important;
}}

[data-testid="stLogoSpacer"] {{
    display: none !important;
}}

/* Hide default Streamlit sidebar navigation */
[data-testid="stSidebarNav"] {{
    display: none !important;
}}

/* Sidebar brand section */
.sidebar-brand {{
    text-align: center;
    padding: 0rem 1rem;
    margin: 0;
    background: rgba(255,255,255,0.05);
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.08);
}}
.sidebar-brand .logo {{
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}}
.sidebar-brand h1 {{
    font-size: 1.25rem !important;
    font-weight: 700 !important;
    color: white !important;
    margin: 0 !important;
}}
.sidebar-brand p {{
    font-size: 0.75rem !important;
    color: rgba(148, 163, 184, 0.7) !important;
    margin: 0.25rem 0 0 0 !important;
}}

/* Section titles */
.sidebar-section-title {{
    font-size: 0.65rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.12em !important;
    color: rgba(148, 163, 184, 0.5) !important;
    padding: 1rem 0.75rem 0.25rem !important;
    margin: 0 !important;
}}

/* Dividers */
.sidebar-divider {{
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
    margin: 0.75rem 0;
}}

/* Stats card */
.sidebar-stats {{
    background: rgba(255,255,255,0.04);
    border-radius: 12px;
    padding: 1rem;
    margin: 0.5rem 0;
}}
.sidebar-stats .stat-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.4rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}}
.sidebar-stats .stat-row:last-child {{
    border-bottom: none;
}}
.sidebar-stats .stat-label {{
    font-size: 0.75rem;
    color: rgba(148, 163, 184, 0.8);
}}
.sidebar-stats .stat-value {{
    font-size: 0.85rem;
    font-weight: 600;
    color: white;
}}

/* Headers */
h1, h2, h3, h4, h5, h6 {{
    color: {TEXT_PRIMARY};
    font-weight: 600;
}}

/* Metric cards */
[data-testid="stMetric"] {{
    background-color: {BG_CARD};
    border: 1px solid {BORDER_COLOR};
    border-radius: {BORDER_RADIUS};
    padding: 1.25rem;
    box-shadow: {SHADOW_SM};
}}

[data-testid="stMetricLabel"] {{
    color: {TEXT_SECONDARY} !important;
    font-size: 0.875rem !important;
    font-weight: 500;
}}

[data-testid="stMetricValue"] {{
    color: {TEXT_PRIMARY} !important;
    font-weight: 700;
    font-size: 1.5rem !important;
}}

/* Dataframes */
[data-testid="stDataFrame"], [data-testid="stTable"] {{
    background-color: {BG_CARD};
    border-radius: {BORDER_RADIUS};
    border: 1px solid {BORDER_COLOR};
}}

[data-testid="stDataFrame"] thead th {{
    background-color: {BG_PRIMARY} !important;
    color: {TEXT_PRIMARY} !important;
    font-weight: 600;
    border-bottom: 2px solid {BORDER_COLOR} !important;
}}

/* Expanders */
[data-testid="stExpander"] {{
    background-color: {BG_CARD};
    border-radius: {BORDER_RADIUS};
    border: 1px solid {BORDER_COLOR};
}}

/* Success/Error/Warning/Info boxes */
.element-container div:has(> div.stAlert) {{
    border-radius: {BORDER_RADIUS};
}}

.stSuccess {{
    background-color: #ecfdf5 !important;
    border: 1px solid #a7f3d0 !important;
    border-radius: {BORDER_RADIUS};
}}

.stSuccess > div {{
    color: #065f46 !important;
}}

.stWarning {{
    background-color: #fffbeb !important;
    border: 1px solid #fde68a !important;
    border-radius: {BORDER_RADIUS};
}}

.stWarning > div {{
    color: #92400e !important;
}}

.stError {{
    background-color: #fef2f2 !important;
    border: 1px solid #fecaca !important;
    border-radius: {BORDER_RADIUS};
}}

.stError > div {{
    color: #991b1b !important;
}}

.stInfo {{
    background-color: #eff6ff !important;
    border: 1px solid #bfdbfe !important;
    border-radius: {BORDER_RADIUS};
}}

.stInfo > div {{
    color: #1e40af !important;
}}

/* File uploader */
[data-testid="stFileUploader"] {{
    background-color: {BG_CARD};
    border: 2px dashed {BORDER_COLOR};
    border-radius: {BORDER_RADIUS};
    padding: 2rem;
}}

[data-testid="stFileUploader"]:hover {{
    border-color: {ACCENT_COLOR};
}}

/* Progress bars */
.stProgress > div > div {{
    background-color: {ACCENT_COLOR};
}}

/* Radio buttons */
[data-testid="stRadio"] label {{
    background-color: {BG_CARD};
    border: 1px solid {BORDER_COLOR};
    border-radius: 8px;
    padding: 0.5rem 1rem;
    margin-right: 0.5rem;
}}

[data-testid="stRadio"] label:has(> div:first-child input:checked) {{
    background-color: {PRIMARY_COLOR};
    border-color: {PRIMARY_COLOR};
    color: white;
}}

/* Custom section headers */
.enterprise-section {{
    background: linear-gradient(135deg, {PRIMARY_COLOR} 0%, #2d4a6f 100%);
    color: white;
    padding: 1.5rem 2rem;
    border-radius: {BORDER_RADIUS};
    margin: 1.5rem 0;
    box-shadow: {SHADOW_MD};
}}

.enterprise-section h2 {{
    color: white !important;
    margin: 0;
    font-size: 1.25rem;
}}

.enterprise-section .section-subtitle {{
    color: rgba(255,255,255,0.8);
    font-size: 0.875rem;
    margin-top: 0.25rem;
}}

/* Card container */
.enterprise-card {{
    background-color: {BG_CARD};
    border: 1px solid {BORDER_COLOR};
    border-radius: {BORDER_RADIUS};
    padding: 1.5rem;
    box-shadow: {SHADOW_SM};
}}

/* KPI card */
.kpi-card {{
    background: linear-gradient(135deg, {BG_CARD} 0%, {BG_PRIMARY} 100%);
    border: 1px solid {BORDER_COLOR};
    border-radius: {BORDER_RADIUS};
    padding: 1.5rem;
    box-shadow: {SHADOW_MD};
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}}

.kpi-card:hover {{
    transform: translateY(-2px);
    box-shadow: {SHADOW_LG};
}}

.kpi-label {{
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: {TEXT_SECONDARY};
    margin-bottom: 0.5rem;
}}

.kpi-value {{
    font-size: 1.75rem;
    font-weight: 700;
    color: {TEXT_PRIMARY};
}}

.kpi-trend {{
    font-size: 0.875rem;
    margin-top: 0.5rem;
}}

.kpi-trend.positive {{
    color: {SUCCESS_COLOR};
}}

.kpi-trend.negative {{
    color: {ERROR_COLOR};
}}

/* Upload zone */
.upload-zone {{
    background: linear-gradient(135deg, {BG_CARD} 0%, {BG_PRIMARY} 100%);
    border: 2px dashed {ACCENT_COLOR};
    border-radius: 16px;
    padding: 3rem 2rem;
    text-align: center;
    transition: all 0.3s ease;
}}

.upload-zone:hover {{
    border-color: {PRIMARY_COLOR};
    box-shadow: {SHADOW_LG};
}}

.upload-zone.dragover {{
    border-color: {SUCCESS_COLOR};
    background: linear-gradient(135deg, #ecfdf5 0%, {BG_PRIMARY} 100%);
}}

/* Navigation */
.nav-link {{
    display: block;
    padding: 0.75rem 1rem;
    color: rgba(255,255,255,0.7);
    text-decoration: none;
    border-radius: 8px;
    margin: 0.25rem 0;
    transition: all 0.2s ease;
}}

.nav-link:hover, .nav-link.active {{
    background-color: rgba(255,255,255,0.1);
    color: white;
}}

/* Divider */
.enterprise-divider {{
    height: 1px;
    background: linear-gradient(90deg, transparent, {BORDER_COLOR}, transparent);
    margin: 2rem 0;
}}

/* Status badges */
.badge {{
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 600;
}}

.badge-success {{
    background-color: #d1fae5;
    color: #065f46;
}}

.badge-warning {{
    background-color: #fef3c7;
    color: #92400e;
}}

.badge-error {{
    background-color: #fee2e2;
    color: #991b1b;
}}

.badge-info {{
    background-color: #dbeafe;
    color: #1e40af;
}}

/* Hide default streamlit elements */
footer {{visibility: hidden;}}


/* Custom scrollbar */
::-webkit-scrollbar {{
    width: 8px;
    height: 8px;
}}

::-webkit-scrollbar-track {{
    background: {BG_PRIMARY};
}}

::-webkit-scrollbar-thumb {{
    background: {BORDER_COLOR};
    border-radius: 4px;
}}

::-webkit-scrollbar-thumb:hover {{
    background: {TEXT_MUTED};
}}

/* Chart styling */
[data-testid="stVegaLiteChart"], [data-testid="stDeckGlChart"] {{
    border-radius: {BORDER_RADIUS};
    overflow: hidden;
}}
</style>
"""
