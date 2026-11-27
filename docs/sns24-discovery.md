# SNS 24: descoberta funcional e possibilidades de integração

Verificação: 27/11/2026. Pesquisa de documentação pública do SNS 24/SPMS e lojas oficiais. Não foi iniciada sessão de utente, instalada ou testada a app, nem efetuado qualquer pedido administrativo ou clínico. Funcionalidade documentada não significa API disponível ao eCidadão.

## Descobertas com maior valor

| Necessidade | O SNS 24 permite | Oportunidade e limite para eCidadão |
|---|---|---|
| Consulta no centro de saúde | Pedir consulta/teleconsulta quando a unidade de inscrição disponibiliza agenda | Orientação por canal já é viável; vagas e confirmação exigem acesso autorizado. Não prometer marcação para amanhã pelo percurso normal |
| Exames perto de mim | Portal filtra prestadores convencionados por localização; app também mostra mapa de proximidade. O utente escolhe exames de uma requisição ativa e envia pedido | Excelente percurso inicial: explicar requisitos e passagem para o SNS 24. O prestador confirma data/hora posteriormente; o email de pedido não é confirmação |
| Renovação de medicação habitual | Pedir renovação de medicamentos ativos, com inscrição em centro de saúde, incluindo utentes sem médico de família | Guiar o pedido e explicar os estados; a unidade aprova e só depois surge a receita. Não escolher nem alterar tratamento |
| Consulta hospitalar | Consultar o estado de referenciações emitidas por profissionais | Explicar onde acompanhar e quais as opções oficiais; não confundir com agenda hospitalar de livre marcação |
| Cirurgia | Consultar posição na lista e detalhes no Portal | Encaminhamento direto para instruções oficiais. Dados pessoais integrados dependem de acesso delegado |
| Teleconsulta | Unidades SNS usam LIVE; agenda online depende da unidade e avaliação clínica | Preparar equipamento e orientar entrada. Não criar uma consulta clínica sem confirmação da unidade |
| Triagem digital | App disponibiliza questionário para adultos com sintomas respiratórios/orofaringe; pode encaminhar para consulta consoante situação, localização e vagas | Explicar o acesso e passar para o serviço oficial. Não reproduzir a triagem nem garantir consulta; outras idades/sintomas não têm essa cobertura documentada |
| Contactar centro de saúde | SARA permite retorno de chamada em unidades aderentes | Ajudar a encontrar o contacto e explicar callback. Não é uma fila pública de atendimento presencial |
| Documentos | Autodeclaração de doença, consulta de baixas e outros certificados; boletim de vacinas descarregável em PDF | Orientação imediata. Importação voluntária de um documento específico é opção futura distinta de sincronizar a conta |
| Apoiar familiares | Portal/app permitem perfis associados autorizados | Guiar associação oficial. Não usar esta funcionalidade como autorização automática para uma aplicação terceira |

