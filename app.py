# We're bringing in the tools (libraries) we need to build this app.
# Think of libraries as pre-built toolkits someone else made so we don't have to build everything from scratch.

import streamlit as st          # This is what turns our Python script into a visual web app — buttons, charts, sidebars, all of it
import pandas as pd              # This helps us work with data in table form (rows and columns), like Excel but in Python
import plotly.express as px      # This draws beautiful, interactive charts with very little effort
import plotly.graph_objects as go  # This is the more detailed version of Plotly — gives us extra control over charts

# We're pulling in our own custom functions from a separate file called sql_queries.py
# 'run' runs a database query, 'summary' gets a quick overview, 'core_queries' and 'advanced_queries' are dictionaries of pre-written questions to ask the database
from sql_queries import run, summary, core_queries, advanced_queries


# PAGE CONFIG

# This is the very first thing Streamlit needs — it sets up how our web page looks before anything else appears
st.set_page_config(
    page_title="Expense Analytics Dashboard",  # This is the name that shows on the browser tab
    page_icon="💳",                             # This little icon appears on the browser tab too
    layout="wide",                             # This makes the page use the full width of the screen instead of a narrow column
    initial_sidebar_state="expanded",          # This makes the left sidebar open by default when someone visits
)


# CUSTOM CSS

# Here we're writing CSS (styling rules) directly inside our Python file
# CSS controls how things look: colours, fonts, spacing, shadows etc.
# 'unsafe_allow_html=True' means we're telling Streamlit "yes, we know this is raw HTML/CSS, let it through"
st.markdown("""
<style>
/* We're loading two special fonts from Google's free font library */
/* DM Sans is a clean modern font for general text */
/* Playfair Display is an elegant serif font great for headings */
/* Hide the Streamlit sidebar key watermark */
[data-testid="stSidebarHeader"] {
    display: none;
}
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

/* Apply DM Sans font to everything on the page */
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

/* Set a soft gradient as the background of the whole app */
/* 135deg means the gradient goes diagonally */
.stApp {
    background: linear-gradient(135deg, #f0f4ff 0%, #fdf6ff 50%, #f0fbff 100%);
}

/* Style the left sidebar — white at top fading to a soft purple at the bottom */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ffffff 0%, #f8f0ff 100%);
    border-right: 1px solid #e8e0f0;  /* Thin line on the right edge of the sidebar */
}
/* Make sure text inside the sidebar also uses DM Sans */
section[data-testid="stSidebar"] * { font-family: 'DM Sans', sans-serif; }

/* ── KPI Cards — these are the big number boxes at the top of the overview page ── */
.kpi-card {
    background: white;                                          /* White background */
    border-radius: 16px;                                        /* Rounded corners */
    padding: 24px 20px;                                         /* Space inside the card */
    box-shadow: 0 4px 24px rgba(120, 80, 200, 0.07);           /* Soft purple shadow underneath */
    border: 1px solid rgba(200, 180, 255, 0.25);               /* Very faint purple border */
    transition: transform 0.2s ease, box-shadow 0.2s ease;     /* Smooth animation when hovered */
    margin-bottom: 12px;                                        /* Space below each card */
}
/* When someone hovers over a KPI card, it floats up slightly */
.kpi-card:hover {
    transform: translateY(-3px);                               /* Move 3px upward */
    box-shadow: 0 8px 32px rgba(120, 80, 200, 0.13);           /* Bigger shadow to look lifted */
}
/* The small label text at the top of the card */
.kpi-label {
    font-size: 12px; font-weight: 600; letter-spacing: 0.08em;
    text-transform: uppercase; color: #9b8ab0; margin-bottom: 6px;
}
/* The big number shown in the card */
.kpi-value {
    font-family: 'Playfair Display', serif; font-size: 28px;
    font-weight: 700; color: #2d1b69; margin: 0;
}
/* The emoji icon at the top of the card */
.kpi-icon { font-size: 28px; margin-bottom: 10px; }

/* ── Stat Cards — colourful boxes used for showing single values like totals ── */
.stat-card {
    border-radius: 16px;
    padding: 22px 20px;
    margin-bottom: 8px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    transition: transform 0.2s ease;  /* Smooth hover animation */
}
/* Float up a little when hovered */
.stat-card:hover { transform: translateY(-2px); }
/* Label inside the stat card */
.stat-label {
    font-size: 11px; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; opacity: 0.75; margin-bottom: 4px;
}
/* The actual value shown in the stat card */
.stat-value {
    font-family: 'Playfair Display', serif;
    font-size: 26px; font-weight: 700; margin: 0;
}
/* A small subtitle below the value — like extra context */
.stat-sub { font-size: 12px; opacity: 0.65; margin-top: 4px; }

/* ── Insight Box — the small highlighted tip shown below each chart ── */
.insight-box {
    background: linear-gradient(135deg, #f8f5ff 0%, #f0fbff 100%);  /* Soft gradient background */
    border-left: 4px solid #7c5cbf;                                   /* Purple strip on the left side */
    border-radius: 0 12px 12px 0;                                     /* Rounded only on the right side */
    padding: 12px 16px;
    font-size: 13px; color: #4a3b6e;
    line-height: 1.7; margin-top: 8px;
}

/* ── Analysis Block — the written paragraph analysis section ── */
.analysis-block {
    background: white; border-radius: 16px; padding: 28px 32px;
    box-shadow: 0 4px 24px rgba(100, 80, 180, 0.07);
    border: 1px solid rgba(200, 190, 240, 0.2);
    line-height: 1.9; color: #3a2d55; font-size: 15px;
}
/* Heading style inside the analysis block */
.analysis-block h3 {
    font-family: 'Playfair Display', serif; color: #2d1b69;
    font-size: 20px; margin-bottom: 14px;
}
/* The .highlight class puts a gradient background behind certain words to make them stand out */
.highlight {
    background: linear-gradient(90deg, #e8d5ff, #d5eeff);
    border-radius: 6px; padding: 2px 8px;
    font-weight: 600; color: #2d1b69;
}

/* Page header — the title and subtitle at the top of each section */
.page-header { padding: 10px 0 4px 0; margin-bottom: 28px; }
.page-header h1 {
    font-family: 'Playfair Display', serif; font-size: 32px;
    font-weight: 700; color: #2d1b69; margin: 0;
}
.page-header p { color: #9b8ab0; font-size: 14px; margin: 4px 0 0 0; }

/* Footer — the small text at the very bottom of the page */
.footer {
    text-align: center; color: #b0a0c8; font-size: 12px;
    padding: 32px 0 16px 0; border-top: 1px solid #ede8f8; margin-top: 40px;
}

/* Style the built-in Streamlit metric boxes with a white card look */
div[data-testid="stMetric"] {
    background: white; border-radius: 12px; padding: 16px;
    border: 1px solid rgba(200, 180, 255, 0.2);
}

/* Style the download button with a purple-to-blue gradient */
.stDownloadButton > button {
    background: linear-gradient(90deg, #7c5cbf, #5ba8d4);
    color: white; border: none; border-radius: 8px;
    font-size: 12px; padding: 6px 16px; font-family: 'DM Sans', sans-serif;
}
/* Slightly fade the button when hovered */
.stDownloadButton > button:hover { opacity: 0.88; }
</style>
""", unsafe_allow_html=True)


