import tkinter as tk
from tkinter import ttk

def exibir_tablertu():
    # Esta função será chamada quando o botão "Localização das UTRs" for pressionado
    pass

def calcular_ptno():
    # Implemente a lógica de cálculo para PTNO aqui
    pass

def calcular_bitbyte():
    # Implemente a lógica de cálculo para BitByte aqui
    pass

def exibir_codigos_cores():
    # Esta função exibirá a tabela com os códigos de cores
    pass

app = tk.Tk()
app.title("IEC-870-5 Unbalanced Mode")

frame_principal = ttk.Frame(app)
frame_principal.pack(padx=10, pady=10)


# Seção de Conversor BitByte <-> PTNO
label_sostat = ttk.Label(frame_principal, text="SOSTAT")
label_sostat.grid(row=0, column=0, sticky="w", pady=(0, 10))

label_conversor = ttk.Label(frame_principal, text="Conversor BitByte <-> PTNO")
label_conversor.grid(row=1, column=0, sticky="w", pady=(0, 5))

entry_bitbyte = ttk.Entry(frame_principal)
entry_bitbyte.grid(row=2, column=0, sticky="w", pady=5)

btn_calc_ptno = ttk.Button(frame_principal, text="Calcular PTNO", command=calcular_ptno)
btn_calc_ptno.grid(row=2, column=1, padx=5, pady=5)

entry_ptno = ttk.Entry(frame_principal)
entry_ptno.grid(row=3, column=0, sticky="w", pady=5)

btn_calc_bit = ttk.Button(frame_principal, text="Calcular Bit...", command=calcular_bitbyte)
btn_calc_bit.grid(row=3, column=1, padx=5, pady=5)

btn_limpar = ttk.Button(frame_principal, text="Limpar valores")
btn_limpar.grid(row=4, column=0, columnspan=2, pady=(5, 10))

# Seção de Localização/código de cores dos cabos
label_localizacao = ttk.Label(frame_principal, text="Localização/código de cores dos cabos")
label_localizacao.grid(row=5, column=0, sticky="w", pady=(0, 5))

btn_utrs = ttk.Button(frame_principal, text="Localização das UTRs", command=exibir_tablertu)
btn_utrs.grid(row=6, column=0, sticky="w", pady=5)

btn_cod_cores = ttk.Button(frame_principal, text="Código e Cores dos Cabos de UTRs", command=exibir_codigos_cores)
btn_cod_cores.grid(row=7, column=0, sticky="w", pady=5)

