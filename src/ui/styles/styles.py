# ui/styles.py

# ==================================
# COLOR PALETTES & VARIABLES
# ==================================
COLOR_PRIMARY = "#2563EB"       # Main blue
COLOR_PRIMARY_HOVER = "#1D4ED8" # Hover state for primary buttons
COLOR_ACCENT = "#38BDF8"        # Accent color for highlights and active states
COLOR_DARK = "#0F172A"          # Dark text
COLOR_TEXT_MUTED = "#64748B"    # Muted text for secondary information
COLOR_BORDER = "#E2E8F0"        # Light border color for cards and inputs
COLOR_BG_APP = "#F1F5F9"        # Background color for the entire app
COLOR_BG_CARD = "#FFFFFF"       # Background color for cards and panels

# ==================================
# Stylesheets (QSS) for reusable components
# ==================================

BODY_CONTAINER_STYLE = f"""
    background-color: {COLOR_BG_APP};
    font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
"""

SIDEBAR_STYLE = f"""
    SidebarWidget {{
        background-color: {COLOR_BG_CARD};
        border-right: 1px solid {COLOR_BORDER};
    }}
    
    QLabel#LogoTitle {{
        font-size: 18px;
        font-weight: 800;
        color: {COLOR_DARK};
    }}
    
    QLabel#LogoSubtitle {{
        font-size: 11px;
        color: {COLOR_TEXT_MUTED};
    }}
    
    QLabel#SectionHeader {{
        font-size: 13px;
        font-weight: 500;
        color: #94A3B8;
        letter-spacing: 1.5px;
        margin-top: 8px;
        margin-bottom: 8px;
        margin-left: 8px;
    }}
    
    QPushButton {{
        background-color: transparent;
        border: none;
        border-radius: 8px;
        color: {COLOR_TEXT_MUTED};
        font-size: 13px;
        font-weight: 500;
        padding: 10px 14px;
        text-align: left;
    }}
    
    QPushButton:hover {{
        background-color: {COLOR_BG_APP};
        color: {COLOR_DARK};
    }}
    
    QPushButton[active="true"] {{
        background-color: {COLOR_PRIMARY};
        color: {COLOR_BG_CARD};
        font-weight: 600;
    }}
    
    QPushButton[active="true"]:hover {{
        background-color: {COLOR_PRIMARY_HOVER};
    }}

    #SubMenuContainer {{
        background-color: transparent;
        margin-left: 20px;
        border-left: 1px solid #E2E8F0;
        padding-left: 8px;
        margin-top: 4px;
        margin-bottom: 4px;
    }}

    QPushButton.SubMenuButton {{
        font-size: 12px;
        padding: 8px 14px;
        color: {COLOR_TEXT_MUTED};
    }}
    QPushButton.SubMenuButton:hover {{
        background-color: #F1F5F9;
        color: {COLOR_DARK};
    }}
    QPushButton.SubMenuButton[active="true"] {{
        background-color: {COLOR_PRIMARY};
        color: {COLOR_BG_CARD};
    }}
"""

FILE_LIST_STYLE = f"""
    FileListWidget {{
        background-color: {COLOR_BG_CARD};
        border: 1px solid {COLOR_BORDER};
        border-radius: 12px;
    }}
"""
