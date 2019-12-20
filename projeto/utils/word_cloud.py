from wordcloud import WordCloud
import matplotlib.pyplot as plt

from dataset.preprocessing import preparing_data


def plot_wordcloud(X, width=800, height=500, max_font_size=21, figsize=(10, 7)):
	"""
	Funcao responsavel por plotar a nuvem de palavras.

	----------
	parameters:
		X: Dados transformado em versao numerica, indicado a nao aplicar stemming nos dados
		para essa tarefa.
		width: largura da nuvem de palavras
		height: altura da nuvem de palavras
		max_font_size: tamanho maximo da fonte
		figsize: tamanho do grafico
	"""
	all_words = ' '.join([text for text in X])

	wordcloud = WordCloud(
	    width=width, 
	    height=height, 
	    random_state=21, 
	    max_font_size=max_font_size).generate(all_words)

	plt.figure(figsize=figsize)
	plt.imshow(wordcloud)
	plt.axis("off")
	plt.show()
