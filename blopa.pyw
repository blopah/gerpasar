# INICIO FUNCOES
import smbclient
# import smbprotocol
# import subprocess
import os
import shutil
from datetime import date

hoje = date.today().strftime("%Y-%m-%d")
today = f'Data - {hoje}'

prefix_ori_S2G = '\\\\192.168.20.6\\icommgroup\\Pablo\\Servidor\\S2G\\Originais'.split('\\')
prefix_ori_OQV = '\\\\192.168.20.6\\icommgroup\\Pablo\\Servidor\\Icommgroup\\OQV\\Originais'.split('\\')
prefix_tra_S2G = '\\\\192.168.20.6\\icommgroup\\Pablo\\Servidor\\S2G\\Tratadas'.split('\\')
prefix_tra_OQV = '\\\\192.168.20.6\\icommgroup\\Pablo\\Servidor\\Icommgroup\\OQV\\Tratadas'.split('\\')
prefix_user = 'C:\\Users\\pablo.lucena\\Documents\\projeto\\Sandbox-Sys-Icomm\\Usuario\\Pablo Lucena'.split('\\')
prefix_user_S2G = prefix_user + [today] + ['S2G']
prefix_user_OQV = prefix_user + [today] + ['OQV']


def check_paths(reference, t_d):
    """
    :param reference: receives what is returned by the list_way function
    :param t_d: arg that defines if it is a take or a drop operation
    :return: returns the result of the verification of all paths and prefixes
    """
    if t_d == 't':
        # Checks original's paths from server
        # Checks all original's prefixes
        if os.path.exists('\\'.join(prefix_ori_OQV)):
            validprefix_ori_OQV = True
        else:
            validprefix_ori_OQV = False
        if os.path.exists('\\'.join(prefix_ori_S2G)):
            validprefix_ori_S2G = True
            # print('validprefix_ori_S2G = True')
        else:
            validprefix_ori_S2G = False

        # Checks each complete path, and if that is not found, is saved in a list
        list_of_not_found_srcs = list()
        list_of_not_found_srcs_txt = ''
        for refs in reference:
            if refs[0] == 'S2G':
                if not validprefix_ori_S2G:
                    return ('O caminho para a pasta originais da S2G não existe', False)
                del refs[0]
                src_path = '\\'.join(prefix_ori_S2G + refs)
                if not os.path.exists(src_path):
                    list_of_not_found_srcs.append(src_path)
                # else:
                #     print(os.path.exists(src_path))

            elif refs[0] == 'OQV':
                if not validprefix_ori_OQV:
                    return ('O caminho para a pasta originais da OQV não existe', False)
                del refs[0]
                src_path = '\\'.join(prefix_ori_OQV + refs)
                if not os.path.exists(src_path):
                    list_of_not_found_srcs.append(f'\n {src_path}')
        for list_items in list_of_not_found_srcs:
            list_of_not_found_srcs_txt += list_items
            print(list_of_not_found_srcs_txt)
        if not len(list_of_not_found_srcs) == 0:
            return ('Não foram enconstradas as seguintes pastas: \n{}'.format(list_of_not_found_srcs_txt), False)
        return ('Todos os caminhos das pastas foram encontrados.', True)
    elif t_d == 'd':
        # Checks user's local paths
        # Checks all user's prefixes
        if os.path.exists('\\'.join(prefix_user_OQV)):
            validprefix_user_OQV = True
        else:
            validprefix_user_OQV = False
        if os.path.exists('\\'.join(prefix_user_S2G)):
            validprefix_user_S2G = True
            print('validprefix_user_S2G = True')
        else:
            validprefix_user_S2G = False
            print('validprefix_user_S2G = False')

        # Checks each complete path, and if that is not found, is saved in a list
        list_of_not_found_srcs = list()
        list_of_not_found_srcs_txt = ''
        for refs in reference:
            if refs[0] == 'S2G':
                if not validprefix_user_S2G:
                    return ('O caminho para a pasta do usuario da S2G não existe', False)
                del refs[0]
                src_path = '\\'.join(prefix_user_S2G + refs)
                if not os.path.exists(src_path):
                    list_of_not_found_srcs.append(src_path)

            elif refs[0] == 'OQV':
                if not validprefix_user_OQV:
                    return ('O caminho para a pasta do usuario da OQV não existe', False)
                del refs[0]
                src_path = '\\'.join(prefix_user_OQV + refs)
                if not os.path.exists(src_path):
                    list_of_not_found_srcs.append(f'\n {src_path}')
        for list_items in list_of_not_found_srcs:
            list_of_not_found_srcs_txt += list_items
            print(list_of_not_found_srcs_txt)
        if not len(list_of_not_found_srcs) == 0:
            return ('Não foram enconstradas as seguintes pastas: \n{}'.format(list_of_not_found_srcs_txt), False)
        return ('Todos os caminhos das pastas foram encontrados.', True)


