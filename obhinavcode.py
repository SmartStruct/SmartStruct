import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Set page configuration
st.set_page_config(page_title="Building Life Prediction", layout="wide")

# Custom CSS for navigation bar and sections
st.markdown(
    """
    <style>
        /* Navigation bar container */
        .navbar {
            background-color: #001f3f; /* Navy Blue */
            display: flex;
            justify-content: right;
            padding: 8px 0;
        }

        /* Links in the navigation bar */
        .navbar a {
            float: left;
            display: block;
            color: white;
            text-align: right;
            padding: 8px 20px;
            text-decoration: none;
            font-size: 16px;
        }

        /* Change link colors on hover */
        .navbar a:hover {
            background-color: #00509E;
            color: white;
        }

        /* Content section styling */
        section {
            padding: 40px;
            margin-top: 20px;
            background-color: #f4f4f4;
            border-radius: 8px;
        }

        #about-us, #how-to-use, #contact-us, #feedback {
            text-align: left;  /* Align text to the left */
            color: black;      /* Set text color to black */
            font-size: 30px;   /* Adjust font size if needed */
            line-height: 1.6;  /* Adjust line spacing for better readability */
            padding: 0px;     /* Add padding to space out the content */
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Navigation bar
st.markdown(
    """
    <div class="navbar">
        <a href="#about-us">About Us</a>
        <a href="#how-to-use">How to Use</a>
        <a href="#contact-us">Contact Us</a>

    </div>
    """,
    unsafe_allow_html=True,
)

# Main App: Upload CSV and Predict
st.subheader("Upload Your Data and Predict Building Life")

# CSV file uploader
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Clean column names
    df.columns = df.columns.str.strip()

    required_columns = [
        "Cement", "Blast_furnace_Slag", "Fly_Ash", "Water",
        "Super_plasticizer", "Coarse_Aggregate", "Fine_Aggregate",
        "Compressive_Strength", "Building_life"
    ]
    if all(col in df.columns for col in required_columns):
        df.fillna(df.mean(), inplace=True)
        
        X = df[required_columns[:-1]]
        y = df["Building_life"]
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train model
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train_scaled, y_train)

        st.markdown("### Predict Building Life")
        cement = st.number_input("Cement", min_value=0.0, value=300.0)
        blast_furnace_slag = st.number_input("Blast Furnace Slag", min_value=0.0, value=50.0)
        fly_ash = st.number_input("Fly Ash", min_value=0.0, value=50.0)
        water = st.number_input("Water", min_value=0.0, value=200.0)
        super_plasticizer = st.number_input("Super Plasticizer", min_value=0.0, value=5.0)
        coarse_aggregate = st.number_input("Coarse Aggregate", min_value=0.0, value=1000.0)
        fine_aggregate = st.number_input("Fine Aggregate", min_value=0.0, value=500.0)
        compressive_strength = st.number_input("Compressive Strength", min_value=0.0, value=40.0)

        if st.button("Predict"):
            input_data = pd.DataFrame({
                "Cement": [cement],
                "Blast_furnace_Slag": [blast_furnace_slag],
                "Fly_Ash": [fly_ash],
                "Water": [water],
                "Super_plasticizer": [super_plasticizer],
                "Coarse_Aggregate": [coarse_aggregate],
                "Fine_Aggregate": [fine_aggregate],
                "Compressive_Strength": [compressive_strength]
            })
            input_data_scaled = scaler.transform(input_data)
            prediction = model.predict(input_data_scaled)[0]
            st.success(f"Predicted Building Life: {prediction:.2f} years")

        # Evaluation Metrics
        y_pred = model.predict(X_test_scaled)
        st.markdown("### Model Performance")
        st.write(f"MAE: {mean_absolute_error(y_test, y_pred):.2f}")
        st.write(f"RMSE: {mean_squared_error(y_test, y_pred, squared=False):.2f}")
        st.write(f"R²: {r2_score(y_test, y_pred):.2f}")

        # Plotting
        fig, ax = plt.subplots()
        ax.scatter(y_test, y_pred, alpha=0.6)
        ax.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], "--", color="red")
        ax.set_xlabel("True Building Life")
        ax.set_ylabel("Predicted Building Life")
        st.pyplot(fig)
    else:
        st.error("Uploaded file does not contain required columns.")
else:
    st.info("Please upload a CSV file.")

# "About Us" section
st.markdown(
    """
    <section id="about-us">
        <h2>About Us</h2>
        <p>At Buildworks, we specialize in harnessing advanced data analytics and AI to predict the lifespan and structural integrity of buildings. Our innovative platform leverages cutting-edge technology, analyzing key parameters like fly ash density, cement density, and water content to provide accurate lifespan forecasts. With a commitment to sustainability and precision, we help architects, engineers, and construction professionals make informed decisions, ensuring the longevity and safety of infrastructure. At Buildworks, we believe in transforming the way the world thinks about building longevity, combining intelligence with innovation to shape resilient, sustainable structures.</p>
    </section>
    """,
    unsafe_allow_html=True,
)

# "How to Use" section
st.markdown(
    """
    <section id="how-to-use">
        <h2>How to Use</h2>
        <p>To use Buildworks, simply upload an Excel file containing data on fly ash density, cement density, and water content for your building project. Our platform will process the data and generate a detailed analysis of the building's predicted lifespan based on these parameters. Buildworks uses advanced AI algorithms to provide precise lifespan forecasts, helping engineers and architects make informed decisions. The results are presented in an easy-to-understand graph comparing predicted vs. actual building lifespan. This allows users to assess the long-term performance of structures, optimize designs, and ensure safety and sustainability in construction projects.</p>
    </section>
    """,
    unsafe_allow_html=True,
)

# "Contact Us" section
st.markdown(
    """
    <section id="contact-us">
        <h2>Contact Us</h2>
        <p>Feel free to reach out to us for any queries, suggestions, or feedback. Our team is here to assist you in understanding building longevity and optimizing construction designs.</p>
        <p>Email: support@Buildworks.com</p>
        <p>Phone: +1 (123) 456-7890</p>
    </section>
    """,
    unsafe_allow_html=True,
)

