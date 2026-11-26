---
name: siga-assistido
description: Ajuda a encontrar os percursos oficiais para consultar filas, obter uma senha ou marcar atendimento no SIGA em Portugal.
---

# SIGA assistido

Use este percurso quando a pessoa pedir senhas, filas ou marcações no SIGA.

1. Identifique o assunto, entidade e tipo de senha. Use `siga_visit_guidance` para apresentar o percurso oficial quando a pessoa ainda não souber qual ação quer realizar.
2. Para consultar filas ou obter uma senha, encaminhe para a página oficial devolvida por `siga_visit_guidance`. A pessoa escolhe distrito, entidade e tipo de senha no SIGA e confirma a disponibilidade atual nesse portal. Este plugin não consulta nem compara tempos de espera em tempo real.
3. Para marcar atendimento, encaminhe para o URL oficial devolvido pela ferramenta. Se um navegador estiver disponível e a pessoa pedir acompanhamento, pode navegar no portal com ela. A pessoa introduz o seu email, autentica-se, confirma códigos e resolve verificações de segurança no portal oficial.
4. Só diga que há uma senha ou marcação depois de a pessoa apresentar um comprovativo oficial. Não peça passwords, códigos de autenticação ou documentos de identificação na conversa.

O eCidadão é independente do SIGA. As páginas oficiais podem mudar ou ficar indisponíveis.
