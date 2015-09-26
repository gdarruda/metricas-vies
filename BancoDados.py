import mysql.connector

class BancoMySQL():

    def __init__(self, usuario, senha, host, banco):
        self.conexao = mysql.connector.connect(user=usuario, password=senha, host='127.0.0.1', database=banco, buffered=True)

    def seleciona_noticias(self, id_entidade, id_perfil):

        cursor_noticia = self.conexao.cursor()

        query_noticias = ('select n.id_noticia, n.ind_corpus, n.corpo from noticias n' +
                          ' where exists(select * from entidades_x_noticias exn join entidades e on e.id_entidade = exn.id_entidade where exn.id_noticia = n.id_noticia and (e.id_entidade = %s or e.id_entidade_pai = %s))' +
                          ' and id_perfil = %s')
        dados_noticia = (id_entidade, id_entidade, id_perfil)

        cursor_noticia.execute(query_noticias, dados_noticia)

        return cursor_noticia

    def soma_polaridade(self, id_noticia, id_entidade):

        cursor_polaridade = self.conexao.cursor()

        query_polaridade = ('select ncp.polaridade from noticias_x_paragrafo ncp join entidade_corpus_x_entidade ece on ece.nome = ncp.entidade where  ece.id_entidade = %s and id_noticia = %s')
        dados_polaridade = (id_entidade, id_noticia)

        cursor_polaridade.execute(query_polaridade, dados_polaridade)

        return cursor_polaridade

    def seleciona_perfis(self):

        cursor_perfil = self.conexao.cursor()

        query_perfil = ('select id_perfil from perfis_twitter')

        cursor_perfil.execute(query_perfil)

        return cursor_perfil

    def existe_entidade_tweet(self, id_entidade, id_noticia):

        count_noticia = self.conexao.cursor()

        query_entidade_tweet = '''select count(*) 
                                  from noticias n
                                  join entidades_x_noticias exn
                                  on   exn.id_noticia = n.id_noticia
                                  join entidades e
                                  on   e.id_entidade = exn.id_entidade
                                  and  e.id_entidade_pai =  %s
                                  where n.id_noticia = %s'''

        dados_entidade_tweet = (id_entidade, id_noticia)
        count_noticia.execute(query_entidade_tweet, dados_entidade_tweet)

        return count_noticia.fetchone()[0]

    def conta_noticias(self, id_perfil, corpus):

        count_noticia = self.conexao.cursor()

        query_perfil = 'select count(*) from noticias n join noticias_x_paragrafo np on n.id_noticia = np.id_noticia where id_perfil = %s'

        if corpus:
            query_perfil = query_perfil + ' and ind_corpus = \'S\''

        dados_perfil = (id_perfil,)

        count_noticia.execute(query_perfil, dados_perfil)

        return count_noticia.fetchone()[0]
