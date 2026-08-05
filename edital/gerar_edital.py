# -*- coding: utf-8 -*-
"""Reescreve o corpo do edital preservando estilos, cabecalhos e rodapes do original."""
import re, shutil, subprocess, os

SRC = 'orig/word/document.xml'
raw = open(SRC, encoding='utf-8').read()

head = raw[:raw.index('<w:body>') + len('<w:body>')]
sect = raw[raw.index('<w:sectPr'):]           # sectPr + fechamento

def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def runs(text):
    """**negrito** vira run com <w:b/>."""
    out = []
    for i, part in enumerate(re.split(r'\*\*', text)):
        if not part:
            continue
        b = '<w:rPr><w:b/></w:rPr>' if i % 2 else ''
        out.append('<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>' % (b, esc(part)))
    return ''.join(out)

B = []
def h(level, text):
    B.append('<w:p><w:pPr><w:pStyle w:val="Ttulo%d"/></w:pPr>%s</w:p>' % (level, runs(text)))

def p(text, after=80):
    B.append('<w:p><w:pPr><w:spacing w:after="%d"/></w:pPr>%s</w:p>' % (after, runs(text)))

def item(num, text, after=80):
    B.append('<w:p><w:pPr><w:spacing w:after="%d"/></w:pPr>'
             '<w:r><w:rPr><w:b/></w:rPr><w:t xml:space="preserve">%s</w:t></w:r>'
             '<w:r><w:t xml:space="preserve"> </w:t></w:r>%s</w:p>' % (after, esc(num), runs(text)))

def lista(num_id, itens):
    for k, it in enumerate(itens):
        after = 160 if k == len(itens) - 1 else 0
        B.append('<w:p><w:pPr><w:numPr><w:ilvl w:val="0"/><w:numId w:val="%d"/></w:numPr>'
                 '<w:spacing w:after="%d"/></w:pPr>%s</w:p>' % (num_id, after, runs(it)))

def espaco():
    B.append('<w:p><w:pPr><w:spacing w:after="0"/></w:pPr></w:p>')

def assinatura(text, bold=False, after=0, center=True):
    jc = '<w:jc w:val="center"/>' if center else ''
    B.append('<w:p><w:pPr><w:spacing w:after="%d"/>%s</w:pPr>%s</w:p>'
             % (after, jc, runs(('**%s**' % text) if bold else text)))

def tabela(widths, header, rows, aligns=None):
    aligns = aligns or ['left'] * len(widths)
    total = sum(widths)
    x = ['<w:tbl><w:tblPr><w:tblStyle w:val="Tabelanormal"/><w:tblW w:w="%d" w:type="dxa"/>' % total,
         '<w:tblBorders>']
    for side in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        x.append('<w:%s w:val="single" w:sz="4" w:space="0" w:color="BFBFBF"/>' % side)
    x.append('</w:tblBorders><w:tblCellMar><w:top w:w="60" w:type="dxa"/><w:left w:w="108" w:type="dxa"/>'
             '<w:bottom w:w="60" w:type="dxa"/><w:right w:w="108" w:type="dxa"/></w:tblCellMar></w:tblPr>')
    x.append('<w:tblGrid>' + ''.join('<w:gridCol w:w="%d"/>' % w for w in widths) + '</w:tblGrid>')

    def cel(w, texto, cabecalho, align):
        shd = '<w:shd w:val="clear" w:color="auto" w:fill="00352F"/>' if cabecalho else ''
        jc = '<w:jc w:val="center"/>' if align == 'center' else ''
        if cabecalho:
            r = '<w:r><w:rPr><w:b/><w:color w:val="FFFFFF"/></w:rPr><w:t xml:space="preserve">%s</w:t></w:r>' % esc(texto)
        else:
            r = runs(texto)
        return ('<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/>%s<w:vAlign w:val="center"/></w:tcPr>'
                '<w:p><w:pPr><w:spacing w:before="60" w:after="60" w:line="240" w:lineRule="auto"/>%s'
                '%s</w:pPr>%s</w:p></w:tc>'
                % (w, shd, jc, '<w:rPr><w:b/></w:rPr>' if cabecalho else '', r))

    x.append('<w:tr><w:trPr><w:cantSplit/><w:tblHeader/></w:trPr>'
             + ''.join(cel(widths[i], header[i], True, aligns[i]) for i in range(len(widths))) + '</w:tr>')
    for row in rows:
        x.append('<w:tr><w:trPr><w:cantSplit/></w:trPr>'
                 + ''.join(cel(widths[i], row[i], False, aligns[i]) for i in range(len(widths))) + '</w:tr>')
    x.append('</w:tbl>')
    B.append(''.join(x))
    espaco()


