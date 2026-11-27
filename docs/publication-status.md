# Publicação e capacidades

Verificação: 27/11/2026. Separar sempre versão do pacote, disponibilidade do endpoint e aprovação de cada diretório.

## Preparação 0.3.4 — pendente de rollout

O ramo `feat/municipal-support-0.3.4` prepara o manifesto e os adaptadores 0.3.4 para dez ferramentas públicas.
As novas capacidades abaixo estão **pendentes de rollout confirmado do servidor**; esta preparação local não fez push, PR, tag ou release.
O registo da verificação HTTP 0.3.3 abaixo é histórico e não confirma a disponibilidade das três ferramentas novas.
A versão publicada continua identificada separadamente na tabela; não atualizar estados de diretórios sem evidência própria.

## Distribuição

| Canal | Versão / estado | Evidência e trabalho pendente |
|---|---|---|
| GitHub Release | v0.3.3 publicada em 27/11/2026 | [Release e ZIP](https://github.com/ecidadao/plugins/releases/tag/v0.3.3) |
| Codex, marketplace deste repositório | Pacote 0.3.3 disponível | Manifesto e catálogo em GitHub; comandos no README |
| Claude Code, marketplace deste repositório | Pacote 0.3.3 disponível | Adaptadores gerados e validados pela CI; comandos no README |
| OpenAI, diretório oficial | 0.3.1: último estado comunicado **In review**, 13/11/2026 | [Registo histórico](https://github.com/ecidadao/ecidadao/blob/main/docs/plugin-submission-0.3.1.md); reconfirmar painel antes de anunciar aprovação ou publicação |
| Anthropic, diretório oficial | Publicação não confirmada | Marketplace próprio não demonstra inclusão no diretório oficial |
| Mistral, conector personalizado | Configuração documentada; teste no cliente pendente | [Guia](mistral.md); sem publicação em catálogo Mistral confirmada |

O endpoint `https://ecidadao.pt/mcp/public` respondeu a `initialize` (protocolo `2025-06-18`) e `tools/list` nesta verificação, identificando servidor 0.3.3 e sete ferramentas. Isto não substitui um teste dentro de cada cliente.

## Matriz de funcionalidades

| Funcionalidade | Plugin / MCP público | Website / experimental |
|---|---|---|
| Orientação SIGA | `siga_visit_guidance` | Percurso assistido no site |
| Orientação Finanças | `financas_service_guidance` | Percurso assistido no site |
| Rascunho e-balcão | `prepare_financas_ebalcao` | Preparação assistida |
| Rascunho A Minha Rua | `prepare_street_report` | Preparação assistida |
| Reclamação de consumo | `prepare_complaint`, `official_submission_guidance` | Preparação e encaminhamento |
| Pesquisa municipal estática | `municipal_service_search`, **pendente de rollout 0.3.4**; 320 entradas: Gondomar 136, Maia 126, Ponte de Lima 58 | Encaminhamento oficial; entrada de catálogo não equivale a operação executável |
| Disponibilidade municipal | `municipal_appointment_availability`, **pendente de rollout 0.3.4** | Apenas Ponte de Lima; GET do frontend público em tempo real, sem reserva |
| Apoios de habitação e ambiente | `public_support_guidance`, **pendente de rollout 0.3.4** | Sete percursos PT/EN com fontes e datas; sem candidatura, dados pessoais ou garantia de aprovação |
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

## Passagem a release 0.3.4

1. Aguardar confirmação do coordenador de que a aplicação 0.3.4 está implantada; até lá, manter os três estados como pendentes e não fazer push, PR, tag ou release.
2. Depois dessa confirmação, verificar `initialize` e `tools/list` no endpoint público e registar data, versão e os dez nomes exatos; executar os [cenários de revisão](review-0.3.4.md), incluindo falhas de leitura e limites de cobertura.
3. Só com evidência, atualizar esta matriz e o registo HTTP, retirar os avisos de rollout pendente do manifesto (longDescription/release_notes), dos dois READMEs e do guia Mistral; preservar as limitações e os registos históricos.
4. Executar novamente sync/check/build e validações; após autorização de publicação, publicar o pacote/tag correspondente e atualizar links e estados GitHub/Codex/Claude para 0.3.4 apenas quando confirmados.
5. Manter OpenAI 0.3.1, Anthropic e validação Mistral independentes: disponibilidade HTTP ou GitHub Release não comprova aprovação nem execução dentro desses clientes.

Serviços de apoio: `porta65_young`, `porta65_plus`, `gondomar_housing`, `environmental_fund`, `vale_efficiency`, `elar`, `green_mobility`.
Estados devem distinguir candidatura nova, ação de beneficiário existente e pagamento de fornecedor; nunca converter prazo antigo em disponibilidade atual, nem dotação total em saldo disponível.
