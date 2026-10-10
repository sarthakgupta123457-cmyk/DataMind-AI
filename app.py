import streamlit as st
import pandas as pd
import io

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="DataMind AI",
    page_icon="🤖",
    layout="wide"
)

# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.title("🤖 DataMind AI")
st.subheader("Intelligent Data Analysis Agent")
st.write(
    "Upload your CSV or Excel dataset and explore your data "
    "with automatic analysis, graphs and simple questions."
)

# -------------------------------------------------
# SAMPLE DATASET
# -------------------------------------------------
def create_sample_data():

    data = {
        "Date": [
            "2026-01-05",
            "2026-01-12",
            "2026-01-18",
            "2026-02-03",
            "2026-02-14",
            "2026-02-22",
            "2026-03-02",
            "2026-03-11",
            "2026-03-25",
            "2026-04-07",
            "2026-04-15",
            "2026-04-20",
            "2026-05-02",
            "2026-05-12",
            "2026-05-20"
        ],

        "Product": [
            "Laptop",
            "Mouse",
            "Keyboard",
            "Laptop",
            "Monitor",
            "Mouse",
            "Laptop",
            "Keyboard",
            "Monitor",
            "Headphones",
            "Laptop",
            "Mouse",
            "Monitor",
            "Headphones",
            "Keyboard"
        ],

        "Category": [
            "Electronics",
            "Accessories",
            "Accessories",
            "Electronics",
            "Electronics",
            "Accessories",
            "Electronics",
            "Accessories",
            "Electronics",
            "Accessories",
            "Electronics",
            "Accessories",
            "Electronics",
            "Accessories",
            "Accessories"
        ],

        "Region": [
            "North",
            "North",
            "West",
            "West",
            "South",
            "East",
            "South",
            "East",
            "North",
            "West",
            "North",
            "South",
            "East",
            "West",
            "North"
        ],

        "Quantity": [
            3, 15, 10, 2, 6,
            25, 4, 18, 8, 20,
            5, 30, 7, 15, 12
        ],

        "Unit_Price": [
            55000,
            800,
            1500,
            55000,
            12000,
            800,
            55000,
            1500,
            12000,
            2500,
            55000,
            800,
            12000,
            2500,
            1500
        ]
    }

    df = pd.DataFrame(data)

    df["Sales"] = df["Quantity"] * df["Unit_Price"]

    return df


# -------------------------------------------------
# DATASET SECTION
# -------------------------------------------------
st.markdown("---")

st.header("📁 Dataset")

st.write("Upload CSV or Excel")

uploaded_file = st.file_uploader(
    "Choose a dataset",
    type=["csv", "xlsx"],
    help="Upload a CSV or Excel file"
)

sample_button = st.button("🧪 Try Sample Dataset")

df = None

# -------------------------------------------------
# READ UPLOADED FILE
# -------------------------------------------------
if uploaded_file is not None:

    try:

        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)

        elif uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)

        st.success(
            f"✅ File uploaded successfully: {uploaded_file.name}"
        )

    except Exception as e:

        st.error(f"❌ Could not read file: {e}")


# -------------------------------------------------
# SAMPLE DATA
# -------------------------------------------------
if sample_button:

    df = create_sample_data()

    st.success("✅ Sample dataset loaded successfully!")


