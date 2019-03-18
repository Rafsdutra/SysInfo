import sys
import os
import psutil
import platform
import pdfkit
from fpdf import FPDF


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
    print("============================ Unidades de Armazenamento =============================")
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

        device = str(part.device)
        usoTotal = str(bytesParaMB(uso.total))
        usoUsado = str(bytesParaMB(uso.used))
        usoLivre = str(bytesParaMB(uso.free))
        porcent = str(int(uso.percent))
        fs = str(part.fstype)
        mount = str(part.mountpoint)

        f = open("SysInfo.txt", "w+")
        f.writelines(device + ' '),
        f.writelines(usoTotal + ' '),
        f.writelines(usoLivre + ' '),
        f.write(usoUsado + ' '),
        f.write(porcent + ' '),
        f.write(fs + ' '),
        f.write(mount + ' '),
        f.close()

        # pdfKIT = pdfkit.from_string('============================ Unidades de Armazenamento =============================', 'SysInfo.pdf')
        # pdfkit.from_string(templ % (
        #     part.device,
        #     bytesParaMB(uso.total),
        #     bytesParaMB(uso.used),
        #     bytesParaMB(uso.free),
        #     int(uso.percent),
        #     part.fstype,
        #     part.mountpoint), 'SysInfo.pdf')

        print(
            "-------------------------------------------------------------------------------------------------------------")


# def printPDF():
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)
#     pdf.cell(200, 10, txt=main(),  align="C")
#     pdf.output("SysInfo.pdf")

def pdfkitTest():
    pdfkit.from_string(main(), 'SysInfo.pdf')


if __name__ == '__main__':
    infoBasicas()
    main()
    # pdfkitTest()
    # printPDF()
print(" ")
