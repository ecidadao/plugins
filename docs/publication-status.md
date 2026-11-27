# Publicação e capacidades

Verificação: 27/11/2026. Separar sempre versão do pacote, disponibilidade do endpoint e aprovação de cada diretório.

## Servidor 0.3.4 confirmado

Em 27/11/2026, o [deploy 46009722760](https://github.com/ecidadao/ecidadao/actions/runs/46009722760) terminou com sucesso.
O endpoint `/health` anunciou exatamente `96e027d39b83da1b6123277a8c487c9014ed5fa3`, merge do [PR da aplicação #11](https://github.com/ecidadao/ecidadao/pull/11).
O pacote 0.3.4 foi publicado em 27/11/2026 às 13:50 UTC; a release e o ZIP descarregado foram confirmados após o workflow.
A evidência HTTP e os limites estão registados na [revisão 0.3.4](review-0.3.4.md).

## Distribuição

| Canal | Versão / estado | Evidência e trabalho pendente |
|---|---|---|
| GitHub Release | v0.3.4 publicada em 27/11/2026 | [Release e ZIP](https://github.com/ecidadao/plugins/releases/tag/v0.3.4) |
| Codex, marketplace deste repositório | Pacote 0.3.4 disponível | Manifesto e catálogo em GitHub; comandos no README |
| Claude Code, marketplace deste repositório | Pacote 0.3.4 disponível | Adaptadores gerados e validados pela CI; comandos no README |
| OpenAI, diretório oficial | 0.3.1: último estado comunicado **In review**, 13/11/2026 | [Registo histórico](https://github.com/ecidadao/ecidadao/blob/main/docs/plugin-submission-0.3.1.md); reconfirmar painel antes de anunciar aprovação ou publicação |
| Anthropic, diretório oficial | Publicação não confirmada | Marketplace próprio não demonstra inclusão no diretório oficial |
| Mistral, conector personalizado | Configuração documentada; teste no cliente pendente | [Guia](mistral.md); sem publicação em catálogo Mistral confirmada |

O endpoint `https://ecidadao.pt/mcp/public` respondeu a `initialize` (protocolo `2025-06-18`) e `tools/list` nesta verificação, identificando servidor 0.3.4 e dez ferramentas. Isto não substitui um teste dentro de cada cliente.

## Matriz de funcionalidades

| Funcionalidade | Plugin / MCP público | Website / experimental |
|---|---|---|
| Orientação SIGA | `siga_visit_guidance` | Percurso assistido no site |
| Orientação Finanças | `financas_service_guidance` | Percurso assistido no site |
| Rascunho e-balcão | `prepare_financas_ebalcao` | Preparação assistida |
| Rascunho A Minha Rua | `prepare_street_report` | Preparação assistida |
| Reclamação de consumo | `prepare_complaint`, `official_submission_guidance` | Preparação e encaminhamento |
| Pesquisa municipal estática | `municipal_service_search`, disponível no servidor 0.3.4; 320 entradas: Gondomar 136, Maia 126, Ponte de Lima 58 | Encaminhamento oficial; entrada de catálogo não equivale a operação executável |
| Disponibilidade municipal | `municipal_appointment_availability`, disponível no servidor 0.3.4 | Apenas Ponte de Lima; GET do frontend público em tempo real, sem reserva |
| Apoios de habitação e ambiente | `public_support_guidance`, disponível no servidor 0.3.4 | Sete percursos PT/EN com fontes e datas; sem candidatura, dados pessoais ou garantia de aprovação |
| Pesquisa por necessidade | Não incluída | [Website](https://ecidadao.pt/servicos), nove percursos curados |
| Livro Amarelo: reclamação, elogio, sugestão | Não incluído | Website e `prepare_public_service_feedback` em `/mcp` experimental |
| Filas SIGA em tempo real | Não incluídas | Adaptador do website, com cobertura limitada; acesso de integração por confirmar |
| Inglês e tema automático | Funcionalidades de interface do site; não são ferramentas MCP | Disponíveis no website; rascunhos MCP continuam em português |
| Marcação, senha, submissão oficial ou acesso a contas | Não disponível | Não implementado como operação concluída pelo serviço |
| Orientação SNS 24 | `sns24_service_guidance`: consultas, exames, medicação e referenciações em PT/EN | `/saude`, mesmos percursos; sem acesso a contas, vagas ou submissões |
| Saúde: filas, dados pessoais e marcações executadas | Não disponível | [Opções e plano de integração](health-options.md); nenhuma integração transacional SNS ativa |

As duas skills distribuídas são `siga-assistido` e `financas-assistido`. Ligar apenas o MCP noutro cliente não instala automaticamente essas skills.

## Próximas versões

1. Avaliar ferramentas públicas para pesquisa curada e Livro Amarelo, com testes, documentação e atualização do âmbito de revisão.
2. Validar Mistral com chamada real dentro do cliente e registar data, versão, resultado e limitações.
3. Só acrescentar consultas ou transações externas após confirmar contrato, cobertura e permissões. CUSP, SIGA transacional e SNS são dependências distintas.

A versão 0.3.3 acrescenta orientação SNS 24. A candidatura OpenAI 0.3.1 continua a ser um registo separado; a publicação desta versão no GitHub não atualiza nem aprova essa candidatura. Ao alterar estados, conservar fonte e data; nunca converter «submetido» em «aprovado» sem confirmação.

## Publicação do pacote 0.3.4

O [PR #6](https://github.com/ecidadao/plugins/pull/6) foi integrado com [CI verde](https://github.com/ecidadao/plugins/actions/runs/46010344688) no head `2233a2e3a6cdfe8f5072aee36d3466505de27016`.
A tag `v0.3.4` aponta para o merge `633fbea4b82c6aaa58aae4fe53bed9356e201396`.
O [workflow da tag](https://github.com/ecidadao/plugins/actions/runs/46010532379) gerou a [release pública](https://github.com/ecidadao/plugins/releases/tag/v0.3.4), sem marcação draft ou prerelease.
O ZIP foi descarregado sem autenticação: dez ficheiros correspondem byte a byte aos ficheiros do plugin na tag, ambos os manifestos indicam 0.3.4, as duas skills e o endpoint público são preservados.
SHA-256: `ee6c883c438997f472b9bfa008a8dcffa3a39ee5a08f562753b16b428b71f4e0`.
Não foi instalada nem atualizada uma instância do plugin no cliente do utilizador.
OpenAI 0.3.1, Anthropic e validação Mistral mantêm estados independentes: disponibilidade HTTP ou GitHub Release não comprova aprovação nem execução dentro desses clientes.

Serviços de apoio: `porta65_young`, `porta65_plus`, `gondomar_housing`, `environmental_fund`, `vale_efficiency`, `elar`, `green_mobility`.
Estados devem distinguir candidatura nova, ação de beneficiário existente e pagamento de fornecedor; nunca converter prazo antigo em disponibilidade atual, nem dotação total em saldo disponível.
