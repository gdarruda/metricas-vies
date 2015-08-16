from ExtratorMetricas import ExtratorMetricas
from BancoDados import BancoMySQL
from GeradorLaTeX import GeradorLaTeX

bd = BancoMySQL('garruda', 'garruda', '127.0.0.1', 'noticias')
EM = ExtratorMetricas(bd)
GL = GeradorLaTeX(EM)


def calcula_metricas(id_entidade):
    print (EM.contabiliza_metricas(id_entidade,id_perfil,True))
    # EM.calcula_distancia_total(id_entidade, True)

def imprime_metricas(id_entidade):
    for id_perfil in range (1,5):
        print(id_perfil, id_entidade, EM.contabiliza_metricas(id_entidade, id_perfil, True))

# imprime_metricas(4074)  # Alckmin
# imprime_metricas(4078)  # Padilha
# imprime_metricas(4075)  # Skaf
# imprime_metricas(3956)  # Aecio
# imprime_metricas(4031)  # Dilma
# imprime_metricas(4039)  # Marina

# GL.gera_vies_tabela('SELECAO')
GL.gera_desvio('SELECAO', 'MEDIA')
GL.gera_desvio('SELECAO', 'MEDIANA')
