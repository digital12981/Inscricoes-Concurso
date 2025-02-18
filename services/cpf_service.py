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
        Consulta CPF na API externa
        """
        session = None
        try:
            cpf_numerico = ''.join(filter(str.isdigit, cpf))

            if not cpf_numerico or len(cpf_numerico) != 11:
                logger.error("CPF inválido")
                return None

            url = self.api_url.format(cpf=cpf_numerico)

            session = requests.Session()
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
                'Origin': 'https://concurso-827f3dcc0df6.herokuapp.com',
                'Referer': 'https://concurso-827f3dcc0df6.herokuapp.com/',
            })

            logger.info(f"Iniciando consulta de CPF: {cpf_numerico[:3]}***{cpf_numerico[-2:]}")

            logger.info(f"Fazendo requisição para URL: {url}")
            response = session.get(url, timeout=60, verify=True)
            logger.info(f"Status code: {response.status_code}")
            logger.info(f"Response body: {response.text[:500]}")

            if response.status_code != 200:
                logger.error(f"API returned non-200 status code: {response.status_code}")
                return None

            dados = response.json()
            return dados.get('DADOS', {})

        except Exception as e:
            logger.error(f"Erro na consulta do CPF: {str(e)}")
            return None
        finally:
            if session:
                session.close()