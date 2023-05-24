import streamlit as st
import requests
from PIL import Image

def welcome():
	return 'Welcome  to Ada Asia'

image = Image.open('img/adaasia-logo.png')

col1, col2, col3, col4 = st.columns(4)

with col1:
	st.write(' ')

with col2:
	st.image(image, width=400)

with col3:
	st.write(' ')

with col4:
	st.write(' ')

# this is the main function in which we define our webpage
def main():
	# giving the webpage a title
	# st.title("Ada Asia Prediction")
	
	# here we define some of the front end elements of the web page like
	# the font and background color, the padding and the text to be displayed
	html_temp = """
	<div style ="background-color:yellow;padding:13px">
	<h1 style ="color:black;text-align:center;">TCGC Ada Asia Status Machine Learning Classifier App </h1>
	</div>
	"""
	
	# this line allows us to display the front end aspects we have
	# defined in the above code
	st.markdown(html_temp, unsafe_allow_html = True)
	
	# the following lines create text boxes in which the user can enter
	# test
	# the data required to make the prediction

	tcgc_budget = st.text_input("Please input tcgc budget", "Type Here")
	tcgc_type = st.text_input("Please input tcgc type", "Type Here")
	tcgc_flag_lock = st.text_input("Please input tcgc flag lock", "Type Here")
	tcm_success = st.text_input("Please input tcm success ", "Type Here")
	tcm_status_campaign = st.text_input("Please input tcm status campaign", "Type Here")
	tcm_channel = st.text_input("Please input tcm channel", "Type Here")
	feature_tf_id = st.text_input("Please input feature tf id", "Type Here")
	tcm_inventory_id = st.text_input("Please input tcm inventory id", "Type Here")
	tcm_external_entity_id = st.text_input("Please input tcm external entity id", "Type Here")
	
	# the below line ensures that when the button called 'Predict' is clicked,
	# the prediction function defined above is called to make the prediction
	# and store it in the variable result
	if st.button("Predict"):
		url1 = "http://172.17.0.1:80"
		url2 = "http://172.17.0.1:8000"
		
		data = {
		"tcgc_budget": tcgc_budget,
		"tcgc_type": tcgc_type,
        "tcgc_flag_lock": tcgc_flag_lock,
        "tcm_success": tcm_success,
	    "tcm_status_campaign": tcm_status_campaign,
        "tcm_channel": tcm_channel,
        "feature_tf_id": feature_tf_id,
        "tcm_inventory_id": tcm_inventory_id,
        "tcm_external_entity_id": tcm_external_entity_id}
		

		try :
			response = requests.post(f"{url1}/predict", json=data, timeout=8000)
		except:
			response = requests.post(f"{url2}/predict", json=data, timeout=8000)

		if response.status_code == 200:
			hasil = response.json()
			st.success('The TFGC status is {}'.format(hasil['tcgc_status']))
		else:
			st.error("Error:", response.status_code, response.json())

if __name__=='__main__':
	main()