def copy_refs(reference, t_d):
    """
    :param reference: receives what is returned by the list_way function
    :param t_d: arg that defines if it is a take or a drop operation
    :return: copys the references from src_path to dst_path
    """

    if t_d == 't':
        list_of_not_found_srcs = list()
        list_of_not_found_dsts = list()
        list_of_not_found_srcs_txt = ''
        list_of_not_found_dsts_txt = ''
        for refs in reference:
            src_path = ''
            dst_path = ''
            try:
                if refs[0] == 'S2G':
                    del refs[0]
                    src_path = '\\'.join(prefix_ori_S2G + refs)
                    dst_path = '\\'.join(prefix_user_S2G + refs)
                    copy_tree(src_path, dst_path)

                elif refs[0] == 'OQV':
                    # print('refs[0] = OQV')
                    del refs[0]
                    src_path = '\\'.join(prefix_ori_OQV + refs)
                    dst_path = '\\'.join(prefix_user_OQV + refs)
                    copy_tree(src_path, dst_path)
                else:
                    print('Nao foi possível interpretar se o caminho é para S2G ou OQV')
                    return 'Nao foi possível interpretar se o caminho é para S2G ou OQV.'
            except FileNotFoundError:
                list_of_not_found_srcs.append(f'\n {src_path}')
                continue
            except FileExistsError:
                list_of_not_found_dsts.append(f'\n {dst_path}')
                continue
        for list_items in list_of_not_found_srcs:
            list_of_not_found_srcs_txt += list_items
            print(list_of_not_found_srcs_txt)
        for list_items in list_of_not_found_dsts:
            list_of_not_found_dsts_txt += list_items
            print(list_of_not_found_dsts_txt)
        if len(list_of_not_found_srcs) == 0 and len(list_of_not_found_dsts) == 0:
            return 'Tarefa Finalizada\n'
        elif not len(list_of_not_found_srcs) == 0 and not len(list_of_not_found_dsts) == 0:
            return 'Tarefa Finalizada \nCaminhos não encontrados no servidor: {} \nCaminho ja existente no seu Mac: \n {}'.format(
                list_of_not_found_srcs_txt, list_of_not_found_dsts_txt)
        elif not len(list_of_not_found_srcs) == 0:
            return 'Tarefa Finalizada \nCaminhos não encontrados no servidor: \n {}'.format(list_of_not_found_srcs_txt)
        elif not len(list_of_not_found_dsts) == 0:
            return 'Tarefa Finalizada \nCaminhos ja existentes no seu Mac: \n {}'.format(list_of_not_found_dsts_txt)


    elif t_d == 'd':
        list_of_not_found_srcs = list()
        list_of_not_found_dsts = list()
        list_of_not_found_srcs_txt = ''
        list_of_not_found_dsts_txt = ''
        for refs in reference:
            src_path = ''
            dst_path = ''
            try:
                if refs[0] == 'S2G':
                    del refs[0]
                    src_path = '\\'.join(prefix_user_S2G + refs)
                    dst_path = '\\'.join(prefix_tra_S2G + refs)
                    shutil.copytree(src_path, dst_path)
                    # print(f' dst_path {dst_path}')
                    # print(f' src_path {src_path}')

                elif refs[0] == 'OQV':
                    # print('refs[0] = OQV')
                    del refs[0]
                    src_path = '\\'.join(prefix_user_OQV + refs)
                    dst_path = '\\'.join(prefix_tra_OQV + refs)
                    shutil.copytree(src_path, dst_path)
                    # print(f' dst_path {dst_path}')
                    # print(f' src_path {src_path}')
                else:
                    print('Nao foi possível interpretar se o caminho é para S2G ou OQV.')
                    return 'Nao foi possível interpretar se o caminho é para S2G ou OQV.'
            except FileNotFoundError:
                list_of_not_found_srcs.append(f'\n {src_path}')
                continue
            except FileExistsError:
                list_of_not_found_dsts.append(f'\n {dst_path}')
                continue
        for list_items in list_of_not_found_srcs:
            list_of_not_found_srcs_txt += list_items
            print(list_of_not_found_srcs_txt)
        for list_items in list_of_not_found_dsts:
            list_of_not_found_dsts_txt += list_items
            print(list_of_not_found_dsts_txt)
        if len(list_of_not_found_srcs) == 0 and len(list_of_not_found_dsts) == 0:
            return 'Tarefa Finalizada0\n'
        elif not len(list_of_not_found_srcs) == 0 and not len(list_of_not_found_dsts) == 0:
            return 'Tarefa Finalizada1 \nCaminhos não encontrados no seu Mac: {} \nCaminho ja existente no servidor: \n {}'.format(
                list_of_not_found_srcs_txt, list_of_not_found_dsts_txt)
        elif not len(list_of_not_found_srcs) == 0:
            return 'Tarefa Finalizada2 \nCaminhos não encontrados no seu Mac: \n {}'.format(list_of_not_found_srcs_txt)
        elif not len(list_of_not_found_dsts) == 0:
            return 'Tarefa Finalizada3 \nCaminhos ja existentes no servidor: \n {}'.format(list_of_not_found_dsts_txt)


