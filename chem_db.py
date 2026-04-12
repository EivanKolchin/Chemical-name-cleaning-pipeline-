"""
build_db_hardcoded.py
Builds a local PubChem-style SQLite database with all data hardcoded.
Run this once to generate pubchem_local.db, then use db_query.py to query it.
"""
import sqlite3

DB_PATH = "pubchem_local.db"

# Schema
SCHEMA = """
CREATE TABLE IF NOT EXISTS compounds (
    cid              INTEGER PRIMARY KEY,
    iupac_name       TEXT,
    molecular_formula TEXT,
    molecular_weight  REAL,
    inchi            TEXT,
    inchikey         TEXT UNIQUE,
    isomeric_smiles  TEXT,
    canonical_smiles TEXT,
    xlogp            REAL,
    hbond_donors     INTEGER,
    hbond_acceptors  INTEGER,
    rotatable_bonds  INTEGER,
    heavy_atom_count INTEGER,
    charge           INTEGER
);

CREATE TABLE IF NOT EXISTS synonyms (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    cid  INTEGER NOT NULL REFERENCES compounds(cid),
    name TEXT NOT NULL,
    UNIQUE(cid, name)
);

CREATE TABLE IF NOT EXISTS name_index (
    name_lower TEXT NOT NULL,
    cid        INTEGER NOT NULL REFERENCES compounds(cid),
    PRIMARY KEY (name_lower, cid)
);

CREATE INDEX IF NOT EXISTS idx_inchikey   ON compounds(inchikey);
CREATE INDEX IF NOT EXISTS idx_formula    ON compounds(molecular_formula);
CREATE INDEX IF NOT EXISTS idx_name_lower ON name_index(name_lower);
CREATE INDEX IF NOT EXISTS idx_syn_cid    ON synonyms(cid);
"""