# ============================================================
# CORPO DO EDITAL
# ============================================================

h(1, 'Edital 01/2026, Processo Seletivo 2026')

p('A **NeuroDynamics (NRO)** é uma equipe de estudantes da Escola de Engenharia da Universidade '
  'Federal de Minas Gerais (UFMG) que desenvolve tecnologia em engenharia biomédica, com base no '
  'LABBIO, o Laboratório de Bioengenharia da universidade. Por meio deste Edital, a equipe abre o '
  '**Processo Seletivo 2026** e torna públicas as regras, os requisitos, as fases e as datas para a '
  'entrada de novos membros.')

h(2, '1. Sobre este edital')
item('1.1.', 'O Processo Seletivo é público e aberto a estudantes regularmente matriculados na UFMG '
     'ou em instituições parceiras, conforme o art. 31, alínea “a”, do Estatuto da NeuroDynamics '
     '(NRO-DIR-001).')
item('1.2.', 'A condução do processo cabe ao **Comitê de Seleção**, formado por membros do '
     'Departamento de Pessoal e pelos gestores das áreas com vagas abertas. É ele quem organiza as '
     'fases, avalia os candidatos e publica os resultados, seguindo as diretrizes da Diretoria e do '
     'Conselho Consultivo.')
item('1.3.', 'Tudo o que for oficial sai em **selecao.neurodynamics.dev** e no e-mail que você '
     'informar na inscrição. Informação passada por qualquer outro canal não vale.')
item('1.4.', 'Acompanhar as publicações e cumprir os prazos é responsabilidade sua.')
item('1.5.', 'Ao se inscrever, você declara que leu e aceita as regras deste Edital.')
item('1.6.', 'Participar da NeuroDynamics não gera vínculo de emprego, salário, bolsa ou qualquer '
     'pagamento, nos termos do art. 33, §2º, do Estatuto. É atividade de formação, pesquisa, '
     'desenvolvimento e inovação.')
item('1.7.', 'Se em algum ponto o site e este Edital divergirem, vale o que está escrito aqui.')

h(2, '2. A NeuroDynamics')
item('2.1.', 'Desenvolvemos projetos de engenharia de ponta a ponta: da concepção e da simulação à '
     'fabricação, à eletrônica e ao software, passando por testes e documentação.')
item('2.2.', 'Trabalhamos lado a lado com a pesquisa acadêmica do LABBIO, transformando conhecimento '
     'científico em protótipos e resultados concretos. Nossas soluções são voltadas à saúde, com foco '
     'em reabilitação neurológica e cuidado crítico, passando por neuromodulação, interfaces '
     'cérebro-máquina, estimulação elétrica funcional, próteses, órteses, dispositivos vestíveis e '
     'tecnologias assistivas.')
item('2.3.', 'Somos uma organização gerida pelos próprios estudantes, com processos claros de gestão, '
     'avaliação e desenvolvimento de cada membro. Nossa documentação segue as normas ISO 13485, '
     'ISO 14971 e IEC 62304 e a RDC ANVISA nº 751/2022, e o trabalho é organizado em ciclos com '
     'metodologias ágeis.')
