# Financial Dashboard - Enterprise UI Design System

## Overview

This document details the enterprise-grade UI/UX design system applied to the Streamlit Financial Dashboard. The design follows modern enterprise SaaS principles with a focus on clarity, consistency, and professional aesthetics.

---

## 1. Design Tokens & Variables

### CSS Custom Properties (Design Tokens)

```css
:root {
    /* Primary Colors */
    --primary: #0f172a;           /* Deep Slate - Main brand color */
    --primary-light: #1e293b;     /* Lighter slate for backgrounds */
    
    /* Accent Colors */
    --accent: #0891b2;           /* Cyan - Primary accent */
    --accent-light: #22d3ee;     /* Light cyan */
    
    /* Semantic Colors */
    --success: #059669;           /* Emerald - Positive/Incoming */
    --success-light: #34d399;     /* Light green */
    --warning: #d97706;           /* Amber - Caution states */
    --warning-light: #fbbf24;    /* Light amber */
    --danger: #dc2626;           /* Red - Negative/Expense */
    --danger-light: #f87171;     /* Light red */
    
    /* Secondary Accent */
    --purple: #7c3aed;           /* Purple - Secondary emphasis */
    --purple-light: #a78bfa;    /* Light purple */
    
    /* Neutral Colors */
    --bg: #f1f5f9;               /* Page background */
    --card: #ffffff;              /* Card background */
    --border: #e2e8f0;           /* Subtle borders */
    
    /* Text Colors */
    --text: #0f172a;             /* Primary text */
    --text-secondary: #64748b;   /* Secondary text */
    --text-muted: #94a3b8;       /* Muted/placeholder text */
}
```

### Usage Patterns

| Purpose | Color | Hex | Usage |
|---------|-------|-----|-------|
| Income/Positive | Success | `#059669` | Money coming in |
| Expenses/Negative | Danger | `#dc2626` | Money going out |
| Savings/Net | Accent | `#0891b2` | Balance indicators |
| Recurring/Subscriptions | Purple | `#7c3aed` | Regular payments |
| Warnings/Caution | Warning | `#d97706` | Attention needed |
| Page Background | - | `#f1f5f9` | Streamlit default |
| Card Background | - | `#ffffff` | All cards |
| Borders | - | `#e2e8f0` | Dividers, card edges |

---

## 2. Typography System

### Font Family

```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* { 
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; 
}
```

### Type Scale

| Element | Size | Weight | Usage |
|---------|------|--------|-------|
| Page Title | 1.5rem (24px) | 700 | Main header |
| Section Title | 1.125rem (18px) | 600 | Card headers |
| Card Title | 0.9375rem (15px) | 600 | Small cards |
| Body | 0.875rem (14px) | 400 | Paragraphs |
| Label | 0.8125rem (13px) | 500 | Form labels |
| Caption | 0.75rem (12px) | 400 | Helper text |
| Small Label | 0.6875rem (11px) | 600 | Badges, tags |

### Text Labels (Uppercase)

```css
text-transform: uppercase;
letter-spacing: 0.05em;  /* 0.5px letter spacing for uppercase labels */
```

### Numeric Display

```css
font-feature-settings: 'tnum';  /* Tabular numbers for aligned figures */
```

---

## 3. Spacing System

### Base Unit: 4px

| Name | Value | Usage |
|------|-------|-------|
| xs | 4px (0.25rem) | Tight gaps |
| sm | 8px (0.5rem) | Inner padding |
| md | 12px (0.75rem) | Small gaps |
| base | 16px (1rem) | Standard padding |
| lg | 24px (1.5rem) | Section padding |
| xl | 32px (2rem) | Large padding |

### Component Spacing

| Component | Padding | Margin Bottom | Gap |
|----------|---------|---------------|-----|
| Card | 1.25rem (20px) | 1.5rem (24px) | 1rem (16px) |
| Metric Card | 1.25rem (20px) | - | - |
| List Item | 0.75rem (12px) | 0.5rem (8px) | - |
| Section Header | 1.25rem (20px) | 1rem (16px) | - |

---

## 4. Border Radius

### Scale

| Name | Value | Usage |
|------|-------|-------|
| sm | 6px | Progress bars, small elements |
| base | 8px | Buttons, inputs |
| md | 10px | Small icons |
| lg | 12px | Cards, badges |
| xl | 14px | Section headers |
| 2xl | 16px | Main cards |
| full | 9999px | Pills, badges |

### Usage Examples

```css
.card {
    border-radius: 16px;  /* Main cards */
}

.badge {
    border-radius: 9999px;  /* Pill badges */
}

.icon-box {
    border-radius: 10px;  /* Icon containers */
}
```

