# Site do Processo Seletivo — selecao.neurodynamics.dev

Site público do PS da NeuroDynamics: divulgação, cronograma, edital e
resultados, inscrição sem login e agendamento das dinâmicas/entrevistas.
Arquivo único (`index.html`), no mesmo padrão dos demais apps do SOMA.

## Pré-requisitos

Aplicar as migrações **`soma_v6.sql`** e **`soma_v7.sql`** (na raiz deste
repositório) no SQL Editor do Supabase. Sem elas o site continua no ar com
o conteúdo de reserva (cronograma fixo), mas inscrição/acompanhamento
ficam indisponíveis.

A dinâmica em grupo (`dinamica*.html`) pede também a **`soma_v12.sql`**,
que está no repositório `nro-pessoal` junto das demais migrações do SOMA.

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

## FAQ e competências (editados pelo SOMA)

Depois da migração **`soma_v11.sql`** (repositório `nro-pessoal`), duas
coisas saem do código e passam a ser editadas em **SOMA → Seleção**:

- **As perguntas frequentes** da página inicial, na aba **FAQ**: pergunta,
  resposta, ordem, publicar/ocultar e o escopo (uma edição específica ou
  todas). A resposta aceita `*negrito*`, `[texto](https://link)` e linha
  em branco para separar parágrafos — HTML digitado ali aparece como
  texto, não é interpretado.
- **O catálogo de competências** que o formulário de inscrição exibe
  (tabela `ps_competencias`). Na inscrição, o candidato marca uma vez o
  que já sabe fazer e duas vezes o que quer desenvolver; as duas listas
  vão para a ficha dele, e o comitê ajusta durante as fases.

Enquanto a migração não roda, o site usa as listas `FAQ_RESERVA` e
`COMPETENCIAS_RESERVA`, no topo do `<script>` — vale manter as duas mais
ou menos em sincronia com o que estiver no banco.

## Cartazes (`cartazes.html`)

Gerador de cartazes impressos do PS, por unidade acadêmica da UFMG. É um
arquivo único e independente do resto: abra direto no navegador (dois
cliques no arquivo já servem), escolha as unidades e mande imprimir. Nada
sai do navegador — sem servidor, sem upload, sem biblioteca externa.

- **Frente:** a peça de rua. A mensagem grande vem da **linha de
  conhecimento** da unidade — as mesmas cinco frentes de "De onde você
  vem" do site, na lógica das mensagens que a gente manda separadas por
  área nos grupos. O que muda de unidade para unidade é o rótulo do topo,
  o gancho e a lista de cursos. Leva QR da inscrição, prazo e uma faixa
  de **tiras destacáveis** com o endereço.
- **Verso:** o briefing de quem vai afixar — onde fica a unidade (campus,
  endereço e prédio), pontos recomendados em ordem de prioridade, regras
  de afixação, o que levar, o que fazer depois, respostas curtas para
  quem parar você no corredor e campos para anotar à mão quem afixou,
  quando e onde.
- **A3 e A4**, retrato. É o mesmo desenho: o A3 é a folha A4 multiplicada
  por √2, então nada precisa ser reajustado.
- Três fundos: **Cortex** (verde, padrão), **Void** (escuro) e **Claro**
  (fundo branco, para impressora comum — gasta bem menos toner).

### O que editar

Tudo que muda por edição do PS (datas, endereço, contato) está no painel
da esquerda e fica guardado no navegador para a próxima vez. O conteúdo
fica em três blocos no topo do `<script>`:

- **`LINHAS`** — a mensagem de cada linha de conhecimento: título, texto
  de apoio, os quatro tópicos e a cor de acento.
- **`UNIDADES`** — uma versão de cartaz por unidade: a linha que ela usa,
  o local (campus, endereço, prédio), o gancho, os cursos e os pontos de
  afixação. Vale conferir prédio e mural antes de imprimir uma tiragem
  grande: mural muda de lugar.
- **`AFIXACAO`** — o que vale para qualquer unidade: regras, o que levar,
  o que fazer depois e as perguntas frequentes do verso.

### Como imprimir

Botão **Imprimir / salvar PDF**. Na caixa de impressão: papel no tamanho
escolhido, escala **100 %** (sem "ajustar à página"), margens "nenhuma" e
**gráficos de fundo** ligados. As páginas saem na ordem frente, verso,
frente, verso — para duplex, vire pela **borda maior**. Impressora que
não imprime até a borda: ligue a opção de **margem branca de 5 mm**.