item('2.4.', 'Cada membro pertence a uma área, participa de projetos interdisciplinares e tem um '
     'gestor imediato que acompanha seu desenvolvimento. O ritmo é o de um ambiente profissional: '
     'reuniões gerais, entregas combinadas, avaliações periódicas e espaço para crescer, errar e '
     'aprender. A dedicação é compatível com a graduação, e a rotina é combinada com cada equipe.')
item('2.5.', 'Nossa sede fica no Laboratório de Bioengenharia (LABBIO), Escola de Engenharia da UFMG, '
     'Av. Antônio Carlos, 6.627, Pampulha, Belo Horizonte, MG, CEP 31.270-901.')

h(2, '3. As vagas')
item('3.1.', 'As vagas deste processo estão distribuídas nas seguintes áreas:')
tabela(
    [2100, 6948, 1300],
    ['Área', 'O que você vai fazer', 'Vagas'],
    [
        ['Mecânica', 'Projeto mecânico, modelagem 3D, manufatura aditiva, prototipagem e montagem '
                     'dos dispositivos', '[__]'],
        ['Eletrônica', 'Circuitos, instrumentação biomédica, aquisição de sinais, firmware e sistemas '
                       'embarcados', '[__]'],
        ['Software', 'Aplicações e interfaces, processamento de sinais, análise de dados e integração '
                     'com os dispositivos', '[__]'],
        ['Simulação', 'Modelagem computacional, análise por elementos finitos, simulação de sistemas '
                      'biológicos e validação virtual', '[__]'],
        ['Gestão e Operações', 'Planejamento e acompanhamento de projetos, processos, documentação, '
                               'qualidade, parcerias e captação de recursos', '[__]'],
        ['Comunicação e Marketing', 'Identidade visual, produção de conteúdo, redes sociais, '
                                    'audiovisual e divulgação científica', '[__]'],
    ],
    aligns=['left', 'left', 'center'])
item('3.2.', 'Na inscrição você escolhe **até três áreas de interesse**. Elas orientam a avaliação e a '
     'formação dos grupos, mas não são uma promessa de alocação: a área definitiva é combinada ao '
     'longo do período trainee.')
item('3.3.', 'Quem for aprovado e não for chamado por falta de vaga fica em cadastro de reserva até o '
     'fim do semestre letivo 2027/1, e pode ser chamado a qualquer momento nesse período.')
item('3.4.', 'A NeuroDynamics pode não preencher todas as vagas, caso não haja candidatos com o perfil '
     'necessário.')

h(2, '4. Quem pode participar')
item('4.1.', 'Pode se inscrever quem:', after=80)
lista(4, [
    'estiver com **matrícula ativa** em curso de graduação ou pós-graduação da UFMG ou de instituição '
    'parceira, e mantiver esse vínculo durante todo o processo;',
    'tiver interesse em tecnologia aplicada à saúde e vontade de aprender na prática;',
    'tiver **tempo para participar de verdade**. A rotina da equipe pede cerca de 10 horas por semana, '
    'entre projetos, reuniões e compromissos combinados com o time;',
    'gostar de trabalhar em grupo, com pessoas de cursos e áreas diferentes;',
    'levar a sério prazos, combinados e as regras de confidencialidade da equipe;',
    'se identificar com o nosso jeito de trabalhar: capricho, responsabilidade, organização e vontade '
    'de gerar impacto real.',
])
item('4.2.', 'Esses requisitos vêm do art. 33 do Estatuto.')
item('4.3.', 'Não exigimos curso específico, período mínimo, nota mínima nem experiência prévia. O que '
     'avaliamos é potencial, comprometimento e aderência à equipe.')
item('4.4.', 'Alguma área pode pedir requisitos extras, nos termos do art. 33, §1º, do Estatuto. Se '
     'isso acontecer, eles serão divulgados junto com a convocação da fase correspondente.')

