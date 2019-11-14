""""

Задание 1

0) Повторение понятий из биологии (ДНК, РНК, нуклеотид, протеин, кодон)

1) Построение статистики по входящим в последовательность ДНК нуклеотидам 
для каждого гена (например: [A - 46, C - 66, G - 23, T - 34])

2) Перевод последовательности ДНК в РНК (окей, Гугл)

3) Перевод последовательности РНК в протеин*


*В папке files вы найдете файл rna_codon_table.txt - 
в нем содержится таблица переводов кодонов РНК в аминокислоту, 
составляющую часть полипептидной цепи белка.


Вход: файл dna.fasta с n-количеством генов

Выход - 3 файла:
 - статистика по количеству нуклеотидов в ДНК
 - последовательность РНК для каждого гена
 - последовательность кодонов для каждого гена

 ** Если вы умеете в matplotlib/seaborn или еще что, 
 welcome за дополнительными баллами за
 гистограммы по нуклеотидной статистике.
 (Не забудьте подписать оси)

P.S. За незакрытый файловый дескриптор - караем штрафным дезе.

"""

# read the file dna.fasta
dna = open(r'files/dna.fasta')


def translate_from_dna_to_rna(dna):
    # writes rna chains for each gene in file
    # and returns a list of rna chains
    rna = []
    dna.seek(0)
    with open(r'files/2_rna.txt', 'w') as wf:
        for line in dna:
            if line[0] != ">":
                s = line.replace("T", "U").rstrip()
                wf.write(s + "\n")
                rna.append(s)
            else:
                wf.write(line)
                rna.append("sep")
    rna = "".join(rna).split("sep")[1:]
    return rna


def count_nucleotides(dna):
    # creates a file with number of repetitions
    # for each nucleotides in gene
    storage = {}
    file_out = r'files/1_count_nucl.txt'
    with open(file_out, 'w') as wf:
        for index, line in enumerate(dna):
            if line[0] == ">":
                wf.write("".join([f"{key} - {value}, "
                                  for key, value in storage.items()])[:-2] + "\n" if index else "")
                storage = {}
            else:
                for i in sorted(line.strip()):
                    storage[i] = storage.get(i, 0) + 1
        wf.write("".join([f"{key} - {value}, "
                          for key, value in storage.items()])[:-2])
    return


def translate_rna_to_protein(rna):

    # convert codon table to a dictionary:
    keys, values = [], []
    with open(r'files/rna_codon_table.txt') as rf:
        for line in rf:
            for index, k in enumerate(line.rstrip().split()):
                keys.append(k) if index % 2 == 0 else values.append(k)
    dict_table = dict(zip(keys, values))

    # reverse rna chains,
    # divide the chains into triplets and convert to protein
    # returns a list of proteins
    with open(r'files/3_protein.txt', 'w') as wf:
        protein = []
        for chain in rna:
            chain = chain[::-1]
            temp = []
            for index, i in enumerate(chain[:(len(chain) // 3 * 3):3]):
                triplet = chain[index * 3: index * 3 + 3]
                temp.append(dict_table[triplet])
            protein.append("".join(temp))
            wf.write("".join(temp) + "\n")
    return protein


count_nucleotides(dna)
rna = translate_from_dna_to_rna(dna)
dna.close()
translate_rna_to_protein(rna)
