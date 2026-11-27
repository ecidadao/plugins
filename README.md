# eCidadão — plugins

Plugins abertos para Codex e Claude Code, sob licença Apache-2.0. Partilham duas skills e o servidor MCP público do [eCidadão](https://ecidadao.pt).

O serviço é independente do Estado. Ajuda a encontrar os portais oficiais e a preparar rascunhos; não acede a contas, não emite senhas nem submete pedidos.

## Estado de publicação e funcionalidades

Verificado em 27/11/2026. Consulte [os estados por plataforma e a matriz de funcionalidades](docs/publication-status.md).

| Canal | Estado |
|---|---|
| GitHub / Codex / Claude Code | Pacote aberto [v0.3.2 publicado](https://github.com/ecidadao/plugins/releases/tag/v0.3.2), instalável pelos comandos abaixo |
| Diretório OpenAI | Último estado comunicado: **In review**, versão 0.3.1, em 13/11/2026; estado atual não reconfirmado |
| Diretório oficial Anthropic | Aprovação/publicação não confirmadas; instalação pelo marketplace deste repositório disponível |
| Mistral | [Configuração MCP documentada](docs/mistral.md); validação dentro do cliente pendente |

Os plugins públicos expõem seis ferramentas. A pesquisa de serviços do website, o Livro Amarelo experimental e as consultas de filas do site não estão incluídos nesse catálogo público. Publicação no GitHub não equivale a aprovação num diretório oficial.

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

Ferramentas: `siga_visit_guidance`, `financas_service_guidance`, `prepare_financas_ebalcao`, `prepare_street_report`, `prepare_complaint` e `official_submission_guidance`.

Exemplos: “Ajuda-me a marcar atendimento pelo SIGA” e “Prepara uma questão sobre IMI para o e-balcão”. Não inclua credenciais ou documentos de identificação.

## Desenvolvimento

`plugins/ecidadao/plugin.json` e `mcp.json` são a fonte dos metadados e da ligação MCP. As skills são partilhadas. Depois de editar, gere e valide os adaptadores Claude:

```sh
python3 scripts/package.py --sync
python3 scripts/package.py --check
claude plugin validate plugins/ecidadao
claude plugin validate .
python3 scripts/package.py --build
```

O ZIP é criado em `dist/`, com os ficheiros do plugin na raiz. A CI verifica os adaptadores e publica o ZIP como artefacto; tags `v*` criam uma GitHub Release. A versão da tag deve coincidir com o manifesto.

A distribuição por GitHub não significa aprovação nos directórios da OpenAI ou da Anthropic. O pacote 0.3.1 submetido anteriormente continua separado desta versão.

## Contribuir

Abra uma issue para discutir um problema ou envie um pull request. Veja [CONTRIBUTING.md](CONTRIBUTING.md). O código do servidor está em [ecidadao/ecidadao](https://github.com/ecidadao/ecidadao).
