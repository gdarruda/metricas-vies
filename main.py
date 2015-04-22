from ExtratorMetricas import ExtratorMetricas
from BancoDados import BancoMySQL

bd = BancoMySQL('garruda', 'garruda', '127.0.0.1', 'noticias')
EM = ExtratorMetricas(bd)

def calcula_metricas(id_entidade):
    # print (EM.contabiliza_metricas(id_entidade,id_perfil,True))
    EM.calcula_distancia_total(id_entidade,True)

# calcula_metricas(4074) #Alckmin
# calcula_metricas(4078) #Padilha
# calcula_metricas(4075) #Skaf
# calcula_metricas(3956) #Aecio
# calcula_metricas(4031) #Dilma
EM.classifica_tweets()
