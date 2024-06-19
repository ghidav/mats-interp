import numpy as np
import numpy.random as random

all_species = ['grimpus', 'lorpus', 'wumpus', 'zumpus', 'sterpus', 'numpus', 'jompus', 'brimpus', 'yumpus', 'tumpus', 'dumpus', 'vumpus', 'rompus', 'lempus', 'gorpus', 'shumpus', 'impus']
all_attributes = ['fast', 'luminous', 'tall', 'large', 'heavy', 'blonde', 'crazy', 'hungry', 'happy']
all_subjects = ['Grom', 'Wren', 'Trux', 'Jinx', 'Rast']

def s2a(x, y):
        if random.rand() > 0.5:
            return f"{x}es are {y}.".capitalize()
        else:
            return f"Each {x} is {y}.".capitalize()
        
def s2s(x, y):
    if random.rand() > 0.5:
        return f"{x}es are {y}es.".capitalize()
    else:
        return f"Each {x} is a {y}.".capitalize()

def generate_1hop(p=0.5):
    A, B, C = random.choice(np.arange(len(all_species)), size=3, replace=False)
    a, b, c = random.choice(np.arange(len(all_attributes)), size=3, replace=False)
    X = random.choice(np.arange(len(all_subjects)), size=1)[0]

    A = all_species[A]
    B = all_species[B]
    C = all_species[C]

    a = all_attributes[a]
    b = all_attributes[b]
    c = all_attributes[c]

    X = all_subjects[X]

    clues = []
    x_clues = []

    a_1 = a
    a_2 = "not " + a
    label = "Yes"

    if random.rand() > p:
        a_1, a_2 = a_2, a_1
        label = "No"

    if random.rand() > 0.5: b = "not " + b
    if random.rand() > 0.5: c = "not " + c

    clues.append(s2a(C, b))
    clues.append(s2s(B, C))
    clues.append(s2a(A, a_1))
    clues.append(s2a(B, a_2))
    clues.append(s2a(A, c))

    x_clues.append(f"{X} is a {A}.")
    x_clues.append(f"{X} is a {C}.")

    cot = [
        f"{X} is a {A}.",
        s2a(A, a_1),
        f"{X} is {a_1}."
    ]

    context = ' '.join(random.choice(clues, len(clues), replace=False))
    context += ' ' + ' '.join(random.choice(x_clues, len(x_clues), replace=False))

    question = f"Is {X} {a}?"

    return context, question, label, cot

def generate_2hops(p=0.5):
    A, B, C, D = random.choice(np.arange(len(all_species)), size=4, replace=False)
    a, b, c = random.choice(np.arange(len(all_attributes)), size=3, replace=False)
    X = random.choice(np.arange(len(all_subjects)), size=1)[0]

    A = all_species[A]
    B = all_species[B]
    C = all_species[C]
    D = all_species[D]

    a = all_attributes[a]
    b = all_attributes[b]
    c = all_attributes[c]

    X = all_subjects[X]

    clues = []
    x_clues = []

    a_1 = a
    a_2 = "not " + a
    label = "Yes"

    if random.rand() > p:
        a_1, a_2 = a_2, a_1
        label = "No"

    if random.rand() > 0.5: b = "not " + b
    if random.rand() > 0.5: c = "not " + c

    clues.append(s2a(A, b))
    clues.append(s2s(A, B))
    clues.append(s2s(D, C))
    clues.append(s2a(B, a_1))
    clues.append(s2a(D, a_2))
    clues.append(s2a(D, b))
    clues.append(s2a(B, c))

    x_clues.append(f"{X} is a {A}.")
    x_clues.append(f"{X} is a {C}.")

    cot = [
        f"{X} is a {A}.",
        s2s(A, B),
        f"{X} is a {B}.",
        s2a(B, a_1),
        f"{X} is {a_1}."
    ]

    context = ' '.join(random.choice(clues, len(clues), replace=False))
    context += ' ' + ' '.join(random.choice(x_clues, len(x_clues), replace=False))

    question = f"Is {X} {a}?"

    return context, question, label, cot

def generate_3hops(p=0.5):
    A, B, C, D, E, F = random.choice(np.arange(len(all_species)), size=6, replace=False)
    a, b, c, d = random.choice(np.arange(len(all_attributes)), size=4, replace=False)
    X = random.choice(np.arange(len(all_subjects)), size=1)[0]

    A = all_species[A]
    B = all_species[B]
    C = all_species[C]
    D = all_species[D]
    E = all_species[E]
    F = all_species[F]

    a = all_attributes[a]
    b = all_attributes[b]
    c = all_attributes[c]
    d = all_attributes[d]

    X = all_subjects[X]

    clues = []
    x_clues = []

    a_1 = a
    a_2 = "not " + a
    label = "Yes"

    if random.rand() > p:
        a_1, a_2 = a_2, a_1
        label = "No"

    if random.rand() > 0.5: b = "not " + b
    if random.rand() > 0.5: c = "not " + c
    if random.rand() > 0.5: d = "not " + d

    clues.append(s2s(A, C))
    clues.append(s2s(C, D))
    clues.append(s2s(B, F))
    clues.append(s2s(E, B))
    clues.append(s2a(A, b))
    clues.append(s2a(C, c))
    clues.append(s2a(D, a_1))
    clues.append(s2a(E, a_2))
    clues.append(s2a(F, d))
    clues.append(s2a(E, c))

    x_clues.append(f"{X} is a {A}.")
    x_clues.append(f"{X} is a {B}.")

    cot = [
        f"{X} is a {A}.",
        s2s(A, C),
        f"{X} is a {C}.",
        s2s(C, D),
        f"{X} is a {D}.",
        s2a(D, a_1),
        f"{X} is {a_1}."
    ]

    context = ' '.join(random.choice(clues, len(clues), replace=False))
    context += ' ' + ' '.join(random.choice(x_clues, len(x_clues), replace=False))

    question = f"Is {X} {a}?"

    return context, question, label, cot

def prepare_prompt(context, question, label, cot, solved=True, with_cot=True):
    prompt = context + '\n\nQuestion: ' + question + '\n'
    if with_cot:
        prompt += "Think step by step.\n"
    else:
        prompt += "Answer Yes or No.\n"
    if solved:
        if with_cot:
            for i, step in enumerate(cot):
                prompt += f"\n({i+1}) {step}"

        prompt += f"\nAnswer: {label}"
    return prompt

def few_shot_example(n_hops, n_shots, p=0.5, with_cot=True):
    prompt = "Answer to the following question as shown in the following examples.\n"
    for i in range(n_shots): 
        if n_hops == 1:
            c, q, l, cot = generate_1hop(p=p)
        elif n_hops == 2:
            c, q, l, cot = generate_2hops(p=p)
        elif n_hops == 3:
            c, q, l, cot = generate_3hops(p=p)
        else:
            raise NotImplementedError(f"{n_hops} hops is not implemented yet.")
        
        prompt += prepare_prompt(c, q, l, cot, with_cot=with_cot) + "\n\n\n"

    if n_hops == 1:
        c, q, l, cot = generate_1hop()
    elif n_hops == 2:
        c, q, l, cot = generate_2hops()
    elif n_hops == 3:
        c, q, l, cot = generate_3hops()

    prompt += prepare_prompt(c, q, l, cot, solved=False, with_cot=with_cot) 
    return prompt, (c, q, l, cot)