# -------------------------------------------------
# DATA PROCESSING
# -------------------------------------------------
if df is not None:

    # Remove completely empty rows
    df = df.dropna(how="all")

    # Remove completely empty columns
    df = df.dropna(axis=1, how="all")

    # Try to detect date column
    for col in df.columns:

        if "date" in str(col).lower():

            try:
                df[col] = pd.to_datetime(df[col])

            except:
                pass


    # -------------------------------------------------
    # DATASET OVERVIEW
    # -------------------------------------------------
    st.markdown("---")

    st.header("📊 Dataset Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Rows",
            df.shape[0]
        )

    with col2:
        st.metric(
            "Columns",
            df.shape[1]
        )

    with col3:
        st.metric(
            "Missing Values",
            int(df.isnull().sum().sum())
        )

    with col4:
        st.metric(
            "Duplicate Rows",
            int(df.duplicated().sum())
        )


    # -------------------------------------------------
    # DATA PREVIEW
    # -------------------------------------------------
    st.markdown("---")

    st.header("👀 Data Preview")

    st.dataframe(
        df.head(20),
        use_container_width=True
    )


    # -------------------------------------------------
    # COLUMN INFORMATION
    # -------------------------------------------------
    st.markdown("---")

    st.header("🔎 Column Information")

    column_info = pd.DataFrame({
        "Column": df.columns,
        "Data Type": [
            str(df[col].dtype)
            for col in df.columns
        ],
        "Missing Values": [
            int(df[col].isnull().sum())
            for col in df.columns
        ],
        "Unique Values": [
            int(df[col].nunique())
            for col in df.columns
        ]
    })

    st.dataframe(
        column_info,
        use_container_width=True
    )


    # -------------------------------------------------
    # AUTOMATIC GRAPH SECTION
    # -------------------------------------------------
    st.markdown("---")

    st.header("📈 Data Visualization")

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    categorical_columns = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()


    # -------------------------------------------------
    # SALES GRAPHS
    # -------------------------------------------------
    if "Sales" in df.columns:

        st.subheader("💰 Sales Analysis")


        # Sales by Product
        if "Product" in df.columns:

            product_sales = (
                df.groupby("Product")["Sales"]
                .sum()
                .sort_values(ascending=False)
            )

            st.write("### 🛍️ Sales by Product")

            st.bar_chart(product_sales)


        # Sales by Category
        if "Category" in df.columns:

            category_sales = (
                df.groupby("Category")["Sales"]
                .sum()
                .sort_values(ascending=False)
            )

            st.write("### 🏷️ Sales by Category")

            st.bar_chart(category_sales)


        # Sales by Region
        if "Region" in df.columns:

            region_sales = (
                df.groupby("Region")["Sales"]
                .sum()
                .sort_values(ascending=False)
            )

            st.write("### 🌍 Sales by Region")

            st.bar_chart(region_sales)


        # Sales Trend
        date_columns = []

        for col in df.columns:

            if pd.api.types.is_datetime64_any_dtype(df[col]):

                date_columns.append(col)


        if len(date_columns) > 0:

            date_col = date_columns[0]

            trend = (
                df.groupby(date_col)["Sales"]
                .sum()
                .sort_index()
            )

            st.write("### 📅 Sales Trend")

            st.line_chart(trend)


    # -------------------------------------------------
    # QUANTITY GRAPH
    # -------------------------------------------------
    if "Quantity" in df.columns:

        st.markdown("---")

        st.subheader("📦 Quantity Analysis")

        if "Product" in df.columns:

            quantity_product = (
                df.groupby("Product")["Quantity"]
                .sum()
                .sort_values(ascending=False)
            )

            st.write("### 📦 Quantity by Product")

            st.bar_chart(quantity_product)


    # -------------------------------------------------
    # NUMERIC COLUMN GRAPHS
    # -------------------------------------------------
    st.markdown("---")

    st.subheader("📊 Numeric Data Analysis")

    if len(numeric_columns) > 0:

        selected_numeric = st.selectbox(
            "Select numeric column",
            numeric_columns
        )

        st.write(
            f"### Distribution of {selected_numeric}"
        )

        chart_data = df[[selected_numeric]].dropna()

        st.bar_chart(
            chart_data
        )

    else:

        st.info(
            "No numeric columns found in this dataset."
        )


    # -------------------------------------------------
    # ASK DATAMIND AI
    # -------------------------------------------------
    st.markdown("---")

    st.header("💬 Ask DataMind AI")

    st.write(
        "Ask questions about your dataset in simple language."
    )

    question = st.text_input(
        "Ask your question:",
        placeholder="Example: Which product has the highest sales?"
    )


    # -------------------------------------------------
    # QUESTION ANSWERING
    # -------------------------------------------------
    if question:

        q = question.lower().strip()

        # Highest sales product
        if (
            ("highest" in q or "maximum" in q or "top" in q)
            and "sales" in q
            and "product" in q
            and "Product" in df.columns
            and "Sales" in df.columns
        ):

            result = (
                df.groupby("Product")["Sales"]
                .sum()
                .sort_values(ascending=False)
            )

            product = result.index[0]
            value = result.iloc[0]

            st.success(
                f"🤖 DataMind AI: {product} has the highest "
                f"total sales of ₹{value:,.0f}."
            )

            st.dataframe(
                result.reset_index(name="Total Sales"),
                use_container_width=True
            )


        # Lowest sales product
        elif (
            ("lowest" in q or "minimum" in q)
            and "sales" in q
            and "product" in q
            and "Product" in df.columns
            and "Sales" in df.columns
        ):

            result = (
                df.groupby("Product")["Sales"]
                .sum()
                .sort_values()
            )

            product = result.index[0]
            value = result.iloc[0]

            st.success(
                f"🤖 DataMind AI: {product} has the lowest "
                f"total sales of ₹{value:,.0f}."
            )


        # Highest quantity
        elif (
            ("highest" in q or "maximum" in q or "most" in q)
            and "quantity" in q
            and "Product" in df.columns
            and "Quantity" in df.columns
        ):

            result = (
                df.groupby("Product")["Quantity"]
                .sum()
                .sort_values(ascending=False)
            )

            product = result.index[0]
            value = result.iloc[0]

            st.success(
                f"🤖 DataMind AI: {product} has the highest "
                f"total quantity of {value}."
            )


        # Total sales
        elif (
            "total sales" in q
            and "Sales" in df.columns
        ):

            total = df["Sales"].sum()

            st.success(
                f"🤖 DataMind AI: Total sales are "
                f"₹{total:,.0f}."
            )


        # Average sales
        elif (
            "average sales" in q
            and "Sales" in df.columns
        ):

            average = df["Sales"].mean()

            st.success(
                f"🤖 DataMind AI: Average sales are "
                f"₹{average:,.2f}."
            )


        # Number of rows
        elif (
            "rows" in q
            or "records" in q
        ):

            st.success(
                f"🤖 DataMind AI: Your dataset contains "
                f"{len(df)} rows."
            )


        # Number of columns
        elif "columns" in q:

            st.success(
                f"🤖 DataMind AI: Your dataset contains "
                f"{len(df.columns)} columns."
            )


        # Missing values
        elif (
            "missing" in q
            or "null" in q
        ):

            missing = int(
                df.isnull().sum().sum()
            )

            st.success(
                f"🤖 DataMind AI: Your dataset has "
                f"{missing} missing values."
            )


        # Column names
        elif (
            "column names" in q
            or "columns name" in q
            or "what columns" in q
        ):

            columns = ", ".join(
                [str(c) for c in df.columns]
            )

            st.success(
                f"🤖 DataMind AI: The columns are: {columns}"
            )


        # General fallback
        else:

            st.info(
                "🤖 DataMind AI: I can answer questions such as:"
            )

            st.write(
                """
                • Which product has the highest sales?

                • Which product has the lowest sales?

                • Which product has the highest quantity?

                • What is the total sales?

                • What is the average sales?

                • How many rows are there?

                • How many columns are there?

                • How many missing values are there?

                • What are the column names?
                """
            )


    # -------------------------------------------------
    # DOWNLOAD DATASET
    # -------------------------------------------------
    st.markdown("---")

    st.header("⬇️ Download")

    csv_data = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Dataset as CSV",
        data=csv_data,
        file_name="datamind_analysis.csv",
        mime="text/csv"
    )


    # -------------------------------------------------
    # FOOTER
    # -------------------------------------------------
    st.markdown("---")

    st.caption(
        "© DataMind AI • Intelligent Data Analysis Agent"
    )

else:

    st.info(
        "👆 Upload a CSV/Excel dataset or click "
        "'Try Sample Dataset' to begin."
    )