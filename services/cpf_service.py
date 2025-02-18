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

            # Faz a requisição com timeout reduzido
            response = requests.get(
                self.api_url.format(cpf=cpf_numerico),
                timeout=10,
                headers={'Accept': 'application/json'}
            )

            # Verifica o status code
            if response.status_code == 200:
                try:
                    # Tenta fazer o parse do JSON de forma segura
                    texto_resposta = response.text
                    if not texto_resposta:
                        logger.error("Resposta vazia da API")
                        return None
                    
                    dados = response.json()
                    if dados and isinstance(dados, dict) and 'DADOS' in dados:
                        return dados['DADOS']
                    else:
                        logger.error(f"Formato de resposta inválido: {texto_resposta[:100]}")
                        return None
                except ValueError as e:
                    logger.error(f"Erro ao fazer parse do JSON: {str(e)}")
                    return None
                except Exception as e:
                    logger.error(f"Erro ao processar resposta: {str(e)}")
                    return None
            else:
                logger.error(f"Erro na API: Status {response.status_code}")
                return None

        except requests.exceptions.Timeout:
            logger.error("Timeout na requisição")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro na requisição: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Erro inesperado: {str(e)}")
            return None