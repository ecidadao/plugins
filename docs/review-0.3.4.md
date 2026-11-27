# Revisão do pacote 0.3.4

Revisão de 27/11/2026, com verificações HTTP em produção registadas abaixo.
Os cenários em linguagem natural continuam a ser critérios de revisão em clientes; não foram executados dentro de Codex, Claude ou Mistral.
Os casos de revisão dos manifestos anteriores são preservados.

## Catálogo confirmado por HTTP

Dez nomes exatos, sem substituir as sete ferramentas anteriores:

1. `siga_visit_guidance`
2. `financas_service_guidance`
3. `prepare_financas_ebalcao`
4. `prepare_street_report`
5. `prepare_complaint`
6. `official_submission_guidance`
7. `sns24_service_guidance`
8. `municipal_service_search`
9. `municipal_appointment_availability`
10. `public_support_guidance`

Confirmar `initialize` e `tools/list`, usando os schemas efetivamente devolvidos pelo servidor para construir as chamadas; não inventar parâmetros de pesquisa ou disponibilidade.

## Casos positivos e limites

| Pedido | Resultado a verificar |
|---|---|
| Onde encontro serviços de habitação de Gondomar? | Pesquisa estática com fontes oficiais; não apresenta o catálogo como vagas em tempo real ou 320 operações executáveis |
| Há horários de atendimento em Ponte de Lima? | Leitura GET pública, apenas modalidades suportadas; horários disponíveis no instante da consulta, nunca reserva |
| Consulta vagas na Maia/Gondomar pelo mesmo serviço | Explica cobertura limitada a Ponte de Lima, sem fabricar vagas |
| O portal não responde ou já não tem horários | Distingue erro de leitura de ausência confirmada de disponibilidade; não reutiliza uma observação antiga como atual |
| Explain Porta 65 Young | Responde em inglês, distingue candidatura sem contrato de pagamento condicionado ao contrato, mantém fontes e datas |
| Como funciona Porta 65+? | Quebra de rendimentos superior a 20% ou família monoparental, independentemente da idade, com outros requisitos; sem copiar limites monetários históricos |
| Qual o prazo de Gondomar +Habitação? | Segunda fase com prazo publicado 30/11/2026, renda/crédito; distingue do arrendamento de habitações municipais e marca expiração após a data |
| Todos os apoios do Fundo Ambiental estão fechados? | Limita a observação à secção anual consultada; não extrapola a avisos anteriores/PRR nem afirma saldo disponível |
| Vale Eficiência II aceita novos beneficiários? | Novos beneficiários encerrados; manifestação de interesse até 25/01/2027 apenas para já elegíveis à espera de facilitador técnico, com expiração após a data |
| O prazo E-Lar de 30/11/2026 é para novas candidaturas? | Não: refere pedidos de pagamento de fornecedores; novas candidaturas encerradas |
| Posso candidatar-me à segunda fase da Mobilidade Verde? | Prazo publicado 27/07/2026 ultrapassado; encaminha acompanhamento ao eFundos, sem presumir nova fase |

Para `public_support_guidance`, usar apenas `service` e `language` (`pt`/`en`): `porta65_young`, `porta65_plus`, `gondomar_housing`, `environmental_fund`, `vale_efficiency`, `elar`, `green_mobility`.
Exemplo PT: `{"service":"elar","language":"pt"}`; exemplo EN: `{"service":"porta65_young","language":"en"}`.
Verificar `status: guidance_only`, `submitted: false`, fontes/data, fases distintas e ausência de garantia de elegibilidade, aprovação ou pagamento.
Testar serviços/idiomas desconhecidos e campos adicionais com marcadores sintéticos, sem dados pessoais reais; devem ser rejeitados sem ecoar os valores.

## Regressão e evidência

Manter os casos existentes de SIGA, Finanças, rascunhos e SNS 24: não emitir senha, entrar em contas, consultar dados clínicos ou submeter pedidos.
Um pedido de reserva municipal ou candidatura a apoio deve continuar a ser encaminhamento, nunca operação concluída.
Confirmar os totais documentados do catálogo estático: Gondomar 136, Maia 126, Ponte de Lima 58, total 320.
Registar separadamente versão/data, resposta HTTP, resultado dentro de cada cliente e falhas; um teste HTTP não valida Mistral, Codex ou Claude.
O pacote mantém as duas skills existentes; nenhuma skill nova é necessária para estas três ferramentas MCP.

## Evidência HTTP em produção — 27/11/2026, 13:47 UTC

- Deploy [46009722760](https://github.com/ecidadao/ecidadao/actions/runs/46009722760) concluído com sucesso; `/health` devolveu a revisão `96e027d39b83da1b6123277a8c487c9014ed5fa3`.
- `initialize` confirmou servidor 0.3.4 e protocolo 2025-06-18; `tools/list` devolveu exatamente os dez nomes acima.
- 31 chamadas HTTP às três ferramentas: pesquisa nos três municípios em PT/EN com totais 136/126/58; sete apoios em ambos os idiomas; áreas, datas e horários de Ponte de Lima; oito rejeições de campos extra, cobertura, serviço ou idioma inválidos.
- As três ferramentas rejeitaram um campo extra sintético sem ecoar o marcador; disponibilidade rejeitou Maia/Gondomar, pesquisa rejeitou município desconhecido e apoios rejeitaram serviço/idioma desconhecidos.
- Ponte de Lima devolveu cinco áreas; a área 7 devolveu datas e quatro horários para 02/12/2026 (09:30, 10:30, 11:30 e 15:30, Europe/Lisbon), sempre com `reserved: false` e `submitted: false`. São observações às 13:47 UTC, não disponibilidade garantida para uma consulta posterior.
- O smoke completo da aplicação passou com `--municipal --live-municipal --locales --services --sns24 --feedback --brand` e a revisão exata acima.
- Não foram introduzidos dados pessoais, feitas reservas, candidaturas ou envios de email. Os apoios mantêm `guidance_only`, `submitted: false` e verba remanescente desconhecida.

Não se induziu uma falha do portal externo para este teste de produção, nem se alterou o relógio do servidor para testar expiração futura.
Os casos de falha e fronteira temporal permanecem critérios de regressão; a verificação HTTP não comprova execução dos prompts em clientes nem aprovação de diretórios.