# CONSTANTS


# A list of nice colours to use across all charts — these are hex colour codes
# Think of this as a colour palette we've picked out in advance
PASTEL_COLORS = [
    "#7c5cbf", "#5ba8d4", "#e88fc7", "#5dcfb0",
    "#f0a070", "#a0c878", "#9b6ec8", "#60b8c8",
    "#d478a0", "#78c8a0", "#f0b060", "#7888d4",
]

# These are the colour themes for the colourful stat cards
# Each theme has a 'bg' (background gradient) and 'color' (text colour)
CARD_THEMES = [
    {"bg": "linear-gradient(135deg,#ede0ff,#d5eeff)", "color": "#2d1b69"},
    {"bg": "linear-gradient(135deg,#d5f5ec,#a8edea)", "color": "#1a4d3a"},
    {"bg": "linear-gradient(135deg,#ffecd2,#ffb347aa)", "color": "#7a3010"},
    {"bg": "linear-gradient(135deg,#ffd6e7,#ffb3c1)", "color": "#7a1035"},
    {"bg": "linear-gradient(135deg,#d0f0fd,#a8edea)", "color": "#0a4a5e"},
    {"bg": "linear-gradient(135deg,#e0ffe0,#b7f0b7)", "color": "#1a4d1a"},
]

# A dictionary to convert month numbers into short names
# e.g. 1 → "Jan", 2 → "Feb" ... this is used when showing months on charts
MONTH_MAP = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
             7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}

# A dictionary to convert quarter numbers to labels like "Q1", "Q2" etc.
QUARTER_MAP = {1:"Q1",2:"Q2",3:"Q3",4:"Q4"}

# Layout settings shared across all Plotly charts so they all look consistent
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",  # Transparent outer background
    plot_bgcolor="rgba(0,0,0,0)",   # Transparent inner chart area
    font=dict(family="DM Sans", color="#3a2d55"),  # Font family and colour for all chart text
    margin=dict(t=36, b=30, l=20, r=20),           # Space around the chart (top, bottom, left, right)
    legend=dict(bgcolor="rgba(255,255,255,0.8)", borderwidth=0),  # Semi-transparent legend box
)

# This maps internal database column names to friendlier readable labels
# e.g. "total_spent" becomes "Total Spent (₹)" on the screen
LABEL_MAP = {
    "total_spent": "Total Spent (₹)", "amount_paid": "Amount Paid (₹)",
    "total_cashback": "Cashback Earned (₹)", "avg_spent": "Avg Spent (₹)",
    "daily_avg": "Daily Avg Spend (₹)", "max_spent": "Max Spend (₹)",
    "min_spent": "Min Spend (₹)", "total_transactions": "No. of Transactions",
    "total_no_cashback": "Transactions Without Cashback",
    "frequency": "No. of Transactions", "total": "Transaction Count",
    "cashback_percent": "Cashback Rate (%)",
    "cashback_efficiency_percent": "Cashback Efficiency (%)",
    "high_value_percent": "High-Value Transactions (%)",
    "percentage": "Share of Total Spend (%)",
    "avg_weekend": "Avg Weekend Spend (₹)",
    "avg_weekday": "Avg Weekday Spend (₹)",
    "range_start": "Spend Range (₹)",
    "day_type": "Day Type", "payment_mode": "Payment Mode",
    "category": "Category", "year": "Year",
    "Month": "Month", "Quarter": "Quarter",
    "cashback": "Cashback (₹)", "id": "Transaction ID",
    "date": "Date",
}

