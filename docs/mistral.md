# eCidadão no Mistral

Estado em 27/11/2026: endpoint MCP verificado por HTTP; loader nativo Vibe 3.1.5 verificado com artefacto adaptado; execução com modelo e dentro de Le Chat/Work ainda não verificadas. Não há conector eCidadão publicado no catálogo Mistral confirmado.

## Conector personalizado no Le Chat / Work

Na documentação atual do Mistral, a configuração está descrita em Work:

1. Como administrador da conta/organização, abrir Connectors e Add Connector.
2. Selecionar Custom MCP Connector.
3. Nome: `ecidadao`. URL: `https://ecidadao.pt/mcp/public`.
4. Ligar; o endpoint não exige autenticação. Confirmar as dez ferramentas do servidor 0.3.4 da [matriz](publication-status.md), verificadas por HTTP em 27/11/2026.
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

Para utilização programática, o Studio permite registar servidores MCP como conectores; o registo e os testes requerem acesso à conta/API Mistral. Não é necessária uma reimplementação das ferramentas só para mudar de cliente.

Fontes oficiais: [configurar conectores MCP](https://docs.mistral.ai/vibe/work/web/connectors/mcp-connectors), [quickstart de conectores Studio](https://docs.mistral.ai/studio/connectors/quickstart). Consultadas em 27/11/2026.

## Catálogo 0.3.4

Após reconexão/atualização do catálogo, verificar também `municipal_service_search`, `municipal_appointment_availability` e `public_support_guidance`: dez ferramentas no total, mantendo as sete existentes.
Testar pesquisa de serviços de Gondomar (catálogo estático de 320 entradas nos três municípios), leitura de horários apenas em Ponte de Lima e orientação Porta 65 Jovem em inglês.
A leitura de horários usa GET do frontend público; não é reserva nem cobre Maia/Gondomar.
Os sete apoios são snapshots PT/EN, não candidaturas ou pesquisa de verba disponível.
Usar os [cenários de revisão](review-0.3.4.md); registar resultados dentro do cliente separadamente da verificação HTTP.
A verificação HTTP não altera o estado pendente de validação Mistral.

## Vibe CLI: loader verificado, artefacto adaptado

O teste real do `PluginResolver` em Mistral Vibe 3.1.5 carrega as duas skills e o servidor MCP do ZIP adaptado, em diretórios temporários e sem API key.
O mcp.json original do pacote 0.3.4 é rejeitado pelo parser por conter a extensão OpenAI no servidor.
Essa extensão é preservada no pacote principal; o job Vibe gera um artefacto separado apenas com a projeção MCP padrão, validada por schema.
Não foi substituído o ZIP da release 0.3.4, nem testada uma sessão de modelo ou /reload-plugins.
Veja a [matriz, reprodução e limites do CI](ci-compatibility.md) e a [documentação oficial de plugins Vibe](https://docs.mistral.ai/vibe/code/cli/plugins).