---

## 5. Shadows

### Elevation Levels

```css
/* Level 1 - Subtle (Cards) */
box-shadow: 0 1px 3px rgba(0,0,0,0.05), 0 1px 2px rgba(0,0,0,0.1);

/* Level 2 - Elevated (Hover state) */
box-shadow: 0 4px 6px rgba(0,0,0,0.05), 0 2px 4px rgba(0,0,0,0.1);

/* Level 3 - Floating (Modals, Popovers) */
box-shadow: 0 10px 25px rgba(0,0,0,0.1), 0 5px 10px rgba(0,0,0,0.05);

/* Colored Shadows (Icon boxes) */
box-shadow: 0 4px 12px rgba(8,145,178,0.3);  /* Cyan accent */
box-shadow: 0 2px 8px rgba(5,150,105,0.3);   /* Success accent */
box-shadow: 0 2px 8px rgba(220,38,38,0.3);  /* Danger accent */
```

---

## 6. Component Library

### 6.1 Enterprise Card

```css
.enterprise-card {
    background: var(--card);
    border-radius: 16px;
    border: 1px solid var(--border);
    box-shadow: 0 1px 3px rgba(0,0,0,0.05), 0 1px 2px rgba(0,0,0,0.1);
    transition: box-shadow 0.2s ease, transform 0.2s ease;
}

.enterprise-card:hover {
    box-shadow: 0 4px 6px rgba(0,0,0,0.05), 0 2px 4px rgba(0,0,0,0.1);
    transform: translateY(-1px);
}
```

**Usage:** Main container for all dashboard sections

---

### 6.2 Metric Card

```css
.metric-card {
    background: linear-gradient(135deg, var(--card) 0%, #f8fafc 100%);
    border-radius: 12px;
    padding: 1.25rem;
    border: 1px solid var(--border);
    position: relative;
    overflow: hidden;
}

/* Radial decoration overlay */
.metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    width: 100px;
    height: 100px;
    background: radial-gradient(
        circle at top right, 
        var(--accent-color, rgba(8,145,178,0.1)) 0%, 
        transparent 70%
    );
    pointer-events: none;
}
```

**Structure:**
```
┌─────────────────────────────────┐
│ [Icon]  LABEL          ●      │  ← Header with icon and indicator dot
├─────────────────────────────────┤
│                                 │
│     1,234,567                  │  ← Large metric value
│     Subtitle text               │  ← Helper text
│                                 │
└─────────────────────────────────┘
```

---

### 6.3 Badge/Pill

```css
.enterprise-badge {
    display: inline-flex;
    align-items: center;
    padding: 0.375rem 0.75rem;  /* 6px 12px */
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 600;
    gap: 0.375rem;
}

/* Variants */
.badge-success {
    background: #ecfdf5;
    color: #059669;
}

.badge-warning {
    background: #fef3c7;
    color: #d97706;
}

.badge-danger {
    background: #fef2f2;
    color: #dc2626;
}

.badge-purple {
    background: #f5f3ff;
    color: #7c3aed;
}
```

---

### 6.4 List Item

```css
.list-item {
    display: flex;
    align-items: center;
    padding: 0.75rem;
    background: #f8fafc;
    border-radius: 10px;
    margin-bottom: 0.5rem;
    transition: all 0.15s ease;
}

.list-item:hover {
    background: #f1f5f9;
    transform: translateX(2px);  /* Subtle movement on hover */
}
```

---

### 6.5 Progress Bar

```css
.progress-bar {
    width: 100%;
    height: 8px;
    background: #e2e8f0;
    border-radius: 4px;
    overflow: hidden;
}

.progress-bar-fill {
    height: 100%;
    border-radius: 4px;
    transition: width 0.5s ease;
}

/* Gradient fill variant */
.progress-bar-fill {
    background: linear-gradient(90deg, #059669, #059669cc);
}
```

---

### 6.6 Section Header

```css
.section-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1rem;
}

.section-title {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.section-title-icon {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
}

.section-title-text h3 {
    margin: 0;
    font-size: 1rem;
    font-weight: 600;
    color: var(--text);
}

.section-title-text p {
    margin: 0;
    font-size: 0.75rem;
    color: var(--text-muted);
}
```

---

### 6.7 Icon Box

```css
.icon-box {
    width: 36px;
    height: 36px;
    background: linear-gradient(135deg, #0891b2 0%, #0e7490 100%);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 2px 8px rgba(8,145,178,0.3);  /* Colored shadow */
}

/* Sizes */
.icon-box-sm { width: 28px; height: 28px; border-radius: 8px; }
.icon-box-md { width: 36px; height: 36px; border-radius: 10px; }
.icon-box-lg { width: 44px; height: 44px; border-radius: 12px; }
.icon-box-xl { width: 56px; height: 56px; border-radius: 16px; }
```

