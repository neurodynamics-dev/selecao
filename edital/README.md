# Edital do Processo Seletivo

`NROPES019_EDITAL_012026_REV_A.docx` é o edital do Processo Seletivo 2026,
alinhado ao que o site (`../index.html`) prevê: três fases (dinâmica em
grupo, entrevista individual e período trainee), cronograma de 17/07/2026 a
30/11/2026, áreas de interesse do formulário de inscrição e condução pelo
**Comitê de Seleção**.

## Como o arquivo é gerado

`gerar_edital.py` reescreve apenas o `word/document.xml`, reaproveitando
estilos, numeração, cabeçalho, rodapé e fontes do arquivo original. Assim o
layout e a identidade visual do documento continuam iguais aos dos demais
documentos do sistema documental.

Para regerar, coloque o `.docx` original descompactado em `orig/` e rode:

```bash
python3 gerar_edital.py
```

O script recusa a geração se encontrar travessão, meia risca ou ponto médio
no corpo do texto.

## O que ainda precisa ser preenchido

A coluna **Vagas** da tabela da seção 3 está com `[__]` em todas as áreas.