h(2, '5. Como se inscrever')
item('5.1.', 'A inscrição é **gratuita** e só pode ser feita pelo formulário em '
     '**selecao.neurodynamics.dev**, dentro do prazo do cronograma da seção 7.')
item('5.2.', 'Não é preciso criar conta nem senha. O formulário leva cerca de dez minutos e tem cinco '
     'passos:', after=80)
lista(5, [
    '**Sobre você:** dados pessoais e de contato;',
    '**Vida acadêmica:** instituição, curso, período e o que você já fez, como iniciação científica, '
    'equipes de competição, projetos pessoais, trabalho e links de portfólio;',
    '**Motivação:** até três áreas de interesse, o motivo de querer entrar na equipe e sua '
    'disponibilidade semanal;',
    '**Termos:** aceite do edital e do tratamento de dados, além da autorização de uso de imagem, que '
    'é opcional;',
    '**Revisão:** conferir tudo antes de enviar.',
])
item('5.3.', 'Ao enviar, você recebe um **protocolo**. Guarde esse número: é com ele e com o e-mail '
     'cadastrado que você acompanha sua situação, agenda a dinâmica e a entrevista e consulta os '
     'resultados, na área **Acompanhar** do site.')
item('5.4.', 'Depois de enviada, a inscrição não pode ser editada pelo site. Se precisar corrigir '
     'algo, procure a equipe pelos canais oficiais indicados no site.')
item('5.5.', 'Não aceitamos inscrição feita por outro meio, fora do prazo ou com o formulário '
     'incompleto.')
item('5.6.', 'Se você precisar de algum apoio para participar das fases, escreva no campo de '
     'acessibilidade do formulário. O pedido é tratado com discrição e faremos o que estiver ao nosso '
     'alcance.')
item('5.7.', 'Informação falsa ou documento inválido elimina o candidato a qualquer momento, sem '
     'prejuízo de outras medidas cabíveis.')
item('5.8.', 'Seus dados são usados apenas para conduzir este Processo Seletivo, conforme a Lei '
     'nº 13.709/2018 (LGPD). Os dados de quem não for efetivado são apagados ao fim do prazo do item '
     '3.3. Os dados de quem entrar na equipe passam a integrar o registro institucional.')

h(2, '6. As fases do processo')
item('6.1.', 'Depois da inscrição, o processo tem **três fases**: dinâmica em grupo, entrevista '
     'individual e período trainee. Antes delas, o Comitê de Seleção analisa as inscrições recebidas.')

h(3, '6.2. Análise das inscrições')
item('6.2.1.', 'O Comitê de Seleção confere se a inscrição está completa e se você atende aos '
     'requisitos da seção 4, e lê com atenção a motivação e o histórico que você apresentou.')
item('6.2.2.', 'O resultado é o **deferimento** ou o **indeferimento** da inscrição, publicado na data '
     'do cronograma. Quem tiver a inscrição deferida segue para a Fase 1.')

h(3, '6.3. Fase 1: dinâmica em grupo')
item('6.3.1.', 'É uma atividade em grupo com um desafio prático, realizada presencialmente na Escola '
     'de Engenharia da UFMG.')
item('6.3.2.', 'Assim que a inscrição for deferida, **você mesmo agenda o horário** da sua dinâmica na '
     'área Acompanhar do site. As vagas por horário são limitadas e valem por ordem de escolha.')
item('6.3.3.', 'O que a gente olha:', after=80)
lista(1, [
    'como você escuta e considera as ideias dos outros;',
    'como colabora e ajuda o grupo a avançar;',
    'como organiza o raciocínio diante de um problema novo;',
    'a clareza ao explicar o que está pensando.',
])
item('6.3.4.', 'Não é preciso conhecimento técnico prévio. O desafio é pensado para que qualquer '
     'estudante consiga participar.')
