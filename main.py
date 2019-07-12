from flask import Flask, request, g, redirect, url_for, render_template, flash
from dotenv import load_dotenv
import requests
import os
import io

app = Flask(__name__)
APP_ROOT = os.path.join(os.path.dirname(__file__), '..') 
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

@app.route('/')
def hello_world():
	return render_template('index.html')
	

@app.route("/query", methods=["POST"])
def query():
	if request.method == 'POST':
		# RECIBIR DATA DEL POST
		image = request.files["file"]
		image_data = image.read()
		# POST A AZURE
		url = os.getenv("API_URL")
		api_key = os.getenv("API_KEY")
		headers={"Content-Type":"application/octet-stream", "Ocp-Apim-Subscription-Key":api_key}
		azure_post = requests.post(url,headers=headers,data=image_data)
		# azure_post es un objeto response, necesitamos parsear su data

		# import pdb; pdb.set_trace()
		azure_obj = azure_post.json()
		if azure_obj['categories'][0]['detail']['celebrities'][0]:
			name = azure_obj['categories'][0]['detail']['celebrities'][0]['name']
			confidence = azure_obj['categories'][0]['detail']['celebrities'][0]['confidence']
			return render_template('index.html', azure = azure_obj, name=name, confidence=confidence)
		return render_template('index.html', azure = azure_obj)

	return render_template('index.html')


	# POST con un binario que viene en el adjunto
	# Setear headers antse de enviar el request (Content Type, API KEY)
	
	


if __name__ == '__main__':
    app.run()