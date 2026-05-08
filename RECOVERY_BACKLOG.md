# Recovery Backlog

- Verificar com fonte operacional se o Link da UTR506 deve permanecer `1` como no Java ou mudar para `6` pela sequencia visual. Mantido `1` neste slice para preservar compatibilidade com `BiByte_java`.
- Validar em Windows e Linux se as medidas pixel-tuned do QML preservam a aparencia aprovada antes de qualquer novo ajuste visual.
- Confirmar com fonte operacional se o raw analogico deve permanecer `0..32767` para todos os equipamentos ou se precisa virar configuracao.
- Planejar migracao futura das tabelas de UTR/cabos para arquivo versionado com validacao, mantendo fallback compilado.
- Avaliar `QSortFilterProxyModel` ou carga assincrona apenas se as tabelas crescerem a ponto de causar atraso perceptivel; com o volume atual, manter caminho simples.
