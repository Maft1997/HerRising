import streamlit as st
from PIL import Image
from info import detail

# Set page configuration with a representative maiden icon
st.set_page_config(page_title="HerRising Club", page_icon="🚥", layout="centered")


with st.container(border=True):
    # Display image
    try:
        logo = Image.open('./media/maft.jpg')
        st.image(logo, use_container_width=True)
    except FileNotFoundError:
        st.warning("Kindly wait it's loading")
     
    # Create two columns
    col1, col2 = st.columns(2)
  
    detail()
    
    # Main function based on selection
 

# Hide Streamlit elements
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}  /* Hide the hamburger menu */
    footer {visibility: hidden;}  /* Hide the footer */
    header {visibility: hidden;}  /* Hide the header */
    </style>
    """,
    unsafe_allow_html=True
)