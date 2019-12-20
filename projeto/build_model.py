import os
import pickle
from glob import glob
from shutil import copy2

from sklearn.cluster import KMeans

class BuildModel:
	""" 
	Classe de responsabilidade de treinar os dados usando o algoritmo não supervicionado
	K-Means.
	"""

	def __init__(self, X_transform):
		self.__X_transform = X_transform

	def train(self, **kwargs):
		"""
		Metodo responsavel por treinar os dados.

		---------
		parameters:
			n_clusters: O número de clusters a serem formados e o número de centróides a serem gerados.
			init: Método para inicialização do algoritmo
			n_init: Número de vezes que o algoritmo k-means será executado com diferentes sementes de centróide
			max_iter: Número máximo de iterações do algoritmo k-means para uma única execução.

		return:
			instancia do kmeans apos o treino
		"""
		kmeans = KMeans(n_clusters=kwargs.get('n_clusters'), init=kwargs.get('init'), n_init=kwargs.get('n_init'), max_iter=kwargs.get('max_iter'))
		kmeans.fit(self.__X_transform)
		return kmeans

	def get_clusters_words(self, vectorizer):
		"""
		Metodo responsavel retornar os dados de cada cluster

		----------
		parameters:
			vectorizer: dados apos aplicacao de vectorizacao
		"""
		words = vectorizer.get_feature_names()
		kmeans = self.train()
		common_words = kmeans.cluster_centers_.argsort()[:,-1:-11:-1]

		for num, centroid in enumerate(common_words):
			print(str(num) + ' : ' + ', '.join(words[word] for word in centroid))

	def saving_model(self, model):
		"""
		Metodo responsavel por fazer o versionamento do retrino do modelo

		----------
		parameters:
			model: instancia do modelo apos o treino
		"""
		try:
			# lista de arquivos com extensao .pkl na pasta models_pkl
			files = [file.split('/')[1] for file in glob(os.path.join('models_pkl', '*.pkl'))]

			if files:
				# lista numeros do tipo inteiro que estao apos a letra v de cada arquivo .pkl
				version_number = [int(file.split('.')[0][1:]) for file in files if file.startswith('v')]
				
				# ordena os numeros em ordem crescente e pega apenas o ultimo valor
				i = sorted(version_number)[-1]

				print('-------------------------------- Model --------------------------------')

				for file in files:
					# verifica se tem arquivos dentro da pasta models_pkl
					if os.path.isfile('models_pkl/' + file):
						print(file)
					
					dir_ = os.listdir('models_pkl')
					for f in dir_:
						# verifica se existe algum arquivo que comece com a palara lasted
						if f.startswith('lasted'):
							os.remove('models_pkl/' + f) # caso sim, os remove

				# Incrementa mais 1 ao ultimo numero retornado das versoes dos arquivos							
				i += 1
				# salva o modelo com extensao
				pickle.dump(model, open(f'models_pkl/v{i}.pkl', 'wb'))

				# Bloco responsavel de fazer a copia do ultimo modelo gerado do retreino
				source = f'models_pkl/v{str(i)}.pkl'
				destination = "models_pkl/lasted_{}.pkl".format(source.split('/')[1][:-4])
				metadata = os.stat(source)

				copy2(source, destination)

			else:
				# Bloco responsavel de fazer a copia do ultimo modelo gerado do retreino
				pickle.dump(model, open(f'models_pkl/v1.pkl', 'wb'))

				source = f'models_pkl/v1.pkl'
				destination = "models_pkl/lasted_{}.pkl".format(source.split('/')[1][:-4])
				metadata = os.stat(source)

				copy2(source, destination)

		except Exception as e:
			raise e


if __name__ == '__main__':

	# Roda o modelo K-Means

	from features_extraction.transform import FeatureExtraction

	from dataset.preprocessing import preparing_data
	from dataset.read_dataset import MongoDB

	feature = FeatureExtraction()

	df = MongoDB()

	input_ = preparing_data(df.dataset())

	tfidf = feature.tfidf_vectorizer_fit(input_)
	X = feature.tfidf_vectorizer_transform(input_)

	model = BuildModel(X)
	m = model.train(n_clusters=6, init='k-means++', n_init=10, max_iter=300)

	#model.saving_model(m)
	#feature.saving_vectorizer(tfidf)

