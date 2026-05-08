# Riscos tecnicos do NMR5 Qt/QML

Este arquivo registra os pontos frageis atuais do slice Qt/QML. Ele nao e um
pedido para refatorar tudo agora; use como guia para proteger a interface que
esta funcionando e escolher mudancas futuras pequenas.

## Preservar baseline visual atual

O layout QML esta intencionalmente ajustado para a visualizacao desktop atual.
Nao alterar larguras, alturas, fontes, espacamentos, pesos das tabelas ou
posicoes de secoes sem checagem visual contra o baseline aprovado em
`layout_baselines/`.

## Premissas de dominio

- Valores analogicos raw usam atualmente faixa positiva de 15 bits: `0..32767`.
- O HEX de 16 bits representa o inteiro raw atual formatado com quatro digitos.
- Intervalos PTNO e BitByte estao codificados a partir do comportamento Java recuperado.
- Linhas de UTR e cabos usam CSV versionado com fallback compilado.
- Entrada decimal aceita ponto ou virgula, por exemplo `12.5` ou `12,5`.

## Registro de riscos atual

| Area | Risco | Mitigacao atual |
| --- | --- | --- |
| Layout QML | Medidas pixel-tuned podem regredir em outro DPI, fonte ou plataforma. | Manter baseline QML aprovado, capturar screenshot e revisar visualmente antes de edicoes de layout. |
| Larguras de tabela | Pesos de coluna sao manuais e a ultima coluna absorve a sobra. | Alterar proporcoes de tabela somente com revisao visual. |
| Contrato do modo analogico | QML envia ids em string para C++. | Labels estao desacoplados dos ids, e testes cobrem os ids aceitos. |
| Faixa raw analogica | Equipamento com outra faixa raw calcularia valores errados. | Maximo raw centralizado em `AnalogCalculator::RawMax`. |
| Regras PTNO/BitByte | Intervalos e offsets de dominio sao constantes internas. | Testes de borda cobrem as faixas recuperadas. |
| Dados de tabela | CSV externo pode ser alterado com schema ou colunas invalidas. | Validar cabecalho e numero de colunas antes de substituir o fallback compilado. |
| Empacotamento | Ferramentas Qt variam por plataforma e origem de instalacao. | Manter scripts por plataforma e matriz de validacao. |
| Smoke runtime | Checagem de log nao valida clipping visual ou interacao. | Usar como smoke test, nao como aceitacao visual. |

## Ordem preferida para hardening futuro

1. Capturar screenshot e revisar visualmente antes de tocar no layout de novo.
2. Validar constantes PTNO/BitByte contra fonte Java ou documentacao operacional.
3. Decidir se a faixa raw precisa virar configuracao.
4. Validar CSVs de UTR/cabos em Windows e Linux, mantendo fallback compilado.
5. Trocar contratos QML por interface mais tipada somente se a API crescer.
