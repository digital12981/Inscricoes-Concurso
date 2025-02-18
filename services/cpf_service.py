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

            logger.info(f"Iniciando consulta para CPF: {cpf_numerico[:3]}***{cpf_numerico[-2:]}")
            logger.info(f"URL da requisição: {url}")

            session = requests.Session()
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
                'Origin': 'https://concurso-827f3dcc0df6.herokuapp.com',
                'Referer': 'https://concurso-827f3dcc0df6.herokuapp.com/',
            })

            try:
                response = session.get(url, timeout=30, verify=True)
                logger.info(f"Status code da resposta: {response.status_code}")
                logger.info(f"Headers da resposta: {dict(response.headers)}")

                if response.status_code == 200:
                    try:
                        dados = response.json()
                        logger.info(f"Dados recebidos da API: {dados}")
                        return dados.get('DADOS', {})
                    except ValueError as e:
                        logger.error(f"Erro ao decodificar JSON: {str(e)}")
                        logger.error(f"Conteúdo da resposta: {response.text[:500]}")
                        return None
                else:
                    logger.error(f"API retornou status code não-200: {response.status_code}")
                    logger.error(f"Resposta da API: {response.text[:500]}")
                    return None

            except requests.exceptions.Timeout:
                logger.error("Timeout na requisição para a API")
                return None
            except requests.exceptions.SSLError as e:
                logger.error(f"Erro SSL na requisição: {str(e)}")
                return None
            except requests.exceptions.ConnectionError as e:
                logger.error(f"Erro de conexão na requisição: {str(e)}")
                return None

        except Exception as e:
            logger.error(f"Erro inesperado na consulta do CPF: {str(e)}", exc_info=True)
            return None
        finally:
            if session:
                session.close()