def creates_paths(reference, t_d):
    """
    :param reference: receives what is returned by the list_way function
    :param t_d: arg that defines if it is a take or a drop operation
    :return: creates the folders
    """

    if reference == 'IndexError':
        return 'Nao foi possível interpretar o caminho inserido.'

    # Converts the path's list to a path
    references = list()
    for refes in reference:
        refs = '\\'.join(refes[:-1])  # This '[:-1]' is to exclude the last reference's folder
        references.append(refs)
    # Form the path and creates the paths
    # In case of 't'(take) there is only one block of code
    if t_d == 't':
        for refs in references:
            caminho = os.path.join('\\'.join(prefix_user), today, refs)
            if not os.path.exists(caminho):
                os.makedirs(caminho)
    # In case of 'd'(drop) there are 2 blocks of code possibles
    elif t_d == 'd':
        for refs in references:
            if refs[:3] == 'S2G':
                caminho = os.path.join('\\'.join(prefix_tra_S2G), refs[4:])
                if not os.path.exists(caminho):
                    print('caminho nao existe. (ta ok)')
                    os.makedirs(caminho)
            elif refs[:3] == 'OQV':
                caminho = os.path.join('\\'.join(prefix_tra_OQV), refs[4:])
                if not os.path.exists(caminho):
                    os.makedirs(caminho)


def list_way(section):
    """
    :param section: Receives the raw paths inserted in the text area, copied from the spreadsheet 'Produtividade'
    :return: Returns a list, created from the processed section param
    """

    section_list = section.split('\n')
    section_list_ref = list()
    for refe in section_list:
        ref = refe.split('\t')  # Makes the line a list
        section_list_ref.append(ref)  # Appends the whole created list
    references = list()
    try:
        for ref in section_list_ref:
            ref.insert(0, ref[5])
            references.append(ref[:5])
        return references
    except IndexError:
        print('IndexError')
    return 'IndexError'


