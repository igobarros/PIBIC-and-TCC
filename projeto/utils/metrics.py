from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score



def sillouette_score(X_transform, range_start=2, range_end=11):
	"""
	Metrica usada para calcular o coeficiente medio da silhueta de todas as amostras.
	O melhor valor é 1 e o pior valor é -1. Valores próximos a 0 indicam clusters sobrepostos. 
	Valores negativos geralmente indicam que uma amostra foi atribuída ao cluster errado, 
	pois um cluster diferente é mais semelhante.

	----------
	parameters:
		X_transform: Dados transformado em versao numerica
		range_start: intervalo inicial de quantas vezes o kmeans irá rodar
		range_end: intervalo final de quantas vezes o kmeans irá rodar
	"""
	for i in range(range_start, range_end):
	    cluster = KMeans(n_clusters=i)
	    preds = cluster.fit_predict(X_transform)
	    score = silhouette_score(X_transform, preds)
	    print('Silhueta para ' + str(i) + ' clusters : ' + str(score))