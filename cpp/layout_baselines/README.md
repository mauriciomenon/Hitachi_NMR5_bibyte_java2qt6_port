# QML layout baselines

Esta pasta guarda snapshots versionados de layouts QML aprovados.

Regras:

- Nao editar os arquivos dentro dos snapshots.
- Criar novo snapshot quando houver nova aprovacao visual relevante.
- Usar timestamp no nome do arquivo.
- Registrar plataforma, commit base e observacoes de validacao.
- Guardar snapshots como `.tar.gz` para deixar claro que sao backup historico,
  nao QML ativo do app.

O objetivo e permitir comparacao e rollback manual de layout sem depender de
memoria visual ou screenshots soltos.

Snapshot atual:

- `2026-05-08_001348_mac_ok.tar.gz`
- Commit base: `155b615`
- Plataforma validada: macOS
- App: `cpp/build/nmr5_qml`
- Comentario: layout aprovado visualmente no macOS apos ajuste de proporcao,
  alinhamento e largura da area de calculadoras.