Fontes por percurso: [consultas](https://www.sns24.gov.pt/pt/servico/marcacao-de-consultas/), [exames](https://www.sns24.gov.pt/pt/servico/exames-e-resultados/), [medicação](https://www.sns24.gov.pt/pt/servico/renovar-medicacao-habitual/), [referenciações](https://www.sns24.gov.pt/pt/servico/referenciacoes/), [cirurgia](https://www.sns24.gov.pt/pt/servico/lista-de-espera-para-cirurgia/), [teleconsulta](https://www.sns24.gov.pt/pt/servico/teleconsulta-unidades-sns/), [triagem digital](https://www.sns24.gov.pt/pt/servico/triagem-digital-sns-24/), [SARA](https://www.sns24.gov.pt/pt/servico/sistema-de-atendimento-e-resposta-agil-sara/), [autodeclaração](https://www.sns24.gov.pt/pt/servico/autodeclaracao-de-doenca/), [vacinas](https://www.sns24.gov.pt/pt/servico/boletim-de-vacinas/), [perfis associados](https://www.sns24.gov.pt/pt/servico/utilizadores-associados/).

### Exames: pedido não equivale a vaga reservada

A lista é limitada aos prestadores convencionados para os exames escolhidos. É necessário confirmar a morada concreta quando o prestador tem vários locais. O SNS 24 envia o pedido por email, com cópia ao utente, e o prestador combina o horário. A documentação indica que alteração/cancelamento do pedido não estão disponíveis no SNS 24; o contacto com o prestador continua necessário. O eCidadão não deve automatizar novos pedidos repetidos como se fossem cancelamentos.

### App e portal não são contratos de integração

A [app oficial](https://www.sns24.gov.pt/pt/servico/app-sns-24/) organiza os serviços em saúde, consultas/referenciações, receitas/exames e documentos, além de perfil e configurações. A autenticação usa número de utente e contactos RNU ou CMD; um PIN dá acesso posterior na app. O [portal](https://www.sns24.gov.pt/pt/servico/iniciar-sessao-no-portal-sns-24) tem também serviços pessoais. Não foi encontrado nesta pesquisa um contrato público de deep links autenticados ou OAuth de consentimento para aplicações de consumo terceiras.

Usar páginas HTTPS oficiais como destino inicial; só anunciar abertura de um ecrã específico da app após validar links suportados em Android/iOS. Ligar ao SNS 24 não transfere a sessão nem autoriza o eCidadão a ler dados. Android/iOS/Huawei e versões da app podem diferir; os percursos acima foram verificados na documentação, não num dispositivo.

## Evidência técnica: RSE WebAPI

Foi possível descarregar e ler as 87 páginas da [especificação RSE WebAPI 1.6.1](https://www.spms.min-saude.pt/wp-content/uploads/2024/10/ET-RSE-WebAPI_v1.6.1.pdf). A data interna é **10/12/2018**; o caminho de alojamento contém 2024/10, o que não torna o contrato recente.

- Secção 2, página 5: os recursos requerem autorização da aplicação. A SPMS documenta pedido de credenciais via `servicedesk@spms.min-saude.pt`, assunto `RSE - Acesso WebAPI`. Confirmar se este continua a ser o percurso atual antes de o tratar como canal de adesão vigente.
- Secções 4–5: autorização aplicacional e bearer tokens. O nome `publicCredentials` não significa acesso anónimo nem consentimento delegado genérico do cidadão.
- Secção 6: instituições e tempos médios de urgência (TEMS), incluindo leitura de `standbyTime/{IdInstitution}`. Não foram pedidos tokens ou invocados endpoints protegidos.
- Secção 7: envio/cancelamento de contactos clínicos regista episódios para o cronograma. Não é evidência de criação/cancelamento de reservas de consulta.

Conclusão: existe um percurso técnico documentado para pedir acesso; não está demonstrada elegibilidade do eCidadão, atualidade dos endpoints, cobertura de centros de saúde ou API de agendamento.

## Representação e integrações institucionais

Os [utilizadores associados](https://www.sns24.gov.pt/pt/servico/utilizadores-associados/) permitem gerir familiares/pessoas autorizadas, até nove associações, por períodos de 12 meses e com revogação. Isso é uma autorização entre pessoas no SNS 24, não um SDK de representação para o eCidadão.

O [Balcão SNS 24](https://www.sns24.gov.pt/pt/servico/balcao-sns-24/) distingue acesso facilitado e acesso mediado por colaborador através de área administrativa. Demonstra que há percursos institucionais de assistência, mas não que um assistente web privado possa aderir ao mesmo regime. É uma pergunta específica para a SPMS.

O inventário iAP contém serviços SPMS 24–29 (atestados, vacinas, incapacidade temporária, multiusos e prescrição). São pistas de contratos institucionais a analisar, não capacidades liberadas pela autenticação CMD.

## Proposta de implementação

Atualização: a primeira entrega de orientação para consultas, exames, medicação e referenciações foi implementada em 0.3.3 (`/saude` e `sns24_service_guidance`). Documentos e outros percursos continuam propostos; não há acesso delegado ao SNS.

1. **Primeira entrega, sem conta SNS:** ferramenta proposta `sns24_service_guidance` e percursos PT/EN para consultas, exames, medicação, referenciações, documentos e apoio de acesso. Devolver canal, requisitos, passos, fonte/data e significado da confirmação. Não pedir número de utente nem dados clínicos para orientar.
2. **Informação pública:** integração de tempos de urgência e diretório apenas após confirmar acesso/reutilização; apresentar qualidade, cobertura e hora da leitura. Listas pessoais, filas presenciais e agendas são capacidades separadas.
3. **Acompanhamento controlado pelo utilizador:** avaliar importação pontual de comprovativo e lembrete escolhido pela pessoa. Não inferir confirmação a partir do pedido nem criar sincronização automática de email/documentos de saúde.
4. **Piloto com acesso autorizado:** começar por um percurso não clínico, por exemplo consulta do estado de um pedido; depois agendamento com confirmação oficial, prevenção de duplicação e cancelamento documentado. Não automatizar a triagem clínica.

Critérios de aceitação da primeira entrega: links oficiais verificados; casos PT/EN; distinção portal/app; ausência de promessa de vagas; pedidos separados de confirmações; nenhum segredo ou identificador pedido; explicação de alternativas quando a unidade não disponibiliza o serviço. Publicar ferramenta nova exige atualizar testes, manifesto/documentação e âmbito de revisão dos plugins.

## Perguntas concretas a esclarecer com SPMS

- Qual a versão suportada da API TEMS/RSE e o processo de registo para consumidor privado só de leitura? Licença, quotas, cache, timestamps e cobertura?
- Existe API autorizada para diretório de prestadores convencionados por exame/local, sem dados do utente?
- Há mecanismo de acesso delegado por cidadão, com scopes, revogação e auditoria, para disponibilidade, pedidos, estado e comprovativos?
- Qual a diferença contratual entre reserva confirmada e pedido remetido à unidade/prestador? Como tratar alteração, cancelamento e repetição?
- Existem dados públicos de filas/atendimento em cuidados primários ou integração SARA para parceiros?
- Há deep links oficiais, SDK, sandbox e contas sintéticas para testes de portal/app?
- O modelo de assistência mediada dos Balcões admite parceiros digitais privados? Que condições se aplicam?

Nenhuma destas questões foi enviada nesta investigação. O formulário de apoio ao SNS 24 destina-se à utilização dos seus canais; não deve ser assumido como processo de adesão técnica.
