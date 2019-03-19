import sys
import os
import psutil
import platform
import cpuinfo


# import pdfkit
# from fpdf import FPDF


def infoBasicas():
    # ============================== Tela ========================================
    print(" ")
    print("============================ Informações Básicas ===============================")
    print('SO   :', platform.system())
    print('Versão do SO  :', platform.release())
    print('Host     :', platform.node())
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
    f.write('SO: ' + so + '\n')
    f.write('Versão do SO: ' + versaoSO + '\n')
    f.write('Nome da Máquina: ' + host + '\n')
    f.write('Arquitetura: ' + arquitetura + '\n')
    f.write('\n')
    f.close()


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

#Conversão de Bytes para MB
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
    # ============================================ Tela ===========================================#
    print("============================ Unidades de Armazenamento ====================================================")
    print(" ")
    # ============================================================================================= #

    # Inserção do cabeçalho do programa no file txt
    f = open("SysInfo.txt", "a+")
    f.write("============================ Unidades de Armazenamento ====================================================\n\n")
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


        #Inserção das informações no file txt
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
    cpuInfo()
    main()

print(" ")
