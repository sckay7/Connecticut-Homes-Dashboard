import os
import streamlit as st
import pandas as pd
import plotly.express as px
import requests


st.title("Connecticut Homes Dashboard")

st.markdown(
    """
This dashboard provides insights into the Connecticut housing market. Explore various metrics and visualizations to understand trends
in home prices, sales volume, and other key indicators.
"""
)


API_BASE = os.getenv("API_BASE", "http://localhost:8000")


def fetch_toptowns():
    url = f"{API_BASE}/v1/towns/toptowns"
    try:
        r = requests.get(url, timeout=20)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        st.error(f"Failed to fetch data from API ({url}): {e}")
        return pd.DataFrame()

    if isinstance(data, dict) and ("x" in data and "y" in data):
        return pd.DataFrame({"Town": data["x"], "Count": data["y"]})

    if isinstance(data, list):
        rows = []
        for doc in data:
            town = doc.get("_id") or doc.get("Town") or doc.get("town")
            cnt = doc.get("count") or doc.get("Count") or doc.get("COUNT(`town`)") or 0
            rows.append({"Town": town, "Count": cnt})
        return pd.DataFrame(rows)

    return pd.DataFrame()

# Fetch distinct towns for user knowledge
def fetch_townslist():
    url = f"{API_BASE}/v1/towns/townslist"
    try:
        r = requests.get(url, timeout=20)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        st.error(f"Failed to fetch data from API ({url}): {e}")
        return []

    towns = data.get("Towns", [])
    if isinstance(towns, list):
        return sorted(towns)
    return []

# Top Towns Bar Chart
st.header("Top Towns")
st.write("This graph shows the top 25 towns by number of houses listed and sold in the dataset.")
df = fetch_toptowns()
if not df.empty:
    df["Count"] = pd.to_numeric(df["Count"], errors="coerce").fillna(0).astype(int)
    df = df.sort_values("Count", ascending=False)

    fig = px.bar(df, x="Town", y="Count", title="Top Towns by Count")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.write("No data available")

# Fetch distinct towns and returns paginated dataframe
distinct_towns = fetch_townslist()
if distinct_towns:
    st.header("Towns List")
    st.write("This is a list of all distinct towns in the dataset.")
    total_towns = len(distinct_towns)
    st.write(f"Total distinct towns: {total_towns}")

    per_page = st.selectbox("Rows per page", [10, 25, 50, 100], index=1, key="towns_per_page_select")

    if "towns_page" not in st.session_state:
        st.session_state["towns_page"] = 1
    if "towns_per_page" not in st.session_state:
        st.session_state["towns_per_page"] = per_page

    if per_page != st.session_state["towns_per_page"]:
        st.session_state["towns_page"] = 1
        st.session_state["towns_per_page"] = per_page

    total_pages = (total_towns - 1) // per_page + 1

    col_prev, col_page, col_next = st.columns([1, 2, 1])
    with col_prev:
        if st.button("Prev", key="prev_towns"):
            if st.session_state["towns_page"] > 1:
                st.session_state["towns_page"] -= 1
    with col_page:
        new_page = st.number_input(
            "Page",
            min_value=1,
            max_value=total_pages,
            value=st.session_state["towns_page"],
            step=1,
            key="towns_page_input",
        )

        st.session_state["towns_page"] = int(max(1, min(total_pages, new_page)))
    with col_next:
        if st.button("Next", key="next_towns"):
            if st.session_state["towns_page"] < total_pages:
                st.session_state["towns_page"] += 1

    start = (st.session_state["towns_page"] - 1) * per_page
    end = start + per_page
    page_items = distinct_towns[start:end]

    st.dataframe(pd.DataFrame({"Towns": page_items}), use_container_width=True)
    st.write(f"Page {st.session_state['towns_page']} of {total_pages}")