---

## 7. SVG Icon System

### Design Guidelines

- **Stroke Width:** 2px (consistent across all icons)
- **Line Caps:** `round`
- **Line Joins:** `round`
- **Size:** 18px (default), 22px (large headers)
- **Color:** `stroke="white"` for dark backgrounds, `stroke="currentColor"` for light backgrounds

### Core Icons Used

#### Dashboard/Metrics

```svg
<!-- Bar Chart -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <path d="M3 3v18h18"/>
    <path d="M18 17V9"/>
    <path d="M13 17V5"/>
    <path d="M8 17v-3"/>
</svg>

<!-- Trending Up -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/>
    <polyline points="17 6 23 6 23 12"/>
</svg>

<!-- Trending Down -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <polyline points="23 18 13.5 8.5 8.5 13.5 1 6"/>
    <polyline points="17 18 23 18 23 12"/>
</svg>

<!-- Dollar/Currency -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <line x1="12" y1="1" x2="12" y2="23"/>
    <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
</svg>

<!-- Calendar -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
    <line x1="16" y1="2" x2="16" y2="6"/>
    <line x1="8" y1="2" x2="8" y2="6"/>
    <line x1="3" y1="10" x2="21" y2="10"/>
</svg>

<!-- Clock -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <circle cx="12" cy="12" r="10"/>
    <polyline points="12 6 12 12 16 14"/>
</svg>
```

#### Status Icons

```svg
<!-- Check Circle -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
    <polyline points="22 4 12 14.01 9 11.01"/>
</svg>

<!-- Alert Triangle -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
    <line x1="12" y1="9" x2="12" y2="13"/>
    <line x1="12" y1="17" x2="12.01" y2="17"/>
</svg>

<!-- Info Circle -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <circle cx="12" cy="12" r="10"/>
    <line x1="12" y1="16" x2="12" y2="12"/>
    <line x1="12" y1="8" x2="12.01" y2="8"/>
</svg>
```

#### Category Icons

```svg
<!-- Pie Chart -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <path d="M21.21 15.89A10 10 0 1 1 8 2.83"/>
    <path d="M22 12A10 10 0 0 0 12 2v10z"/>
</svg>

<!-- Trophy -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/>
    <path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/>
    <path d="M4 22h16"/>
    <path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/>
    <path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/>
    <path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/>
</svg>

<!-- Refresh/Recurring -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <polyline points="23 4 23 10 17 10"/>
    <polyline points="1 20 1 14 7 14"/>
    <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>
</svg>

<!-- Credit Card -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <rect x="1" y="4" width="22" height="16" rx="2" ry="2"/>
    <line x1="1" y1="10" x2="23" y2="10"/>
</svg>

<!-- Star -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
</svg>

<!-- Building -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <rect x="2" y="7" width="20" height="14" rx="2" ry="2"/>
    <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>
</svg>
```

#### Navigation/Icons

```svg
<!-- Upload -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
    <polyline points="17 8 12 3 7 8"/>
    <line x1="12" y1="3" x2="12" y2="15"/>
</svg>

<!-- Document -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
    <polyline points="14 2 14 8 20 8"/>
    <line x1="16" y1="13" x2="8" y2="13"/>
    <line x1="16" y1="17" x2="8" y2="17"/>
</svg>

<!-- Grid Pattern -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <rect x="3" y="3" width="7" height="7"/>
    <rect x="14" y="3" width="7" height="7"/>
    <rect x="14" y="14" width="7" height="7"/>
    <rect x="3" y="14" width="7" height="7"/>
</svg>
```

---

## 8. Animation & Transitions

### Timing Functions

```css
/* Quick interactions */
transition: all 0.15s ease;

/* Standard transitions */
transition: all 0.2s ease;

/* Smooth animations */
transition: all 0.3s ease;

/* Progress bars */
transition: width 0.5s ease;
```

### Hover Effects

```css
/* Cards */
.card:hover {
    box-shadow: 0 4px 6px rgba(0,0,0,0.05), 0 2px 4px rgba(0,0,0,0.1);
    transform: translateY(-1px);
}

/* List items */
.list-item:hover {
    background: #f1f5f9;
    transform: translateX(2px);
}

/* Buttons */
.btn:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}
```

---

## 9. Layout Patterns

### Card Grid

