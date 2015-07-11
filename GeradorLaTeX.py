#coding: utf-8

from ExtratorMetricas import ExtratorMetricas

class GeradorLaTeX():

    def __init__(self, EM):
        self.entidades = {4074: 'Alckmin', 4078: 'Padilha', 4075: 'Skaf', 3956: 'Neves', 4031: 'Rousseff', 4039:'Silva'}
        self.perfis = {1:'@EstadaoPolitica', 2:'@g1politica', 3:'@folha\_poder', 4:'@cartacapital', 5:'@VEJA'}
        self.EM = EM

    def gera_header(self):
        print('\cline{2-7}')
        print('\multirow{2}{*}{Perfil} & \multicolumn{6}{c}{Entidade} \\\ \cline{2-7}')
        print('& ' + self.entidades[4074] + ' & ' + self.entidades[4078] + ' & ' + self.entidades[4075] + ' & ' + self.entidades[3956] + ' & ' + self.entidades[4031] + ' & ' + self.entidades[4039] + ' \\\ \hline ')

    def gera_vies_selecao(self):

        self.gera_header()

        for id_perfil, nome_perfil in self.perfis.iteritems():
            linha = nome_perfil

            for id_entidade in [4074, 4078, 4075, 3956, 4031, 4039]:
                percentual = self.EM.contabiliza_metricas(id_entidade, id_perfil, True)[0]
                linha = linha + " & " + str(round(percentual, 2)).replace('.', ',')

            print(linha + " \\\\")
