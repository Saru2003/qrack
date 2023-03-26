import pdfkit
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from datetime import date
import streamlit as st
import re
from streamlit.components.v1 import iframe
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
st.set_page_config(layout="centered", page_icon="🎓", page_title="Diploma Generator")
st.title("🎓 Resume Generator")

left, right = st.columns(2)

env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())
template = env.get_template("template.html")
def check(email):
	email = email.strip()
	if not (re.fullmatch(regex, email)):
		return 1
	return 0

left.write("Fill in the data:")
form = left.form("template_form")
name = form.text_input("Name")
mail= form.text_input("Email")
git= form.text_input("Github URL")
li = form.text_input("Linkedin URl")
submit = form.form_submit_button("Generate PDF")
mail_err=0
if submit:
    if check(mail):
        st.error("Enter valid Mail ID")
    else:
        mail_err=1
    if mail_err==1:
        html = template.render(
            name=name,
            mail=mail,
            git=git,
            li=li,
            date=date.today().strftime("%B %d, %Y"),
        )

        pdf = pdfkit.from_string(html, False)
        st.balloons()

        right.success("🎉 Your resume was generated!")
        # st.write(html, unsafe_allow_html=True)
        # st.write("")
        right.download_button(
            "⬇️ Download PDF",
            data=pdf,
            file_name="resume.pdf",
            mime="application/octet-stream",
        )