# These are query names that should be shown as a plain table instead of a chart
# because they return full transaction details, not just summary numbers
TABLE_QUERIES = {
    "cashback transactions",
    "above average transactions",
    "highest cashback transaction",
}


# This is a helper function — a small reusable action
# It takes a column name and returns its friendly readable version using LABEL_MAP above
# If it's not in the map, it just cleans up the name (removes underscores, capitalises)
def friendly(col):
    return LABEL_MAP.get(col, col.replace("_", " ").title())


# CHART HELPERS


# This function draws a bar chart using Plotly
# df = the data (table), x = horizontal axis column, y = vertical axis column, title = chart heading
def styled_bar(df, x, y, title=""):
    # Find all text (non-number) columns — we'll use the first one for bar colours
    str_cols = df.select_dtypes("object").columns.tolist()
    # Use the first text column for colouring, or fall back to x if none found
    color_col = str_cols[0] if str_cols else x
    # Create the bar chart using plotly express
    fig = px.bar(df, x=x, y=y, title=title,
                 color=color_col,
                 color_discrete_sequence=PASTEL_COLORS,  # Use our custom colour palette
                 template="plotly_white")
    # Apply our shared layout settings, and add axis labels using friendly names
    fig.update_layout(**PLOTLY_LAYOUT,
                      xaxis_title=friendly(x),
                      yaxis_title=friendly(y))
    # Remove bar outlines and make them slightly transparent
    fig.update_traces(marker_line_width=0, opacity=0.88)
    return fig  # Return the finished chart so it can be displayed


# This function draws a donut / pie chart
# names = the label column, values = the number column
def styled_pie(df, names, values, title=""):
    fig = px.pie(df, names=names, values=values, title=title,
                 color_discrete_sequence=PASTEL_COLORS,
                 template="plotly_white", hole=0.38)  # hole=0.38 makes it a donut shape
    fig.update_layout(**PLOTLY_LAYOUT)
    # Show both the percentage AND label text inside each slice
    fig.update_traces(textposition="inside", textinfo="percent+label")
    return fig


# This function draws a line chart — great for showing trends over time
def styled_line(df, x, y, title=""):
    fig = px.line(df, x=x, y=y, title=title,
                  color_discrete_sequence=PASTEL_COLORS,
                  template="plotly_white", markers=True)  # markers=True adds dots at each data point
    fig.update_layout(**PLOTLY_LAYOUT,
                      xaxis_title=friendly(x),
                      yaxis_title=friendly(y))
    fig.update_traces(line_width=2.5, marker_size=7)  # Slightly thick line and visible dots
    return fig


# This function adds a "Download CSV" button below a chart
# When clicked, it lets the user save the data as a spreadsheet file
def download_btn(df, label="Download CSV", filename="data.csv"):
    csv = df.to_csv(index=False).encode("utf-8")  # Convert the data table to CSV text format
    st.download_button(label=f"⬇ {label}", data=csv,
                       file_name=filename, mime="text/csv")  # Create the download button


# COLOURFUL STAT CARD HELPER


