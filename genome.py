import random

genome = "gggggggggggggggggggggggg"

def translate(genome):
    # turns (translates) 21 character string into 7 parameters based on each codon.
    codons = []
    r_codon = genome[0:3]
    g_codon = genome[3:6]
    b_codon = genome[6:9]
    size_codon = genome[9:12]
    speed_codon = genome[12:15]
    reproduction_rate_codon = genome[15:18]
    n_offspring_codon = genome[18:21]
    run_variance_codon = genome[21:24] # variance in direction running away from the predator

    # print(size_codon, speed_codon, r_codon, g_codon, b_codon, reproduction_rate_codon, n_offspring_codon)
    return (color_from_codons(codon_to_number(r_codon), codon_to_number(g_codon), codon_to_number(b_codon)),
          codon_to_number(size_codon),
          codon_to_number(speed_codon),
          codon_to_number(reproduction_rate_codon) * 10/63 + 10, # from 10-20 seconds per reproduction?
          codon_to_number(n_offspring_codon) * 3//63,
          codon_to_number(run_variance_codon) * 90/63 - 45 # convert to range within 90 degrees
          )

def codon_to_number(codon):
    number_str = ""
    convert = {"a":"0", "c":"1", "g":"2", "t":"3"}
    for letter in codon:
        number_str += convert[letter]
    # print(number_str)
    # base four covers 0-63
    number = int(number_str,4)
    return number

def color_from_codons(r_number, g_number, b_number):
    # converts 3 codon number inputs into 3 rgb color values.
    # each value can go from 0-252, so not quite full range of rgb is possible
    r = r_number * 4
    g = g_number * 4
    b = b_number * 4
    # print(r, g, b)
    return r, g, b

def transcribe(parent_genome):
    # transcribes the parent genome with mutations, returning a new genome for a given offspring
    offspring_genome = ""
    nucleotides = ["a","c","g","t"]
    for n in range(0, 24):
        rand_int = random.randrange(0, 10)
        if rand_int < 1:
            # mutate
            offspring_genome += random.choice(nucleotides)
        else:
            # pass through nucleotide as is
            offspring_genome += parent_genome[n]
    return(offspring_genome)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(transcribe(genome))
    print(translate(genome))
