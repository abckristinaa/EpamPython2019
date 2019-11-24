from Bio import SeqIO


def translate_from_dna_to_rna(dna):
    # returns a generator object with two values:
    # a sequence's ID and rna

    with open(dna) as f:
        for line in SeqIO.parse(f, "fasta"):
            rna = line.seq.transcribe()
            yield (line.id, rna)


dna = 'dna.fasta'
for ID, rna in translate_from_dna_to_rna(dna):
    print(f"{ID}:")
    print(rna)
