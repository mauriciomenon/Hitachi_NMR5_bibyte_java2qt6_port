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

## Validacao local

Rodar os testes de calculo:

```bash
cd cpp
ctest --test-dir build --output-on-failure
```

Verificar o log de inicializacao QML por erros comuns:

```bash
cd cpp
./check_runtime_log.sh
```

Gerar pacote local do executavel:

```bash
cd cpp
cmake --build build --target package
```

Os arquivos gerados ficam em `cpp/build/`, por exemplo `nmr5-qml-0.1.0-Darwin.tar.gz`
e `nmr5-qml-0.1.0-Darwin.zip`. Este pacote e um artefato local leve e pressupoe
Qt disponivel no ambiente onde o executavel sera rodado.

## Build no Windows

Dependencias recomendadas via `winget`:

```powershell
winget install -e --id Git.Git
winget install -e --id Kitware.CMake
winget install -e --id Ninja-build.Ninja
winget install -e --id Microsoft.VisualStudio.2022.BuildTools
```

No Visual Studio Build Tools, instalar os componentes de C++:

- MSVC v143 C++ x64/x86 build tools.
- Windows 10/11 SDK.
- C++ CMake tools for Windows.

Instalar o Qt pelo Qt Online Installer com:

- Qt 6.x MSVC 2022 64-bit.
- Qt Declarative / QML / Quick / QuickControls2.

Build com `qt-cmake.bat`:

```powershell
cd C:\path\Hitachi_NMR5_bibyte_java2qt6_port\cpp
C:\Qt\6.x.x\msvc2022_64\bin\qt-cmake.bat -S . -B build -G Ninja
cmake --build build
.\build\nmr5_qml.exe
```

Build alternativo com CMake puro:

```powershell
cd C:\path\Hitachi_NMR5_bibyte_java2qt6_port\cpp
cmake -S . -B build -G Ninja -DCMAKE_PREFIX_PATH=C:\Qt\6.x.x\msvc2022_64
cmake --build build
.\build\nmr5_qml.exe
```

Alternativa para instalar Qt por CLI:

```powershell
winget install -e --id miurahr.aqtinstall
aqt list-qt windows desktop
```

Depois de escolher a versao disponivel, instalar o alvo `win64_msvc2022_64`.

## Conteudo

- `src/AppBackend.*`: backend C++ para conversao PTNO/BitByte, calculo analogico e dados de tabela.
- `qml/Main.qml`: interface QML com paineis de calculadora e tabelas.
- `CMakeLists.txt`: projeto Qt 6 com QML module.

## Notas de layout

- O redimensionamento deve preservar a proporcao visual atual entre calculadoras e tabelas.
- As tabelas devem ter sobra para conforto visual, mas colunas nao devem crescer sem necessidade.
- A tabela de localizacao deve reservar espaco suficiente para `Cota [m]` e `Eixo` sem depender de esconder colunas.
- A coluna `Localizacao` deve caber nomes como `Casa de Forca` com pequena reserva, sem consumir espaco excessivo.
- A tabela de cabos inclui `Cor an.`; por isso `Anilha` deve ficar apenas com o conforto necessario para valores como `I`, `II` e `III`.
- Ajustes de largura devem manter a soma total coerente e evitar aumentar a janela inicial como solucao primaria.

Este slice nao substitui a versao PyQt. Ele existe para avaliar a direcao C++/Qt/QML.