item('6.3.5.', 'Fase **eliminatória e classificatória**, avaliada de 0 a 100 pontos. Quem ficar abaixo '
     'de 60 pontos não segue para a fase seguinte.')
item('6.3.6.', 'Quem não aparecer no horário agendado, sem avisar com pelo menos 24 horas de '
     'antecedência, está eliminado.')

h(3, '6.4. Fase 2: entrevista individual')
item('6.4.1.', 'É uma conversa de cerca de 30 minutos com o Comitê de Seleção, com pelo menos dois '
     'avaliadores, sendo um deles da área que você escolheu.')
item('6.4.2.', 'Pode ser presencial, na Escola de Engenharia da UFMG, ou remota. O horário também é '
     'agendado por você na área Acompanhar do site.')
item('6.4.3.', 'Falamos sobre sua trajetória, seus interesses, sua disponibilidade e o que você espera '
     'da equipe. É também a hora de tirar suas dúvidas sobre a NeuroDynamics.')
item('6.4.4.', 'O que a gente olha:', after=80)
lista(1, [
    'aderência ao jeito de trabalhar e aos valores da equipe;',
    'clareza na comunicação;',
    'comprometimento, maturidade e disponibilidade real;',
    'potencial de desenvolvimento e de contribuição aos projetos.',
])
item('6.4.5.', 'Fase **eliminatória e classificatória**, avaliada de 0 a 100 pontos, com mínimo de 60 '
     'pontos.')
item('6.4.6.', 'Faltar à entrevista sem avisar com pelo menos 24 horas de antecedência elimina o '
     'candidato.')

h(3, '6.5. Fase 3: período trainee')
item('6.5.1.', 'Quem passa na entrevista **entra na equipe como trainee** e vive a última fase por '
     'dentro, trabalhando junto com os membros.')
item('6.5.2.', 'O período trainee é um **desafio em grupos interdisciplinares**. Cada grupo reúne '
     'trainees de áreas diferentes e recebe um desafio ligado aos projetos e às linhas de trabalho da '
     'NeuroDynamics.')
item('6.5.3.', 'Cada grupo se reporta aos **supervisores de projetos**, que acompanham o trabalho do '
     'começo ao fim, dão retorno periódico e ajudam a destravar o que for preciso.')
item('6.5.4.', 'O grupo é responsável por três coisas:', after=80)
lista(6, [
    '**Planejar:** definir o escopo, dividir as tarefas, montar o cronograma e prever os riscos;',
    '**Executar:** desenvolver a solução, testar, documentar e corrigir o rumo com base nos '
    'resultados;',
    '**Levar parte do que foi desenvolvido para o mundo real:** entregar algo que saia da bancada e '
    'seja usado, demonstrado ou validado fora do grupo, com usuários, parceiros, laboratórios, '
    'profissionais de saúde ou a comunidade.',
])
item('6.5.5.', 'O desafio é divulgado na data prevista no cronograma, junto com a composição dos '
     'grupos, o material de apoio e os critérios de avaliação.')
item('6.5.6.', 'Logo no início da fase acontece a **reunião geral de integração**, em que os trainees '
     'conhecem a equipe, os projetos em andamento e a rotina de trabalho.')
item('6.5.7.', 'Ao longo do período há **duas avaliações parciais**, nas datas do cronograma. Em cada '
     'uma, o grupo mostra o andamento aos supervisores de projetos e recebe retorno sobre o que está '
     'bom e o que precisa mudar. Cada trainee também recebe um retorno individual.')
item('6.5.8.', 'A fase termina com a **apresentação final**, aberta à equipe, em que cada grupo mostra '
     'o que planejou, o que executou e o que foi de fato levado para fora.')
item('6.5.9.', 'A nota da Fase 3 é a média ponderada da primeira avaliação parcial (peso 2), da '
     'segunda avaliação parcial (peso 3) e da apresentação final (peso 5). Contam tanto o resultado do '
     'grupo quanto a contribuição individual de cada trainee.')
