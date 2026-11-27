# eCidadão no Mistral

Estado em 27/11/2026: endpoint MCP verificado por HTTP; instalação e execução dentro do Mistral ainda não verificadas. Não há conector eCidadão publicado no catálogo Mistral confirmado.

## Conector personalizado no Le Chat / Work

Na documentação atual do Mistral, a configuração está descrita em Work:

1. Como administrador da conta/organização, abrir Connectors e Add Connector.
2. Selecionar Custom MCP Connector.
3. Nome: `ecidadao`. URL: `https://ecidadao.pt/mcp/public`.
4. Ligar; o endpoint não exige autenticação. Confirmar que aparecem as sete ferramentas da [matriz](publication-status.md).
5. Testar «Onde começo para marcar atendimento pelo SIGA?» e «Prepara uma questão sobre IMI para o e-balcão».

Verificar que são usadas as ferramentas apropriadas e que o resultado distingue orientação/rascunho de uma operação oficial concluída. Confirmar também que um pedido para entrar nas Finanças ou emitir senha não é apresentado como executado.

Esta ligação fornece ferramentas MCP. Os manifestos e skills Codex/Claude deste repositório não são automaticamente importados. Uma distribuição nativa para outros produtos Mistral, incluindo clientes CLI, necessita de validação própria.

## Verificação técnica reproduzível

```sh
curl --fail-with-body https://ecidadao.pt/mcp/public \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  --data '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"ecidadao-check","version":"1"}}}'
```

O servidor requer o cabeçalho Accept indicado; um pedido curl sem ele recebeu HTTP 406 na verificação. Com o cabeçalho, `initialize` e `tools/list` responderam corretamente. Este resultado comprova o endpoint, não o comportamento do cliente Mistral.

Para utilização programática, o Studio permite registar servidores MCP como conectores; o registo e os testes requerem acesso à conta/API Mistral. Não é necessária uma reimplementação das sete ferramentas só para mudar de cliente.

Fontes oficiais: [configurar conectores MCP](https://docs.mistral.ai/vibe/work/web/connectors/mcp-connectors), [quickstart de conectores Studio](https://docs.mistral.ai/studio/connectors/quickstart). Consultadas em 27/11/2026.