# fmt: (cid, iupac_name, formula, mw, inchi, inchikey, iso_smiles, can_smiles, xlogp, hbd, hba, rb, hac, charge)
COMPOUNDS = [
    (702,  "ethanol", "C2H6O", 46.068,
     "InChI=1S/C2H6O/c1-2-3/h3H,2H2,1H3", "LFQSCWFLJHTTHZ-UHFFFAOYSA-N",
     "CCO", "CCO", -0.1, 1, 1, 1, 3, 0),

    (2244, "2-(acetyloxy)benzoic acid", "C9H8O4", 180.158,
     "InChI=1S/C9H8O4/c1-6(10)13-8-5-3-2-4-7(8)9(11)12/h2-5H,1H3,(H,11,12)",
     "BSYNRYMUTXBXSQ-UHFFFAOYSA-N",
     "CC(=O)Oc1ccccc1C(=O)O", "CC(=O)Oc1ccccc1C(=O)O", 1.2, 1, 4, 3, 13, 0),

    (1983, "N-(4-hydroxyphenyl)acetamide", "C8H9NO2", 151.163,
     "InChI=1S/C8H9NO2/c1-6(10)9-7-2-4-8(11)5-3-7/h2-5,11H,1H3,(H,9,10)",
     "RZVAJINKPMORJF-UHFFFAOYSA-N",
     "CC(=O)Nc1ccc(O)cc1", "CC(=O)Nc1ccc(O)cc1", 0.5, 2, 2, 2, 11, 0),

    (176,  "acetic acid", "C2H4O2", 60.052,
     "InChI=1S/C2H4O2/c1-2(3)4/h1H3,(H,3,4)", "QTBSBXVTEAMEQO-UHFFFAOYSA-N",
     "CC(=O)O", "CC(=O)O", -0.2, 1, 2, 1, 4, 0),

    (2519, "1,3,7-trimethylpurine-2,6(1H,3H)-dione", "C8H10N4O2", 194.194,
     "InChI=1S/C8H10N4O2/c1-10-4-9-6-5(10)7(13)11(2)8(14)12(6)3/h4H,1-3H3",
     "RYYVLZVUVIJVGH-UHFFFAOYSA-N",
     "Cn1cnc2c1c(=O)n(C)c(=O)n2C", "Cn1cnc2c1c(=O)n(C)c(=O)n2C", -0.1, 0, 3, 0, 14, 0),

    (3672, "2-[4-(2-methylpropyl)phenyl]propanoic acid", "C13H18O2", 206.281,
     "InChI=1S/C13H18O2/c1-9(2)8-10-4-6-11(7-5-10)12(3)13(14)15/h4-7,9,12H,8H2,1-3H3,(H,14,15)",
     "HEFNNWSXXWATRW-UHFFFAOYSA-N",
     "CC(Cc1ccc(cc1)C(C)C(=O)O)C", "CC(Cc1ccc(cc1)C(C)C(=O)O)C", 3.5, 1, 2, 4, 15, 0),

    (5793, "(3R,4S,5S,6R)-6-(hydroxymethyl)oxane-2,3,4,5-tetrol", "C6H12O6", 180.156,
     "InChI=1S/C6H12O6/c7-1-2-3(8)4(9)5(10)6(11)12-2/h2-11H,1H2/t2-,3-,4+,5-,6+/m1/s1",
     "WQZGKKKJIJFFOK-GASJEMHNSA-N",
     "[C@@H]1([C@H]([C@@H]([C@H](C(O1)CO)O)O)O)O",
     "C(C1C(C(C(C(O1)O)O)O)O)O", -2.8, 5, 6, 1, 12, 0),

    (5234, "sodium chloride", "ClNa", 58.44,
     "InChI=1S/ClH.Na/h1H;/q;+1/p-1", "FAPWRFPIFSIZLT-UHFFFAOYSA-M",
     "[Na+].[Cl-]", "[Na+].[Cl-]", None, 0, 1, 0, 2, 0),

    (241,  "benzene", "C6H6", 78.112,
     "InChI=1S/C6H6/c1-2-4-6-5-3-1/h1-6H", "UHOVQNZJYSORNB-UHFFFAOYSA-N",
     "c1ccccc1", "c1ccccc1", 2.1, 0, 0, 0, 6, 0),

    (887,  "methanol", "CH4O", 32.042,
     "InChI=1S/CH4O/c1-2/h2H,1H3", "OKKJLVBELUTLKV-UHFFFAOYSA-N",
     "CO", "CO", -0.7, 1, 1, 1, 2, 0),

    (180,  "propan-2-one", "C3H6O", 58.079,
     "InChI=1S/C3H6O/c1-3(2)4/h1-2H3", "CSCPPACGZOOCGX-UHFFFAOYSA-N",
     "CC(C)=O", "CC(C)=O", -0.2, 0, 1, 2, 4, 0),

    (1140, "methylbenzene", "C7H8", 92.139,
     "InChI=1S/C7H8/c1-7-5-3-2-4-6-7/h2-6H,1H3", "YXFVVABEGXRONW-UHFFFAOYSA-N",
     "Cc1ccccc1", "Cc1ccccc1", 2.7, 0, 0, 1, 7, 0),

    (1118, "sulfuric acid", "H2O4S", 98.072,
     "InChI=1S/H2O4S/c1-5(2,3)4/h(H2,1,2,3,4)", "QAOWNCQODCNURD-UHFFFAOYSA-N",
     "OS(=O)(=O)O", "OS(=O)(=O)O", -1.0, 2, 4, 0, 5, 0),

    (785,  "benzene-1,4-diol", "C6H6O2", 110.111,
     "InChI=1S/C6H6O2/c7-5-1-2-6(8)4-3-5/h1-4,7-8H", "QIGBRXMKCJKVMJ-UHFFFAOYSA-N",
     "Oc1ccc(O)cc1", "Oc1ccc(O)cc1", 0.6, 2, 2, 0, 8, 0),

    (753,  "propane-1,2,3-triol", "C3H8O3", 92.094,
     "InChI=1S/C3H8O3/c4-1-3(6)2-5/h3-6H,1-2H2", "PEDCQBHIVMGVHV-UHFFFAOYSA-N",
     "OCC(O)CO", "OCC(O)CO", -1.8, 3, 3, 2, 6, 0),

    (996,  "phenol", "C6H6O", 94.111,
     "InChI=1S/C6H6O/c7-6-4-2-1-3-5-6/h1-5,7H", "ISWSIDIOOBJBQZ-UHFFFAOYSA-N",
     "Oc1ccccc1", "Oc1ccccc1", 1.5, 1, 1, 0, 7, 0),

    (1176, "urea", "CH4N2O", 60.056,
     "InChI=1S/CH4N2O/c2-1(3)4/h(H4,2,3,4)", "XSQUKJJJFZCRTK-UHFFFAOYSA-N",
     "NC(N)=O", "NC(N)=O", -1.5, 2, 1, 0, 4, 0),

    (311,  "2-hydroxypropane-1,2,3-tricarboxylic acid", "C6H8O7", 192.124,
     "InChI=1S/C6H8O7/c7-3(8)1-6(13,5(11)12)2-4(9)10/h13H,1-2H2,(H,7,8)(H,9,10)(H,11,12)",
     "KRKNYBCHXYNGOX-UHFFFAOYSA-N",
     "OC(CC(=O)O)(CC(=O)O)C(=O)O", "OC(CC(=O)O)(CC(=O)O)C(=O)O", -1.6, 4, 7, 5, 13, 0),

    (6212, "trichloromethane", "CHCl3", 119.369,
     "InChI=1S/CHCl3/c2-1(3)4/h1H", "HEDRZPFGACZZDS-UHFFFAOYSA-N",
     "ClC(Cl)Cl", "ClC(Cl)Cl", 2.0, 0, 0, 0, 4, 0),

    (712,  "formaldehyde", "CH2O", 30.026,
     "InChI=1S/CH2O/c1-2/h1H2", "WSFSSNUMVMOOMR-UHFFFAOYSA-N",
     "C=O", "C=O", 0.4, 0, 1, 1, 2, 0),

    (784,  "hydrogen peroxide", "H2O2", 34.015,
     "InChI=1S/H2O2/c1-2/h1-2H", "MHAJPDPJQMAIIY-UHFFFAOYSA-N",
     "OO", "OO", -1.4, 2, 2, 1, 2, 0),

    (222,  "azane", "H3N", 17.031,
     "InChI=1S/H3N/h1H3", "NLXLAEXVIDQMFP-UHFFFAOYSA-N",
     "N", "N", -3.2, 1, 1, 0, 1, 0),

    (284,  "formic acid", "CH2O2", 46.025,
     "InChI=1S/CH2O2/c2-1-3/h1H,(H,2,3)", "BDAGIHXWWSANSR-UHFFFAOYSA-N",
     "OC=O", "OC=O", -0.5, 1, 2, 1, 3, 0),

    (338,  "2-hydroxybenzoic acid", "C7H6O3", 138.121,
     "InChI=1S/C7H6O3/c8-6-4-2-1-3-5(6)7(9)10/h1-4,8H,(H,9,10)",
     "YGSDEFSMJLZEOE-UHFFFAOYSA-N",
     "OC(=O)c1ccccc1O", "OC(=O)c1ccccc1O", 2.3, 2, 3, 1, 10, 0),

    (174,  "ethane-1,2-diol", "C2H6O2", 62.068,
     "InChI=1S/C2H6O2/c3-1-2-4/h3-4H,1-2H2", "LYCAIKOWRPUZTN-UHFFFAOYSA-N",
     "OCCO", "OCCO", -1.4, 2, 2, 1, 4, 0),

    # Extra compounds not in queries.csv
    (3383, "7-chloro-1-methyl-5-phenyl-3H-1,4-benzodiazepin-2-one", "C16H13ClN2O", 284.74,
     "InChI=1S/C16H13ClN2O/c1-19-14-8-7-12(17)9-13(14)16(18-10-15(19)20)11-5-3-2-4-6-11/h2-9H,10H2,1H3",
     "AAOVKJBEBIDNHE-UHFFFAOYSA-N",
     "CN1C(=O)CN=C(c2ccccc2)c2cc(Cl)ccc21",
     "CN1C(=O)CN=C(c2ccccc2)c2cc(Cl)ccc21", 2.9, 0, 3, 3, 20, 0),

    (5090, "4-(2-aminoethyl)benzene-1,2-diol", "C8H11NO2", 153.179,
     "InChI=1S/C8H11NO2/c9-4-3-6-1-2-7(10)8(11)5-6/h1-2,5,10-11H,3-4,9H2",
     "VYFYYTLLBUKUHU-UHFFFAOYSA-N",
     "NCCc1ccc(O)c(O)c1", "NCCc1ccc(O)c(O)c1", -1.6, 3, 3, 3, 11, 0),

    (5842, "(3S,4R,5R)-6-(hydroxymethyl)oxane-2,3,4,5-tetrol", "C6H12O6", 180.156,
     "InChI=1S/C6H12O6/c7-1-2-3(8)4(9)5(10)6(11)12-2/h2-11H,1H2/t2-,3-,4-,5+,6-/m1/s1",
     "LKDRXBCSQODPBY-AMVSKUEXSA-N",
     "OC[C@@H]1OC(O)[C@H](O)[C@@H](O)[C@H]1O",
     "OCC1OC(O)C(O)C(O)C1O", -3.0, 5, 6, 1, 12, 0),

    (2723949, "beta-D-fructose", "C12H22O11", 342.297,
     "InChI=1S/C12H22O11/c13-1-4(16)7(19)10(22)11(23-8(4)17)6(18)3(15)2(14)5(20)9(11)21/h2-10,13-22H,1H2",
     "CZMRCDWAGMRECN-UGDNZRGBSA-N",
     "OC[C@H]1O[C@@](CO)(O)[C@@H](O)[C@@H]1O",
     "OCC1OC(O)(CO)C(O)C1O", -3.7, 8, 11, 7, 23, 0),

    (5988, "(3S,8S,9S,10R,13R,14S,17R)-10,13-dimethyl-17-[(2R)-6-methylheptan-2-yl]-2,3,4,7,8,9,10,11,12,13,14,15,16,17-tetradecahydro-1H-cyclopenta[a]phenanthren-3-ol",
     "C27H46O", 386.654,
     "InChI=1S/C27H46O/c1-18(2)7-6-8-19(3)23-11-12-24-22-10-9-20-17-21(28)13-15-26(20,4)25(22)14-16-27(23,24)5/h9,18-19,21-25,28H,6-8,10-17H2,1-5H3/t19-,21+,22+,23-,24+,25+,26+,27-/m1/s1",
     "HVYWMOMLDIMFJA-DPAQBDIFSA-N",
     "[C@@H]1(CC[C@@H]2[C@@]1(CC[C@H]3[C@H]2CC=C4[C@@]3(CC[C@@H](C4)O)C)C)[C@H](C)CCCC(C)C",
     "CC(C)CCCC(C)C1CCC2C1(CCC3C2CC=C4C3(CCC(C4)O)C)C", 7.3, 1, 1, 5, 28, 0),

    (5291, "4-(1-hydroxy-2-(methylamino)ethyl)benzene-1,2-diol", "C9H13NO3", 183.204,
     "InChI=1S/C9H13NO3/c1-10-5-9(13)7-3-6(11)2-4-8(7)12/h2-4,9-13H,5H2,1H3",
     "UCTWMZBAZVARLO-UHFFFAOYSA-N",
     "CNCCc1ccc(O)c(O)c1", "CNCCc1ccc(O)c(O)c1", -1.2, 3, 3, 4, 13, 0),

    (4946, "(2S,5R,6R)-3,3-dimethyl-7-oxo-6-[(2-phenylacetyl)amino]-4-thia-1-azabicyclo[3.2.0]heptane-2-carboxylic acid",
     "C16H18N2O4S", 334.39,
     "InChI=1S/C16H18N2O4S/c1-16(2)11(15(21)22)18-13(20)10(14(18)23-16)17-12(19)8-9-6-4-3-5-7-9/h3-7,10-11H,8H2,1-2H3,(H,17,19)(H,21,22)/t10-,11+,14-/m1/s1",
     "JGSARCRWWKOVFU-XIRDDKMYSA-N",
     "CC1(C)SC2C(NC(=O)Cc3ccccc3)C(=O)N2C1C(=O)O",
     "CC1(C)SC2C(NC(=O)Cc3ccccc3)C(=O)N2C1C(=O)O", 1.8, 2, 6, 4, 23, 0),

    (3423265, "(S)-2-(6-methoxynaphthalen-2-yl)propanoic acid", "C14H14O3", 230.259,
     "InChI=1S/C14H14O3/c1-9(14(15)16)10-3-4-12-8-13(17-2)6-5-11(12)7-10/h3-9H,1-2H3,(H,15,16)/t9-/m0/s1",
     "CMWTZPSULFXXJA-VIFPVBQESA-N",
     "COc1ccc2cc([C@@H](C)C(=O)O)ccc2c1",
     "COc1ccc2cc(C(C)C(=O)O)ccc2c1", 3.2, 1, 3, 3, 17, 0),

    (2723872, "2-(diethylamino)-N-(2,6-dimethylphenyl)acetamide", "C14H22N2O", 234.338,
     "InChI=1S/C14H22N2O/c1-5-16(6-2)10-13(17)15-14-11(3)8-7-9-12(14)4/h7-9H,5-6,10H2,1-4H3,(H,15,17)",
     "NNJVILVZNWIQJA-UHFFFAOYSA-N",
     "CCN(CC)CC(=O)Nc1c(C)cccc1C",
     "CCN(CC)CC(=O)Nc1c(C)cccc1C", 2.3, 1, 2, 6, 17, 0),

    (6918289, "3-(diaminomethylidene)-1,1-dimethylguanidine", "C4H11N5", 129.164,
     "InChI=1S/C4H11N5/c1-9(2)4(7)8-3(5)6/h(H5,5,6,7,8)/p+1",
     "XZWYZXLIPXDOLR-UHFFFAOYSA-O",
     "CN(C)C(=N)NC(=N)N", "CN(C)C(=N)NC(=N)N", -2.6, 3, 4, 3, 9, 1),

    (4583, "4-hydroxy-3-(3-oxo-1-phenylbutyl)-2H-chromen-2-one", "C19H16O4", 312.33,
     "InChI=1S/C19H16O4/c1-12(20)11-15(13-7-3-2-4-8-13)17-18(21)14-9-5-6-10-16(14)23-19(17)22/h2-10,15,21H,11H2,1H3",
     "PJVWKTKQMONHTI-UHFFFAOYSA-N",
     "CC(=O)CC(c1ccccc1)c1c(O)c2ccccc2oc1=O",
     "CC(=O)CC(c1ccccc1)c1c(O)c2ccccc2oc1=O", 2.7, 1, 4, 5, 23, 0),

    (5755, "[(4R,4aR,7S,7aR,12bS)-9-methoxy-3-methyl-2,3,4,4a,7,7a-hexahydro-1H-4,12-methanobenzofuro[3,2-e]isoquinolin-7-yl] acetate",
     "C19H21NO4", 331.375,
     "InChI=1S/C19H21NO4/c1-10-8-18-11-4-5-12(22-3)16(11)24-17(18)13(21-10)6-7-19(18)9-14(20)15(19)23-2/h4-5,10,13-15,17H,6-9H2,1-3H3/t10-,13+,14-,15-,17-,18-,19+/m0/s1",
     "BQJCRHHNABKAKU-KBQPJGBKSA-N",
     "CN1CC[C@]23[C@@H]1Cc1ccc(OC)c4c1[C@@H]2OC[C@]3(OC(C)=O)[C@H]4O",
     "CN1CCC23CC1c1ccc(OC)c4c1C2OCC3(OC(C)=O)C4O", 0.9, 1, 4, 2, 24, 0),

    (44390, "3-(1-methylpyrrolidin-2-yl)pyridine", "C10H14N2", 162.231,
     "InChI=1S/C10H14N2/c1-12-7-3-4-9(12)10-6-2-5-11-8-10/h2,5-6,8-9H,3-4,7H2,1H3",
     "SNICXCGAKADSCV-UHFFFAOYSA-N",
     "CN1CCC[C@H]1c1cccnc1", "CN1CCCC1c1cccnc1", 1.2, 0, 2, 1, 12, 0),
]

