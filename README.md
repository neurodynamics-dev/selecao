# Site do Processo Seletivo — selecao.neurodynamics.dev

Site público do PS da NeuroDynamics: divulgação, cronograma, edital e
resultados, inscrição sem login e agendamento das dinâmicas/entrevistas.
Arquivo único (`index.html`), no mesmo padrão dos demais apps do SOMA.

## Pré-requisitos

Aplicar as migrações **`soma_v6.sql`** e **`soma_v7.sql`** (na raiz deste
repositório) no SQL Editor do Supabase. Sem elas o site continua no ar com
o conteúdo de reserva (cronograma fixo), mas inscrição/acompanhamento
ficam indisponíveis.

## A página "A NeuroDynamics"

Tudo dela sai do bloco `SOBRE`, no topo do `<script>` de `index.html`:
os textos, as fotos e as duas listas da seção de imprensa.

- **`videos`** é o carrossel de reportagens. Cada item leva só o **id do
  YouTube** — o que vem depois de `watch?v=` ou de `youtu.be/`, jogando
  fora tudo a partir do `&`. O `titulo` é opcional: sem ele, quem rotula
  o clipe é o `veiculo`, com o `ano` na linha de baixo. O `url`, também
  opcional, vira o botão "Matéria".

  ```js
  { titulo:'', veiculo:'TV UFMG', ano:'2025', youtube:'dQw4w9WgXcQ', url:'' }
  ```

  Vídeo com visibilidade **"não listado" embute normalmente; "privado"
  não** — e a permissão de incorporação precisa estar ligada no canal de
  quem subiu. O clipe que não carrega é pulado em silêncio, então vale
  conferir se todos aparecem.

  O carrossel toca mudo (única forma de autoplay que os navegadores
  aceitam), passa sozinho para o próximo quando o vídeo acaba, pausa
  fora da tela e não toca sozinho para quem pede
  `prefers-reduced-motion`. Monta um único player para a lista inteira.

- **`nota_videos`** é a linha logo abaixo do carrossel. Deixe `''` para
  não exibir nenhuma.

- **`materias`** são as reportagens escritas, em cartões menores sob o
  rótulo *Também escreveram sobre*: `{ titulo, veiculo, ano, url }`.

Lista vazia não aparece; vazias as duas, a seção de imprensa some por
inteiro. Os mesmos vídeos e matérias estão no site institucional, no
repositório `neurodynamics-dev/website` — ao acrescentar um, vale
atualizar os dois.

O endereço do site institucional fica na constante
`SITE_INSTITUCIONAL`, usada nos direcionamentos espalhados pelo site
(início, esta página, FAQ, menu e rodapé).

## Como publicar

O GitHub Pages atende **um domínio por repositório** — e este repositório
já usa `pessoal.neurodynamics.dev`. Duas opções:

1. **Repositório próprio (recomendado):** crie `neurodynamics-dev/nro-selecao`,
   copie `index.html` e `CNAME` desta pasta para a raiz, ative o Pages
   (branch `main`) e crie o CNAME `selecao` → `neurodynamics-dev.github.io`
   no Cloudflare.
2. **Cloudflare Pages:** aponte um projeto para este repositório com
   "build output directory" = `selecao/` e o domínio customizado
   `selecao.neurodynamics.dev`.

## Segurança

O site usa apenas a chave `anon` do Supabase e conversa com o banco
exclusivamente pelas funções `security definer` da migração
(`ps_site`, `ps_inscrever`, `ps_acompanhar`, `ps_horarios`, `ps_agendar`).
Nenhuma tabela do módulo tem política de leitura/escrita para `anon`;
o candidato se identifica por **protocolo + e-mail**, sem senha.
O controle do processo é feito pelo Comitê de Seleção na página
**Seleção** do SOMA · Gestão (papel `selecao` no banco).
