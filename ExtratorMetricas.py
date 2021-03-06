from nltk.tokenize import RegexpTokenizer
from math import fabs, floor
import numpy as np
from scipy.spatial.distance import pdist
from sklearn.preprocessing import scale
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import matplotlib.cm as cm


class ExtratorMetricas():

    def __init__(self, bd):
        self.bd = bd

    def desvio_padrao_media(self, valores):
        valores_np = np.array(valores)
        return (np.std(valores_np), np.mean(valores_np))

    def desvio_absoluto_mediana(self, valores):

        B = 1.4826
        tamanho = len(valores)
        posic_mediana = int(floor(tamanho / 2))

        valores.sort()
        mediana_valores = []
        for valor in valores:
            mediana_valores.append(fabs(valor - valores[posic_mediana]))

        mediana_valores.sort()
        return (B * mediana_valores[posic_mediana], valores[posic_mediana])

    def contabiliza_metricas(self, id_entidade, id_perfil, corpus):

        total_referencias = 0
        total_referencias_tweet = 0
        total_palavras = 0
        positivo = 0.
        neutro = 0.
        negativo = 0.
        tokenizer = RegexpTokenizer(r'\w+')  # Tokenizer que considera apenas alfa-numerico

        for (id_noticia, ind_corpus, corpo) in self.bd.seleciona_noticias(id_entidade, id_perfil):

            if (corpus and ind_corpus == 'N'):
                continue

            tokens_noticia = tokenizer.tokenize(corpo)
            total_palavras = total_palavras + len(tokens_noticia)

            for (polaridade,) in self.bd.soma_polaridade(id_noticia, id_entidade):

                total_referencias += 1

                if polaridade == 'PO':
                    positivo += 1
                elif polaridade == 'NE':
                    neutro += 1
                elif polaridade == 'NG':
                    negativo += 1

                total_referencias_tweet += self.bd.existe_entidade_tweet(id_entidade, id_noticia)

        if total_referencias == 0:
            media_palavras = 0
        else:
            media_palavras = float(total_palavras) / float(total_referencias)

        total_noticias_perfil = self.bd.conta_noticias(id_perfil, corpus)
        media_referencias = float(total_referencias) / total_noticias_perfil
        media_referencias_tweet = float(total_referencias_tweet) / total_noticias_perfil

        if positivo + neutro + negativo == 0:
            total_polaridade = 1
        else:
            total_polaridade = positivo + neutro + negativo

        proporcao_positivo = positivo / total_polaridade
        proporcao_neutro = neutro / total_polaridade
        proporcao_negativo = negativo / total_polaridade

        return np.array([media_referencias, media_palavras, proporcao_positivo, proporcao_neutro, proporcao_negativo, media_referencias_tweet])

    def mapeia_posicao(self, i, j, range):
        def deslcocamento(i, range):
            if i == 0:
                return 0

            return deslcocamento(i - 1, range) + range - (i + 1)

        return j - 1 + deslcocamento(i, range)

    def gera_pca(self, matriz_metricas, lista_perfis, id_entidade):

        pca = PCA(n_components=2)

        X = pca.fit(matriz_metricas).transform(matriz_metricas)
        y = np.array(lista_perfis)

        target_names = np.array(['Estadao', 'G1', 'Folha', 'Carta Capital', 'VEJA'])
        colors = cm.rainbow(np.linspace(0, 1, 5))

        plt.figure()
        for c, i, target_name in zip(colors, [1, 2, 3, 4, 5], target_names):
            plt.scatter(X[y == i, 0], X[y == i, 1], c=c, label=target_name)
        plt.legend()
        plt.title(id_entidade)

        plt.show()

    def calcula_distancia_total(self, id_entidade, corpus):

        lista_metricas = list()
        lista_perfis = list()

        for (id_perfil,) in self.bd.seleciona_perfis():

            lista_metricas.append(self.contabiliza_metricas(id_entidade, id_perfil, corpus))
            lista_perfis.append(id_perfil)

        matriz_metricas = scale(np.array(lista_metricas))
        vetor_distancias = pdist(matriz_metricas, 'euclidean')
        qtd_perfis = len(lista_perfis)

        for i in range(0, qtd_perfis):
            for j in range(i + 1, qtd_perfis):
                posic = self.mapeia_posicao(i, j, qtd_perfis)
                distancia = vetor_distancias[posic]
                id_perfil_1 = lista_perfis[i]
                id_perfil_2 = lista_perfis[j]
                print(id_perfil_1, id_perfil_2, distancia)
