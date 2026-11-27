# Publicação e capacidades

Verificação: 27/11/2026. Separar sempre versão do pacote, disponibilidade do endpoint e aprovação de cada diretório.

## Distribuição

| Canal | Versão / estado | Evidência e trabalho pendente |
|---|---|---|
| GitHub Release | v0.3.2 publicada em 26/11/2026 | [Release e ZIP](https://github.com/ecidadao/plugins/releases/tag/v0.3.2) |
| Codex, marketplace deste repositório | Pacote 0.3.2 disponível | Manifesto e catálogo em GitHub; comandos no README |
| Claude Code, marketplace deste repositório | Pacote 0.3.2 disponível | Adaptadores gerados e validados pela CI; comandos no README |
| OpenAI, diretório oficial | 0.3.1: último estado comunicado **In review**, 13/11/2026 | [Registo histórico](https://github.com/ecidadao/ecidadao/blob/main/docs/plugin-submission-0.3.1.md); reconfirmar painel antes de anunciar aprovação ou publicação |
| Anthropic, diretório oficial | Publicação não confirmada | Marketplace próprio não demonstra inclusão no diretório oficial |
| Mistral, conector personalizado | Configuração documentada; teste no cliente pendente | [Guia](mistral.md); sem publicação em catálogo Mistral confirmada |

O endpoint `https://ecidadao.pt/mcp/public` respondeu a `initialize` (protocolo `2025-06-18`) e `tools/list` nesta verificação, identificando servidor 0.3.2 e seis ferramentas. Isto não substitui um teste dentro de cada cliente.

## Matriz de funcionalidades

| Funcionalidade | Plugin / MCP público | Website / experimental |
|---|---|---|
| Orientação SIGA | `siga_visit_guidance` | Percurso assistido no site |
| Orientação Finanças | `financas_service_guidance` | Percurso assistido no site |
| Rascunho e-balcão | `prepare_financas_ebalcao` | Preparação assistida |
| Rascunho A Minha Rua | `prepare_street_report` | Preparação assistida |
| Reclamação de consumo | `prepare_complaint`, `official_submission_guidance` | Preparação e encaminhamento |
| Pesquisa por necessidade | Não incluída | [Website](https://ecidadao.pt/servicos), nove percursos curados |
| Livro Amarelo: reclamação, elogio, sugestão | Não incluído | Website e `prepare_public_service_feedback` em `/mcp` experimental |
| Filas SIGA em tempo real | Não incluídas | Adaptador do website, com cobertura limitada; acesso de integração por confirmar |
| Inglês e tema automático | Funcionalidades de interface do site; não são ferramentas MCP | Disponíveis no website; rascunhos MCP continuam em português |
| Marcação, senha, submissão oficial ou acesso a contas | Não disponível | Não implementado como operação concluída pelo serviço |
| Saúde: filas e consultas | Não disponível | Em investigação; nenhuma integração SNS ativa |

As duas skills distribuídas são `siga-assistido` e `financas-assistido`. Ligar apenas o MCP noutro cliente não instala automaticamente essas skills.

## Próximas versões

1. Avaliar ferramentas públicas para pesquisa curada e Livro Amarelo, com testes, documentação e atualização do âmbito de revisão.
2. Validar Mistral com chamada real dentro do cliente e registar data, versão, resultado e limitações.
3. Só acrescentar consultas ou transações externas após confirmar contrato, cobertura e permissões. CUSP, SIGA transacional e SNS são dependências distintas.

Não foi criada uma versão nova do pacote para esta atualização documental. Ao alterar estados, conservar fonte e data; nunca converter «submetido» em «aprovado» sem confirmação.