def copy_tree(src_path, dst_path):
    """
    :param src_path: receives the root of the source path
    :param dst_path: receives the root of the destiny path
    :return: copy references from the server to local or from the local to the server
    """
    walk = smbclient.walk(src_path)
    sufixo_index = 0
    for step in walk:
        endereco = step[0].split('\\')
        pastas = step[1]
        arquivos = step[2]
        print(' end = ', endereco, '\n', 'pas = ', pastas, '\n', 'arq = ', arquivos)
        if sufixo_index == 0:
            sufixo_index = endereco.index(endereco[-1]) + 1
        print(sufixo_index)
        print('*' * 50)
        os.makedirs(os.path.join(dst_path, '\\'.join(endereco[sufixo_index:])))
        for arq in arquivos:
            with smbclient.open_file(os.path.join('\\'.join(endereco), arq),
                                     'rb') as file:  # Abre o arquivo no servidor e o copia em uma variavel
                content = file.read()
                print(file.name)
                with open(os.path.join(dst_path, '\\'.join(endereco[sufixo_index:]), arq),
                          'wb') as filedst:  # Abre o arquivo localmente criandoo e escrevendo o contenteudo q foi armazenado em uma variavel nele
                    filedst.write(content)

# INICIO FUNCOES

referencias = '''OUTONO 20	Adidas	1111	vermelho	modelo	S2G
OUTONO 20	Nike	2222	off white	still	S2G
OUTONO 20	Calvin Klein	3333	branco	modelo e still	S2G
OUTONO 20	Swarovski	4444	cinza	mesa	S2G
OUTONO 19	Adidas	1111	vermelho	modelo	S2G
OUTONO 19	Nike	2222	off white	still	S2G
OUTONO 19	Calvin Klein	3333	branco	modelo e still	S2G
OUTONO 19	Swarovski	4444	cinza	mesa	S2G
VERAO 21	Adidas	1111	vermelho	modelo	S2G
VERAO 21	Nike	2222	off white	still	S2G
VERAO 21	Calvin Klein	3333	branco	modelo e still	S2G
VERAO 21	Swarovski	4444	cinza	mesa	S2G
OUTONO 20	Adidas	1111	vermelho	modelo	OQV
OUTONO 20	Nike	2222	off white	still	OQV
OUTONO 20	Calvin Klein	3333	branco	modelo e still	OQV
OUTONO 20	Swarovski	4444	cinza	mesa	OQV
OUTONO 19	Adidas	1111	vermelho	modelo	OQV
OUTONO 19	Nike	2222	off white	still	OQV
OUTONO 19	Calvin Klein	3333	branco	modelo e still	OQV
OUTONO 19	Swarovski	4444	cinza	mesa	OQV
VERAO 21	Adidas	1111	vermelho	modelo	OQV
VERAO 21	Nike	2222	off white	still	OQV
VERAO 21	Calvin Klein	3333	branco	modelo e still	OQV
VERAO 21	Swarovski	4444	cinza	mesa	OQV'''

referencia = 'OUTONO 20	Adidas	1111	vermelho	modelo	S2G'

# # TESTA O TAKE COMPLETO
# if check_paths(list_way(referencias), 'd')[1]:
#     print(check_paths(list_way(referencias), 'd')[0])
#     creates_paths(list_way(referencias), 'd')
#     print(copy_refs(list_way(referencias), 'd'))
#
# else:
#     print(check_paths(list_way(referencias), 'd')[0])

# TESTA O RETORNO DA FUNCAO create_paths
# creates_paths(list_way(referencia), 'd')

# TESTA O RETORNO DA FUNCAO check_paths
# check_paths(list_way(referencia), 'd')


# TESTA O RETORNO DA FUNCAO list_way
# return_list_way = list_way(referencias)
# for paths in return_list_way:
#     print(paths)

# origem = '\\\\192.168.20.6\\icommgroup\\Pablo\\Servidor\\S2G\\Originais\\OUTONO 19\\Adidas\\1111\\vermelho'
# destino = 'C:\\Users\\pablo.lucena\\Documents\\projeto\\Sandbox-Sys-Icomm'
#
# copy_tree(origem, destino)