O QR é gerado no próprio arquivo (sem CDN), então funciona offline e sai
vetorial na impressão — cerca de 0,8 mm por módulo no A4 e 1,1 mm no A3,
folgado para qualquer câmera de celular. A tipografia vem do Google
Fonts: sem internet o cartaz continua saindo, com a fonte do sistema no
lugar da Archivo.

O **imagotipo oficial** vai embutido no arquivo (token `--imagotipo`, no
`:root`), então aparece na frente e no verso de toda versão mesmo offline.
Ele entra como máscara CSS: como o original é uma silhueta com canal
alfa, a marca assume a cor do texto — branca sobre os fundos escuros,
preta sobre o claro — sem precisar de dois arquivos nem de filtro. Para
trocar por uma marca nova, substitua o `data:` desse token; a proporção
fica em `--imagotipo-razao`.

Quem se inscreve marca **Cartazes** em "Como soube do processo?" — é por
ali que dá para medir o retorno da campanha.

## Redes sociais (`redes.html`)

Gerador das publicações do PS: a imagem no tamanho exato de cada rede,
mais a legenda, o texto do LinkedIn e a mensagem para os grupos. Também é
arquivo único e roda inteiro no navegador — a imagem que você sobe não
sai da sua máquina.

### Mensagem para grupo de WhatsApp

É o primeiro roteiro da lista e funciona diferente dos outros: sai **uma
imagem só**, quadrada, que se explica sozinha — e o texto pronto para
colar logo abaixo dela.

Dois seletores comandam imagem e texto ao mesmo tempo:

- **A área do grupo** (seis: geral, engenharia e exatas, saúde,
  comunicação e artes, gestão e direito, humanas) troca o gancho da
  imagem, a cor de acento e a abertura da mensagem.
- **O momento da campanha** (abertura, durante, reta final) troca o selo
  do canto, o prazo em destaque e o fecho da mensagem. Na reta final o
  selo conta os dias sozinho, a partir do prazo.

São 18 combinações prontas. Mande a imagem primeiro e o texto embaixo,
uma área por vez e espaçadas ao longo do dia: várias mensagens iguais de
uma vez, do mesmo número, são tratadas como spam. O quadrado é o formato
que aparece inteiro na bolha da conversa — no 1080 × 1350 o WhatsApp
corta a prévia.

### Os outros roteiros

- **Seis roteiros de feed**, cada um uma publicação inteira: *Inscrições
  abertas*, *As perguntas do direct*, *Não é só engenharia*, *O processo
  inteiro*, *Reta final* e *O que já saiu daqui*. O conteúdo vem do que o
  site já responde — FAQ, cronograma, as cinco frentes e as reportagens
  —, na ideia de publicar o que a pessoa ia perguntar, não o que a gente
  gosta de dizer.
- **Quatro formatos**, gerados em pixel exato: carrossel 1080 × 1350,
  quadrado 1080 × 1080, story 1080 × 1920 e LinkedIn 1200 × 627. A
  resolução **Alta** multiplica por 4/3 (1440 e 1600 de largura), que é
  o teto que o Instagram e o LinkedIn aproveitam.
- **Os textos**, prontos para copiar: legenda do Instagram, texto do
  LinkedIn, o primeiro comentário com o link, a mensagem de WhatsApp em
  seis versões (uma por linha de conhecimento) e o texto alternativo da
  imagem.
- **Um plano de publicação** com o que publicar em cada momento da
  campanha e as práticas que fazem a peça circular.

O número de dias da *Reta final* é calculado a partir do prazo — não
precisa editar nada quando a data mudar.

### Foto

A capa e o encerramento aceitam foto. **Foto da equipe rende mais que
foto de banco**: bancada, teste, competição, gente trabalhando. Sem foto,
a peça sai com a linguagem da marca, que também funciona.

Para banco de imagens, o campo aceita o **endereço da imagem** do
Unsplash (na foto aberta, botão direito → *copiar endereço da imagem*, o
que começa com `images.unsplash.com`) — o endereço da página não serve,
e o gerador avisa se for esse o caso. Os botões de busca abrem o Unsplash
já com termos que costumam devolver imagem com a cara da marca. Preencha
o crédito do fotógrafo: ele sai discreto no canto da peça.

