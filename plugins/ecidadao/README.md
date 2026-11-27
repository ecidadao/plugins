# eCidadão

Encontre os percursos oficiais do SIGA e das Finanças e prepare rascunhos para o e-balcão, reclamações de consumo e ocorrências A Minha Rua. O serviço é independente do Estado e não submete pedidos oficiais.

Depois de instalar, peça “Ajuda-me a marcar atendimento pelo SIGA”, “Prepara uma questão para o e-balcão” ou “Como peço exames perto de mim na App SNS 24?”. As duas skills orientam os percursos SIGA/Finanças e as sete ferramentas MCP da versão publicada 0.3.3 fornecem orientação ou rascunhos para revisão. A pessoa conclui qualquer pedido no portal oficial.

`sns24_service_guidance` explica consultas, exames, renovação de medicação habitual e referenciações em PT/EN, para portal/app. Não consulta contas, vagas ou dados clínicos, não faz triagem e não envia pedidos. Indique apenas `service`, `language` e `channel`, sem dados pessoais.

Não precisa de uma chave de API. As ferramentas ligam a `https://ecidadao.pt/mcp/public`; o texto necessário à preparação é enviado ao servidor e não é guardado como rascunho. Não envie credenciais ou documentos de identificação.

[Privacy / Privacidade](https://ecidadao.pt/privacidade) · [Termos](https://ecidadao.pt/termos) · [Apoio](https://ecidadao.pt/apoio)

Instalar no Claude Code:

```
/plugin install ecidadao --marketplace ecidadao/plugins
```

Instalação e código: [ecidadao/plugins](https://github.com/ecidadao/plugins). Servidor e alojamento próprio: [ecidadao/ecidadao](https://github.com/ecidadao/ecidadao). Licença Apache-2.0.

## Preparação da versão 0.3.4 — rollout pendente

Este pacote prepara dez ferramentas MCP, preservando as sete anteriores e acrescentando:

- `municipal_service_search`: 320 entradas estáticas de Gondomar (136), Maia (126) e Ponte de Lima (58), com encaminhamento para fontes oficiais.
- `municipal_appointment_availability`: consulta em tempo real apenas em Ponte de Lima, por GET do frontend público; não reserva nem confirma atendimento.
- `public_support_guidance`: orientação datada em PT/EN para `porta65_young`, `porta65_plus`, `gondomar_housing`, `environmental_fund`, `vale_efficiency`, `elar` e `green_mobility`; aceita apenas `service` e `language`, sem dados pessoais ou candidatura.

Depois de confirmado o rollout, experimente “Onde encontro os serviços municipais de Gondomar?”, “Há horários de atendimento disponíveis em Ponte de Lima?” ou “Explain Porta 65 Young”.
Os apoios são snapshots, não pesquisa de verbas em tempo real: não há garantia de elegibilidade, aprovação ou pagamento, nem extensão presumida dos prazos.
A consulta de vagas mostra o estado no instante da leitura; confirme sempre no portal oficial.
A disponibilidade destas três ferramentas depende do rollout do servidor e da atualização do catálogo do cliente.
[Estado de publicação](https://github.com/ecidadao/plugins/blob/main/docs/publication-status.md); preparar este pacote não significa publicação em GitHub ou aprovação em diretórios oficiais.