# from smbclient.shutil import copytree

# pt1 Esse trecho do codigo faz a copia de um arquivo do servidor armazenando seu conteudo em uma variavel (metodo trabalhoso)

# with smbclient.open_file("\\\\192.168.20.6\\icommgroup\\Pablo\\dois\\bola.txt", mode="r") as fd:
#     response = fd.read()
#     print(response)
#
#
# arquivo = open('C:\\Users\\pablo.lucena\\Documents\\projeto\\teste\\Jhony.txt', 'w')
# arquivo.write(response)
# arquivo.close()

# pt1 fim


# pt2 Esse trecho do codigo checka se um caminho no servidor esta ativo, testando assim, se a conexão esta bem sussedida
# smbclient._os.('\\\\192.168.20.6\\icommgroup\\Pablo\\dois\\aa048A7560.CR2', 'r')

# if smbclient._os.open_file('\\\\192.168.20.6\\icommgroup\\Pablo\\dois\\048A7560.CR2', 'r'):
#     print('Endereço Valido')
# else:
#     print('Endereço Invalido')

# smbclient.shutil.copyfile("\\\\192.168.20.6\\icommgroup\\Pablo\\dois", "\\\\192.168.20.6\\icommgroup\\Pablo\\tres")

# smbprotocol.get("\\\\192.168.20.6\\icommgroup\\Pablo\\dois\\bola.txt")

# print(a)

# pt2 fim

# pt3 Tentativa de baixar o arquivo do servidor como se fosse da internet


# EXERCICIO DE MANIPULAÇÃO DE ARQUIVO
#
# file = smbclient.open_file("\\\\192.168.20.6\\icommgroup\\Pablo\\dois\\bola.txt", mode="w+")
# file.write("BlopaBlapo")
# file.seek(0)
# print(file.read())

# TESTE DE WALK

# ualque = smbclient.walk("\\\\192.168.20.6\\icommgroup\\Pablo")
#
# passos = []
# for step in ualque:
#     print(step)
#     passos.append(step)
#
# print("="*30)
# for passo in passos:
#     print(passo)

# FIM FUNCOES

# INICIO GUI

from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk


def take():
    secao = text_area.get()
    if check_paths(list_way(secao), 't')[1]:
        feedback['text'] = check_paths(list_way(secao), 't')[0]
        creates_paths(list_way(secao), 't')
        feedback['text'] = copy_refs(list_way(secao), 't')

    else:
        feedback['text'] = check_paths(list_way(secao), 't')[0]


def drop():
    secao = text_area.get()
    if check_paths(list_way(secao), 'd')[1]:
        feedback['text'] = check_paths(list_way(secao), 'd')[0]
        creates_paths(list_way(secao), 'd')
        feedback['text'] = copy_refs(list_way(secao), 'd')
    else:
        feedback['text'] = check_paths(list_way(secao), 'd')[0]


janela = ThemedTk('arc')
janela.get_themes()
janela.set_theme('arc')
janela.geometry('530x110')
janela.title('Gerenciador de Pastas')
janela.wm_iconbitmap('favicon.ico')




container1 = ttk.Frame(janela)
container1.pack()

container2 = ttk.Frame(janela)
container2.pack()

container3 = ttk.Frame(janela, borderwidth=5)
container3.pack()

container4 = ttk.Frame(janela)
container4.pack()

enunciated = ttk.Label(container1, text='Cole os caminhos')
enunciated.pack()

text_area = ttk.Entry(container2, width='70')
text_area.pack()

take_button = ttk.Button(container3, text='Pegar', width=32, command=take)
take_button.pack(side=LEFT)

drop_button = ttk.Button(container3, text='Jogar', width=32, command=drop)
drop_button.pack(side=LEFT)

feedback = ttk.Label(container4, text='')
feedback.pack()

janela.mainloop()


# FIM GUI