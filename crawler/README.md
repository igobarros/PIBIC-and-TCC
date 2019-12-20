## Resumo
O `TweetScraper` pode obter tweets de [Twitter Search](https://twitter.com/search-home). 
Ele é construído em [Scrapy](http://scrapy.org/) sem usar [APIs do Twitter](https://dev.twitter.com/rest/public).
Os dados rastreados não são tão * limpos * quanto os obtidos pelas APIs, mas os benefícios são que você pode se livrar dos limites e restrições de taxa da API. Idealmente, você pode obter todos os dados da Pesquisa do Twitter.

**DETALHE**: Sempre siga a [política dos rastreadores](https://en.wikipedia.org/wiki/Web_crawler#Politeness_policy).

### Dependências

```
$ git clone https://github.com/IgoPereiraBarros
$ cd crawler
$ pip install -r requirements.txt
$ scrapy list
```

### Rodando o projeto

1. Altere os parâmetros de acordo com sua necessidade, ```crawler/TwitterScrapy/settings.py```:
    ```
     USER_AGENT = 'web site/email/etc'
     
     Retire o comentário da linha 17 no parâmetro ```ITEM_PIPELINES```, caso queira salvar no banco mongodb:

     ITEM_PIPELINES = {
        'TwitterScrapy.pipelines.SaveToMongoPipeline': 300,
     }

     Altere as credenciais de acordo com as do seu banco:

     MONGODB_SERVER_PORT = "mongodb://user:passoword@localhost:27017/admin"
     MONGODB_DB = "DBNAME"
     MONGODB_TWEET_COLLECTION = "COLECCTION_NAME"
    ```
2. Se apenas desejar visualizar os dados obtidos pela pesquisa no prompt/terminal siga os passos em ```crawler/TwitterScrapy/settings.py```:
    ```
    Mantenha comentado a linha 8 e 17:
    #LOG_LEVEL = 'INFO'

    ITEM_PIPELINES = {
        #'TwitterScrapy.pipelines.SaveToMongoPipeline': 300,
     }
    ```
3. Na raiz do projeto rode o código com:
    ```scrapy crawl TwitterScrapy -a query=example```

    Com esse comando é possível buscar assuntos relacionado a palavra chave passada na consulta, e salvará o conteúdo de todos os tweets capturados, desde que você use o pipeline. O twitter nos fornece a possibilidade de pesquisas avançadas e foi usado tais formas para melhorar a experiência de se usar a ferramenta.

    | Operador | Comando | Breve explicação |
	| --- | --- | --- |
	| query | query=foo,#ba | palavra(as) chave da pesquisa |
	| no_query | no_query=-a,-b,-c | palavra(as) chave que não conste na pesquisa |
	| state | state="**near**:estado **within**:15**mi**" | pesquisa por Estado |
	| date | date="**until**:yyy-MM-dd **since**:yyyy-MM-dd" | Pesquisa por data until:data fim since data início |
	| lang | lang="pt-br", "en", etc | Pesquisa por idioma |
	| top_tweet | top_tweet=False(antigos) ou True(atuais)  | Pesquisa por tweets mais recentes ou antigos |

### Rodando o projeto na nuvem
Existe uma plataforma chamada [scrapyhub](https://scrapinghub.com/) para hospedar projetos usando scrapy. Para este estudo o projeto foi hospedado no scrapyhub para melhorar a experiência de uso do crawler.

1. Acesse o site do [scrapyhub](https://scrapinghub.com/) e faça uma conta
2. Com a conta criada, no dashboard inicial na parte superior a direita vá em ```CREATE PROJECT```.
3. Após tudo concluído se você perceber a plataforma nos permite 2 opções para subir o projeto, por comando de linha ou pelo github. Seguindo pela opção de comando de linha, na raiz do projeto ```cd crawler``` execute no terminal:
    ```
    $ pip install shub
    $ shub login
    API key: API_KEY
    $ shub deploy 000000
    ```
    Se tudo ocorrer bem, já foi feito o deploy do seu projeto.

    Obs: O banco de dados mongodb também está na nuvem, no Mongodb Atlas. No entanto, para os testes usamos um banco local mesmo.

### Agradecimentos
Gostaria de parabenizar e agradecer pelo trabalho open source de [jonbakerfish](https://github.com/jonbakerfish/TweetScraper), e todos os seus [colaboradores](https://github.com/jonbakerfish/TweetScraper/graphs/contributors).

### Contados
* E-mail: igorestacioceut@gmail.com
* Linkendin: [Igo Pereira Barros](https://www.linkedin.com/in/igo-pereira-barros-developer/)
* Instagram: [igor.p.barros](https://www.instagram.com/igor.p.barros/)
* Telegram: @IgoBarros
