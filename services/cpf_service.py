import requests
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class CpfService:
    def __init__(self, api_url: str, token: str):
        self.api_url = api_url
        self.token = token
        self.timeout = 10
        self.headers = {
            'User-Agent': 'Mozilla/5.0',
            'Accept': 'application/json',
            'Accept-Language': 'pt-BR,pt;q=0.9',
        }

    def consultar_cpf(self, cpf: str) -> Optional[Dict[str, Any]]:
        """
        Consulta CPF na API externa de forma simples e direta
        """
        try:
            # Limpa o CPF
            cpf_numerico = ''.join(filter(str.isdigit, cpf))
            if not cpf_numerico or len(cpf_numerico) != 11:
                logger.error(f"CPF inválido: {cpf}")
                return None

            # Monta a URL
            url = self.api_url.format(cpf=cpf_numerico)
            logger.info(f"Iniciando consulta de CPF: {cpf_numerico[:3]}***{cpf_numerico[-2:]}")

            # Faz a requisição
            response = requests.get(
                url,
                headers=self.headers,
                timeout=self.timeout,
                verify=True
            )

            # Verifica o status code
            if response.status_code == 200:
                try:
                    dados = response.json()
                    return dados.get('DADOS', {})
                except ValueError as e:
                    logger.error(f"Erro ao decodificar JSON: {e}")
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