```css
/* 2 Column Grid */
display: grid;
grid-template-columns: repeat(2, 1fr);
gap: 1rem;

/* 3 Column Grid */
display: grid;
grid-template-columns: repeat(3, 1fr);
gap: 1rem;

/* 4 Column Grid */
display: grid;
grid-template-columns: repeat(4, 1fr);
gap: 1rem;
```

### Flex Layouts

```css
/* Center aligned */
display: flex;
align-items: center;
justify-content: space-between;

/* Start aligned */
display: flex;
align-items: center;
gap: 1rem;

/* With wrapping */
display: flex;
flex-wrap: wrap;
gap: 1.5rem;
```

---

## 10. Scrollable Containers

```css
.scrollable {
    max-height: 320px;
    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: #cbd5e1 transparent;
}

.scrollable::-webkit-scrollbar {
    width: 6px;
}

.scrollable::-webkit-scrollbar-track {
    background: transparent;
}

.scrollable::-webkit-scrollbar-thumb {
    background-color: #cbd5e1;
    border-radius: 3px;
}
```

---

## 11. Responsive Considerations

### Breakpoints (Streamlit Specific)

| Viewport | Columns | Gap |
|----------|---------|-----|
| Desktop (>1200px) | 4 columns | 1rem |
| Tablet (768-1200px) | 2 columns | 1rem |
| Mobile (<768px) | 1 column | 0.75rem |

### Streamlit Column Usage

```python
# Two equal columns
col1, col2 = st.columns(2)

# Three equal columns
col1, col2, col3 = st.columns(3)

# Four equal columns
col1, col2, col3, col4 = st.columns(4)

# Custom ratios
col1, col2 = st.columns([14, 8])  # 14:8 ratio
```

---

## 12. Color Coding Standards

### Semantic Color Usage

| Context | Positive Color | Negative Color | Neutral |
|---------|----------------|----------------|---------|
| Income | `#059669` (Green) | - | - |
| Expenses | - | `#dc2626` (Red) | - |
| Savings | `#0891b2` (Cyan) | - | - |
| Trend Up | `#059669` (Green) | - | - |
| Trend Down | - | `#dc2626` (Red) | - |
| Weekend | `#d97706` (Amber) | - | - |
| Weekday | `#0891b2` (Cyan) | - | - |
| Status Clear | `#059669` (Green) | - | - |
| Status Warning | - | `#dc2626` (Red) | - |

### Gradient Usage

```css
/* Primary gradient (Dark to Accent) */
background: linear-gradient(135deg, #0f172a 0%, #0891b2 100%);

/* Success gradient */
background: linear-gradient(135deg, #059669 0%, #047857 100%);

/* Warning gradient */
background: linear-gradient(135deg, #d97706 0%, #b45309 100%);

/* Danger gradient */
background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);

/* Purple gradient */
background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%);
```

---

## 13. Implementation Notes

### Streamlit HTML Rendering

1. Use `st.html()` instead of `st.markdown()` with `unsafe_allow_html=True`
2. Build complete HTML strings before rendering
3. Include all nested content in single `st.html()` call
4. Use proper CSS containment with `overflow: hidden`

### Dataframe Styling

```python
# Always use container width
st.dataframe(df, use_container_width=True, hide_index=True)

# Filter columns if needed
existing_cols = [c for c in ["col1", "col2"] if c in df.columns]
st.dataframe(df[existing_cols], use_container_width=True, hide_index=True)
```

### Expander Usage

```python
# Clean expander labels with SVG icons
with st.expander("""
    <svg width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2'>
        <path d='M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z'/>
        <polyline points='14 2 14 8 20 8'/>
    </svg> View Records
""", expanded=False):
    st.dataframe(data)
```

---

## 14. Best Practices Checklist

- [ ] Use Inter font for consistent typography
- [ ] Apply consistent border-radius (16px for cards, 9999px for badges)
- [ ] Use CSS custom properties for colors
- [ ] Add subtle shadows for depth
- [ ] Use SVG icons instead of emojis
- [ ] Maintain 8px spacing grid
- [ ] Use tabular numbers for financial data
- [ ] Apply hover states for interactivity
- [ ] Keep text hierarchy consistent
- [ ] Use semantic colors for data visualization
- [ ] Build complete HTML before rendering
- [ ] Test on mobile/tablet viewports

---

## 15. File Structure

```
finance_audit_system/
├── app/
│   ├── pages/
│   │   └── dashboard.py      # Main dashboard with all UI
│   └── assets/
│       └── logo.png           # Company logo
├── components/
│   └── ui.py                 # Theme and styling utilities
└── requirements.txt          # Dependencies
```

---

## 16. Dependencies

```txt
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.18.0
```

---

*Document Version: 1.0*
*Last Updated: 2026-03-21*
