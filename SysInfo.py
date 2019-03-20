import sys
import os
import psutil
import platform
import cpuinfo
import ctypes
from fpdf import FPDF


def infoBasicas():
    # ============================== Tela ========================================
    print(" ")
    print("============================ Informações Básicas ===============================")
    print('Host     :', platform.node())
    print('SO   :', platform.system())
    print('Versão do SO  :', platform.release())
    print('Arquitetura:', platform.processor())
    print(" ")
    # ==============================================================================

    #  Variáveis contendo as informações para serem usadas no file
    so = str(platform.system())
    versaoSO = str(platform.release())
    host = str(platform.node())
    arquitetura = str(platform.processor())

    # Inserção das informações no file txt
    f = open('SysInfo.txt', 'a+')
    f.write('============================ Informações Básicas ===============================\n')
    f.write('Nome da Máquina: ' + host + '\n')
    f.write('SO: ' + so + '\n')
    f.write('Versão do SO: ' + versaoSO + '\n')
    f.write('Arquitetura: ' + arquitetura + '\n')
    f.write('\n')
    f.close()


# Conversão de Bytes para MB
def bytesParaMB(n):
    # >>> bytesParaMB(10000)
    # '9.8K'
    # >>> bytesParaMB(100001221)
    # '95.4M'
    #
    simbolos = ('K', 'MB', 'GB', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(simbolos):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(simbolos):
        if n >= prefix[s]:
            valor = float(n) / prefix[s]
            return '%.1f%s' % (valor, s)
    return "%sB" % n


# Pega as informações do processador
def cpuInfo():
    infoMarca = str(cpuinfo.get_cpu_info()['brand'])
    infoFrequencia = str(cpuinfo.get_cpu_info()['hz_advertised'])
    print('======================== Informações do Processador ==============================\n\n')
    print('Marca/Modelo do Processador: ' + infoMarca)
    print('Frequência: ' + infoFrequencia)
    print('\n\n')
    f = open('SysInfo.txt', 'a+')
    f.write('======================== Informações do Processador ==============================\n\n')
    f.write('Marca/Modelo do Processador: ' + infoMarca)
    f.write('\n')
    f.write('Frequência: ' + infoFrequencia)
    f.write('\n\n')
    f.close()


# def ramMB(nt):
#     for nome in nt._fields:
#         valor = getattr(nt, nome)
#         if nome != 'percent':
#             valor = bytesParaMB(valor)
#             print('%-10s : %7s' % (nome.capitalize(), valor))


#Função para mostrar as informações da memória RAM e Swap
def ramInfo():

    print('======================== Informações da Memória RAM ===============================\n\n')
    f = open('SysInfo.txt', 'a+')

    totalRAM = bytesParaMB(psutil.virtual_memory().total)
    totalSWAP = bytesParaMB(psutil.swap_memory().total)

    print('Total Memória RAM: ' + totalRAM)
    print('Total Memória SWAP: ' + totalSWAP)

    f.write('======================== Informações da Memória RAM ===============================\n\n')
    f.write('Total Memória RAM: ' + totalRAM + '\n')
    f.write('Total Memória SWAP: ' + totalSWAP + '\n')
    f.write('\n')
    f.close()
    print('\n')


def main():
    # ============================================ Tela ===========================================#
    print("============================ Unidades de Armazenamento ==================================")
    print(" ")
    # ============================================================================================= #

    # Inserção do cabeçalho do programa no file txt
    f = open("SysInfo.txt", "a+")
    f.write("============================ Unidades de Armazenamento =====================================\n\n")
    f.write("Dispositivo" + "          " + "Total" + "     " + "Usado" + "    " + "Livre" + "   " + "Uso " + "   " + "Tipo" + "   " + "Partição\n")
    f.close()

    templ = "%-17s %8s %8s %8s %5s%% %9s  %s"
    # ====================================== Tela ================================== #
    print(templ % ("Dispositivo", "Total", "Usado", "Livre", "Uso ", "Tipo",
                   "Partição"))
    # ============================================================================== #

    # Laço contendo partições que não sejam CD-ROM
    for part in psutil.disk_partitions(all=False):
        if os.name == 'nt':
            if 'cdrom' in part.opts == '':
                continue
        uso = psutil.disk_usage(part.mountpoint)
        # ====================== Tela ===================== #
        print(templ % (
            part.device,
            bytesParaMB(uso.total),
            bytesParaMB(uso.used),
            bytesParaMB(uso.free),
            int(uso.percent),
            part.fstype,
            part.mountpoint))
        # ================================================= #

        # Inserção das informações no file txt
        f = open("SysInfo.txt", "a+")
        f.write(str(templ % (
            part.device,
            bytesParaMB(uso.total),
            bytesParaMB(uso.used),
            bytesParaMB(uso.free),
            int(uso.percent),
            part.fstype,
            part.mountpoint + '\n')))
        # f.write('\n')
        f.close()

        print(
            "-------------------------------------------------------------------------------------------------------------")


title = 'Especificações do PC - 9TALK'


class PDF(FPDF):
    def header(self):
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        #  Calcula largura e posição do titulo
        w = self.get_string_width(title) + 6
        self.set_x((210 - w) / 2)
        # Cores do Frame, do background e dos textos
        self.set_draw_color(0, 80, 180)
        self.set_fill_color(230, 230, 0)
        self.set_text_color(220, 50, 50)
        # Espessura do frame (1 mm)
        self.set_line_width(1)
        # TITULO
        self.cell(w, 9, title, 1, 1, 'C', 1)
        # Quebra de linha
        self.ln(10)

    def footer(self):
        #  Posição a 1,5cm de baixo pra cima
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Cor do texto em cinza
        self.set_text_color(128)
        # Número da página
        self.cell(0, 10, 'Página:  ' + str(self.page_no()), 0, 0, 'C')

    def arquivo_doc(self, num, label):
        # Arial 12
        self.set_font('Arial', '', 12)
        # Cor do fundo
        self.set_fill_color(200, 220, 255)
        self.ln(4)

    def arquivo_corpo(self, name):
        # Lê arquivo de texto
        with open(name, 'rb') as fh:
            try:
                txt = fh.read().decode('UTF-8')
            except:
                txt = fh.read().decode('latin1')
        # Times 12
        self.set_font('Times', '', 12)
        # Texto justificado do output
        self.multi_cell(0, 5, txt)
        # Line break
        self.ln()
        # Indicação do fim de arquivo em itálico
        self.set_font('', 'I')
        self.cell(0, 5, '(Fim do Arquivo)')

    def print_arquivo(self, num, title, name):
        self.add_page()
        self.arquivo_doc(num, title)
        self.arquivo_corpo(name)


pdf = PDF()
pdf.set_title(title)
pdf.set_author('Rafael')
pdf.print_arquivo(1, 'Especificações', 'SysInfo.txt')
pdf.output('SysInfo.pdf', 'F')

if __name__ == '__main__':
    infoBasicas()
    cpuInfo()
    ramInfo()
    # HDinfo()
    main()
    PDF()

print(" ")
