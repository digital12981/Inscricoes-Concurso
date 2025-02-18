import requests
import logging
from typing import Dict, Any, Optional
import time

logger = logging.getLogger(__name__)

class CpfService:
    def __init__(self, api_url: str, token: str):
        self.api_url = api_url
        self.token = token
        self.max_retries = 3
        self.retry_delay = 1  # segundos entre tentativas

    def consultar_cpf(self, cpf: str) -> Optional[Dict[str, Any]]:
        """
        Consulta CPF na API externa usando abordagem iterativa
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
                max_retries=0,  # Desabilita retries automáticos
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
            
            # Loop de tentativas
            for tentativa in range(self.max_retries):
                try:
                    response = session.get(
                        url, 
                        timeout=5,  # Reduzido timeout
                        verify=True
                    )
                    
                    logger.info(f"Tentativa {tentativa + 1}: Status code {response.status_code}")
                    
                    if response.status_code == 200:
                        dados = response.json()
                        return dados.get('DADOS', {})
                    
                    # Se não for 200, espera antes da próxima tentativa
                    if tentativa < self.max_retries - 1:
                        time.sleep(self.retry_delay)
                        
                except requests.exceptions.RequestException as e:
                    logger.warning(f"Erro na tentativa {tentativa + 1}: {str(e)}")
                    if tentativa < self.max_retries - 1:
                        time.sleep(self.retry_delay)
                    continue

            logger.error("Todas as tentativas falharam")
            return None

        except Exception as e:
            logger.error(f"Erro inesperado na consulta: {str(e)}")
            return None
        finally:
            if session:
                session.close()