# This function draws one colourful stat card on the screen
# label = title shown at top, value = big number/text, sub = small description below, theme_idx = which colour theme to use
def stat_card(label, value, sub="", theme_idx=0):
    # Pick a colour theme from CARD_THEMES, cycling through them using % (modulo)
    t = CARD_THEMES[theme_idx % len(CARD_THEMES)]
    # If a subtitle was given, wrap it in HTML — otherwise leave it empty
    sub_html = f"<div class='stat-sub'>{sub}</div>" if sub else ""
    # Write out the HTML for the card using the chosen colours and content
    st.markdown(f"""
    <div class='stat-card' style='background:{t["bg"]};color:{t["color"]}'>
        <div class='stat-label'>{label}</div>
        <div class='stat-value'>{value}</div>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)



# CACHED DATA LOADERS

# @st.cache_data(ttl=300) means: remember the result of this function for 5 minutes (300 seconds)
# so if someone clicks around the app, it doesn't re-query the database every single time
# This speeds things up significantly

@st.cache_data(ttl=300)
def load_summary():
    # Call the summary() function from our sql_queries file and return the result
    return summary()

@st.cache_data(ttl=300)
def load_core(name):
    # Run a specific core query by name (looked up from our core_queries dictionary)
    return run(core_queries[name])

@st.cache_data(ttl=300)
def load_advanced(name):
    # Same idea but for advanced queries
    return run(advanced_queries[name])

@st.cache_data(ttl=300)
def load_all_expenses():
    # Fetch every single row from the expenses table in the database
    return run("SELECT * FROM expenses")


# SIDEBAR


# Everything inside this 'with' block appears in the left sidebar
with st.sidebar:
    st.markdown("### 💳 Expense Tracker")  # Bold heading at the top of the sidebar
    st.markdown("---")                     # A horizontal line (divider)

    # A radio button group — the user picks one of three pages to view
    nav = st.radio(
        "Navigate",
        ["Financial Performance Overview",
         "Operational Analytics",
         "Strategic Financial Insights"],
        label_visibility="collapsed",  # Hide the "Navigate" label since it's obvious
    )

    st.markdown("---")
    st.markdown("**🔍 Filters**")  # Bold heading for the filters section

    # Try to load all expense data to build the filters
    # If something goes wrong, show an error instead of crashing
    try:
        df_all = load_all_expenses()                       # Load all data from the database
        df_all["date"] = pd.to_datetime(df_all["date"])   # Convert the date column to actual date objects

        # Find the earliest and latest dates in the data — used as limits for the date picker
        min_d = df_all["date"].min().date()
        max_d = df_all["date"].max().date()

        # Show a date range picker — user can select a start and end date
        date_range = st.date_input("Date Range", value=(min_d, max_d),
                                   min_value=min_d, max_value=max_d)

        # Get a sorted list of all unique category names, then show as a multi-select checkbox list
        categories = sorted(df_all["category"].dropna().unique().tolist())
        sel_cat = st.multiselect("Category", categories, default=categories)  # All selected by default

        # Same thing for payment modes
        pay_modes = sorted(df_all["payment_mode"].dropna().unique().tolist())
        sel_pay = st.multiselect("Payment Mode", pay_modes, default=pay_modes)

        # Create a filter mask — a True/False list for each row, showing which rows match all selected filters
        mask = (
            (df_all["date"].dt.date >= date_range[0]) &   # Date is within selected range
            (df_all["date"].dt.date <= date_range[1]) &
            (df_all["category"].isin(sel_cat)) &           # Category is in selected list
            (df_all["payment_mode"].isin(sel_pay))         # Payment mode is in selected list
        )
        # Apply the filter — only keep rows where all conditions are True
        df_filtered = df_all[mask].copy()

    except Exception as e:
        st.error(f"Filter error: {e}")      # Show the error message if something went wrong
        df_filtered = pd.DataFrame()        # Use an empty table as fallback

    st.markdown("---")
    # A tiny note reminding users where the filters apply
    st.caption("💡 Filters apply to Financial Performance Overview only.")



# RENDER CHART — smart dispatcher


# This is the most important display function — it looks at the data and the title,
# figures out the best way to show it (pie, bar, line, table, or a single stat card),
# and draws it on the screen
def render_chart(df, title, theme_idx=0):
    # If there's no data, show a simple "no data" message and stop
    if df is None or df.empty:
        st.info("No data available.")
        return

    title_lower = title.lower()  # Lowercase the title so comparisons are case-insensitive
    df = df.copy()               # Make a copy so we don't accidentally change the original data

    # ── Clean up time columns — replace numbers with readable labels ──

    # If there's a "month" column with numbers (1, 2, 3...), convert to names (Jan, Feb, Mar...)
    if "month" in df.columns:
        df["month"] = pd.to_numeric(df["month"], errors="coerce").map(MONTH_MAP)
        df.rename(columns={"month": "Month"}, inplace=True)  # Rename to capital "Month"

    # Same for quarters — convert 1,2,3,4 → Q1,Q2,Q3,Q4
    if "quarter" in df.columns:
        df["quarter"] = pd.to_numeric(df["quarter"], errors="coerce").map(QUARTER_MAP)
        df.rename(columns={"quarter": "Quarter"}, inplace=True)

    # Convert year numbers to string so they show as "2023" not 2023.0
    if "year" in df.columns:
        df["year"] = df["year"].astype(int).astype(str)

    # Get lists of all column names, all number columns, and all text columns
    cols     = df.columns.tolist()
    num_cols = df.select_dtypes("number").columns.tolist()   # e.g. ["total_spent", "cashback"]
    str_cols = df.select_dtypes("object").columns.tolist()   # e.g. ["category", "payment_mode"]


    # 1. TABLE QUERIES (SELECT * multi-row)

    # If this query is in our "show as table" list, handle it specially
    if title_lower in TABLE_QUERIES:
        # Special case: if it's the highest cashback query AND there's just one row, show a stat card layout
        if "highest cashback transaction" in title_lower and len(df) == 1:
            row     = df.iloc[0]                                    # Grab the single row
            date_v  = str(row.get("date",""))[:10]                  # Get just the date part (first 10 characters)
            cat_v   = row.get("category","N/A")
            amt_v   = float(row.get("amount_paid", 0))
            cb_v    = float(row.get("cashback", 0))
            pay_v   = row.get("payment_mode","N/A")
            # Show each field in its own colourful stat card
            stat_card("📅 Transaction Date", date_v, "", theme_idx % 6)
            c1, c2 = st.columns(2)
            with c1: stat_card("🏷️ Category", cat_v, "", (theme_idx+1) % 6)
            with c2: stat_card("💳 Payment Mode", pay_v, "", (theme_idx+2) % 6)
            c3, c4 = st.columns(2)
            with c3: stat_card("💰 Amount Paid", f"₹{amt_v:,.2f}", "", (theme_idx+3) % 6)
            with c4: stat_card("🎁 Cashback Earned", f"₹{cb_v:,.2f}", "Highest cashback in dataset", (theme_idx+4) % 6)
            return  # Stop here, we're done rendering this card

        # Otherwise, show the data as a plain table
        display_df = df.copy()
        # Format the date column nicely (just "YYYY-MM-DD" format)
        if "date" in display_df.columns:
            display_df["date"] = pd.to_datetime(display_df["date"]).dt.strftime("%Y-%m-%d")
        st.dataframe(display_df, use_container_width=True, hide_index=True)  # Show table without row numbers
        return


    # 2. SPECIAL SINGLE-ROW NAMED QUERIES

    # Highest spending month — show as a stat card with the month name and total
    if ("highest spending month" in title_lower or "lowest spending month" in title_lower) and len(df) <= 2:
        month_v = df["Month"].iloc[0] if "Month" in df.columns else "N/A"      # Get first value in Month column
        spent_v = float(df["total_spent"].iloc[0]) if "total_spent" in df.columns else 0
        icon    = "📈" if "highest" in title_lower else "📉"                    # Pick icon based on whether it's high or low
        lbl     = "Peak Spending Month" if "highest" in title_lower else "Lowest Spending Month"
        stat_card(f"{icon} {lbl}", month_v,
                  f"Total spent: ₹{spent_v:,.2f}", theme_idx % 6)
        return

    # Top category by share — show category name and its % of total spending
    if "top category share" in title_lower and len(df) == 1:
        cat_v = df["category"].iloc[0] if "category" in df.columns else "N/A"
        pct_v = float(df["percentage"].iloc[0]) if "percentage" in df.columns else 0
        stat_card("🏆 Top Spending Category", cat_v,
                  f"Accounts for {pct_v:.2f}% of total spending", theme_idx % 6)
        return

    # Most used payment mode — show mode name and how many times it was used
    if "most used payment mode" in title_lower and len(df) == 1:
        mode_v  = df["payment_mode"].iloc[0] if "payment_mode" in df.columns else "N/A"
        count_v = int(df["total"].iloc[0]) if "total" in df.columns else 0
        stat_card("💳 Most Used Payment Mode", mode_v,
                  f"Used in {count_v:,} transactions", theme_idx % 6)
        return

    # Transactions with no cashback — just show the count
    if "transactions with no cashback" in title_lower and len(df) == 1:
        col_v = "total_no_cashback" if "total_no_cashback" in df.columns else df.columns[0]
        count_v = int(df[col_v].iloc[0])
        stat_card("🚫 Transactions Without Cashback",
                  f"{count_v:,} transactions",
                  "These transactions earned no cashback reward", theme_idx % 6)
        return

    # Spending by year — show as a bar chart (might be a single row if only one year of data)
    if "spending trend by year" in title_lower:
        if "year" in df.columns and "total_spent" in df.columns:
            fig = styled_bar(df, "year", "total_spent", title)
            st.plotly_chart(fig, use_container_width=True)
            return


    # 3. GENERIC SINGLE-VALUE SCALARS


    # If the result is just one cell — one row, one column — show it as a big stat card
    if len(df) == 1 and len(df.columns) == 1:
        val      = df.iloc[0, 0]                # Grab the single value
        col_name = df.columns[0]
        # Check if it's a percentage value based on the column name
        is_pct   = any(k in col_name.lower() for k in
                       ["percent","ratio","efficiency","high_value","percentage"])
        # Format it appropriately — % or ₹
        fmt_val  = f"{float(val):.2f}%" if is_pct else f"₹{float(val):,.2f}"
        stat_card(friendly(col_name), fmt_val, "", theme_idx % 6)
        return

    # One row with one number column (like weekend vs weekday average)
    if len(df) == 1 and len(num_cols) == 1:
        val      = df[num_cols[0]].iloc[0]
        col_name = num_cols[0]
        is_pct   = any(k in col_name.lower() for k in
                       ["percent","ratio","efficiency","high_value"])
        fmt_val  = f"{float(val):.2f}%" if is_pct else f"₹{float(val):,.2f}"
        stat_card(friendly(col_name), fmt_val, "", theme_idx % 6)
        return


    # 4. CHART ROUTING


    # Now we try to figure out which chart type fits best for multi-row data
    try:
        # If the title matches any of these keywords, show a PIE chart
        PIE_KEYS = ["weekday vs weekend", "total spent by payment",
                    "total spent by payment mode", "payment mode cashback",
                    "payment mode efficiency", "cashback by category"]
        if any(k in title_lower for k in PIE_KEYS):
            if str_cols and num_cols:
                # Use the first text column as slice labels, first number column as slice sizes
                fig = styled_pie(df, str_cols[0], num_cols[0], title)
                st.plotly_chart(fig, use_container_width=True)
                return

        # If the title matches any of these keywords, show a LINE chart
        LINE_KEYS = ["monthly spending", "monthly cashback", "quarterly spending",
                     "seasonal", "daily average per month"]
        if any(k in title_lower for k in LINE_KEYS):
            # Figure out what goes on the horizontal axis — Month, Quarter, or the first column
            x_col = ("Month"   if "Month"   in df.columns else
                     "Quarter" if "Quarter" in df.columns else cols[0])
            y_col = num_cols[0] if num_cols else cols[1]
            fig = styled_line(df, x_col, y_col, title)
            st.plotly_chart(fig, use_container_width=True)
            return

        # Default: show a BAR chart for everything else
        if num_cols:
            # Pick the best column for the horizontal axis
            if str_cols:
                x_col = str_cols[0]        # Use text column if available
            elif "Month" in df.columns:
                x_col = "Month"
            elif "Quarter" in df.columns:
                x_col = "Quarter"
            elif "year" in df.columns:
                x_col = "year"
            else:
                x_col = cols[0]            # Just use the first column as a fallback
            y_col = num_cols[0]            # Always use the first number column for height
            fig = styled_bar(df, x_col, y_col, title)
            st.plotly_chart(fig, use_container_width=True)
            return

    except Exception:
        pass  # If something goes wrong drawing a chart, silently move on

    # Last resort — if nothing else worked, just show the raw data as a table
    st.dataframe(df, use_container_width=True, hide_index=True)


# SMART INSIGHT GENERATOR

# This function reads the data and automatically writes a short insight sentence about it
# It figures out what the data is about and picks the right phrasing
def smart_insight(df, title):
    # If there's no data, return a simple message
    if df is None or df.empty:
        return "No data available."

    title_lower = title.lower()
    df = df.copy()

    # Normalise month and quarter columns just like we did in render_chart
    if "month" in df.columns:
        df["month"] = pd.to_numeric(df["month"], errors="coerce").map(MONTH_MAP)
        df.rename(columns={"month": "Month"}, inplace=True)
    if "quarter" in df.columns:
        df["quarter"] = pd.to_numeric(df["quarter"], errors="coerce").map(QUARTER_MAP)
        df.rename(columns={"quarter": "Quarter"}, inplace=True)
    if "year" in df.columns:
        df["year"] = df["year"].astype(str)

    num_cols = df.select_dtypes("number").columns.tolist()
    str_cols = df.select_dtypes("object").columns.tolist()

    # For table-type queries, return a count of records or the highest cashback amount
    if title_lower in TABLE_QUERIES:
        if "highest cashback" in title_lower and len(df) == 1:
            cb_v = float(df.get("cashback", pd.Series([0])).iloc[0])
            return f"Highest cashback of <b>₹{cb_v:,.2f}</b> earned in a single transaction."
        return f"Showing <b>{len(df)}</b> matching transaction records."

    # Custom messages for specific known queries
    if "highest spending month" in title_lower and len(df) <= 2:
        m = df["Month"].iloc[0] if "Month" in df.columns else "N/A"
        v = float(df["total_spent"].iloc[0]) if "total_spent" in df.columns else 0
        return f"Spending peaked in <b>{m}</b> at <b>₹{v:,.2f}</b>."

    if "lowest spending month" in title_lower and len(df) <= 2:
        m = df["Month"].iloc[0] if "Month" in df.columns else "N/A"
        v = float(df["total_spent"].iloc[0]) if "total_spent" in df.columns else 0
        return f"Spending was lowest in <b>{m}</b> at <b>₹{v:,.2f}</b>."

    if "top category share" in title_lower and len(df) == 1:
        cat = df["category"].iloc[0] if "category" in df.columns else "N/A"
        pct = float(df["percentage"].iloc[0]) if "percentage" in df.columns else 0
        return f"<b>{cat}</b> leads with <b>{pct:.2f}%</b> of total expenditure."

    if "most used payment mode" in title_lower and len(df) == 1:
        mode  = df["payment_mode"].iloc[0] if "payment_mode" in df.columns else "N/A"
        count = int(df["total"].iloc[0]) if "total" in df.columns else 0
        return f"<b>{mode}</b> is the most frequently used mode — <b>{count:,}</b> transactions."

    if "transactions with no cashback" in title_lower and len(df) == 1:
        v = int(df.iloc[0, 0])
        return f"<b>{v:,}</b> out of 300 transactions had no cashback benefit."

    if "spending trend by year" in title_lower:
        if "total_spent" in df.columns:
            v = float(df["total_spent"].max())
            return f"Total annual expenditure recorded: <b>₹{v:,.2f}</b>."

    # If no number columns exist, just say how many rows there are
    if not num_cols:
        return f"Showing {len(df)} records."

    val_col   = num_cols[0]       # Use the first number column
    col_lower = val_col.lower()

    # Detect what kind of value this column holds — percentage, count, or money
    is_pct = any(k in col_lower for k in
                 ["percent", "ratio", "efficiency", "high_value", "percentage"])

    # These are the exact column names we know represent counts (not money)
    is_count = col_lower in {
        "total_transactions", "total_no_cashback",
        "frequency", "total", "count"
    }

    # These column names are money-related
    is_money = any(k in col_lower for k in
                   ["spent", "paid", "cashback", "avg", "amount",
                    "max", "min", "daily", "weekly", "weekend", "weekday"])

    # A tiny helper function inside this function — formats a number depending on what type it is
    def fmt(v):
        if is_pct:              return f"{float(v):.2f}%"
        if is_count:            return f"{int(v):,} transactions"
        if is_money or True:    return f"₹{float(v):,.2f}"  # Default is to treat as money

    # If it's a single value, write a one-sentence insight about it
    if len(df) == 1:
        v = df[val_col].iloc[0]
        if is_pct:   return f"Overall rate: <b>{float(v):.2f}%</b>."
        if is_count: return f"Total count: <b>{int(v):,}</b> transactions."
        return f"Recorded value: <b>₹{float(v):,.2f}</b>."

    # Find the highest value in the column
    top_val = df[val_col].max()

    # If there's a time column (Month, Quarter, Year), mention the peak period
    time_col = next((c for c in ["Month", "Quarter", "year"] if c in df.columns), None)
    if time_col:
        idx      = df[val_col].idxmax()        # Get the row index of the highest value
        peak_lbl = df.loc[idx, time_col]       # Get the time label of that row
        return f"Peak in <b>{peak_lbl}</b> with {fmt(top_val)}."

    # If there's a category/text column, mention which category had the highest value
    if str_cols:
        idx       = df[val_col].idxmax()
        top_label = df.loc[idx, str_cols[0]]
        col_title = friendly(str_cols[0])
        return f"Highest {col_title}: <b>{top_label}</b> — {fmt(top_val)}."

    # Absolute fallback — just say what the peak value was
    return f"Peak value: {fmt(top_val)}."


# PAGE 1 — FINANCIAL PERFORMANCE OVERVIEW


# This is the main overview/summary page — shows KPI cards, charts, and a written analysis
def page_summary():
    # Show the page heading and subtitle using our custom CSS class
    st.markdown("""
    <div class='page-header'>
        <h1>Personal Finance Performance Report</h1>
        <p>Data-driven analysis of spending behaviour, category concentration,
           and cashback effectiveness · All figures in ₹</p>
    </div>
    """, unsafe_allow_html=True)

    # If the filtered data is empty (no rows match the filters), show a warning and stop
    if df_filtered.empty:
        st.warning("No data matches the selected filters.")
        return

    # Calculate the four summary numbers we'll show in the KPI cards
    total_tx    = len(df_filtered)                    # Count how many rows = how many transactions
    total_spent = df_filtered["amount_paid"].sum()    # Add up all the amounts paid
    total_cb    = df_filtered["cashback"].sum()       # Add up all cashback earned
    avg_tx      = df_filtered["amount_paid"].mean()   # Average amount per transaction

    # Create 4 equal columns side by side for the 4 KPI cards
    c1, c2, c3, c4 = st.columns(4)

    # Define the content for each KPI card as a list of tuples
    kpi_cards = [
        (c1, "🧾", "Total Transactions",  f"{total_tx:,}",        "#7c5cbf"),
        (c2, "💰", "Total Expenditure",   f"₹{total_spent:,.2f}", "#5ba8d4"),
        (c3, "🎁", "Total Cashback",      f"₹{total_cb:,.2f}",    "#5dcfb0"),
        (c4, "📊", "Avg Transaction",     f"₹{avg_tx:,.2f}",      "#e88fc7"),
    ]
    # Loop through the list and render each KPI card in its column
    for col, icon, label, value, color in kpi_cards:
        with col:
            st.markdown(f"""
            <div class='kpi-card' style='border-top:4px solid {color}'>
                <div class='kpi-icon'>{icon}</div>
                <div class='kpi-label'>{label}</div>
                <div class='kpi-value'>{value}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)  # Add a small vertical gap

    # Create two side-by-side chart areas
    col_l, col_r = st.columns(2)

    with col_l:
        # Group transactions by month and total up the spending for each month
        df_month = (
            df_filtered.groupby(df_filtered["date"].dt.month)["amount_paid"]
            .sum().reset_index()
            .rename(columns={"date": "Month", "amount_paid": "Total Spent"})
        )
        df_month["Month"] = df_month["Month"].map(MONTH_MAP)  # Convert 1→Jan, 2→Feb etc.

        # Draw a line chart with a shaded area under the line
        fig = px.line(df_month, x="Month", y="Total Spent",
                      title="Monthly Spending Trend",
                      color_discrete_sequence=PASTEL_COLORS,
                      template="plotly_white", markers=True)
        fig.update_layout(**PLOTLY_LAYOUT,
                          xaxis_title="Month",
                          yaxis_title="Total Spent (₹)")
        fig.update_traces(fill="tozeroy",                               # Shade area below the line
                          fillcolor="rgba(124,92,191,0.08)",            # Very transparent purple fill
                          line_color="#7c5cbf",
                          line_width=2.5, marker_size=7)
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        # Group transactions by category and total up spending per category
        df_cat = (
            df_filtered.groupby("category")["amount_paid"]
            .sum().reset_index()
            .rename(columns={"amount_paid": "Total Spent"})
        )
        # Draw a donut chart of category spending
        fig2 = styled_pie(df_cat, "category", "Total Spent", "Spending by Category")
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Now write the automatic text analysis paragraph at the bottom
    if not df_cat.empty:
        # Find which category has the most and least spending
        top_cat  = df_cat.loc[df_cat["Total Spent"].idxmax(), "category"]
        low_cat  = df_cat.loc[df_cat["Total Spent"].idxmin(), "category"]
        top_amt  = df_cat["Total Spent"].max()
        low_amt  = df_cat["Total Spent"].min()

        # Group by month to find which month had most/least spending
        df_m2    = df_filtered.groupby(df_filtered["date"].dt.month)["amount_paid"].sum()
        high_m   = MONTH_MAP.get(int(df_m2.idxmax()), "N/A")
        low_m    = MONTH_MAP.get(int(df_m2.idxmin()), "N/A")

        # Calculate cashback rate as a percentage of total spending
        cb_pct   = (total_cb / total_spent * 100) if total_spent > 0 else 0
        # Count how many transactions actually earned cashback (cashback > 0)
        cb_count = (df_filtered["cashback"] > 0).sum()

        # Render the full written analysis as styled HTML
        st.markdown(f"""
        <div class='analysis-block'>
            <h3>📋 Financial Behaviour Analysis</h3>
            <p>Over the selected period, a total of
            <span class='highlight'>{total_tx:,} transactions</span> were recorded
            amounting to <span class='highlight'>₹{total_spent:,.2f}</span>.
            The average transaction value stood at
            <span class='highlight'>₹{avg_tx:,.2f}</span>, indicating a
            moderate-to-high per-transaction spending pattern consistent with
            regular consumer expenditure across multiple categories.</p>
            <p><strong>Category Insights:</strong> The highest expenditure was
            concentrated in the <span class='highlight'>{top_cat}</span> category,
            totalling ₹{top_amt:,.2f}, suggesting this segment drives the most
            financial outflow. Conversely,
            <span class='highlight'>{low_cat}</span> recorded the lowest spend at
            ₹{low_amt:,.2f}, reflecting either infrequent engagement or lower unit
            costs in that domain.</p>
            <p><strong>Monthly Variation:</strong> Expenditure peaked in
            <span class='highlight'>{high_m}</span> and dipped to its lowest in
            <span class='highlight'>{low_m}</span>. This seasonal variation suggests
            cyclical spending behaviour which may correlate with festive seasons,
            salary cycles, or lifestyle events.</p>
            <p><strong>Cashback Efficiency:</strong> Cashback was earned on
            {cb_count} transactions, yielding a total of
            <span class='highlight'>₹{total_cb:,.2f}</span> — representing a
            <span class='highlight'>{cb_pct:.2f}%</span> effective cashback rate.
            This reflects a disciplined use of reward-driven payment instruments.</p>
        </div>
        """, unsafe_allow_html=True)

    # Show the download button so user can export the filtered data
    download_btn(df_filtered, "Download Filtered Data", "filtered_expenses.csv")


