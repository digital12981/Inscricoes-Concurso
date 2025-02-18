import requests
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class CpfService:
    def __init__(self, api_url: str, token: str):
        self.api_url = api_url
        self.token = token

    def consultar_cpf(self, cpf: str) -> Optional[Dict[str, Any]]:
        """
        Consulta CPF na API externa usando uma única requisição simples
        """
        try:
            # Limpa o CPF
            cpf_numerico = ''.join(filter(str.isdigit, cpf))
            
            if not cpf_numerico or len(cpf_numerico) != 11:
                logger.error(f"CPF inválido: {cpf}")
                return None

            # Log da consulta (mascarando o CPF)
            logger.info(f"Iniciando consulta de CPF: {cpf_numerico[:3]}***{cpf_numerico[-2:]}")

            # Faz a requisição de forma simples
            response = requests.get(
                self.api_url.format(cpf=cpf_numerico),
                timeout=30
            )

            # Verifica o status code
            if response.status_code == 200:
                dados = response.json()
                if dados and 'DADOS' in dados:
                    return dados['DADOS']
                else:
                    logger.error("Resposta da API não contém dados válidos")
                    return None
            else:
                logger.error(f"Erro na API: Status {response.status_code}")
                return None

        except requests.exceptions.Timeout:
            logger.error("Timeout na requisição")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro na requisição: {e}")
            return None
        except Exception as e:
            logger.error(f"Erro inesperado: {e}")
            return None