import re
import string

from pandas import DataFrame

from nltk.stem import RSLPStemmer
from nltk.tokenize import TweetTokenizer


def text_preprocessing(text, is_stemmer=False):
    """
    Função que realizado o pré-processamento dos dados
    ----------
    parameters:
        text: texto que será submetido ao pré-processamento
        type: string

        is_stemmer: Informa a função se deseja aplicar a técnica de stemmer nos dados, 
        por padrão e igual False, se True indica que o stemmer será aplicado
        type: boolean

    
    return:
        lista de tokens
        type: list
    """
    twitter_tokenizer = TweetTokenizer(reduce_len=True, strip_handles=True)
    stemmer = RSLPStemmer()
    
    # remove links
    no_links = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', '', text).lower(
    ).replace('http', re.sub(r'http\S+', '', '')).replace('https', re.sub(r'http\S+', '', '')).replace('\n', ' ')
    
    # remove os números
    no_numbers = re.sub(r'[-|0-9]','', no_links)
    
    # remove palavras com hashtags
    no_hashtags_word = re.sub(r'(#[^#\s]+)', '', no_numbers)
    
    # remove as menções dos tweets
    no_mentions = re.sub(r'(@[^@\s]+)', '', no_hashtags_word)
    
    # Reduz letras repetidas
    no_repeat_letters = re.sub(r'(.)\1+', r'\1\1', no_mentions) 
    
    # remove as pontuações e caracteres especiais
    nopunc = [char for char in no_repeat_letters if char not in string.punctuation]
    
    # retornando para o formato string
    nopunc = ''.join(nopunc)
    
    # Lendo o arquivo(.txt) de stopwords
    file = open('dataset/stopwords.txt', 'r')
    stopwords = [word.replace('\n', '') for word in file]
    
    if is_stemmer:
        # remove stopwords e aplicando stemming
        no_stopwords = [stemmer.stem(word) for word in nopunc.split() if word.lower() not in set(stopwords) and len(word) > 3]
    else:
        # remove stopwords
        no_stopwords = [word for word in nopunc.split() if word.lower() not in set(stopwords) and len(word) > 3]
    
    # Transformando para texto
    text_processed = ' '.join(no_stopwords)
    
    return [word.lower() for word in twitter_tokenizer.tokenize(text_processed)]


def preparing_data(df):
    """
    Função responsavel por preparar os dados usando a biblioteca pandas, dados no qual será
    submetido ao modelo de aprendizagem de maquina.
    
    ----------
    parameters:
        df: São os dados em forma de DataFrame do pandas, pode ser passado a instancia do DataFrame
        ou o texto puro pois a função se encarrega de transformar para o tipo do pandas.
        type: DataFrame
    
    
    return:
        Series do pandas
    """

    try:

        if isinstance(df, DataFrame):
            df['text_tokenized'] = df['text'].apply(text_preprocessing)

            tweets_tokenizer = df['text_tokenized'].copy()

            for i in range(len(tweets_tokenizer)):
                tweets_tokenizer[i] = ' '.join(tweets_tokenizer[i])

            df['text_process'] = tweets_tokenizer
            df['text_tokenizer_lenght'] = df['text_tokenized'].apply(lambda text_p: len(text_p) if len(text_p) > 0 else None)

            df.dropna(inplace=True)

            return df['text_process']

        else:

            new_df = DataFrame(df, columns=['text'])

            new_df['text_tokenized'] = new_df['text'].apply(text_preprocessing)

            tweets_tokenizer = new_df['text_tokenized'].copy()

            for i in range(len(tweets_tokenizer)):
                tweets_tokenizer[i] = ' '.join(tweets_tokenizer[i])

            new_df['text_process'] = tweets_tokenizer
            new_df['text_tokenizer_lenght'] = new_df['text_tokenized'].apply(lambda text_p: len(text_p) if len(text_p) > 0 else None)

            new_df.dropna(inplace=True)

            return new_df['text_process']
            
    except Exception as e:
        raise e