# PAGE 2 — OPERATIONAL ANALYTICS (Core 15)

# This page shows all the "core" pre-written queries — arranged in a 2-column grid
def page_core():
    st.markdown("""
    <div class='page-header'>
        <h1>Core Analytical Insights</h1>
        <p>Foundational spending insights across categories, modes &amp; time</p>
    </div>
    """, unsafe_allow_html=True)

    query_names = list(core_queries.keys())   # Get the list of all core query names

    # Loop through the query names in pairs (2 per row)
    for i in range(0, len(query_names), 2):
        cols = st.columns(2)                  # Create 2 side-by-side columns
        for j, col in enumerate(cols):
            if i + j >= len(query_names):    # If we've run out of queries, stop
                break
            name = query_names[i + j]
            with col:
                try:
                    df = load_core(name)      # Fetch the data for this query
                    with st.expander(f"**{name}**", expanded=True):  # Show in a collapsible box, open by default
                        render_chart(df, name, theme_idx=(i + j))    # Draw the chart
                        insight = smart_insight(df, name)             # Generate the insight text
                        st.markdown(
                            f"<div class='insight-box'>💡 {insight}</div>",
                            unsafe_allow_html=True)                   # Show the insight box
                        download_btn(df, "Download",
                                     f"core_{name.lower().replace(' ','_')}.csv")  # Download button
                except Exception as e:
                    with st.expander(f"**{name}**", expanded=True):
                        st.error(f"Error loading '{name}': {e}")      # Show error if query fails


