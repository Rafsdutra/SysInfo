import sys
import os
import psutil
import platform
import cpuinfo
import ctypes
from fpdf import FPDF


class Print():
    def infoBasicas(self):
        # ============================== Tela ========================================
        print(" ")
        print("============================ Informações Básicas ===============================")
        print('Host     :', platform.node())
        print('SO   :', platform.system())
        print('Versão do SO  :', platform.release())
        print('Arquitetura:', platform.processor())
        # ==============================================================================

    # Conversão de Bytes para MB
    def bytesParaMB(self, n):
        simbolos = ('KB', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
        prefix = {}
        for i, s in enumerate(simbolos):
            prefix = {}
            for i, s in enumerate(simbolos):
                prefix[s] = 1 << (i + 1) * 10
            for s in reversed(simbolos):
                if n >= prefix[s]:
                    valor = float(n) / prefix[s]
                    return '%.1f%s' % (valor, s)
        return "%sB" % n

    # Pega as informações do processador
    def cpuInfo(self):
        infoMarca = str(cpuinfo.get_cpu_info()['brand'])
        infoFrequencia = str(cpuinfo.get_cpu_info()['hz_advertised'])

        print('======================== Informações do Processador ==============================\n\n')
        print('Marca/Modelo do Processador: ' + infoMarca)
        print('Frequência: ' + infoFrequencia)

    # Função para mostrar as informações da memória RAM e Swap
    def ramInfo(self):
        print('======================== Informações da Memória RAM ===============================\n\n')
        totalRAM = self.bytesParaMB(psutil.virtual_memory().total)
        totalSWAP = self.bytesParaMB(psutil.swap_memory().total)
        print('Total Memória RAM: ' + totalRAM)
        print('Total Memória SWAP: ' + totalSWAP)

    def main(self, ):

        global part, uso

        # Variáveis infoBasicas
        so = str(platform.system())
        versaoSO = str(platform.release())
        host = str(platform.node())
        arquitetura = str(platform.processor())

        # Variáveis cpuInfo

        infoMarca = str(cpuinfo.get_cpu_info()['brand'])
        infoFrequencia = str(cpuinfo.get_cpu_info()['hz_advertised'])

        # Variáveis ramInfo

        totalRAM = self.bytesParaMB(psutil.virtual_memory().total)
        totalSWAP = self.bytesParaMB(psutil.swap_memory().total)

        # ================================= Tela =========================================#
        print('======================== Armazenamento ===============================\n')
        templ = "%-17s %8s %8s %8s %5s%% %9s  %s"
        print(templ % ("Dispositivo", "Total", "Usado", "Livre", "Uso ", "Tipo",
                       "Partição"))
        # ============================================================================== #

        # Inserção das informações no txt
        f = open('SysInfo.txt', 'a+')
        f.write('============================ Informações Básicas ===============================\n\n')
        f.write('Nome da Máquina: ' + host + '\n')
        f.write('SO: ' + so + '\n')
        f.write('Versão do SO: ' + versaoSO + '\n')
        f.write('Arquitetura: ' + arquitetura + '\n')
        f.write('\n')
        f.write('======================== Informações do Processador ==============================\n\n')
        f.write('Marca/Modelo do Processador: ' + infoMarca)
        f.write('\n')
        f.write('Frequência: ' + infoFrequencia)
        f.write('\n\n')
        f.write('======================== Informações da Memória RAM ===============================\n\n')
        f.write('Total Memória RAM: ' + totalRAM + '\n')
        f.write('Total Memória SWAP: ' + totalSWAP + '\n')
        f.write('\n')
        f.write("============================ Armazenamento =============================\n\n")
        f.write(
            "Dispositivo" + "          " + "Total" + "     " + "Usado" + "    " + "Livre" + "   " + "Uso " + "   " + "Tipo" + "   " + "Partição\n\n")
        # Laço contendo partições que não sejam CD-ROM
        for part in psutil.disk_partitions(all=False):
            if os.name == 'nt':
                if 'cdrom' in part.opts == '':
                    continue
            uso = psutil.disk_usage(part.mountpoint)

            # ====================== Tela ===================== #
            print(templ % (
                part.device,
                self.bytesParaMB(uso.total),
                self.bytesParaMB(uso.used),
                self.bytesParaMB(uso.free),
                int(uso.percent),
                part.fstype,
                part.mountpoint))
            # ================================================= #

            f.write(str(templ % (
                part.device,
                self.bytesParaMB(uso.total),
                self.bytesParaMB(uso.used),
                self.bytesParaMB(uso.free),
                int(uso.percent),
                part.fstype,
                part.mountpoint + '\n')))
            f.write('--------------------------------------------------------------------------------------')
            f.write('\n')

        f.close()


title = 'Especificações do PC - 9TALK'


class PDF(FPDF):
    def header(self):
        # Arial bold 15
        self.image('9talk.png', 10, 8, 33)
        self.set_font('Arial', 'B', 10)
        #  Calcula largura e posição do titulo
        w = self.get_string_width(title) + 6
        self.set_x((210 - w) / 2)
        # Cores do Frame, do background e dos textos
        self.set_draw_color(0, 80, 180)
        self.set_fill_color(255, 255, 255)
        self.set_text_color(0, 0, 0)
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
        self.cell(0, 10, 'Página  ' + str(self.page_no()), 0, 0, 'C')

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
            except UnicodeDecodeError:
                txt = fh.read().decode('windows-1252')

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
pdf.set_author('9Talk')
pdf.print_arquivo(1, 'Especificações', 'SysInfo.txt')
pdf.output('SysInfo.pdf', 'F')

if __name__ == '__main__':
    # dir = os.getcwd()
    # files = os.listdir()
    # print(dir, files)
    prt = Print()
    print(prt.infoBasicas())
    print(prt.cpuInfo())
    print(prt.ramInfo())
    print(prt.main())
    PDF()
