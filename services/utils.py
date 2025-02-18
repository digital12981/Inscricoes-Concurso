import random
import logging
from typing import List

logger = logging.getLogger(__name__)

def gerar_nomes_falsos(nome_real: str) -> List[str]:
    """
    Gera uma lista de 3 nomes de forma não recursiva.
    """
    try:
        # Lista base de nomes
        nomes_base = [
            "MARIA SILVA SANTOS",
            "JOSE OLIVEIRA SOUZA",
            "ANA PEREIRA LIMA",
            "JOAO FERREIRA COSTA",
            "ANTONIO RODRIGUES ALVES",
            "FRANCISCO GOMES SILVA",
            "CARLOS SANTOS OLIVEIRA",
            "PAULO RIBEIRO MARTINS",
            "PEDRO ALMEIDA COSTA",
            "LUCAS CARVALHO LIMA"
        ]

        # Garante que o nome_real é uma string e está em maiúsculas
        nome_real = str(nome_real).upper()
        palavras_nome_real = set(nome_real.split())
        
        # Filtra nomes diferentes de uma só vez
        nomes_diferentes = []
        for nome in nomes_base:
            palavras_nome = set(nome.split())
            if not palavras_nome.intersection(palavras_nome_real):
                nomes_diferentes.append(nome)
                if len(nomes_diferentes) == 2:
                    break
                    
        # Se não encontrou nomes suficientes, usa nomes padrão
        while len(nomes_diferentes) < 2:
            padrao = "MARIA OLIVEIRA SANTOS" if len(nomes_diferentes) == 0 else "JOSE SILVA COSTA"
            if padrao not in nomes_diferentes:
                nomes_diferentes.append(padrao)

        # Cria lista final e embaralha
        todos_nomes = nomes_diferentes[:2] + [nome_real]
        random.shuffle(todos_nomes)
        
        return todos_nomes

    except Exception as e:
        logger.error(f"Erro ao gerar nomes falsos: {str(e)}")
        return ["MARIA OLIVEIRA SANTOS", "JOSE SILVA COSTA", str(nome_real).upper()]