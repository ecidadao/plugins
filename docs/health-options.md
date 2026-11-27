# Saúde: opções de integração

Investigação em 27/11/2026. A versão 0.3.3 acrescenta orientação estática SNS 24; nenhuma operação é executada no SNS; não foram usados dados de utentes nem realizadas marcações. Saúde pública e navegação de serviços podem avançar antes de qualquer acesso a dados pessoais.

Implementado: `/saude` e `sns24_service_guidance` com percursos PT/EN para consultas, exames, medicação e referenciações. As integrações abaixo permanecem condicionais.

Investigação aprofundada: [funcionalidades do portal/app SNS 24, RSE WebAPI e proposta de implementação](sns24-discovery.md).

## O que podemos oferecer

| Necessidade | Evidência disponível | Implementação proposta / dependência |
|---|---|---|
| Ver tempos de espera nas urgências | Portal oficial Tempos Médios de Espera; distingue triagem, primeira observação e observação | Começar por encaminhamento oficial. Para apresentar dados no eCidadão: confirmar fonte suportada, reutilização, cobertura e atualização; mostrar tipo de urgência, prioridade e hora da leitura |
| Comparar resposta de hospitais para consultas/cirurgias | O mesmo portal publica informação por instituição | Comparar apenas métricas equivalentes e especialidades; são indicadores agregados, não vagas nem previsão pessoal |
| Ver fila em tempo real no centro de saúde | Não foi identificado um feed nacional público suportado nesta pesquisa | Confirmar com SPMS/ULS existência de dados, cobertura e permissão de consumo; não reutilizar tempos das urgências como se fossem filas dos centros de saúde |
| Pedir consulta no centro de saúde | SNS 24 disponibiliza pedido online mediante inscrição e vagas da unidade | Percurso assistido pode ser implementado já. Marcação pelo eCidadão depende de API autorizada, autenticação delegada e confirmação oficial |
| Consulta hospitalar | Existem percursos de referenciação e canais do hospital | Explicar o percurso e as opções aplicáveis; não prometer agenda nacional de livre marcação. Para executar, confirmar regras e integração com o operador |
| Saber a situação pessoal numa lista de espera | A ERS identifica consulta de informação na área pessoal SNS 24 | Encaminhamento possível; consulta integrada exige acesso delegado específico e proteção dos dados de saúde |

O SNS 24 pode procurar alternativas em SAC/CAC quando não existem vagas na unidade, de acordo com critérios clínicos e referenciação. Isso não demonstra uma API aberta a terceiros. Proximidade e menor espera ajudam a compreender opções, mas não substituem a triagem nem determinam sozinhas o serviço adequado.

## Evidência técnica e limites

- A SPMS descreve atualização de urgências de dez em dez minutos e de consultas/cirurgias diariamente. A interface deve mostrar a data real do registo e tratar dados ausentes/desatualizados, sem garantir essa cadência para todas as unidades.
- O HTML e JavaScript públicos do portal foram consultados. A aplicação referencia `/api/institutions`, listas de especialidades e relatórios incorporados. Um GET anónimo a `/api/institutions` devolveu HTTP 400; não foi demonstrado um contrato de leitura utilizável por terceiros.
- A leitura inicial da RSE WebAPI 1.6.1 falhou (403/timeout); numa verificação posterior foi possível ler o PDF completo. A data interna é 10/12/2018 e exige registo/credenciais SPMS. Ver [análise técnica](sns24-discovery.md); não comprova contrato atual ou elegibilidade.
- Não foram contactados endpoints de escrita, usadas credenciais ou extraídos tokens de relatórios.
- A marcação no SNS 24 é descrita como envio de um pedido à unidade. O eCidadão deverá distinguir pedido enviado, aceite e marcação confirmada.

## Ordem de execução

1. **Percurso saúde assistido:** encontrar os canais oficiais para consultas, tempos de espera e referenciações; publicar no site e avaliar uma ferramenta pública específica com testes e documentação.
2. **Tempos de espera públicos:** confirmar acesso e reutilização com SPMS; construir adaptador só de leitura, normalização e testes de dados antigos/indisponíveis. Não ordenar hospitais como recomendação clínica.
3. **Piloto centro de saúde/ULS:** confirmar se existem dados de filas e disponibilidade e quais as unidades abrangidas. Demonstrar uma unidade antes de prometer cobertura nacional.
4. **Marcações e acompanhamento pessoais:** contrato, ambiente de testes, autorização delegada, minimização de dados, cancelamento e prevenção de duplicados. Só apresentar conclusão com confirmação oficial.

## Questões para SPMS/ULS

Há um contrato público suportado para tempos de urgência, indicadores de consultas/cirurgias e diretório de unidades? Quais as condições de reutilização, limites, timestamps e identificadores? Existem filas públicas ou disponibilidade dos cuidados primários? Um serviço privado pode atuar como integrador delegado de marcações? Que autenticação, consentimento, ambientes de teste, unidades e operações são permitidos? Como distinguir pedido de consulta de agendamento aceite e obter/cancelar o comprovativo?

Estas questões estão preparadas para uma eventual consulta técnica; não foram enviadas.

## Fontes oficiais

- [Portal Tempos Médios de Espera](https://tempos.min-saude.pt/).
- [SPMS: funcionamento e atualização do portal, 02/07/2025](https://spms.min-saude.pt/wp-content/uploads/2025/12/Nota-de-Imprensa-SPMS-Portal-Tempos-de-Espera_02.07.2025.pdf).
- [SNS 24: marcação de consultas](https://www.sns24.gov.pt/pt/servico/marcacao-de-consultas/).
- [SNS 24: triagem, disponibilidade e encaminhamento](https://www.sns24.gov.pt/pt/servico/triagem-e-encaminhamento-do-sns-24/).
- [gov.pt: consulta médica no hospital](https://www.gov.pt/servicos/marcar-consulta-medica-no-hospital).
- [ERS: perguntas frequentes e informação sobre acesso](https://www.ers.pt/pt/utentes/perguntas-frequentes/).
