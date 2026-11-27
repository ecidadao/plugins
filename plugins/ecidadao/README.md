# eCidadão

Encontre os percursos oficiais do SIGA e das Finanças e prepare rascunhos para o e-balcão, reclamações de consumo e ocorrências A Minha Rua. O serviço é independente do Estado e não submete pedidos oficiais.

Depois de instalar, peça “Ajuda-me a marcar atendimento pelo SIGA”, “Prepara uma questão para o e-balcão” ou “Como peço exames perto de mim na App SNS 24?”. As duas skills orientam os percursos SIGA/Finanças e as sete ferramentas MCP fornecem orientação ou rascunhos para revisão. A pessoa conclui qualquer pedido no portal oficial.

`sns24_service_guidance` explica consultas, exames, renovação de medicação habitual e referenciações em PT/EN, para portal/app. Não consulta contas, vagas ou dados clínicos, não faz triagem e não envia pedidos. Indique apenas `service`, `language` e `channel`, sem dados pessoais.

Não precisa de uma chave de API. As ferramentas ligam a `https://ecidadao.pt/mcp/public`; o texto necessário à preparação é enviado ao servidor e não é guardado como rascunho. Não envie credenciais ou documentos de identificação.

[Privacy / Privacidade](https://ecidadao.pt/privacidade) · [Termos](https://ecidadao.pt/termos) · [Apoio](https://ecidadao.pt/apoio)

Instalar no Claude Code:

```
/plugin install ecidadao --marketplace ecidadao/plugins
```

Instalação e código: [ecidadao/plugins](https://github.com/ecidadao/plugins). Servidor e alojamento próprio: [ecidadao/ecidadao](https://github.com/ecidadao/ecidadao). Licença Apache-2.0.
