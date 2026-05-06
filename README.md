# Hitachi NMR5 BiByte Java to PyQt6 Port

Porta PyQt6 do utilitario Java `BiByte_java`, usada para conversao
BitByte/PTNO, calculo analogico Raw Counts BIAS/SCALE e consulta de tabelas
de UTRs e cabos.

## Versao

Versao atual do pacote: `0.1.0`

A versao fica definida em `pyproject.toml`.

## Launcher

Launcher principal:

```bash
SCADA_NMR5_tool.py
```

Comando recomendado:

```bash
uv run python SCADA_NMR5_tool.py
```

## Repos de origem

Este projeto consolida duas bases de autoria de Mauricio Menon:

- Porta PyQt6 atual:
  - Remoto: `https://github.com/mauriciomenon/Hitachi_NMR5_bibyte_java2qt6_port`
- Origem Java BitByte/PTNO:
  - Remoto: `https://github.com/mauriciomenon/BiByte_java`
  - Referencia funcional: regras de conversao BitByte/PTNO e tabelas de UTRs/cabos.
  - Historico relevante: aplicacao Swing/Java com builds Ant/Gradle e releases Java.
- Origem analogica Raw Counts BIAS/SCALE:
  - Remoto: `https://github.com/mauriciomenon/RawCountsBIASscale`
  - Referencia funcional adotada neste port: `indicador_v1.12.py` (usado como base
    para os calculos e padrao de interface).
  - Observacao: no repo o launcher local principal pode ficar apontando v1.9; neste
    port a formula e formato final usam o comportamento da v1.12.

## Requisitos

- `uv`
- Python `>=3.13`
- Dependencias resolvidas por `uv sync`

Dependencias principais:

- `PyQt6`
- `pytest`
- `ruff`
- `ty`

## Setup

```bash
uv sync
```

O ambiente local fica em `.venv/`.

## Validacao

Comandos usados para validar este slice:

```bash
uv run python -m py_compile SCADA_NMR5_tool.py bitbyte_logic.py bitbyte_data.py analog_logic.py tests/test_calculos.py tests/test_analog_logic.py
uv run ruff check .
uv run ty check . --exclude 'historico_codigo/**'
uv run pytest tests/test_calculos.py tests/test_analog_logic.py
QT_QPA_PLATFORM=offscreen uv run python - <<'PY'
from PyQt6.QtWidgets import QApplication
from SCADA_NMR5_tool import App
from analog_logic import calculate_analog
from bitbyte_data import CABLE_COLOR_DATA, RTU_DATA
from bitbyte_logic import bitbyte_from_ptno, ptno_from_bitbyte

app = QApplication([])
window = App()
assert window.table.rowCount() == len(RTU_DATA)
assert window.second_table.rowCount() == len(CABLE_COLOR_DATA)
assert bitbyte_from_ptno("15100") == 2248
assert ptno_from_bitbyte("2248") == 15100
assert calculate_analog(4, 20, 0, 10, 5).raw_hex16 == "0x4ccc"
window.calculate_analog()
assert window.analog_raw_hex.text() == "0x4ccc"
window.close()
app.quit()
print("pyqt analog smoke ok")
PY
```

## Arquivos principais

- `SCADA_NMR5_tool.py`: launcher e interface PyQt6.
- `bitbyte_logic.py`: regras de conversao compativeis com a base Java.
- `analog_logic.py`: regras analogicas Raw Counts BIAS/SCALE baseadas na v1.12.
- `bitbyte_data.py`: dados das tabelas de UTRs e cabos.
- `tests/test_calculos.py`: testes focados na logica BitByte/PTNO.
- `tests/test_analog_logic.py`: testes focados na logica analogica.
- `historico_codigo/`: versoes antigas preservadas por nome, fora do caminho funcional.
- `RECOVERY_BACKLOG.md`: itens nao bloqueantes para revisar depois.

## Observacoes

- Os arquivos historicos foram movidos para `historico_codigo/`:
  - `pyqt6_v0_import_sys.py`
  - `tkinter_v0_import_tkinter.py`
  - `pyqt6_v1_teste.py`
- A faixa de PseudoPoint segue o comportamento Java e retorna `0`.
- O campo `Link` da `UTR506` foi mantido como `1`, igual ao Java, ate confirmacao operacional.
- O painel analogico usa a v1.12 do `RawCountsBIASscale` como referencia funcional.
- O grafico analogico foi redesenhado em Qt nativo, sem depender de `tk_tools`.
