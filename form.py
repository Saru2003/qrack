import streamlit as st
from streamlit.components.v1 import iframe
import pdfkit
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
import re
from PIL import Image
import gspread
from oauth2client.service_account import ServiceAccountCredentials

#line
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
regex_git=r'^(?:https?:\/\/)?(?:www\.)?github\.com\/[a-zA-Z0-9_-]+\/[a-zA-Z0-9_-]+$'
regex_link =  '^(?:https?:\/\/)?(?:www\.)?linkedin\.com\/(?:in|pub|company)\/[a-zA-Z0-9-_.]+\/?$'
st.set_page_config(page_title="Qrack")
#go to home page
# link_home = "**[Go to home page](https://technotronz23.wixsite.com/home)**"
# e,w,r=st.columns([2,2, 1])
# with r:
#     st.markdown(link_home, unsafe_allow_html=True)
# img = Image.open('TZ_logo.png')
# st.image(img)
hide_ststyle = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
# st.write("test1")

#line
# def fun3():
#             st.write(f'''<a target="_self" href="https://discord.gg/WgEDCtPN" target="_blank"><button>Click to join Technotronz'23 Discord server to follow regular updates</button></a>''',unsafe_allow_html=True)
#               link = '[Make sure you join our discord server to receive regular updates](https://discord.gg/Pf4cqxZtQu)'
#               st.markdown(link, unsafe_allow_html=True)
#     a2,b2,c2=st.columns([0.1,3,0.1])
    
#     with b2:
#       st.write('''<h5>Please join our Valediction (7th FEB 5:30 pm) to know the Prize Winners!</h5>''',unsafe_allow_html=True)
#     img1 = Image.open('valediction poster.jpg')
#     st.image(img1)
#     a1,b1=st.columns([1,1.9])
#     with b1:
#       st.write('''
# 				<style>
# 				.button {
# 				background-image: linear-gradient(to right, #314755 0%, #26a0da  51%, #314755  100%);
# 				border: none;
# 				color: white;
# 				padding: 15px 30px;
# 				text-align: center;
# 				text-decoration: none;
# 				display: inline-block;
# 				font-size: 16px;
# 				margin: 3px 1px;
# 				transition-duration: 0.4s;
# 				cursor: pointer;
# 				border-radius: 13px;
# 				width: auto;
# 				}
# 				.button1 {
# 				background-image: linear-gradient(to right, #314755 0%, #26a0da  51%, #314755  100%);; 
# 				color: white; 
# 				border: 2px solid #314755;
# 				}
# 				.button1:hover {
# 				background-image: linear-gradient(to right, #314755 0%, #26a0da  51%, #314755  100%);
# 				color: white;
# 				}
# 				</style>
# 				<a  href="https://psgct.webex.com/psgct/j.php?MTID=m979527629f33b3a72076f10ba121a867" target="_blank" > 
# 							<button class="button button1">
# 								Click here
# 							</button>
# 						</a>
# 				''',
# 				unsafe_allow_html=True)

st.markdown(hide_ststyle, unsafe_allow_html=True)
i_=0
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("kriya.json", scope)
client = gspread.authorize(creds)

p=st.empty()
one,two,thr=st.columns([0.1,1, 0.1])
# with two:
#     st.header("Technotronz'23 General Registration ")

# dnote_er = 'Disclaimer: This webpage supports and accepts responses only in latest versions of the following browsers (Google Chrome, Microsoft Edge, Safari, Firefox)'

# st.markdown(dnote_er, unsafe_allow_html=True)
# st.error("Online registrations are closed. Thank you!")
name=st.text_input('Enter your full name: ')
mail=st.text_input('Enter your mail ID: ')
git=st.text_input('Enter your GitHUB profile URL: ')
li=st.text_input('Enter your linkedin profile URL: ')

def check(email):
	email = email.strip()
	if not (re.fullmatch(regex, email)):
		return 1
	return 0
def check2(git):
	git = git.strip()
	if not (re.fullmatch(regex_git,git)):
		return 1
	return 0
def check3(li):
	li = li.strip()
	if not (re.fullmatch(regex_link, li)):
		return 1
	return 0
def valid(name):
    name=name.replace(" ","").replace(".","")
    return name.isalpha()
def valid2(name):
    return name.replace(" ","").isalpha()

col1,col2,col3=st.columns([2,1,2])
m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: rgb(255, 255, 255);
    height:1.5em;
    width: 3em; 
    font-size: 29px;
    color: black;
}
</style>""", unsafe_allow_html=True)

d=st.button("submit")
if d:
	sheet = client.open("kriya").sheet1
	data=sheet.get_all_values()


	name_err=mail_err=git_err=li_err=0
	row=[name,mail,git,li]
	if not valid(name):
		st.error("Enter name in proper format")
	else:
		name_err=1

	if check(mail):
		st.error("Enter valid Mail ID")
	else:
		mail_err=1
# 	if check2(git):
# 		st.error("Enter valid GitHUB profile URL")
# 	else:
# 		git_err=1

# 	if check3(li):
# 		st.error("Enter valid linkedin profile URL")
# 	else:
# 		li_err=1
        li_err=git_err=1

	if name_err==mail_err==git_err==li_err==1:
		r=sheet.cell(len(data),1).value
	# 		em("TZ23"+str(int(r[4:])+1),name,mail,html_gr,ph)
		sheet.insert_row(row)
		st.success("Kindly wait until we cook your resume!")
		st.balloons()
		submit = form.form_submit_button("Generate PDF")
		env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())
		template = env.get_template("template.html")

		if submit:
		    html = template.render(
			name=name,
			li=li,
			git=git,
			mail=mail,
		    )

		    pdf = pdfkit.from_string(html, False)
		    st.balloons()

		    right.success("🎉 Your diploma was generated!")
		    # st.write(html, unsafe_allow_html=True)
		    # st.write("")
		    st.download_button(
			"⬇️ Download PDF",
			data=pdf,
			file_name="diploma.pdf",
			mime="application/octet-stream",
		    )
	# 		a2,b2,c2=st.columns([1.4,3,0.5])
	# 		with b2:
	# 			st.write(f'''<h5>Your Registration ID: {"TZ23"+str(int(r[4:])+1)} <br></h5>''',unsafe_allow_html=True)


