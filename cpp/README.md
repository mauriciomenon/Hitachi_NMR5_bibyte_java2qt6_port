# NMR5 Qt/QML slice

Versao C++/Qt/QML experimental da interface NMR5.

## Objetivo

- Manter a aplicacao Python/PyQt como principal.
- Criar um slice C++ Qt 6 QML isolado em `cpp/`.
- Validar as calculadoras principais e um layout similar ao app atual.

## Build

```bash
cd cpp
qt-cmake -S . -B build
cmake --build build
./build/nmr5_qml
```

## Conteudo

- `src/AppBackend.*`: backend C++ para conversao PTNO/BitByte, calculo analogico e dados de tabela.
- `qml/Main.qml`: interface QML com paineis de calculadora e tabelas.
- `CMakeLists.txt`: projeto Qt 6 com QML module.

Este slice nao substitui a versao PyQt. Ele existe para avaliar a direcao C++/Qt/QML.

