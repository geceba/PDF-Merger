# ui/styles.py

# ==================================
# COLOR PALETTES & VARIABLES
# ==================================
COLOR_PRIMARY = "#ebecfc"       # Main blue
COLOR_PRIMARY_HOVER = "#ebecfc" # Hover state for primary buttons
COLOR_ACCENT = "#38BDF8"        # Accent color for highlights and active states
COLOR_DARK = "#0F172A"          # Dark text
COLOR_TEXT_MUTED = "#64748B"    # Muted text for secondary information
COLOR_BORDER = "#E2E8F0"        # Light border color for cards and inputs
COLOR_BG_APP = "#F7F8FC"        # Background color for the entire app
COLOR_BG_CARD = "#FFFFFF"       # Background color for cards and panels
COLOR_BRAND_PURPLE = "#4F46E5"     # Brand purple for logos and key highlights
COLOR_BG_ACTIVE = "#EEF2FF"     # Light purple background for active states
COLOR_BORDER = "#E2E8F0"        # Light border color for cards and inputs

COLOR_PRIVACY_BANNER_BG = "#F0FDF4"   # Light background for privacy banner
COLOR_PRIVACY_BORDER = "#DCFCE7"              # Border color for privacy banner
COLOR_FONT_PRIVACY_BANNER = "#166534"              # Font color for privacy banner text
# ==================================
# Stylesheets (QSS) for reusable components
# ==================================

BODY_CONTAINER_STYLE = f"""
    background-color: {COLOR_BG_APP};
    font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
"""

SIDEBAR_STYLE = f"""
    SidebarWidget {{
        background-color: {COLOR_BG_APP};
    }}
    
    QLabel#LogoTitle {{ 
        font-size: 18px; 
        font-weight: 800;
        color: {COLOR_DARK};
        margin-bottom: 12px;
    }}
    
    QLabel#LogoSubtitle {{
        font-size: 11px;
        color: {COLOR_TEXT_MUTED};
    }}
    
    QPushButton.SidebarBtn,
    QPushButton.SidebarBtn[active="false"],
    QPushButton.SidebarBtn:unchecked  {{
        background-color: transparent;
        border: none;
        border-radius: 8px;
        color: {COLOR_TEXT_MUTED};
        font-size: 13px;
        font-weight: 600;
        padding: 10px 14px;
        text-align: left;
    }}
    
    QPushButton.SidebarBtn:hover {{
        background-color: {COLOR_PRIMARY_HOVER};
        color: {COLOR_BRAND_PURPLE};
        font-weight: 600;
    }}
    
    QPushButton.SidebarBtn[active="true"],
    QPushButton.SidebarBtn:checked {{
        color: {COLOR_BRAND_PURPLE};
        font-weight: 600;
    }}

    # Privacy Banner
    PrivacyBannerWidget {{
        background-color: {COLOR_PRIVACY_BANNER_BG};
        border: 1px solid {COLOR_PRIVACY_BORDER};
        border-radius: 8px;
        padding: 12px;
    }}

    QLabel#PrivacyText {{
        color: {COLOR_FONT_PRIVACY_BANNER};
        font-size: 12px;
        font-weight: 500;
    }}

"""

FILE_LIST_STYLE = f"""
    FileListWidget {{
        background-color: {COLOR_BG_CARD};
        border: 1px solid {COLOR_BORDER};
        border-radius: 12px;
    }}
"""
