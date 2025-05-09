
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from difflib import get_close_matches

st.set_page_config(page_title="AI Data Analysis Assistant", layout="centered")
st.title("🤖 AI Data Analysis Assistant")
st.markdown("Upload a CSV file and ask me anything about your data!")

# File uploader
uploaded_file = st.file_uploader("📁 Upload your CSV file", type=["csv"])
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
    except UnicodeDecodeError:
        df = pd.read_csv(uploaded_file, encoding="ISO-8859-1")

    st.success(f"✅ File uploaded successfully! Rows: {df.shape[0]}, Columns: {df.shape[1]}")

    # Intent dictionary
    commands = {
        "show_columns": ["show columns", "what are the columns", "list the columns"],
        "show_statistics": ["show statistics", "describe the data", "get data statistics"],
        "show_missing": ["missing values", "null values", "check missing"],
        "plot_line": ["plot line chart", "show line chart", "line plot"],
        "plot_histogram": ["show histogram", "plot histogram"],
        "filter_value": ["filter by value", "filter rows by value"],
        "filter_condition": ["filter by condition", "select rows where"],
        "sort_data": ["sort the data", "order the data", "sort by"],
        "show_top": ["show top rows", "show first rows"],
        "show_bottom": ["show bottom rows", "show last rows"],
        "correlation_heatmap": ["show correlation heatmap", "correlation plot"],
    }

    # Intent detection
    def detect_intent(command):
        command = command.lower()
        for intent, keywords in commands.items():
            if any(kw in command for kw in keywords):
                return intent
        return "unknown"

    # Command box
    user_command = st.text_input("🗨️ Ask something about your data:")
    if user_command:
        intent = detect_intent(user_command)
        st.markdown(f"**🧠 Detected Intent:** `{intent}`")

        if intent == "show_columns":
            st.write("📊 Columns:")
            st.write(df.columns.tolist())

        elif intent == "show_statistics":
            st.write("📈 Summary Statistics:")
            st.write(df.describe())

        elif intent == "show_missing":
            st.write("🧼 Missing Values:")
            st.write(df.isnull().sum())

        elif intent == "plot_line":
            st.write("📉 Line Chart")
            x = st.selectbox("Select X-axis", df.columns)
            y = st.selectbox("Select Y-axis", df.columns)
            fig, ax = plt.subplots()
            sns.lineplot(x=df[x], y=df[y], ax=ax)
            st.pyplot(fig)

        elif intent == "plot_histogram":
            numeric_cols = df.select_dtypes(include='number').columns.tolist()
            col = st.selectbox("Select numeric column", numeric_cols)
            fig, ax = plt.subplots()
            df[col].hist(bins=20, ax=ax)
            st.pyplot(fig)

        elif intent == "filter_value":
            col = st.selectbox("Column to filter", df.columns)
            val = st.text_input("Exact value to match")
            if val:
                filtered = df[df[col].astype(str) == val]
                st.write(filtered)

        elif intent == "filter_condition":
            col = st.selectbox("Column for condition", df.columns)
            op = st.selectbox("Operator", [">", "<", ">=", "<="])
            val = st.text_input("Value to compare")
            if val:
                try:
                    val_num = float(val)
                    if op == ">":
                        filtered = df[df[col] > val_num]
                    elif op == "<":
                        filtered = df[df[col] < val_num]
                    elif op == ">=":
                        filtered = df[df[col] >= val_num]
                    elif op == "<=":
                        filtered = df[df[col] <= val_num]
                    st.write(filtered)
                except:
                    st.error("Invalid numeric value.")

        elif intent == "sort_data":
            col = st.selectbox("Sort by column", df.columns)
            ascending = st.checkbox("Sort ascending?", value=True)
            st.write(df.sort_values(by=col, ascending=ascending))

        elif intent == "show_top":
            st.write(df.head(10))

        elif intent == "show_bottom":
            st.write(df.tail(10))

        elif intent == "correlation_heatmap":
            st.write("🔥 Correlation Heatmap")
            corr = df.corr()
            fig, ax = plt.subplots()
            sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', ax=ax)
            st.pyplot(fig)

        else:
            st.warning("❌ Command not recognized. Try something like 'show statistics' or 'plot histogram'.")
else:
    st.info("Please upload a CSV file to continue.")
