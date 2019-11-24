from Bio import SeqIO


def count_nucleotides(dna):
    with open(dna) as rf:
        count_stats = r'EpamPython2019/01-Data-Structures/hw/carrots/files/count_nucl.txt'
        with open(count_stats, 'w') as wf:
            for line in SeqIO.parse(rf, "fasta"):
                storage = {}
                for i in sorted(str(line.seq)):
                    storage[i] = storage.get(i, 0) + 1
                print(f"{line.id}:", file=wf)
                print(*[f"{key} - {value}" for key, value in storage.items()], sep=", ", file=wf)
        return count_stats


dna = r'EpamPython2019/01-Data-Structures/hw/carrots/files/dna.fasta'

count_nucleotides(dna)