### O que editar

Campanha e perfil ficam no painel e são guardados no navegador. O
conteúdo está em três blocos no topo do primeiro `<script>`:

- **`ROTEIROS`** — as lâminas de cada publicação e os textos que a
  acompanham. Nos textos, `{prazo}`, `{abertura}`, `{site}`, `{dias}` e
  `{edicao}` são trocados na hora de gerar. O roteiro `grupos` monta a
  lâmina por função, a partir da área e do momento escolhidos.
- **`GRUPOS`** — as áreas: o gancho e a cor da imagem, mais a abertura e
  o miolo da mensagem de cada uma.
- **`MOMENTOS`** — abertura, durante e reta final: o selo da imagem, o
  prazo em destaque e o fecho da mensagem.
- **`PLANO`** — o cronograma da campanha e as práticas de publicação.

Nenhum texto fala em taxa de inscrição: processo seletivo de equipe não
cobra, e dizer que não cobra levanta uma dúvida que ninguém tinha. O que
vale mencionar é a inscrição **sem cadastro**, que essa sim é incomum.

Publique a imagem no tamanho gerado: Instagram e LinkedIn recomprimem o
que sobe, e mandar já no tamanho certo evita a segunda compressão, que é
a que borra o texto. Nada de tirar print da prévia.

## Dinâmica em grupo (`dinamica*.html`)

A primeira fase presencial tem três páginas e um roteiro. O roteiro é o
documento **NRO-PES-020 ROTEIRO DA DINÂMICA EM GRUPO** (pasta
`documentos/`), escrito para ser lido em cinco minutos por quem vai
avaliar. As três páginas são estas:

| Arquivo | Quem usa | Quando abre |
|---|---|---|
| `dinamica.html` | um celular por grupo de candidatos | durante a janela |
| `dinamica-painel.html` | o avaliador que opera o projetor | durante a janela |
| `dinamica-avaliador.html` | cada avaliador, no próprio celular | durante a janela, com login do SOMA |

Todas dependem da migração **`soma_v12.sql`** (repositório `nro-pessoal`).
Sem ela as páginas ficam no ar mas não têm de onde ler o conteúdo.

### O código da janela

Cada janela de dinâmica (um slot de `ps_slots` com `fase = 'dinamica'`,
criado na aba **Agenda** do SOMA) ganha automaticamente um código de
quatro caracteres. O alfabeto não usa `O`, `0`, `I`, `1`, `S` nem `5`,
porque o código é lido de longe, num projetor, por gente com pressa.

É o mesmo código nos três lugares: o candidato digita, o painel projeta e
gera o QR (`dinamica.html#CODIGO`), e a mesa do avaliador identifica a
janela. Janela criada antes da migração recebe o código pelo botão
**Gerar código**, em Seleção → Dinâmica → Janelas.

### A janela de tempo

As três páginas só respondem entre `hora_inicio` menos a tolerância de
entrada e `hora_fim` mais a tolerância de saída (30 minutos para cada
lado, no padrão, ajustáveis em Seleção → Dinâmica → Roteiro). Fora desse
intervalo as funções devolvem `fechada` e mais nada: sem lista de
candidato, sem registro de grupo, sem roteiro, **nem para quem tem
login**. A trava mora no banco, nas funções `security definer`, não no
JavaScript da página.

Quem precisa ler o roteiro antes lê o NRO-PES-020 ou abre a aba Dinâmica
do SOMA, que é onde se prepara. A mesa do avaliador é a página do dia,
não a de preparação.

### O registro do candidato

`dinamica.html` foi feita para celular numa sala com quinze pessoas no
mesmo Wi-Fi e vinte e cinco minutos no relógio. As decisões que importam:

- **Rascunho local.** Cada tecla vai para o `localStorage` do aparelho.
  Fechar a aba, travar o navegador ou receber uma ligação no meio não
  perde nada.
- **Gravar é um botão.** Nada sobe sozinho: a barra de baixo diz sempre
  em que estado a coisa está (nada gravado, alterações não gravadas,
  gravado às tal hora, versão tal, por quem).
- **Conflito não apaga ninguém.** Se duas pessoas do mesmo grupo gravam,
  a segunda recebe as duas versões lado a lado e escolhe: manter a dela,
  usar a do servidor ou juntar. A versão do registro sobe a cada
  gravação, e é ela que detecta o conflito.
