# eCidadão — plugins

Plugins abertos para Codex e Claude Code, sob licença Apache-2.0. Partilham duas skills e o servidor MCP público do [eCidadão](https://ecidadao.pt).

O serviço é independente do Estado. Ajuda a encontrar os portais oficiais e a preparar rascunhos; não acede a contas, não emite senhas nem submete pedidos.

## Estado de publicação e funcionalidades

Verificado em 27/11/2026. Consulte [os estados por plataforma e a matriz de funcionalidades](docs/publication-status.md).

| Canal | Estado |
|---|---|
| GitHub / Codex / Claude Code | Pacote aberto [v0.3.4 publicado](https://github.com/ecidadao/plugins/releases/tag/v0.3.4), instalável pelos comandos abaixo |
| Diretório OpenAI | Último estado comunicado: **In review**, versão 0.3.1, em 13/11/2026; estado atual não reconfirmado |
| Diretório oficial Anthropic | Aprovação/publicação não confirmadas; instalação pelo marketplace deste repositório disponível |
| Mistral | [Loader Vibe validado com artefacto adaptado](docs/ci-compatibility.md); Le Chat/Work e execução com modelo pendentes |

O endpoint público 0.3.4 expõe dez ferramentas, verificado em 27/11/2026. O pacote 0.3.4 está publicado no GitHub; os estados de distribuição confirmados constam da tabela acima. A pesquisa de serviços do website e o Livro Amarelo experimental e as consultas de filas do site não estão incluídos nesse catálogo público. Publicação no GitHub não equivale a aprovação num diretório oficial.

## Instalar no Codex

Numa versão do Codex CLI com suporte para plugins:

```sh
codex plugin marketplace add ecidadao/plugins
codex plugin add ecidadao@ecidadao
```

Abra uma nova sessão depois da instalação. Se já tiver o eCidadão instalado de outra origem, escolha uma das instalações para evitar ferramentas duplicadas.

## Instalar no Claude Code

```sh
claude plugin marketplace add ecidadao/plugins
claude plugin install ecidadao@ecidadao
```

Abra uma nova sessão. As skills são `/ecidadao:siga-assistido` e `/ecidadao:financas-assistido`.

## Usar apenas o MCP

Endpoint HTTP: `https://ecidadao.pt/mcp/public`, sem autenticação. Esta opção é alternativa à instalação do plugin.

```sh
codex mcp add ecidadao --url https://ecidadao.pt/mcp/public
claude mcp add --transport http ecidadao https://ecidadao.pt/mcp/public
```

Para outro cliente MCP, configure uma ligação Streamable HTTP com o mesmo URL. Para alojamento próprio, consulte [o código e as instruções do servidor](https://github.com/ecidadao/ecidadao).

Ferramentas existentes, preservadas em 0.3.4: `siga_visit_guidance`, `financas_service_guidance`, `prepare_financas_ebalcao`, `prepare_street_report`, `prepare_complaint`, `official_submission_guidance` e `sns24_service_guidance`.

Exemplos: “Ajuda-me a marcar atendimento pelo SIGA” e “Prepara uma questão sobre IMI para o e-balcão”. Não inclua credenciais ou documentos de identificação.

## SNS 24

Desde 0.3.3, `sns24_service_guidance` explica os percursos de consultas, exames, medicação habitual e referenciações em português ou inglês. Escolha `service` (`appointments`, `exams`, `medication`, `referrals`), `language` (`pt`, `en`) e `channel` (`portal`, `app`, `both`). Não acede a contas ou vagas, não faz triagem nem envia pedidos. [Percursos no site](https://ecidadao.pt/saude).

A ligação MCP descobre a ferramenta no servidor; clientes que guardem o catálogo podem precisar de reconexão. Atualize o pacote para obter os novos metadados e exemplos.

## Municípios e apoios — versão 0.3.4

As sete ferramentas existentes são preservadas. O catálogo público acrescenta:

| Ferramenta | Cobertura e limites |
|---|---|
| `municipal_service_search` | Pesquisa em 320 entradas estáticas: Gondomar 136, Maia 126 e Ponte de Lima 58; encaminhamento oficial, sem executar o serviço |
| `municipal_appointment_availability` | Apenas Ponte de Lima; leitura em tempo real por GET do frontend público, disponibilidade no instante da consulta, sem reserva |
| `public_support_guidance` | Sete percursos de habitação/ambiente em PT/EN, com fontes e datas; sem candidatura ou avaliação pessoal de elegibilidade |

Exemplos: “Onde encontro os serviços municipais de Gondomar?”, “Há horários de atendimento disponíveis em Ponte de Lima?” e “Explain Porta 65 Young”.
Os serviços de apoio são `porta65_young`, `porta65_plus`, `gondomar_housing`, `environmental_fund`, `vale_efficiency`, `elar` e `green_mobility`.
A orientação distingue nova candidatura, ação de beneficiário existente e pedido de pagamento de fornecedor; prazos ultrapassados não implicam prorrogação e o saldo disponível não é conhecido.
Não envie dados pessoais. Consulte [o estado de publicação e a evidência HTTP](docs/publication-status.md) e [os cenários de revisão](docs/review-0.3.4.md).

## Desenvolvimento

Integrações em avaliação: [Caravela — análise, parceria e exemplo de ponte API/MCP](docs/caravela-integration.md). Ainda sem conector Caravela instalado ou teste E2E no fornecedor.

`plugins/ecidadao/plugin.json` e `mcp.json` são a fonte dos metadados e da ligação MCP. As skills são partilhadas. Depois de editar, gere e valide os adaptadores Claude:

```sh
python3 -m pip install --require-hashes -r scripts/requirements-ci.txt
python3 scripts/package.py --sync
python3 scripts/package.py --check
claude plugin validate plugins/ecidadao
claude plugin validate .
python3 scripts/package.py --build
```

A [matriz de CI](docs/ci-compatibility.md) distingue instalação Codex isolada, carregador Vibe real, checks estáticos e verificações externas semanais/manuais. O artefacto Vibe é separado e não substitui o ZIP 0.3.4 publicado.

O ZIP é criado em `dist/`, com os ficheiros do plugin na raiz. A CI verifica os adaptadores e publica o ZIP como artefacto; tags `v*` criam uma GitHub Release. A versão da tag deve coincidir com o manifesto.

A distribuição por GitHub não significa aprovação nos directórios da OpenAI ou da Anthropic. O pacote 0.3.1 submetido anteriormente continua separado desta versão.

## Contribuir

Abra uma issue para discutir um problema ou envie um pull request. Veja [CONTRIBUTING.md](CONTRIBUTING.md). O código do servidor está em [ecidadao/ecidadao](https://github.com/ecidadao/ecidadao).
