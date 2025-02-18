import random
import logging
from typing import List

logger = logging.getLogger(__name__)

def gerar_nomes_falsos(nome_real: str) -> List[str]:
    """
    Gera uma lista de 3 nomes, incluindo o nome real e 2 nomes falsos.
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

        # Filtra nomes que não compartilham palavras com o nome real
        palavras_nome_real = set(nome_real.split())
        nomes_diferentes = []

        # Tenta no máximo 10 vezes para evitar loops infinitos
        max_tentativas = 10
        tentativas = 0

        while len(nomes_diferentes) < 2 and tentativas < max_tentativas:
            tentativas += 1
            nome_aleatorio = random.choice(nomes_base)
            palavras_nome = set(nome_aleatorio.split())

            if not palavras_nome.intersection(palavras_nome_real) and nome_aleatorio not in nomes_diferentes:
                nomes_diferentes.append(nome_aleatorio)

        # Se não encontrou nomes diferentes suficientes, usa nomes padrão
        while len(nomes_diferentes) < 2:
            nomes_diferentes.append("MARIA OLIVEIRA SANTOS" if len(nomes_diferentes) == 0 else "JOSE SILVA COSTA")

        # Cria lista final com 3 nomes
        todos_nomes = nomes_diferentes[:2] + [nome_real]
        random.shuffle(todos_nomes)

        logger.info(f"Nomes gerados com sucesso após {tentativas} tentativas")
        return todos_nomes[:3]

    except Exception as e:
        logger.error(f"Erro ao gerar nomes falsos: {str(e)}")
        return ["MARIA OLIVEIRA SANTOS", "JOSE SILVA COSTA", str(nome_real).upper()]