# Synonyms: (cid, [list of names])
SYNONYMS = {
    702:  ["ethanol","grain alcohol","ethyl alcohol","drinking alcohol",
           "absolute alcohol","EtOH","alcohol","hydroxyethane","spirit"],
    2244: ["aspirin","acetylsalicylic acid","2-acetoxybenzoic acid",
           "ASA","acetosalic acid","Aspro","Disprin","Bayer Aspirin",
           "2-(acetyloxy)benzoic acid"],
    1983: ["paracetamol","acetaminophen","4-hydroxyacetanilide",
           "4-acetamidophenol","Tylenol","Panadol","Calpol","APAP",
           "N-acetyl-p-aminophenol","p-acetamidophenol"],
    176:  ["acetic acid","ethanoic acid","vinegar acid","methanecarboxylic acid",
           "CH3COOH","glacial acetic acid","AcOH","ethylic acid"],
    2519: ["caffeine","1,3,7-trimethylxanthine","theine","methyltheobromine",
           "anhydrous caffeine","coffeine","guaranine","No-Doz"],
    3672: ["ibuprofen","2-(4-isobutylphenyl)propionic acid",
           "2-(4-isobutylphenyl)propanoic acid","Nurofen","Advil",
           "Brufen","Motrin","p-isobutylhydratropic acid"],
    5793: ["glucose","dextrose","d-glucose","blood sugar","grape sugar",
           "corn sugar","D-glucopyranose","C6H12O6"],
    5234: ["sodium chloride","table salt","NaCl","salt","halite",
           "rock salt","sea salt","saline","common salt"],
    241:  ["benzene","cyclohexatriene","benzol","phene","coal naphtha",
           "C6H6","annulene"],
    887:  ["methanol","methyl alcohol","wood alcohol","wood spirits",
           "carbinol","MeOH","wood naphtha","colonial spirit"],
    180:  ["acetone","propan-2-one","dimethyl ketone","2-propanone",
           "beta-ketopropane","propanone","dimethylformaldehyde","DMK"],
    1140: ["toluene","methylbenzene","phenylmethane","toluol",
           "methacide","monomethyl benzene","C7H8"],
    1118: ["sulfuric acid","sulphuric acid","oil of vitriol","dihydrogen sulfate",
           "H2SO4","battery acid","hydrogen sulfate","vitriol"],
    785:  ["hydroquinone","benzene-1,4-diol","1,4-dihydroxybenzene",
           "p-dihydroxybenzene","quinol","p-hydroquinone",
           "1,4-benzenediol","4-hydroxyphenol"],
    753:  ["glycerol","glycerin","glycerine","propane-1,2,3-triol",
           "1,2,3-propanetriol","glycyl alcohol","trihydroxypropane"],
    996:  ["phenol","carbolic acid","hydroxybenzene","benzenol",
           "phenic acid","phenyl alcohol","monohydroxybenzene"],
    1176: ["urea","carbamide","carbonyl diamide","diaminomethanal",
           "carbamide resin","ureaphil","CH4N2O"],
    311:  ["citric acid","2-hydroxypropane-1,2,3-tricarboxylic acid",
           "citrate","2-hydroxy-1,2,3-propanetricarboxylic acid","C6H8O7"],
    6212: ["chloroform","trichloromethane","TCM","methane trichloride",
           "CHCl3","methenyl trichloride","formyl trichloride"],
    712:  ["formaldehyde","methanal","formalin","formic aldehyde",
           "methyl aldehyde","oxomethane","CH2O"],
    784:  ["hydrogen peroxide","dihydrogen dioxide","oxydol","H2O2",
           "peroxide","hydroperoxide"],
    222:  ["ammonia","azane","hydrogen nitride","NH3","anhydrous ammonia",
           "spirit of hartshorn"],
    284:  ["formic acid","methanoic acid","hydrogen carboxylic acid",
           "ant acid","OC=O","aminic acid"],
    338:  ["salicylic acid","2-hydroxybenzoic acid","salicylate",
           "ortho-hydroxybenzoic acid","o-hydroxybenzoic acid","SAL"],
    174:  ["ethylene glycol","ethane-1,2-diol","monoethylene glycol",
           "antifreeze","1,2-ethanediol","glycol","MEG","OCCO"],
    # Extra compounds
    3383: ["diazepam","Valium","2-methylamino-5-chloro-2,3-dihydro-1,4-benzodiazepine",
           "Stesolid","Diazemuls","Apozepam"],
    5090: ["dopamine","4-(2-aminoethyl)benzene-1,2-diol","DA",
           "3-hydroxytyramine","3,4-dihydroxyphenethylamine","Intropin"],
    5842: ["fructose","D-fructose","levulose","fruit sugar",
           "laevulose","D-arabino-hexulose"],
    2723949: ["sucrose","table sugar","cane sugar","beet sugar",
              "sugar","saccharose","alpha-D-glucopyranosyl beta-D-fructofuranoside"],
    5988: ["cholesterol","cholesterin","5-cholesten-3beta-ol",
           "cholesteryl alcohol","NSC 8798"],
    5291: ["epinephrine","adrenaline","adrenalin","l-epinephrine",
           "(R)-adrenaline","Epipen","epinefrin"],
    4946: ["penicillin G","benzylpenicillin","benzylpenicillinic acid",
           "PenG","penicillin"],
    3423265: ["naproxen","(S)-naproxen","Naprosyn","Aleve",
              "2-(6-methoxynaphthalen-2-yl)propanoic acid","Anaprox"],
    2723872: ["lidocaine","lignocaine","Xylocaine","Xylotox",
              "2-(diethylamino)-N-(2,6-dimethylphenyl)acetamide"],
    6918289: ["metformin","dimethylbiguanide","Glucophage","Fortamet",
              "1,1-dimethylbiguanide","Glumetza"],
    4583: ["warfarin","coumadin","4-hydroxy-3-(3-oxo-1-phenylbutyl)-2H-chromen-2-one",
           "Jantoven","Panwarfin","rat poison"],
    5755: ["morphine","MS Contin","Oramorph","morphin",
           "7,8-didehydro-4,5-epoxy-17-methylmorphinan-3,6-diol"],
    44390: ["nicotine","3-(1-methylpyrrolidin-2-yl)pyridine",
            "(S)-nicotine","l-nicotine","tabacin"],
}


def build():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.executescript(SCHEMA)
    conn.commit()

    print(f"Building {DB_PATH}...\n")

    for row in COMPOUNDS:
        conn.execute("""
            INSERT OR REPLACE INTO compounds VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, row)

        cid = row[0]
        iupac = row[1]
        all_names = set(SYNONYMS.get(cid, []))
        all_names.add(iupac)

        for name in all_names:
            if name:
                conn.execute("INSERT OR IGNORE INTO synonyms (cid,name) VALUES (?,?)", (cid, name))
                conn.execute("INSERT OR IGNORE INTO name_index VALUES (?,?)", (name.lower().strip(), cid))

        print(f"  CID {cid:>8}  {iupac[:50]:<50}  {len(all_names)} names")

    conn.commit()

    c = conn.execute("SELECT COUNT(*) FROM compounds").fetchone()[0]
    s = conn.execute("SELECT COUNT(*) FROM synonyms").fetchone()[0]
    n = conn.execute("SELECT COUNT(*) FROM name_index").fetchone()[0]
    print(f"\nDone: {c} compounds | {s} synonym rows | {n} name_index entries")
    conn.close()


if __name__ == "__main__":
    build()