# Tabela completa
table_data = [
    ("UTR501", "A01R01", "1", "1", "CF", "U1", "108", "C-D", "", "UTR520", "C45A01", "20", "19", "GIS", "U2", "124", "A-B"),
    ("UTR502", "A02R01", "2", "2", "CF", "U2", "108", "C-D", "", "UTR520-1", "C45A02", "21", "20", "GIS", "U3", "124", "A-B"),
    ("UTR503", "A03R01", "3", "3", "CF", "U3", "108", "C-D", "", "UTR521", "C45A03", "22", "21", "GIS", "U5", "124", "A-B"),
    ("UTR504", "A04R01", "4", "4", "CF", "U4", "108", "C-D", "", "UTR522", "C45A04", "23", "22", "GIS", "U8", "124", "A-B"),
    ("UTR505", "A05R01", "5", "5", "CF", "U5", "108", "C-D", "", "UTR620", "D45A01", "24", "23", "GIS", "U12", "124", "A-B"),
    ("UTR506", "A06R01", "6", "1", "CF", "U6", "108", "C-D", "", "UTR621", "D45A02", "25", "24", "GIS", "U14", "124", "A-B"),
    ("UTR507", "A07R01", "7", "7", "CF", "U7", "108", "C-D", "", "UTR622", "D45A03", "26", "25", "GIS", "U16", "124", "A-B"),
    ("UTR508", "A08R01", "8", "8", "CF", "U8", "108", "C-D", "", "UTR622-1", "D45A04", "27", "26", "GIS", "U17", "124", "A-B"),
    ("UTR509", "A09R01", "9", "9", "CF", "U9", "108", "C-D", "", "UTR530", "J61A01", "30", "27", "CF", "U3", "115", "C-D"),
    ("UTR610", "B10R01", "10", "10", "CF", "U10", "108", "C-D", "", "UTR531", "J61A02", "31", "28", "CF", "U8", "115", "C-D"),
    ("UTR611", "B11R01", "11", "11", "CF", "U11", "108", "C-D", "", "UTR532", "J61A03", "32", "29", "CF", "AMD2", "127,6", "C-D"),
    ("UTR612", "B12R01", "12", "12", "CF", "U12", "108", "C-D", "", "UTR533", "J61A04", "33", "30", "CF", "AMD3", "144,5", "A-B"),
    ("UTR613", "B13R01", "13", "13", "CF", "U13", "108", "C-D", "", "UTR534", "J61A05", "34", "31", "CF", "U7", "127,6", "C-D"),
    ("UTR614", "B14R01", "14", "14", "CF", "U14", "108", "C-D", "", "UTR534-1", "J61A06", "35", "32", "GIS", "U9A", "132", "A-B"),
    ("UTR615", "B15R01", "15", "15", "CF", "U15", "108", "C-D", "", "UTR630", "K61A01", "36", "33", "CF", "U12", "115", "C-D"),
    ("UTR616", "B16R01", "16", "16", "CF", "U16", "108", "C-D", "", "UTR631", "K61A02", "37", "34", "CF", "AMC2", "127,6", "C-D"),
    ("UTR617", "B17R01", "17", "17", "CF", "U17", "108", "C-D", "", "UTR632", "K61A03", "38", "35", "CF", "U16", "115", "C-D"),
    ("UTR618", "B18R01", "18", "18", "CF", "U18", "108", "C-D", "", "UTR633", "K61A04", "39", "36", "CF", "AMC1", "144,5", "A-B"),
    ("UTR501-1", "A01R02", "51", "43", "CF", "U1", "98", "A-B", "", "UTR634", "K61A05", "40", "37", "CF", "U15", "115", "C-D"),
    ("UTR502-1", "A02R02", "52", "44", "CF", "U2", "98", "A-B", "", "UTR540", "J61A07", "41", "38", "Bar.", "U3", "214", ""),
    ("UTR503-1", "A03R02", "53", "45", "CF", "U3", "98", "A-B", "", "UTR541", "J61A08", "42", "39", "Bar.", "U9", "144,5", ""),
    ("UTR504-1", "A04R02", "54", "46", "CF", "U4", "98", "A-B", "", "UTR640", "K61A06", "43", "40", "Bar.", "U13", "214", ""),
    ("UTR505-1", "A05R02", "55", "47", "CF", "U5", "98", "A-B", "", "UTR641", "K61A07", "44", "41", "Bar.", "U16", "214", ""),
    ("UTR506-1", "A06R02", "56", "48", "CF", "U6", "98", "A-B", "", "UTR550", "H20A01", "80", "62", "Vert.", "", "214", ""),
    ("UTR507-1", "A07R02", "57", "49", "CF", "U7", "98", "A-B", "", "UTR570-2", "T75A04", "81", "63", "CF", "U10", "131", "C-D"),
    ("UTR508-1", "A08R02", "58", "50", "CF", "U8", "98", "A-B", "", "UTR670-1", "T75A05", "82", "64", "CF", "U9A", "131", "C-D"),
    ("UTR509-1", "A09R02", "59", "51", "CF", "U9", "98", "A-B", "", "UTR570-1", "T75A03", "84", "70", "CF", "U9A", "131", "C-D"),
    ("UTR610-1", "B10R02", "60", "52", "CF", "U10", "98", "A-B", "", "UTR670-2", "T75A06", "87", "71", "CF", "U10", "131", "C-D"),
    ("UTR611-1", "B11R02", "61", "53", "CF", "U11", "98", "A-B", "", "", "", "", "", "", "", "", ""),
    ("UTR612-1", "B12R02", "62", "54", "CF", "U12", "98", "A-B", "", "", "", "", "", "", "", "", ""),
    ("UTR613-1", "B13R02", "63", "55", "CF", "U13", "98", "A-B", "", "", "", "", "", "", "", "", ""),
    ("UTR614-1", "B14R02", "64", "56", "CF", "U14", "98", "A-B", "", "", "", "", "", "", "", "", ""),
    ("UTR615-1", "B15R02", "65", "57", "CF", "U15", "98", "A-B", "", "", "", "", "", "", "", "", ""),
    ("UTR616-1", "B16R02", "66", "58", "CF", "U16", "98", "A-B", "", "", "", "", "", "", "", "", ""),
    ("UTR617-1", "B17R02", "67", "59", "CF", "U17", "98", "A-B", "", "", "", "", "", "", "", "", ""),
    ("UTR618-1", "B18R02", "68", "60", "CF", "U18", "98", "A-B", "", "", "", "", "", "", "", "", "")
]


table_frame = ttk.Frame(frame_principal)
table_frame.grid(row=8, column=0, columnspan=2, pady=10)

table = ttk.Treeview(table_frame, columns=[""] * 17, show="headings")
table.heading("#1", text="UTR")
table.heading("#2", text="Code")
table.heading("#3", text="Logic")
table.heading("#4", text="Link")
table.heading("#5", text="Local")
table.heading("#6", text="Unidade")
table.heading("#7", text="Cota")
table.heading("#8", text="Eixo")
# Adicione mais cabeçalhos aqui

for row in table_data:
    table.insert("", "end", values=row)

table.pack()

app.mainloop()