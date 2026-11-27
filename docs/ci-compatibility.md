# CI de pacotes e compatibilidade

Verificado localmente em 27/11/2026. Os checks em GitHub registam o resultado de cada execução; nenhum implica aprovação de diretórios ou execução de um modelo.

## Matriz de evidência

| Check | O que executa | O que não comprova |
|---|---|---|
| PR/tag: validate | Schemas locais, contrato OpenAI explícito, adaptadores Claude estritos, ZIP reproduzível e sete testes negativos/de consistência | Aprovação de qualquer diretório |
| PR/tag: codex-install | Codex CLI 0.172.0 real: marketplace local e instalação; verifica cache, manifesto, duas skills e endpoint num CODEX_HOME temporário | Login, execução de modelo, ligação MCP dentro do cliente ou instalação no perfil do utilizador |
| PR/tag: vibe-loader | Mistral Vibe 3.1.5 real, PluginResolver: duas skills e um servidor Streamable HTTP no artefacto adaptado; confirma rejeição do ficheiro MCP original | Sessão interativa, /reload-plugins, descoberta MCP pelo cliente ou execução de modelo |
| Semanal/manual: published-package | Descarrega ZIP da última release pública, verifica digest GitHub, caminhos, links, duplicados, tamanho, versões e bytes contra a tag | Que a release foi instalada pelo utilizador |
| Semanal/manual: public-endpoint | initialize e tools/list por HTTP; compara versão da release e os dez nomes exatos | Chamadas a todas as ferramentas ou disponibilidade municipal externa |

A instalação Codex e o carregador Vibe passaram localmente sem chave API e sem chamada de modelo.
O checker externo confirmou a release 0.3.4, ZIP original com dez ficheiros e o endpoint 0.3.4 com dez ferramentas.
Os checks completos do contrato MCP e das fontes externas pertencem ao [repositório da aplicação](https://github.com/ecidadao/ecidadao); não são duplicados aqui.

## Vibe: incompatibilidade confirmada e artefacto separado

A [documentação Vibe](https://docs.mistral.ai/vibe/code/cli/plugins) descreve Agent Plugins 1.0, plugin.json, mcp.json e diretórios de plugins.
O parser instalado de `mistral-vibe==3.1.5` rejeita `mcpServers.ecidadao.extensions` com `extra_forbidden`.
O pacote original 0.3.4 mantém `extensions.com.openai.auth.type=none`; não foi alterado nem substituído na release.

O job Vibe gera `ecidadao-plugin-0.3.4-vibe.zip` como **artefacto CI separado**, não como asset da release já publicada.
Só `mcp.json` difere: remove essa extensão e conserva schema, servidor, transporte e URL.
Manifesto, skills e restantes ficheiros são partilhados byte a byte, sem nova skill ou configuração OpenAI removida do pacote principal.
O ZIP Vibe passa o schema estrito e o carregador real reconhece o plugin, a versão, as duas skills e o servidor.
O ficheiro `mcp.json` original é testado como caso negativo; não se declara compatibilidade Vibe integral do ZIP original.

Para experimentar conscientemente o artefacto adaptado, obtenha-o do job Vibe, confira a versão e coloque o conteúdo num diretório de plugin Vibe isolado.
A documentação oficial indica `$VIBE_HOME/plugins/<plugin>/` e `/reload-plugins`; esses passos interativos não foram executados por este CI.
O workflow de release continua a publicar apenas o pacote principal; nenhuma tag nova é criada por esta alteração.

## Executar localmente

Use um ambiente Python 3.12 separado e instale dependências verificadas por hash:

```sh
python3.12 -m venv /tmp/ecidadao-ci
/tmp/ecidadao-ci/bin/pip install --require-hashes -r scripts/requirements-ci.txt
/tmp/ecidadao-ci/bin/python scripts/package.py --check --build
/tmp/ecidadao-ci/bin/python scripts/package.py --check --build --variant vibe
/tmp/ecidadao-ci/bin/python -m unittest discover -s tests -v
claude plugin validate plugins/ecidadao --strict
claude plugin validate . --strict
/tmp/ecidadao-ci/bin/python scripts/check_codex.py
```

O último comando requer Codex CLI 0.172.0 no PATH; CI instala `@openai/codex@0.172.0`.
O script altera CODEX_HOME apenas no ambiente do subprocesso, nunca HOME, e remove a cache temporária ao terminar.
Para Vibe, use outro ambiente Python 3.12 com `scripts/requirements-vibe.txt` e execute `scripts/check_vibe.py`.
O lock Vibe destina-se ao runner Linux x86_64; a versão do loader é fixa e as dependências transitivas têm hashes.
Os dois locks podem ser regenerados com os comandos uv registados no seu cabeçalho; alterações exigem revisão e nova validação.

Checks externos separados:

```sh
/tmp/ecidadao-ci/bin/python scripts/check_published.py release --output /tmp/release-check.json
/tmp/ecidadao-ci/bin/python scripts/check_published.py endpoint --version 0.3.4
```

O workflow `Published package and endpoint` executa às segundas-feiras, 07:19 UTC, ou via workflow_dispatch.
Passa a versão realmente publicada ao segundo job e conserva evidência JSON como artefactos.
Uma falha GitHub/download é reportada no job de pacote; uma falha HTTP, catálogo ou versão é reportada no job de endpoint.
Não há reserva, candidatura, credenciais ou acesso a portais privados.
Uma implantação antecipada da próxima versão pode causar divergência temporária package/server: o check falha até existir publicação consistente, sem alterar estados automaticamente.

## Limites da validação

Os sete testes incluem ZIP adulterado/incompleto, path traversal, caminhos absolutos/Windows, duplicados, symlinks, tamanho excessivo, adaptador divergente e schema/autenticação inesperados.
O leitor não extrai ZIPs antes da validação; compara os bytes com a fonte esperada.
Os limites de tamanho reduzem o risco de arquivos excessivos; isto não é uma auditoria universal de malware.
Dependências e formatos podem evoluir; a pinagem identifica o que foi testado, não promete compatibilidade com versões futuras.
OpenAI 0.3.1 continua no último estado conhecido de revisão; publicação Anthropic é desconhecida; Le Chat/Mistral Work e sessões com modelo continuam não testados.

