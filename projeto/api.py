import os
import pickle
from glob import glob

import numpy as np

from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse

from dataset.preprocessing import preparing_data
from features_extraction.transform import FeatureExtraction

app = Flask(__name__)
api = Api(app)

# ler o modelo salvo k-means
files_model =  [file.split('/')[1] for file in glob(os.path.join('models_pkl', '*.pkl'))]
lasted_model = [f for f in files_model if f.startswith('lasted')]
model = pickle.load(open('models_pkl/' + lasted_model[0], 'rb'))

# ler o arquivo salvo de vetorizacao dos dados
files_vectorizer = [file.split('/')[1] for file in glob(os.path.join('vectorizers_pkl', '*.pkl'))]
lasted_vectorizer = [f for f in files_vectorizer if f.startswith('lasted')]
vectorizer = pickle.load(open('vectorizers_pkl/' + lasted_vectorizer[0], 'rb'))


vec = FeatureExtraction()
vec.tfidf_vec = vectorizer

# argument parsing
parser = reqparse.RequestParser()
parser.add_argument('query')

class PredictionModel(Resource):

	def get(self):
		# use parser and find the user's query
		args = parser.parse_args()
		user_query = args['query']

		df = preparing_data(np.array([user_query]))

		if len(df) > 0:
			transform = vec.tfidf_vectorizer_transform(df.values)
			prediction = model.predict(transform)

			return jsonify({'cluster': str(prediction[0])})
		else:
			return jsonify({"error": "sem informações significativas para o modelo"})

	def post(self):
		json_data = request.get_json(force=True)
		data = json_data['text']

		df = preparing_data(np.array([data]))

		if len(df) > 0:
			transform = vec.tfidf_vectorizer_transform(df.values)
			prediction = model.predict(transform)

			return jsonify(cluster=str(prediction[0]))
		else:
			return jsonify({"error": "sem informações significativas para o modelo"})




api.add_resource(PredictionModel, '/predict')

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)