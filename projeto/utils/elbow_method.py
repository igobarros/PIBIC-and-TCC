from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

from dataset.preprocessing import preparing_data


def plot_elbow_method(X, range_start=1, range_end=11, figsize=(8, 4)):
	"""
	Funcao que realiza o metodo do cotovelo. Esse e um metodo usado para auxiliar
	na escolha do numero de k-cluster do modelo K-means.

	----------
	parameters:
		X: Dados transformado em versao numerica
		range_start: intervalo inicial de quantas vezes o kmeans irá rodar
		range_end: intervalo final de quantas vezes o kmeans irá rodar
		figsize: tamanho do grafico
	"""
	wcss = []
	for i in range(range_start, range_end):
	    kmeans = KMeans(n_clusters=i, init='k-means++', n_init=10, max_iter=300, random_state=0)
	    kmeans.fit(X)
	    wcss.append(kmeans.inertia_)
	plt.figure(figsize=figsize)
	plt.plot(range(range_start, range_end), wcss)
	plt.title('The Elbow Method')
	plt.xlabel('Number of clusters')
	plt.ylabel('WCSS')
	plt.show()