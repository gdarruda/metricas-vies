from ExtratorMetricas import ExtratorMetricas
from BancoDados import BancoMySQL
from GeradorLaTeX import GeradorLaTeX
import csv

bd = BancoMySQL('garruda', 'garruda', '127.0.0.1', 'noticias')
EM = ExtratorMetricas(bd)
GL = GeradorLaTeX(EM)


def calcula_metricas(id_entidade):
    EM.calcula_distancia_total(id_entidade, True)


def imprime_metricas(id_entidade, header=False):

    f = open('saida.csv', 'ab')
    writer = csv.writer(f)

    if header:
        writer.writerow(['entidade', 'perfil', 'selecao', 'cobertura', 'positivo', 'neutro', 'negativo'])

    for id_perfil in range(1, 6):
        metricas = EM.contabiliza_metricas(id_entidade, id_perfil, True)
        writer.writerow([id_entidade, id_perfil, metricas[0], metricas[5], metricas[2], metricas[3], metricas[4]])

    f.close()

imprime_metricas(4074, True)  # Alckmin
imprime_metricas(4078)  # Padilha
imprime_metricas(4075)  # Skaf
imprime_metricas(3956)  # Aecio
imprime_metricas(4031)  # Dilma
imprime_metricas(4039)  # Marina


GL.gera_desvio('SELECAO', 'MEDIA')
GL.gera_desvio('COBERTURA_TWEET', 'MEDIA')
GL.gera_desvio('POLARIDADE_POSITIVA', 'MEDIA')
GL.gera_desvio('POLARIDADE_NEUTRA', 'MEDIA')
GL.gera_desvio('POLARIDADE_NEGATIVA', 'MEDIA')