- **Offline não trava.** Sem internet o botão avisa e o texto fica
  guardado. A página também confere, ao voltar do bloqueio de tela, se
  alguém do grupo gravou nesse meio-tempo.

### O painel projetado

Dez telas, na ordem em que se usa: abertura com o código, a equipe, a
mesa de avaliadores, a agenda dos 75 minutos, as regras da sala, o
desafio, o QR do registro, o cronômetro do trabalho em grupo, o grupo da
vez com o texto dele ao vivo e o fechamento.

Passa com as setas do teclado; `T` liga o cronômetro, `R` zera, `+` e `−`
ajustam um minuto, `G` troca o grupo em exibição, `F` põe em tela cheia e
`?` mostra a lista inteira. O QR é gerado no próprio arquivo, sem CDN, e
tudo escala por `vmin`, então o mesmo desenho serve o projetor 4:3 da
sala e o telão 16:9 do auditório. O cronômetro roda no relógio da
máquina: se a internet cair no meio do bloco, ele não para.

### A mesa do avaliador

Quatro abas na ordem do que acontece na sala: **Roteiro** (o bloco da vez
já aberto, com o que falar e o que cortar se atrasar), **Sala** (presença,
formação dos grupos e os pedidos de acessibilidade da inscrição em
destaque), **Registros** (o que cada grupo está escrevendo, atualizado
sozinho) e **Avaliar** (nota de 1 a 5 por critério, com as âncoras à
vista, parecer e recomendação).

A avaliação cai na mesma tabela `ps_avaliacoes` que o SOMA já usa, com
`fase = 'dinamica'`, então a nota aparece na ficha do candidato sem
nenhuma ponte manual. A página imprime: com o Wi-Fi fora do ar, o roteiro
e a ficha de avaliação saem em papel pelo próprio navegador.

### O que se edita, e onde

Tudo em **SOMA → Seleção → Dinâmica**, sem tocar em código:

- **Painel** — título, subtítulo, resumo da equipe, aviso de imagem,
  Wi-Fi da sala, os cartões de apresentação e as regras.
- **Roteiro** — duração da janela, tamanho do grupo, as duas tolerâncias
  de horário e os blocos (nome, minutos, o que o avaliador faz, o que vai
  no projetor e o que cortar se atrasar). O SOMA soma os minutos e avisa
  quando o roteiro não cabe na janela.
- **Desafio** — o briefing, os casos e os campos do registro.
- **Critérios** — os cinco critérios com as âncoras de nota 1, 3 e 5. O
  SOMA avisa se algum não bater com os critérios da aba Avaliação.
- **Janelas** — o código, os atalhos para as três páginas e a mesa de
  avaliadores de cada janela (quem aparece na tela "Quem avalia").

## Como publicar

Publicados junto com o site, os geradores ficam em
`selecao.neurodynamics.dev/cartazes.html` e
`selecao.neurodynamics.dev/redes.html`. As três páginas da dinâmica
seguem o mesmo caminho e também vão com `noindex`. Nenhum dos dois tem nada
sensível, mas os dois são material interno: já vão com `noindex`, e se a
preferência for não deixá-los no ar, basta não subir os arquivos — eles
funcionam igual abertos do disco.

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
(`ps_site`, `ps_inscrever`, `ps_acompanhar`, `ps_horarios`, `ps_agendar`)
e, na dinâmica, `ps_din_sala`, `ps_din_registro` e `ps_din_gravar`. As
três da dinâmica conferem o horário da janela antes de devolver qualquer
coisa, e nenhuma delas expõe nome de candidato: o candidato entra com o
código da sala, escolhe a letra do grupo e escreve.

A mesa do avaliador (`ps_din_janelas`, `ps_din_mesa`, `ps_din_presenca`,
`ps_din_grupos_salvar`, `ps_din_avaliar`) exige sessão autenticada com
papel de comitê (`eh_comite()`) **e** a janela aberta. As duas condições
são verificadas no banco a cada chamada.
Nenhuma tabela do módulo tem política de leitura/escrita para `anon`;
o candidato se identifica por **protocolo + e-mail**, sem senha.
O controle do processo é feito pelo Comitê de Seleção na página
**Seleção** do SOMA · Gestão (papel `selecao` no banco).