item('6.5.10.', 'Além da nota, são considerados a presença nas atividades combinadas, o cumprimento '
     'dos prazos e a postura no dia a dia da equipe.')
item('6.5.11.', 'Fase **eliminatória e classificatória**. Quem ficar abaixo de 60 pontos não é '
     'efetivado.')

h(3, '6.6. Resultado final')
item('6.6.1.', 'A nota final é a média ponderada das três fases: dinâmica em grupo (peso 2), '
     'entrevista individual (peso 3) e período trainee (peso 5).')
item('6.6.2.', 'Em caso de empate, valem, nesta ordem:', after=80)
lista(7, [
    'maior nota na Fase 3;',
    'maior nota na Fase 2;',
    'maior nota na Fase 1;',
    'maior disponibilidade semanal declarada na inscrição.',
])

h(2, '7. Cronograma')
item('7.1.', 'O Processo Seletivo segue o calendário abaixo:')
tabela(
    [7048, 3300],
    ['Etapa', 'Data'],
    [
        ['Divulgação do edital', '17/07/2026'],
        ['Inscrições', '03/08/2026 a 23/08/2026'],
        ['Divulgação das inscrições deferidas', '24/08/2026'],
        ['Realização das dinâmicas em grupo', '26/08/2026 a 29/08/2026'],
        ['Divulgação do resultado da primeira fase', '31/08/2026'],
        ['Realização das entrevistas individuais', '01/09/2026 a 05/09/2026'],
        ['Divulgação do resultado da segunda fase', '08/09/2026'],
        ['Início do período trainee', '09/09/2026'],
        ['Divulgação do desafio trainee', '14/09/2026'],
        ['Reunião geral e integração com os novos trainees', '19/09/2026'],
        ['Primeira avaliação parcial', '01/10/2026 a 03/10/2026'],
        ['Segunda avaliação parcial', '14/11/2026'],
        ['Apresentação final', '28/11/2026'],
        ['Divulgação do resultado final', '30/11/2026'],
    ],
    aligns=['left', 'center'])
item('7.2.', 'O agendamento da dinâmica abre junto com a divulgação das inscrições deferidas, e o da '
     'entrevista, junto com o resultado da primeira fase. Os horários disponíveis aparecem na área '
     'Acompanhar do site.')
item('7.3.', 'As datas podem mudar. Se isso acontecer, publicamos a retificação no site e avisamos por '
     'e-mail todos os inscritos.')

h(2, '8. Resultados e pedidos de revisão')
item('8.1.', 'Os resultados de cada fase saem na página **Edital e resultados** do site, com a lista '
     'dos candidatos identificados pelo número de protocolo.')
item('8.2.', 'Você também pode consultar sua situação individual na área **Acompanhar**, informando '
     'protocolo e e-mail.')
item('8.3.', 'Quem discordar de um resultado pode pedir revisão ao Comitê de Seleção em até **dois '
     'dias úteis** após a publicação, pelo formulário indicado no site.')
item('8.4.', 'O pedido precisa dizer de forma objetiva o que está sendo questionado e por quê. Pedidos '
     'genéricos, fora do prazo ou enviados por outro meio não são analisados.')
item('8.5.', 'O Comitê de Seleção analisa o pedido, ouve quem avaliou a fase e responde individualmente '
     'ao candidato. A decisão é final dentro deste Processo Seletivo.')

h(2, '9. Efetivação')
item('9.1.', 'Quem concluir o período trainee com aproveitamento é **efetivado** como membro da '
     'NeuroDynamics, com registro institucional próprio, nos termos do art. 32 do Estatuto.')
item('9.2.', 'Para a efetivação é preciso assinar o termo de compromisso e de confidencialidade da '
     'equipe.')
item('9.3.', 'A partir daí, o novo membro passa a integrar uma área e um ou mais projetos, com um '
     'gestor imediato acompanhando seu desenvolvimento.')
