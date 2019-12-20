from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.decomposition import TruncatedSVD as SVD



def plot(X_transform, model, figsize=(15, 6)):
	"""
	Funcao responsavel por plotar um grafico dispersao para avaliar como estar a distribuicao
	dos dados apos treinado.

	----------
	parameters:
		X_transform: Dados transformado em versao numerica
		model: instancia do modelo kmeans apos o treino
		figsize: tamanho do grafico
	"""

	# Usando o SVD para diminuir a dimencionalidade dos dados para 2 dimenções.
	svd = SVD(n_components=2, random_state=0)
	vectorizer_2D = svd.fit_transform(X_transform)

	plt.figure(figsize=figsize)
	plt.scatter(vectorizer_2D[:, 0], vectorizer_2D[:, 1], c=model.labels_)
	plt.scatter(model.cluster_centers_[:, 0], model.cluster_centers_[:, 1], s=200, color='black', label='Centroids')
	plt.title('Cluster of Tweets')
	plt.legend()
	plt.show()