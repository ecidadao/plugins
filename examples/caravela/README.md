# Exemplo de ponte Caravela → eCidadão

Preparado em 27/11/2026. Não é um conector instalado nem um teste E2E Caravela.

- `sns24-request.json`: pedido ilustrativo para Chat Completions, com o schema SNS 24 obtido do MCP público em produção. O nome tem prefixo `ecidadao__` e a escolha da função é forçada para este teste.
- `sns24-mcp-result.json`: resposta real do MCP público a `service=exams`, `language=pt`, `channel=app`. Sem dados pessoais, credenciais ou chamada à Caravela.

Um adaptador deve receber o `tool_call` real da Caravela, validar o nome/argumentos, mapear `ecidadao__sns24_service_guidance` para `sns24_service_guidance` e chamar `https://ecidadao.pt/mcp/public`. Depois devolve o resultado como texto JSON numa mensagem `role: tool`, com o `tool_call_id` recebido, conservando a mensagem anterior do assistente. Não inventar esse identificador nem tratar o ficheiro de exemplo como uma resposta atual a qualquer pedido.

A execução paga não foi realizada. O próximo teste exige uma conta/token Caravela e deve verificar o comportamento das ferramentas internas, além da função externa. Ver [análise e plano](../../docs/caravela-integration.md).