item('9.4.', 'Como membro, você tem direito a participar dos projetos e das atividades da equipe, '
     'pedir o aproveitamento acadêmico do que fizer aqui, receber orientação e retorno sobre o seu '
     'desenvolvimento e ter sua contribuição reconhecida nos resultados, entre outros direitos '
     'previstos no art. 34 do Estatuto.')

h(2, '10. Quando alguém é eliminado')
item('10.1.', 'Está fora do processo, a qualquer momento, quem:', after=80)
lista(8, [
    'deixar de atender a algum requisito da seção 4;',
    'prestar informação falsa ou apresentar documento inválido;',
    'faltar a uma fase para a qual foi convocado ou perder os prazos combinados;',
    'ficar abaixo da nota mínima em qualquer fase;',
    'tiver conduta desrespeitosa, discriminatória ou incompatível com os princípios éticos da '
    'NeuroDynamics em qualquer etapa;',
    'copiar trabalho de outra pessoa, fraudar uma entrega ou tentar obter vantagem indevida em '
    'qualquer avaliação;',
    'perder o vínculo com a instituição de ensino durante o processo.',
])

h(2, '11. Disposições finais')
item('11.1.', 'A NeuroDynamics se compromete com tratamento igual e sem discriminação em todas as '
     'fases deste Processo Seletivo.')
item('11.2.', 'Passar nas fases não garante efetivação automática: ela depende das vagas disponíveis e '
     'da sua avaliação ao longo do período trainee.')
item('11.3.', 'Participar da equipe não substitui nem justifica atrasos nas obrigações acadêmicas do '
     'estudante junto à sua instituição de origem.')
item('11.4.', 'Este Edital vale a partir da data de sua publicação e vigora até o fim do prazo previsto '
     'no item 3.3.')
item('11.5.', 'Dúvidas sobre o Processo Seletivo devem ser enviadas ao Comitê de Seleção pelos canais '
     'indicados no site.')
item('11.6.', 'O que não estiver previsto aqui será resolvido pelo Comitê de Seleção, ouvida a '
     'Diretoria e, quando for o caso, o Conselho Consultivo, nos termos do art. 14, alínea “c”, do '
     'Estatuto.', after=240)

assinatura('Belo Horizonte, 17 de julho de 2026.', after=480)
assinatura('Comitê de Seleção', bold=True, after=0)
assinatura('NeuroDynamics, Escola de Engenharia da UFMG', after=480)
assinatura('Diretoria', bold=True, after=0)
assinatura('NeuroDynamics, Escola de Engenharia da UFMG', after=0)

novo = head + ''.join(B) + sect

# ---------- checagens ----------
proibidos = {'—': 'travessao (em dash)', '–': 'en dash', '·': 'ponto medio',
             '•': 'bullet char', '─': 'box dash'}
for ch, nome in proibidos.items():
    if ch in ''.join(B):
        raise SystemExit('ERRO: encontrado %s no corpo' % nome)

os.makedirs('novo', exist_ok=True)
if os.path.exists('novo'):
    shutil.rmtree('novo')
shutil.copytree('orig', 'novo')
open('novo/word/document.xml', 'w', encoding='utf-8').write(novo)

# titulo nas propriedades
core = open('novo/docProps/core.xml', encoding='utf-8').read()
core = re.sub(r'<dc:title>.*?</dc:title>',
              '<dc:title>Edital 01/2026, Processo Seletivo 2026</dc:title>', core)
open('novo/docProps/core.xml', 'w', encoding='utf-8').write(core)

out = os.path.abspath('NROPES019_EDITAL_012026_REV_A.docx')
if os.path.exists(out):
    os.remove(out)
subprocess.run(['zip', '-Xrq', out, '.'], cwd='novo', check=True)
print('ok:', out, os.path.getsize(out), 'bytes')
