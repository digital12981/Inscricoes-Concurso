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
                logger.error(f"CPF inválido: {cpf}")
                return None

            url = self.api_url.format(cpf=cpf_numerico)

            # Criar uma nova sessão com configurações otimizadas
            session = requests.Session()
            adapter = requests.adapters.HTTPAdapter(
                max_retries=3,
                pool_connections=5,
                pool_maxsize=5
            )
            session.mount('https://', adapter)
            session.mount('http://', adapter)
            
            session.headers.update({
                'User-Agent': 'Mozilla/5.0',
                'Accept': 'application/json',
                'Accept-Language': 'pt-BR,pt;q=0.9',
            })

            logger.info(f"Iniciando consulta de CPF: {cpf_numerico[:3]}***{cpf_numerico[-2:]}")
            
            # Reduzido o timeout para evitar conexões penduradas
            response = session.get(
                url, 
                timeout=15,
                verify=True
            )
            
            logger.info(f"Status code: {response.status_code}")
            
            if response.status_code != 200:
                logger.error(f"API returned non-200 status code: {response.status_code}")
                return None

            dados = response.json()
            return dados.get('DADOS', {})

        except Exception as e:
            logger.error(f"Erro inesperado na consulta: {str(e)}")
            return None
        finally:
            if session:
                session.close()