from ExtratorMetricas import ExtratorMetricas
from BancoDados import BancoMySQL

bd = BancoMySQL('garruda', 'garruda', '127.0.0.1', 'noticias')

def calcula_metricas(id_entidade):
    EM = ExtratorMetricas(bd)
    # print (EM.contabiliza_metricas(id_entidade,id_perfil,True))
    EM.calcula_distancia_total(id_entidade,True)

calcula_metricas(4039)
