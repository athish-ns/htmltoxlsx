import bs4
import openpyxl
import streamlit as st
import io

# Streamlit UI
st.title("HTML to Excel Converter")
st.write("Upload an HTML file, and extract 'name' and 'hostname' into an Excel file.")

# File uploader
uploaded_file = st.file_uploader("Upload HTML file", type=["html"])

if uploaded_file is not None:
    # Read uploaded file
    html_content = uploaded_file.read().decode("utf-8")
    soup = bs4.BeautifulSoup(html_content, "html.parser")
    
    # Extract profiles
    profiles = soup.find_all("html5-access-profile")
    
    # Create Excel file
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Profiles"
    ws.append(["Name", "Hostname"])  # Add header row

    # Extract and append data
    for profile in profiles:
        name_tag = profile.find("name")
        hostname_tag = profile.find("hostname")
        name = name_tag.text.strip() if name_tag else "N/A"
        hostname = hostname_tag.text.strip() if hostname_tag else "N/A"
        ws.append([name, hostname])
    
    # Save Excel file to memory
    excel_file = io.BytesIO()
    wb.save(excel_file)
    excel_file.seek(0)

    # Download button
    st.download_button(
        label="Download Excel file",
        data=excel_file,
        file_name="output.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
