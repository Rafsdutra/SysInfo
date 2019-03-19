import sys
import os
import psutil
import platform


# import pdfkit
# from fpdf import FPDF


def infoBasicas():
    print(" ")
    print("============================ Informações Básicas ===============================")
    print('SO   :', platform.system())
    print('Versão do SO  :', platform.release())
    print('Host     :', platform.node())
    print('Arquitetura:', platform.processor())
    print(" ")

    so = str(platform.system())
    versaoSO = str(platform.release())
    host = str(platform.node())
    arquitetura = str(platform.processor())

    f = open('SysInfo.txt', 'a+')
    f.write('============================ Informações Básicas ===============================\n')
    f.write('SO: ' + so + '\n')
    f.write('Versão do SO: ' + versaoSO + '\n')
    f.write('Nome da Máquina: ' + host + '\n')
    f.write('Processador: ' + arquitetura + '\n')
    f.write('\n')
    f.close()


def bytesParaMB(n):
    # >>> bytesParaMB(10000)
    # '9.8K'
    # >>> bytesParaMB(100001221)
    # '95.4M'
    #
    simbolos = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(simbolos):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(simbolos):
        if n >= prefix[s]:
            valor = float(n) / prefix[s]
            return '%.1f%s' % (valor, s)
    return "%sB" % n


def main():
    print("============================ Unidades de Armazenamento ====================================================")
    print(" ")

    f = open("SysInfo.txt", "a+")
    f.write("============================ Unidades de Armazenamento ====================================================\n\n")
    f.write("Dispositivo" + "          " + "Total" + "     " + "Usado" + "    " + "Livre" + "   " + "Uso " + "   " + "Tipo" + "   " + "Partição\n")
    templ = "%-17s %8s %8s %8s %5s%% %9s  %s"
    print(templ % ("Dispositivo", "Total", "Usado", "Livre", "Uso ", "Tipo",
                   "Partição"))

    for part in psutil.disk_partitions(all=False):
        if os.name == 'nt':
            if 'cdrom' in part.opts == '':
                continue
        uso = psutil.disk_usage(part.mountpoint)
        print(templ % (
            part.device,
            bytesParaMB(uso.total),
            bytesParaMB(uso.used),
            bytesParaMB(uso.free),
            int(uso.percent),
            part.fstype,
            part.mountpoint))


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

        print("-------------------------------------------------------------------------------------------------------------")


# def printPDF():
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)
#     pdf.cell(200, 10, txt=main(),  align="C")
#     pdf.output("SysInfo.pdf")

if __name__ == '__main__':
    infoBasicas()
    main()
    # pdfkitTest()
    # printPDF()
print(" ")
