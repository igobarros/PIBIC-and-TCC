import os
import pickle
from glob import glob
from shutil import copy2

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from gensim.models import Word2Vec

from dataset.preprocessing import preparing_data


class FeatureExtraction:
	""" 
	Classe responsavel por aplicar a vetorizacao nos dados
	"""

	def __init__(self):
		self.bow_vec = CountVectorizer()
		self.tfidf_vec = TfidfVectorizer()

	def bow_vectorizer_fit(self, X):
		""" 
		Treina os dados usando o CountVectorizer

		----------
		parameters:
			X: Dados a serem aplicado o treino
			type: list ou array-numpy

		
		return:
			objeto do tipo CountVectorizer
		"""
		bow = self.bow_vec.fit(X)
		return bow

	def bow_vectorizer_transform(self, X):
		""" 
		Transforma os dados em forma numerica

		----------
		parameters:
			X: Dados a serem aplicado a transformacao
			type: list ou array-numpy

		
		return:
			lista dos dados em representacao numerica
		"""
		X_transform = self.bow_vec.transform(X)
		return X_transform

	def tfidf_vectorizer_fit(self, X):
		"""
		Treina os dados usando o TfidfVectorizer

		----------
		parameters:
			X: Dados a serem aplicado o treino
			type: list ou array-numpy

		
		return:
			objeto do tipo TfidfVectorizer
		"""
		tfidf = self.tfidf_vec.fit(X)
		return tfidf

	def tfidf_vectorizer_transform(self, X):
		"""
		Transforma os dados em forma numerica

		----------
		parameters:
			X: Dados a serem aplicado a transformacao
			type: list ou array-numpy

		
		return:
			lista dos dados em representacao numerica

		"""
		X_transform = self.tfidf_vec.transform(X)
		return X_transform

	def word2vec(self, X):
		"""
		Transforma os dados em forma numerica usando o Word2Vec Embadding

		----------
		parameters:
			X: Dados a serem aplicado a transformacao
			type: list ou array-numpy

		
		return:
			lista
		"""
		tokenizer = X.apply(lambda x: x.split())
		model_w2v = Word2Vec(tokenizer, min_count=1)
		word2vec = model_w2v.wv.vectors
		return word2vec

	def saving_vectorizer(self, vec):
		"""
		Metodo responsavel por fazer o versionamento da vetorizacao dos dados

		----------
		parameters:
			vec: instancia do metodo usadodo para fazer a transformacao dos dados em forma numerica 
		"""
		try:
			# lista de arquivos com extensao .pkl na pasta vectorizers_pkl
			files = [file.split('/')[1] for file in glob(os.path.join('vectorizers_pkl', '*.pkl'))]

			if files:
				# lista numeros do tipo inteiro que estao apos a letra v de cada arquivo .pkl
				version_number = [int(file.split('.')[0][1:]) for file in files if file.startswith('v')]
				
				# ordena os numeros em ordem crescente e pega apenas o ultimo valor
				i = sorted(version_number)[-1]

				print('-------------------- Vectorizer -----------------------')
				for file in files:
					# verifica se tem arquivos dentro da pasta vectorizers_pkl
					if os.path.isfile('vectorizers_pkl/' + file):
						print(file)
					
					dir_ = os.listdir('vectorizers_pkl/')
					for f in dir_:
						# verifica se existe algum arquivo que comece com a palara lasted
						if f.startswith('lasted'):
							os.remove('vectorizers_pkl/' + f) # caso sim, os remove

				# Incrementa mais 1 ao ultimo numero retornado das versoes dos arquivos
				i += 1
				# salva o modelo com extensao
				pickle.dump(vec, open(f'vectorizers_pkl/v{i}.pkl', 'wb'))

				# Bloco responsavel de fazer a copia do ultimo modelo gerado do retreino
				source = f'vectorizers_pkl/v{str(i)}.pkl'
				destination = "vectorizers_pkl/lasted_{}.pkl".format(source.split('/')[1][:-4])
				metadata = os.stat(source)

				copy2(source, destination)

			else:
				# Bloco responsavel de fazer a copia do ultimo modelo gerado do retreino
				pickle.dump(vec, open('vectorizers_pkl/v1.pkl', 'wb'))

				source = 'vectorizers_pkl/v1.pkl'
				destination = "vectorizers_pkl/lasted_{}.pkl".format(source.split('/')[1][:-4])
				metadata = os.stat(source)

				copy2(source, destination)

		except Exception as e:
			raise e