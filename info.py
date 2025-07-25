import streamlit as st
import pandas as pd
from datetime import datetime
from connect import cred
import gspread
import re

def detail():
    try:
        client = cred()
        spreadsheet = client.open("HerRising")
        worksheet = spreadsheet.worksheet("HR")
        st.success("✅ Connected to Google Sheet")
    except Exception as e:
        st.error(f"❌ Failed to connect to Google Sheet: {e}")
        return

    with st.container(border=True):
        st.markdown("**Kindly fill the form below**")

        fullname = st.text_input("Full Name *", placeholder="Enter your full name")
        gender = st.selectbox("Gender *", ["Male", "Female"], index=None)
        edu_level = st.selectbox("Level of Education *", ["Senior High", "Tertiary", "JHS"], index=None)

        shs_level = tert_level = jhs_level = None
        if edu_level == "Senior High":
            shs_level = st.selectbox("SHS Level *", ["Form 1", "Form 2", "Form 3"], index=None)
        elif edu_level == "Tertiary":
            tert_level = st.selectbox("Tertiary Level *",
                ["Level 100", "Level 200", "Level 300", "Level 400", 
                 "Level 500", "Level 600", "Level 700", "Final Year"],
                index=None, key="tert11")
        elif edu_level == "JHS":
            jhs_level = st.selectbox("JHS Level *", ["Form 1", "Form 2", "Form 3"], index=None)

        sch_name = st.text_input("School Name *", placeholder="Enter your school name")
        freq = st.selectbox("Seminar Frequency *", ["Monthly", "Quarterly", "Annually"], index=None, key="freq")
        deno = st.text_input("Denomination *", placeholder="Denomination Name")
        reg = st.text_input("Region *", placeholder="Region Name")
        contact = st.text_input("Telephone Number *", placeholder="Telephone Number")
        email = st.text_input("Email Address *", placeholder="Enter your valid email")

    submit = st.button("Submit Info", type="primary")

    if submit:
        errors = []

        if not fullname.strip():
            errors.append("Full Name is required")
        if not gender:
            errors.append("Gender selection is required")
        if not edu_level:
            errors.append("Education Level is required")
        else:
            if edu_level == "Senior High" and not shs_level:
                errors.append("SHS Level is required")
            elif edu_level == "Tertiary" and not tert_level:
                errors.append("Tertiary Level is required")
            elif edu_level == "JHS" and not jhs_level:
                errors.append("JHS Level is required")
        if not sch_name.strip():
            errors.append("School Name is required")
        if not deno.strip():
            errors.append("Denomination Name")
        if not reg.strip():
            errors.append("Region Name")
        if not freq:
            errors.append("Seminar Frequency is required")
        if not contact.strip():
            errors.append("Contact number is required")
        elif len(contact) != 10 or not contact.isdigit():
            errors.append("Contact number must be 10 digits")
        if not email.strip():
            errors.append("Email address is required")
        elif not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            errors.append("Invalid email format")

        # Check duplicates
        try:
            existing_data = pd.DataFrame(worksheet.get_all_records())
            if not existing_data.empty:
                if contact.strip() in existing_data['Contact'].astype(str).values:
                    errors.append("Contact number already registered")
                if email.strip().lower() in existing_data['Email'].str.lower().values:
                    errors.append("Email address already registered")
        except Exception as e:
            errors.append(f"Error checking existing records: {str(e)}")

        if errors:
            for error in errors:
                st.error(error)
        else:
            # Safely select the correct education detail
            education_detail = (
                shs_level if edu_level == "Senior High"
                else tert_level if edu_level == "Tertiary"
                else jhs_level
            )

            data_row = [
                str(datetime.now()),
                fullname.strip(),
                gender,
                edu_level,
                education_detail,
                sch_name.strip(),
                freq,
                contact.strip(),
                email.strip(),
                deno.strip(),
                reg.strip()
            ]

            try:
                safe_row = [str(item) if item is not None else "" for item in data_row]
                worksheet.append_row(safe_row)
                st.success("✅ Submitted successfully!")
                st.balloons()
            except Exception as e:
                st.error(f"❌ Failed to submit: {e}")

if __name__ == "__main__":
    detail()