# PAGE 3 — STRATEGIC FINANCIAL INSIGHTS (Advanced 15)


# This page is exactly like Page 2 but for the "advanced" queries — deeper analysis
def page_advanced():
    st.markdown("""
    <div class='page-header'>
        <h1>Strategic Financial Insights</h1>
        <p>Deep-dive analytical views for advanced understanding of your spending</p>
    </div>
    """, unsafe_allow_html=True)

    query_names = list(advanced_queries.keys())   # Get all advanced query names

    # Same 2-column grid layout as page_core
    for i in range(0, len(query_names), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i + j >= len(query_names):
                break
            name = query_names[i + j]
            with col:
                try:
                    df = load_advanced(name)      # Fetch the data for this advanced query
                    with st.expander(f"**{name}**", expanded=True):
                        render_chart(df, name, theme_idx=(i + j))
                        insight = smart_insight(df, name)
                        st.markdown(
                            f"<div class='insight-box'>💡 {insight}</div>",
                            unsafe_allow_html=True)
                        download_btn(df, "Download",
                                     f"adv_{name.lower().replace(' ','_')}.csv")
                except Exception as e:
                    with st.expander(f"**{name}**", expanded=True):
                        st.error(f"Error loading '{name}': {e}")



# ROUTER


# This is the part that decides which page to show based on what the user clicked in the sidebar
if nav == "Financial Performance Overview":
    page_summary()          # Show the overview/summary page
elif nav == "Operational Analytics":
    page_core()             # Show the core analytics page
elif nav == "Strategic Financial Insights":
    page_advanced()         # Show the advanced insights page


# FOOTER

# Show a small footer at the very bottom of the page — credits and tools used
st.markdown("""
<div class='footer'>
    Financial Analytics Dashboard &nbsp;·&nbsp;
    Built using Python · MySQL · Streamlit · Plotly<br>
</div>
""", unsafe_allow_html=True)
