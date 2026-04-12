import rdkit.Chem as chem

#defining globally:
global_subscript_map = str.maketrans( {
        '₀': '0',
        '₁': '1',
        '₂': '2',
        '₃': '3',
        '₄': '4',
        '₅': '5',
        '₆': '6',
        '₇': '7',
        '₈': '8',
        '₉': '9'
    })

global_punctuation = '''!-{};:'"\,<>./?@#$%^&*_~'''

global_elements = set([
    'H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne',
    'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar',
    'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe',
    'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As',
    'Se', 'Br', 'Kr', 'Rb', 'Sr', 'Y', 'Zr',
    'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag',
    'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe',
    'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 
    'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho',
    'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta', 'W',
    'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 
    'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn',
    'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu',
    'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md',
    'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs',
    'Mt', 'Ds', 'Rg', 'Cn', 'Nh', 'Fl', 'Mc',
    'Lv', 'Ts', 'Og', 'D' # Deuterium, often represented as D in chemical formulas
])


def clean(query:str) -> str:
    
    subscript_map = global_subscript_map
    punctuation = global_punctuation

    query = query.translate(subscript_map)
    if any(char in query for char in punctuation):
        query = query.replace(char, '')

    return ' '.join(query.strip().split())

def detect_types(query:str) -> str:
    elements = global_elements

    if chem.MolFromSmiles(query) is not None:
        return 'smiles'
    
    elif any(element in query for element in elements):
        return 'molecular_formula'

    else:
        return 'iupac_name'


def normalise(query: str) -> dict:
    cleaned = clean(query)
    detected_type = detect_types(cleaned)
    return {"cleaned": cleaned, "type": detected_type}


if __name__ == "__main__":
    while True:
        enter = input("Enter a query: ")
        print('--- Testing... ---\n\n')
        print(f"Cleaned Query: {clean(enter)}\n")
        print(f"Detected Type: {detect_types(clean(enter))}\n")
        print(f'normalise output: {normalise(enter)}')