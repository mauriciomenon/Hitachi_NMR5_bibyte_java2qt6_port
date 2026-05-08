# NMR5 Qt/QML slice

Versao C++/Qt/QML experimental da interface NMR5.

## Objetivo

- Manter a aplicacao Python/PyQt como principal.
- Criar um slice C++ Qt 6 QML isolado em `cpp/`.
- Validar as calculadoras principais e um layout similar ao app atual.

## Requisitos por sistema

### macOS

Instalar Command Line Tools e dependencias via Homebrew:

```bash
xcode-select --install
brew install cmake ninja qt
```

Se `qt-cmake` nao estiver no `PATH`, use o binario do Homebrew:

```bash
cd cpp
$(brew --prefix qt)/bin/qt-cmake -S . -B build -G Ninja
cmake --build build
```

### Debian

Dependencias recomendadas:

```bash
sudo apt update
sudo apt install build-essential cmake ninja-build qt6-base-dev qt6-declarative-dev qt6-tools-dev-tools
```

O pacote `qt6-declarative-dev` traz as dependencias Qt Quick/QML usadas pelo app,
incluindo Quick Controls nas versoes estaveis atuais do Debian.

### Artix

Dependencias recomendadas:

```bash
sudo pacman -Syu --needed base-devel cmake ninja qt6-base qt6-declarative qt6-tools
```

### Windows 11

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

Alternativa para instalar Qt por CLI:

```powershell
winget install -e --id miurahr.aqtinstall
aqt list-qt windows desktop
aqt install-qt windows desktop 6.8.2 win64_msvc2022_64
```

Use uma versao disponivel na saida de `aqt list-qt` se `6.8.2` nao estiver
listada.

## Build e execucao

### macOS

```bash
cd cpp
qt-cmake -S . -B build -G Ninja
cmake --build build
./build/nmr5_qml
```

Se `qt-cmake` nao estiver no `PATH`:

```bash
cd cpp
$(brew --prefix qt)/bin/qt-cmake -S . -B build -G Ninja
cmake --build build
./build/nmr5_qml
```

### Debian e Artix

```bash
cd cpp
cmake -S . -B build -G Ninja
cmake --build build
./build/nmr5_qml
```

### Windows 11

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

No Windows:

```powershell
cd C:\path\Hitachi_NMR5_bibyte_java2qt6_port\cpp
ctest --test-dir build --output-on-failure
```

## Gerar distribuivel

### Pacote local leve

O target `package` gera `.tar.gz` e `.zip` em `cpp/build/`:

```bash
cd cpp
cmake --build build --target package
```

Exemplos de saida:

- `cpp/build/nmr5-qml-0.1.0-Darwin.tar.gz`
- `cpp/build/nmr5-qml-0.1.0-Darwin.zip`
- `cpp/build/nmr5-qml-0.1.0-Linux.tar.gz`
- `cpp/build/nmr5-qml-0.1.0-Linux.zip`
- `cpp/build/nmr5-qml-0.1.0-win64.zip`

Este pacote e um artefato local leve. Ele pressupoe que Qt ja existe no ambiente
onde o executavel sera rodado.

### Windows portavel com DLLs Qt

Para uma pasta distribuivel no Windows, gere uma instalacao local e rode
`windeployqt`:

```powershell
cd C:\path\Hitachi_NMR5_bibyte_java2qt6_port\cpp
cmake --install build --prefix dist\nmr5_qml
C:\Qt\6.x.x\msvc2022_64\bin\windeployqt.exe --qmldir qml dist\nmr5_qml\bin\nmr5_qml.exe
```

Depois disso, distribuir a pasta `cpp\dist\nmr5_qml`.

### macOS portavel

O pacote atual nao gera `.app` e nao roda `macdeployqt`. Um distribuivel macOS
realmente portavel deve ser feito em um proximo slice separado, criando bundle
`.app` e aplicando `macdeployqt`.

### Debian e Artix

Para Linux, o pacote CPack atual e adequado para ambiente controlado com Qt
instalado via gerenciador do sistema. Um distribuivel Linux independente exigiria
um slice proprio para AppImage, Flatpak ou empacotamento nativo por distro.

## Conteudo

- `src/AppBackend.*`: backend C++ para conversao PTNO/BitByte, calculo analogico e dados de tabela.
- `qml/Main.qml`: interface QML com paineis de calculadora e tabelas.
- `CMakeLists.txt`: projeto Qt 6 com QML module.
- `check_runtime_log.sh`: smoke test local para erros comuns de runtime QML.
- `tests/calculator_tests.cpp`: testes QtTest dos calculos principais.

## Referencias

- Qt CMake command line: https://doc.qt.io/qt-6/cmake-build-on-cmdline.html
- Qt Windows deployment: https://doc.qt.io/qt-6/windows-deployment.html
- Qt macOS deployment: https://doc.qt.io/qt-6/macos-deployment.html
- Apple Command Line Tools: https://developer.apple.com/documentation/xcode/installing-the-command-line-tools/
- Homebrew Qt: https://formulae.brew.sh/formula/qt
- Debian `qt6-declarative-dev`: https://packages.debian.org/stable/qt6-declarative-dev
- Artix `qt6-base`: https://packages.artixlinux.org/packages/world/x86_64/qt6-base/
- Artix `qt6-declarative`: https://packages.artixlinux.org/packages/world/x86_64/qt6-declarative/
- Microsoft winget: https://learn.microsoft.com/windows/package-manager/winget/

## Notas de layout

- O redimensionamento deve preservar a proporcao visual atual entre calculadoras e tabelas.
- As tabelas devem ter sobra para conforto visual, mas colunas nao devem crescer sem necessidade.
- A tabela de localizacao deve reservar espaco suficiente para `Cota [m]` e `Eixo` sem depender de esconder colunas.
- A coluna `Localizacao` deve caber nomes como `Casa de Forca` com pequena reserva, sem consumir espaco excessivo.
- A tabela de cabos inclui `Cor an.`; por isso `Anilha` deve ficar apenas com o conforto necessario para valores como `I`, `II` e `III`.
- Ajustes de largura devem manter a soma total coerente e evitar aumentar a janela inicial como solucao primaria.

Este slice nao substitui a versao PyQt. Ele existe para avaliar a direcao C++/Qt/QML.
