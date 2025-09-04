import streamlit as st
from datetime import datetime
from db_operations import init_db, save_entry, get_entry_by_date, get_all_dates,get_all_entries_by_date
from processor import process_input
import os


# Initialize database
os.makedirs('db', exist_ok=True)
init_db()

# App title
st.title("🌞 ConsciousDay Agent")
st.subheader("Reflect inward. Act with clarity.")

# Tab layout
tab1, tab2 = st.tabs(["New Entry", "Past Entries"])

with tab1:
    with st.form("journal_form"):
        journal = st.text_area("Morning Journal", placeholder="How are you feeling today? What's on your mind?")
        intention = st.text_input("Intention of the Day", placeholder="What's your main intention for today?")
        dream = st.text_area("Dream ", placeholder="Did you have any dreams last night?")
        priorities = st.text_input("Top 3 Priorities", placeholder="Comma separated list of your top 3 priorities")

        submitted = st.form_submit_button("Submit")

        if submitted:
            if journal and intention and priorities:
                reflection_strategy = process_input(journal, intention, dream, priorities)
                save_entry(journal, intention, dream, priorities, reflection_strategy, reflection_strategy)
                st.success("Entry saved successfully!")
                st.subheader("Your Daily Insights:")
                st.markdown(reflection_strategy)
            else:
                st.error("Please fill in all required fields")

with tab2:
    st.subheader("View Past Entries")
    dates = get_all_dates()
    if dates:
        selected_date = st.selectbox("Select a date", dates)

        # Get ALL entries for selected date
        entries = get_all_entries_by_date(selected_date)

        # Let user select which entry to view if multiple exist
        if len(entries) > 1:
            entry_index = st.selectbox(
                "Select entry version",
                range(len(entries)),
                format_func=lambda x: f"Entry {x + 1} ({entries[x][1].split()[1]})"
            )
            entry = entries[entry_index]
        else:
            entry = entries[0]

        if entry:
            st.write(f"### Entry for {selected_date}")
            st.write(f"**Journal:** {entry[3]}")  # Adjusted indexes
            st.write(f"**Intention:** {entry[4]}")
            st.write(f"**Dream:** {entry[5]}")
            st.write(f"**Priorities:** {entry[6]}")
            st.write("---")
            st.write("**Reflection & Strategy:**")
            st.markdown(entry[7])
    else:
        st.info("No past entries found.")
