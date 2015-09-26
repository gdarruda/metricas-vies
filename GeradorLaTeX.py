#coding: utf-8
from scipy.stats.stats import pearsonr
import matplotlib.pyplot as plt


from ExtratorMetricas import ExtratorMetricas

class GeradorLaTeX():

    def __init__(self, EM):
        self.entidades = {4074: 'Alckmin', 4078: 'Padilha', 4075: 'Skaf', 3956: 'Neves', 4031: 'Rousseff', 4039: 'Silva'}
        self.perfis = {1: '@EstadaoPolitica', 2: '@g1politica', 3: '@folha\_poder', 4: '@cartacapital', 5: '@VEJA'}
        self.entidades_ordenadas = [4074, 4078, 4075, 3956, 4031, 4039]
        self.tipo_vies = [0, 5, 2, 3, 4]
        self.EM = EM

    def gera_header(self):
        print('\cline{2-7}')
        print('\multirow{2}{*}{Perfil} & \multicolumn{6}{c}{Entidade} \\\\ \cline{2-7}')
        print('& ' + self.entidades[4074] + ' & ' + self.entidades[4078] + ' & ' + self.entidades[4075] + ' & ' + self.entidades[3956] + ' & ' + self.entidades[4031] + ' & ' + self.entidades[4039] + ' \\\ \hline ')

    def seleciona_metrica(self, metrica):

        case = {'SELECAO': 0,
                'COBERTURA_TAMANHO': 1,
                'COBERTURA_TWEET': 5,
                'POLARIDADE_POSITIVA': 2,
                'POLARIDADE_NEUTRA': 3,
                'POLARIDADE_NEGATIVA': 4}

        return case[metrica]

    def seleciona_tipo_desvio(self, tipo_desvio):

        case = {'MEDIA': 'desvio_padrao_media',
                'MEDIANA': 'desvio_absoluto_mediana'}

        return case[tipo_desvio]

    def gera_correlacao_vies(self):

        vieses = {}
        correlacao_vieses = {}

        for id_perfil in range(1, 5):
            for id_entidade in self.entidades_ordenadas:

                metricas = self.EM.contabiliza_metricas(id_entidade, id_perfil, True)

                for tipo_vies in self.tipo_vies:

                    if tipo_vies not in vieses:
                        vieses[tipo_vies] = []

                    vieses[tipo_vies].append(metricas[tipo_vies])

        for tipo_vies_1 in self.tipo_vies:
            for tipo_vies_2 in self.tipo_vies:

                if tipo_vies_1 not in correlacao_vieses:
                    correlacao_vieses[tipo_vies_1] = {}

                correlacao_vieses[tipo_vies_1][tipo_vies_2] = pearsonr(vieses[tipo_vies_1], vieses[tipo_vies_2])
                print tipo_vies_1
                print tipo_vies_2
                print correlacao_vieses[tipo_vies_1][tipo_vies_2]
                plt.plot(vieses[tipo_vies_1], vieses[tipo_vies_2], 'ro')
                plt.show()

        return correlacao_vieses

    def gera_vies_tabela(self, metrica):

        self.gera_header()
        posic = self.seleciona_metrica(metrica)

        for id_perfil, nome_perfil in self.perfis.iteritems():
            linha = nome_perfil

            for id_entidade in self.entidades_ordenadas:
                if (metrica != 'COBERTURA_TAMANHO'):
                    percentual = self.EM.contabiliza_metricas(id_entidade, id_perfil, True)[posic]
                    linha = linha + " & " + str(round(percentual, 4) * 100).replace('.', ',') + '\\%'
                else:
                    metrica_calculada = self.EM.contabiliza_metricas(id_entidade, id_perfil, True)[posic]
                    linha = linha + " & " + str(round(metrica_calculada, 2))

            print(linha + " \\\\")

    def gera_desvio(self, metrica, tipo_desvio):

        self.gera_header()

        posic = self.seleciona_metrica(metrica)
        tipo_desvio = self.seleciona_tipo_desvio(tipo_desvio)
        mapa_desvio = {}
        mapa_metrica = {}

        for id_entidade in self.entidades_ordenadas:

            mapa_metrica[id_entidade] = {}

            for id_perfil, nome_perfil in self.perfis.iteritems():
                percentual = self.EM.contabiliza_metricas(id_entidade, id_perfil, True)[posic]
                mapa_metrica[id_entidade][id_perfil] = percentual

            valores_entidade = mapa_metrica[id_entidade].values()
            mapa_desvio[id_entidade] = self.EM.desvio_padrao_media(valores_entidade)
            mapa_desvio[id_entidade] = getattr(self.EM, tipo_desvio)(valores_entidade)

        for id_perfil, nome_perfil in self.perfis.iteritems():

            linha = nome_perfil

            for id_entidade in self.entidades_ordenadas:
                dam, m = mapa_desvio[id_entidade]
                qtd_desvio = (mapa_metrica[id_entidade][id_perfil] - m) / dam
                linha = linha + " & " + str(round(qtd_desvio, 2)).replace('.', ',')

            print linha + " \\\\"
