from __future__ import annotations

import pandas as pd
from src import config

# Comprehensive sample dataset based on IAEA PRIS / WNA public records (~140 units).
# Clearly labeled as sample data — not a source-of-record. Use official PRIS exports for production.
# Format: [reactor_name, plant_name, unit_name, country, status, reactor_type, design_name,
#          net_mwe, gross_mwe, construction_start, grid_connection, commercial_operation,
#          shutdown_date, lat, lon, owner, operator, vendor, source_name]

_S = "IAEA-PRIS/WNA-sample"

RAW_REACTORS = [
    # ── ARGENTINA ──────────────────────────────────────────────────────────────
    ["Atucha-1",  "Atucha",  "Unit 1", "Argentina", "operating",          "PHWR", "PHWR-357",  335,  362, "1968-06-01", "1974-03-19", "1974-06-24", "",           -33.967, -59.205, "NASA", "NA-SA", "Siemens/CNEA", _S],
    ["Atucha-2",  "Atucha",  "Unit 2", "Argentina", "operating",          "PHWR", "PHWR-745",  693,  745, "1981-07-14", "2014-06-02", "2014-05-26", "",           -33.967, -59.205, "NASA", "NA-SA", "CNEA/INVAP",   _S],
    ["Embalse",   "Embalse", "Unit 1", "Argentina", "operating",          "PHWR", "CANDU-6",   648,  683, "1974-04-01", "1983-11-15", "1984-04-01", "",           -32.236, -64.438, "NASA", "NA-SA", "AECL",         _S],
    ["CAREM-25",  "Atucha",  "CAREM",  "Argentina", "under construction", "SMR-LWR","CAREM",    27,   30, "2014-02-08", "",           "",           "",           -33.967, -59.205, "CNEA", "CNEA",  "CNEA",         _S],

    # ── ARMENIA ────────────────────────────────────────────────────────────────
    ["Metsamor-2","Metsamor","Unit 2", "Armenia",   "operating",          "VVER", "VVER-440",  376,  408, "1975-07-01", "1980-01-05", "1980-05-03", "",            40.180,  44.149, "ANPP", "ANPP",  "AtomEnergoProject", _S],

    # ── BELGIUM ────────────────────────────────────────────────────────────────
    ["Doel-3",    "Doel",    "Unit 3", "Belgium",   "operating",          "PWR",  "PWR-3loop",1006, 1056, "1975-01-01", "1982-06-24", "1982-10-01", "",            51.325,   4.259, "Electrabel","Engie",    "Framatome",  _S],
    ["Doel-4",    "Doel",    "Unit 4", "Belgium",   "operating",          "PWR",  "PWR-3loop",1037, 1084, "1978-12-01", "1985-04-09", "1985-07-01", "",            51.325,   4.259, "Electrabel","Engie",    "Framatome",  _S],
    ["Tihange-2", "Tihange", "Unit 2", "Belgium",   "operating",          "PWR",  "PWR-3loop",1008, 1055, "1976-04-01", "1982-10-13", "1983-06-01", "",            50.534,   5.271, "Electrabel","Engie",    "Framatome",  _S],
    ["Tihange-3", "Tihange", "Unit 3", "Belgium",   "operating",          "PWR",  "PWR-3loop",1046, 1089, "1978-11-01", "1985-06-28", "1985-09-01", "",            50.534,   5.271, "Electrabel","Engie",    "Framatome",  _S],

    # ── BRAZIL ─────────────────────────────────────────────────────────────────
    ["Angra-1",   "Angra",   "Unit 1", "Brazil",    "operating",          "PWR",  "PWR",       640,  657, "1971-05-01", "1982-03-01", "1985-04-22", "",           -23.008, -44.458, "Eletronuclear","Eletronuclear","Westinghouse",_S],
    ["Angra-2",   "Angra",   "Unit 2", "Brazil",    "operating",          "PWR",  "PWR",      1350, 1400, "1976-01-01", "2000-07-21", "2001-02-01", "",           -23.008, -44.458, "Eletronuclear","Eletronuclear","Siemens/KWU",  _S],
    ["Angra-3",   "Angra",   "Unit 3", "Brazil",    "planned",            "PWR",  "PWR",      1405, 1450, "2010-06-01", "",           "",           "",           -23.008, -44.458, "Eletronuclear","Eletronuclear","Siemens/Areva",_S],

    # ── BULGARIA ───────────────────────────────────────────────────────────────
    ["Kozloduy-5","Kozloduy","Unit 5", "Bulgaria",  "operating",          "VVER", "VVER-1000", 953, 1000, "1980-07-01", "1988-11-23", "1989-12-24", "",            43.797,  23.786, "Kozloduy NPP","Kozloduy NPP","Rosatom",_S],
    ["Kozloduy-6","Kozloduy","Unit 6", "Bulgaria",  "operating",          "VVER", "VVER-1000", 953, 1000, "1982-04-01", "1993-08-30", "1993-12-30", "",            43.797,  23.786, "Kozloduy NPP","Kozloduy NPP","Rosatom",_S],
    ["Belene-1",  "Belene",  "Unit 1", "Bulgaria",  "proposed",           "VVER", "VVER-1000",1000, 1060, "",           "",           "",           "",            43.626,  25.169, "BEH",         "BEH",         "Rosatom",_S],

    # ── CANADA ─────────────────────────────────────────────────────────────────
    ["Bruce-3",      "Bruce",      "Unit 3","Canada","operating","PHWR","CANDU-6", 769, 817,"1967-06-01","1977-02-01","1978-02-01","", 44.326,-81.593,"Bruce Power","Bruce Power","AECL",_S],
    ["Bruce-4",      "Bruce",      "Unit 4","Canada","operating","PHWR","CANDU-6", 769, 817,"1967-06-01","1978-12-15","1979-01-18","", 44.326,-81.593,"Bruce Power","Bruce Power","AECL",_S],
    ["Bruce-5",      "Bruce",      "Unit 5","Canada","operating","PHWR","CANDU-6", 817, 872,"1978-06-01","1984-12-29","1985-03-01","", 44.326,-81.593,"Bruce Power","Bruce Power","AECL",_S],
    ["Bruce-6",      "Bruce",      "Unit 6","Canada","operating","PHWR","CANDU-6", 817, 872,"1978-09-01","1984-09-14","1984-09-14","", 44.326,-81.593,"Bruce Power","Bruce Power","AECL",_S],
    ["Bruce-7",      "Bruce",      "Unit 7","Canada","operating","PHWR","CANDU-6", 817, 872,"1979-05-01","1986-04-10","1986-04-10","", 44.326,-81.593,"Bruce Power","Bruce Power","AECL",_S],
    ["Bruce-8",      "Bruce",      "Unit 8","Canada","operating","PHWR","CANDU-6", 817, 872,"1979-08-01","1987-05-22","1987-05-22","", 44.326,-81.593,"Bruce Power","Bruce Power","AECL",_S],
    ["Darlington-1", "Darlington", "Unit 1","Canada","operating","PHWR","CANDU-6", 878, 935,"1981-04-01","1990-11-14","1992-11-14","", 43.872,-78.719,"OPG","OPG","AECL",_S],
    ["Darlington-2", "Darlington", "Unit 2","Canada","operating","PHWR","CANDU-6", 878, 935,"1981-09-01","1990-01-09","1990-10-09","", 43.872,-78.719,"OPG","OPG","AECL",_S],
    ["Darlington-3", "Darlington", "Unit 3","Canada","operating","PHWR","CANDU-6", 878, 935,"1984-09-01","1992-02-01","1993-02-14","", 43.872,-78.719,"OPG","OPG","AECL",_S],
    ["Darlington-4", "Darlington", "Unit 4","Canada","operating","PHWR","CANDU-6", 878, 935,"1985-07-01","1993-06-14","1993-06-14","", 43.872,-78.719,"OPG","OPG","AECL",_S],
    ["Darlington-SMR-1","Darlington","BWRX-300","Canada","planned","SMR-LWR","BWRX-300", 300, 300,"","","","", 43.872,-78.719,"OPG","OPG","GE Hitachi",_S],

    # ── CHINA ──────────────────────────────────────────────────────────────────
    ["Daya Bay-1",     "Daya Bay",     "Unit 1","China","operating","PWR","M310",    944, 984,"1987-08-07","1993-08-31","1994-02-01","", 22.598,114.538,"CGNPC","CGN","Framatome",_S],
    ["Daya Bay-2",     "Daya Bay",     "Unit 2","China","operating","PWR","M310",    944, 984,"1988-04-07","1994-02-07","1994-05-06","", 22.598,114.538,"CGNPC","CGN","Framatome",_S],
    ["Ling Ao-1",      "Ling Ao",      "Unit 1","China","operating","PWR","CPR-1000", 990,1036,"1997-05-15","2002-05-28","2002-05-28","", 22.598,114.538,"CGNPC","CGN","Framatome",_S],
    ["Ling Ao-2",      "Ling Ao",      "Unit 2","China","operating","PWR","CPR-1000", 990,1036,"1997-11-01","2003-01-08","2003-01-08","", 22.598,114.538,"CGNPC","CGN","Framatome",_S],
    ["Qinshan-1",      "Qinshan",      "Unit 1","China","operating","PWR","CNP-300",  300, 320,"1985-03-20","1991-12-15","1994-04-01","", 30.437,120.954,"CNNC","CNNC","CNNC",_S],
    ["Qinshan-2-1",    "Qinshan II",   "Unit 1","China","operating","PWR","CNP-600",  650, 688,"1996-06-02","2002-02-06","2002-04-15","", 30.437,120.954,"CNNC","CNNC","CNNC",_S],
    ["Sanmen-1",       "Sanmen",       "Unit 1","China","operating","PWR","AP1000",  1157,1250,"2009-04-19","2018-06-30","2018-09-21","", 29.101,121.641,"CNNC","CNNC","Westinghouse",_S],
    ["Sanmen-2",       "Sanmen",       "Unit 2","China","operating","PWR","AP1000",  1157,1250,"2009-12-15","2018-08-17","2018-11-05","", 29.101,121.641,"CNNC","CNNC","Westinghouse",_S],
    ["Haiyang-1",      "Haiyang",      "Unit 1","China","operating","PWR","AP1000",  1157,1250,"2009-09-26","2018-10-22","2018-11-22","", 36.776,121.461,"SPNC","SPNC","Westinghouse",_S],
    ["Haiyang-2",      "Haiyang",      "Unit 2","China","operating","PWR","AP1000",  1157,1250,"2010-06-20","2019-01-09","2019-05-09","", 36.776,121.461,"SPNC","SPNC","Westinghouse",_S],
    ["Taishan-1",      "Taishan",      "Unit 1","China","operating","PWR","EPR",     1660,1750,"2009-10-28","2018-06-29","2018-12-13","", 21.918,112.981,"TNPJVC","CGN","Framatome",_S],
    ["Taishan-2",      "Taishan",      "Unit 2","China","operating","PWR","EPR",     1660,1750,"2010-04-15","2019-06-23","2019-09-07","", 21.918,112.981,"TNPJVC","CGN","Framatome",_S],
    ["Tianwan-1",      "Tianwan",      "Unit 1","China","operating","VVER","VVER-1000",1060,1126,"2000-10-20","2006-05-12","2007-05-17","", 34.692,119.455,"JNPC","JNPC","Rosatom",_S],
    ["Tianwan-2",      "Tianwan",      "Unit 2","China","operating","VVER","VVER-1000",1060,1126,"2000-10-20","2007-08-16","2007-08-16","", 34.692,119.455,"JNPC","JNPC","Rosatom",_S],
    ["Tianwan-3",      "Tianwan",      "Unit 3","China","operating","VVER","VVER-1000",1060,1126,"2012-12-27","2018-02-15","2018-02-15","", 34.692,119.455,"JNPC","JNPC","Rosatom",_S],
    ["Tianwan-4",      "Tianwan",      "Unit 4","China","operating","VVER","VVER-1000",1060,1126,"2013-09-27","2018-12-22","2018-12-22","", 34.692,119.455,"JNPC","JNPC","Rosatom",_S],
    ["Yangjiang-1",    "Yangjiang",    "Unit 1","China","operating","PWR","CPR-1000",1086,1140,"2008-12-16","2013-12-27","2014-03-25","", 21.705,111.606,"CGNPC","CGN","CGN",_S],
    ["Yangjiang-5",    "Yangjiang",    "Unit 5","China","operating","PWR","ACPR-1000",1086,1140,"2013-09-18","2018-07-21","2018-07-21","", 21.705,111.606,"CGNPC","CGN","CGN",_S],
    ["Hongyanhe-1",    "Hongyanhe",    "Unit 1","China","operating","PWR","CPR-1000",1061,1119,"2007-08-18","2013-02-17","2013-06-06","", 39.794,121.474,"CGNPC/CNOOC","CGN","CGN",_S],
    ["Hongyanhe-5",    "Hongyanhe",    "Unit 5","China","operating","PWR","ACPR-1000",1061,1119,"2015-03-29","2021-07-24","2021-09-08","", 39.794,121.474,"CGNPC/CNOOC","CGN","CGN",_S],
    ["Fangchenggang-3","Fangchenggang","Unit 3","China","operating","PWR","HPR-1000",1000,1080,"2015-12-24","2022-03-24","2022-06-10","", 21.483,108.140,"CGNPC","CGN","CGN",_S],
    # Under construction China
    ["Zhangzhou-1",    "Zhangzhou",    "Unit 1","China","under construction","PWR","HPR-1000",1126,1212,"2019-10-16","","","", 24.100,117.855,"CNNC","CNNC","CNNC",_S],
    ["Zhangzhou-2",    "Zhangzhou",    "Unit 2","China","under construction","PWR","HPR-1000",1126,1212,"2020-09-04","","","", 24.100,117.855,"CNNC","CNNC","CNNC",_S],
    ["Tianwan-7",      "Tianwan",      "Unit 7","China","under construction","VVER","VVER-1200",1200,1250,"2021-05-19","","","", 34.692,119.455,"JNPC","JNPC","Rosatom",_S],
    ["Xudabao-3",      "Xudabao",      "Unit 3","China","under construction","VVER","VVER-1200",1200,1250,"2021-07-19","","","", 40.588,120.285,"CGNPC","CGN","Rosatom",_S],
    ["Sanmen-3",       "Sanmen",       "Unit 3","China","under construction","PWR","AP1000",   1157,1250,"2022-07-21","","","", 29.101,121.641,"CNNC","CNNC","Westinghouse",_S],

    # ── CZECH REPUBLIC ─────────────────────────────────────────────────────────
    ["Dukovany-1", "Dukovany","Unit 1","Czech Republic","operating","VVER","VVER-440", 440, 500,"1974-01-01","1985-03-22","1985-05-03","", 49.088, 16.147,"CEZ","CEZ","Rosatom",_S],
    ["Dukovany-3", "Dukovany","Unit 3","Czech Republic","operating","VVER","VVER-440", 440, 500,"1979-03-01","1986-12-17","1987-01-01","", 49.088, 16.147,"CEZ","CEZ","Rosatom",_S],
    ["Temelin-1",  "Temelin", "Unit 1","Czech Republic","operating","VVER","VVER-1000",1000,1078,"1987-11-01","2002-06-10","2002-12-10","", 49.071, 14.374,"CEZ","CEZ","Rosatom",_S],
    ["Temelin-2",  "Temelin", "Unit 2","Czech Republic","operating","VVER","VVER-1000",1000,1078,"1987-11-01","2002-12-18","2003-04-18","", 49.071, 14.374,"CEZ","CEZ","Rosatom",_S],

    # ── EGYPT ──────────────────────────────────────────────────────────────────
    ["El Dabaa-1", "El Dabaa","Unit 1","Egypt","under construction","VVER","VVER-1200",1114,1200,"2022-07-20","","","", 31.041, 28.497,"NPPA","NPPA","Rosatom",_S],
    ["El Dabaa-2", "El Dabaa","Unit 2","Egypt","under construction","VVER","VVER-1200",1114,1200,"2022-11-19","","","", 31.041, 28.497,"NPPA","NPPA","Rosatom",_S],
    ["El Dabaa-3", "El Dabaa","Unit 3","Egypt","planned",           "VVER","VVER-1200",1114,1200,"","","","", 31.041, 28.497,"NPPA","NPPA","Rosatom",_S],

    # ── FINLAND ────────────────────────────────────────────────────────────────
    ["Loviisa-1",    "Loviisa",    "Unit 1","Finland","operating","VVER","VVER-440",496, 535,"1971-05-01","1977-02-09","1977-05-09","", 60.404, 26.370,"Fortum","Fortum","IVO/Rosatom",_S],
    ["Loviisa-2",    "Loviisa",    "Unit 2","Finland","operating","VVER","VVER-440",496, 535,"1972-08-01","1980-01-05","1981-01-05","", 60.404, 26.370,"Fortum","Fortum","IVO/Rosatom",_S],
    ["Olkiluoto-1",  "Olkiluoto",  "Unit 1","Finland","operating","BWR","BWR",       880, 910,"1976-02-01","1978-09-02","1979-10-02","", 61.235, 21.445,"TVO","TVO","ABB Atom",_S],
    ["Olkiluoto-2",  "Olkiluoto",  "Unit 2","Finland","operating","BWR","BWR",       890, 920,"1975-11-01","1980-02-10","1982-07-10","", 61.235, 21.445,"TVO","TVO","ABB Atom",_S],
    ["Olkiluoto-3",  "Olkiluoto",  "Unit 3","Finland","operating","PWR","EPR",      1600,1720,"2005-08-12","2022-03-12","2023-04-16","", 61.235, 21.445,"TVO","TVO","Framatome",_S],

    # ── FRANCE (representative sample) ─────────────────────────────────────────
    ["Civaux-1",       "Civaux",       "Unit 1","France","operating","PWR","N4",       1495,1561,"1988-10-15","1997-12-24","2002-01-24","", 46.457,  0.652,"EDF","EDF","Framatome",_S],
    ["Civaux-2",       "Civaux",       "Unit 2","France","operating","PWR","N4",       1495,1561,"1991-04-01","1999-12-23","2002-04-23","", 46.457,  0.652,"EDF","EDF","Framatome",_S],
    ["Cattenom-1",     "Cattenom",     "Unit 1","France","operating","PWR","P4",       1300,1362,"1979-11-01","1986-11-13","1987-04-01","", 49.402,  6.220,"EDF","EDF","Framatome",_S],
    ["Paluel-1",       "Paluel",       "Unit 1","France","operating","PWR","P4",       1330,1382,"1977-08-15","1985-06-10","1985-12-01","", 49.855, -0.634,"EDF","EDF","Framatome",_S],
    ["Flamanville-1",  "Flamanville",  "Unit 1","France","operating","PWR","P4",       1330,1382,"1979-12-01","1985-12-04","1986-12-04","", 49.536, -1.882,"EDF","EDF","Framatome",_S],
    ["Flamanville-3",  "Flamanville",  "Unit 3","France","operating","PWR","EPR",      1630,1750,"2007-12-03","2024-12-21","2025-01-01","", 49.536, -1.882,"EDF","EDF","Framatome",_S],
    ["Bugey-4",        "Bugey",        "Unit 4","France","operating","PWR","CP1",       880, 937,"1974-06-01","1979-03-11","1979-07-11","", 45.797,  5.272,"EDF","EDF","Framatome",_S],
    ["Blayais-1",      "Blayais",      "Unit 1","France","operating","PWR","CP1",       910, 951,"1977-01-01","1981-06-12","1981-12-12","", 45.255, -0.691,"EDF","EDF","Framatome",_S],
    ["Gravelines-1",   "Gravelines",   "Unit 1","France","operating","PWR","CP1",       910, 951,"1975-02-01","1980-03-13","1980-11-25","", 51.015,  2.136,"EDF","EDF","Framatome",_S],
    ["Tricastin-1",    "Tricastin",    "Unit 1","France","operating","PWR","CP1",       915, 955,"1974-11-01","1980-05-31","1980-12-01","", 44.330,  4.732,"EDF","EDF","Framatome",_S],

    # ── INDIA ──────────────────────────────────────────────────────────────────
    ["Kakrapar-1",   "Kakrapar",  "Unit 1","India","operating","PHWR","PHWR-220",202,220,"1984-12-01","1992-09-03","1993-05-06","", 21.228, 73.057,"NPCIL","NPCIL","DAE",_S],
    ["Kakrapar-3",   "Kakrapar",  "Unit 3","India","operating","PHWR","PHWR-700",640,700,"2010-11-22","2022-07-10","2023-06-01","", 21.228, 73.057,"NPCIL","NPCIL","DAE",_S],
    ["Rajasthan-5",  "Rawatbhata","Unit 5","India","operating","PHWR","PHWR-220",202,220,"2002-09-01","2009-12-04","2010-02-04","", 24.874, 75.583,"NPCIL","NPCIL","NPCIL",_S],
    ["Rajasthan-7",  "Rawatbhata","Unit 7","India","under construction","PHWR","PHWR-700",640,700,"2011-09-18","","","", 24.874, 75.583,"NPCIL","NPCIL","NPCIL",_S],
    ["Kudankulam-1", "Kudankulam","Unit 1","India","operating","VVER","VVER-1000",917,1000,"2002-03-31","2013-10-22","2013-12-31","",  8.169, 77.713,"NPCIL","NPCIL","Rosatom",_S],
    ["Kudankulam-2", "Kudankulam","Unit 2","India","operating","VVER","VVER-1000",917,1000,"2002-07-04","2016-08-29","2017-03-31","",  8.169, 77.713,"NPCIL","NPCIL","Rosatom",_S],
    ["Kudankulam-3", "Kudankulam","Unit 3","India","under construction","VVER","VVER-1000",917,1000,"","","","",  8.169, 77.713,"NPCIL","NPCIL","Rosatom",_S],
    ["PFBR",         "Kalpakkam","PFBR",  "India","under construction","SFR","PFBR",  500, 500,"2004-10-23","","","", 12.552, 80.170,"BHAVINI","BHAVINI","BHAVINI",_S],

    # ── JAPAN ──────────────────────────────────────────────────────────────────
    ["Mihama-3",      "Mihama",     "Unit 3","Japan","operating","PWR","PWR",   826, 896,"1972-12-01","1976-02-25","1976-12-01","", 35.704,135.962,"KEPCO","KEPCO","Westinghouse",_S],
    ["Takahama-3",    "Takahama",   "Unit 3","Japan","operating","PWR","PWR",   870, 912,"1981-01-01","1985-01-17","1985-01-17","", 35.524,135.508,"KEPCO","KEPCO","Westinghouse",_S],
    ["Takahama-4",    "Takahama",   "Unit 4","Japan","operating","PWR","PWR",   870, 912,"1981-11-01","1985-06-05","1985-06-05","", 35.524,135.508,"KEPCO","KEPCO","Westinghouse",_S],
    ["Ikata-3",       "Ikata",      "Unit 3","Japan","operating","PWR","PWR",   846, 890,"1985-09-16","1994-03-22","1994-12-15","", 33.489,132.320,"Shikoku","Shikoku","Mitsubishi",_S],
    ["Sendai-1",      "Sendai",     "Unit 1","Japan","operating","PWR","PWR",   846, 890,"1979-11-01","1984-07-28","1984-07-28","", 31.833,130.185,"Kyushu","Kyushu","Mitsubishi",_S],
    ["Onagawa-2",     "Onagawa",    "Unit 2","Japan","operating","BWR","BWR",   796, 825,"1989-08-03","1994-12-23","1995-07-28","", 38.402,141.500,"Tohoku","Tohoku","Toshiba",_S],

    # ── MEXICO ─────────────────────────────────────────────────────────────────
    ["Laguna Verde-1","Laguna Verde","Unit 1","Mexico","operating","BWR","BWR-5",680,750,"1976-10-01","1988-07-29","1990-07-29","", 19.720,-96.397,"CFE","CFE","GE",_S],
    ["Laguna Verde-2","Laguna Verde","Unit 2","Mexico","operating","BWR","BWR-5",674,750,"1977-06-01","1994-11-10","1995-04-10","", 19.720,-96.397,"CFE","CFE","GE",_S],

    # ── NETHERLANDS ────────────────────────────────────────────────────────────
    ["Borssele-1",   "Borssele",  "Unit 1","Netherlands","operating","PWR","PWR",  515, 540,"1969-07-01","1973-03-26","1973-10-26","", 51.413,  3.723,"EPZ","EPZ","KWU",_S],

    # ── PAKISTAN ───────────────────────────────────────────────────────────────
    ["Karachi-2",    "Karachi",    "Unit 2","Pakistan","operating","PWR","HPR-1000",1100,1161,"2015-08-20","2021-03-21","2021-05-21","", 25.014, 66.784,"PAEC","PAEC","CNNC",_S],
    ["Karachi-3",    "Karachi",    "Unit 3","Pakistan","operating","PWR","HPR-1000",1100,1161,"2016-05-31","2022-03-21","2022-05-21","", 25.014, 66.784,"PAEC","PAEC","CNNC",_S],
    ["Chashma-1",    "Chashma",    "Unit 1","Pakistan","operating","PWR","CNP-300",  300, 325,"1993-08-01","1999-09-13","2000-09-01","", 32.393, 71.463,"PAEC","PAEC","CNNC",_S],
    ["Chashma-2",    "Chashma",    "Unit 2","Pakistan","operating","PWR","CNP-300",  300, 325,"1996-05-01","2011-03-18","2011-05-18","", 32.393, 71.463,"PAEC","PAEC","CNNC",_S],

    # ── ROMANIA ────────────────────────────────────────────────────────────────
    ["Cernavoda-1",  "Cernavoda", "Unit 1","Romania","operating","PHWR","CANDU-6", 650, 706,"1982-07-01","1996-04-11","1996-12-02","", 44.316, 28.058,"SNN","SNN","AECL",_S],
    ["Cernavoda-2",  "Cernavoda", "Unit 2","Romania","operating","PHWR","CANDU-6", 650, 706,"1983-07-01","2007-08-07","2007-11-07","", 44.316, 28.058,"SNN","SNN","AECL",_S],
    ["Cernavoda-3",  "Cernavoda", "Unit 3","Romania","planned",  "PHWR","CANDU-6", 650, 706,"","","","", 44.316, 28.058,"SNN","SNN","AECL",_S],

    # ── RUSSIA ─────────────────────────────────────────────────────────────────
    ["Novovoronezh-6","Novovoronezh","Unit 6","Russia","operating","VVER","VVER-1200",1114,1200,"2008-07-17","2016-12-05","2017-02-05","", 51.288, 39.218,"Rosenergoatom","Rosatom","Rosatom",_S],
    ["Novovoronezh-7","Novovoronezh","Unit 7","Russia","operating","VVER","VVER-1200",1114,1200,"2008-07-17","2018-11-01","2019-02-01","", 51.288, 39.218,"Rosenergoatom","Rosatom","Rosatom",_S],
    ["Leningrad-5",   "Leningrad",  "Unit 5","Russia","operating","VVER","VVER-1200",1114,1200,"2008-10-25","2018-10-09","2018-10-09","", 59.856, 29.076,"Rosenergoatom","Rosatom","Rosatom",_S],
    ["Leningrad-6",   "Leningrad",  "Unit 6","Russia","operating","VVER","VVER-1200",1114,1200,"2010-04-22","2021-03-22","2021-10-22","", 59.856, 29.076,"Rosenergoatom","Rosatom","Rosatom",_S],
    ["Rostov-1",      "Rostov",     "Unit 1","Russia","operating","VVER","VVER-1000",1011,1070,"1990-09-01","2001-03-26","2001-12-25","", 47.573, 42.267,"Rosenergoatom","Rosatom","Rosatom",_S],
    ["Rostov-3",      "Rostov",     "Unit 3","Russia","operating","VVER","VVER-1000",1011,1070,"2009-09-15","2014-12-27","2015-09-17","", 47.573, 42.267,"Rosenergoatom","Rosatom","Rosatom",_S],
    ["Beloyarsk-4",   "Beloyarsk",  "Unit 4","Russia","operating","SFR","BN-800",    789, 880,"2006-07-18","2015-12-10","2016-10-31","", 56.842, 61.322,"Rosenergoatom","Rosatom","OKBM",_S],
    ["Kursk-5",       "Kursk II",   "Unit 5","Russia","under construction","VVER","VVER-TOI",1255,1339,"2021-06-22","","","", 51.667, 35.610,"Rosenergoatom","Rosatom","Rosatom",_S],

    # ── SLOVAKIA ───────────────────────────────────────────────────────────────
    ["Mochovce-1",   "Mochovce","Unit 1","Slovakia","operating","VVER","VVER-440",411,440,"1983-10-01","1998-06-29","1999-10-29","", 48.413, 18.534,"SE","SE","Rosatom",_S],
    ["Mochovce-2",   "Mochovce","Unit 2","Slovakia","operating","VVER","VVER-440",411,440,"1985-01-01","2000-04-18","2000-04-18","", 48.413, 18.534,"SE","SE","Rosatom",_S],
    ["Mochovce-3",   "Mochovce","Unit 3","Slovakia","operating","VVER","VVER-440",471,505,"1987-01-01","2022-10-31","2023-01-31","", 48.413, 18.534,"SE","SE","Rosatom",_S],
    ["Mochovce-4",   "Mochovce","Unit 4","Slovakia","under construction","VVER","VVER-440",471,505,"1987-01-01","","","", 48.413, 18.534,"SE","SE","Rosatom",_S],
    ["Bohunice-3",   "Bohunice", "Unit 3","Slovakia","operating","VVER","VVER-440",408,440,"1976-12-01","1984-11-28","1985-02-14","", 48.493, 17.671,"SE","SE","Rosatom",_S],

    # ── SOUTH AFRICA ───────────────────────────────────────────────────────────
    ["Koeberg-1","Koeberg","Unit 1","South Africa","operating","PWR","PWR-3loop",900,970,"1976-07-01","1984-04-04","1984-07-21","", -33.659, 18.432,"Eskom","Eskom","Framatome",_S],
    ["Koeberg-2","Koeberg","Unit 2","South Africa","operating","PWR","PWR-3loop",900,970,"1976-07-01","1985-07-09","1985-11-09","", -33.659, 18.432,"Eskom","Eskom","Framatome",_S],

    # ── SOUTH KOREA ────────────────────────────────────────────────────────────
    ["Kori-1",       "Kori",    "Unit 1","South Korea","shutdown","PWR","PWR",    587, 609,"1972-01-18","1978-04-29","1978-07-29","2017-06-19", 35.321,129.294,"KHNP","KHNP","Westinghouse",_S],
    ["Kori-2",       "Kori",    "Unit 2","South Korea","operating","PWR","OPR-1000",640,650,"1977-12-23","1983-04-09","1983-07-25","", 35.321,129.294,"KHNP","KHNP","Westinghouse",_S],
    ["Shin Kori-4",  "Shin Kori","Unit 4","South Korea","operating","PWR","APR1400",1340,1455,"2009-08-19","2019-08-29","2019-08-29","", 35.321,129.294,"KHNP","KHNP","KHNP",_S],
    ["Hanbit-1",     "Hanbit",  "Unit 1","South Korea","operating","PWR","OPR-1000",950, 1000,"1981-06-01","1986-08-25","1986-08-25","", 35.413,126.425,"KHNP","KHNP","Westinghouse",_S],
    ["Hanul-1",      "Hanul",   "Unit 1","South Korea","operating","PWR","OPR-1000",950, 1000,"1983-01-26","1988-12-26","1988-12-26","", 37.094,129.381,"KHNP","KHNP","Westinghouse",_S],
    ["Shin Hanul-1", "Shin Hanul","Unit 1","South Korea","operating","PWR","APR1400",1340,1455,"2012-07-10","2022-06-09","2022-06-09","", 37.094,129.381,"KHNP","KHNP","KHNP",_S],
    ["Shin Hanul-2", "Shin Hanul","Unit 2","South Korea","operating","PWR","APR1400",1340,1455,"2012-09-28","2023-12-22","2023-12-22","", 37.094,129.381,"KHNP","KHNP","KHNP",_S],
    ["Wolsong-1",    "Wolsong", "Unit 1","South Korea","shutdown","PHWR","CANDU-6", 679, 700,"1977-10-01","1982-11-21","1983-04-22","2019-12-24", 35.712,129.476,"KHNP","KHNP","AECL",_S],
    ["Wolsong-2",    "Wolsong", "Unit 2","South Korea","operating","PHWR","CANDU-6", 700, 728,"1992-09-01","1997-01-01","1997-07-01","", 35.712,129.476,"KHNP","KHNP","AECL",_S],

    # ── SPAIN ──────────────────────────────────────────────────────────────────
    ["Almaraz-1",   "Almaraz",  "Unit 1","Spain","operating","PWR","PWR-3loop",1049,1100,"1973-07-03","1981-09-01","1983-05-01","", 39.806, -5.698,"Iberdrola","Almaraz NPP","Westinghouse",_S],
    ["Almaraz-2",   "Almaraz",  "Unit 2","Spain","operating","PWR","PWR-3loop",1044,1100,"1973-07-03","1983-06-01","1984-06-01","", 39.806, -5.698,"Iberdrola","Almaraz NPP","Westinghouse",_S],
    ["Vandellos-2", "Vandellos","Unit 2","Spain","operating","PWR","PWR-3loop",1045,1100,"1980-12-01","1987-09-01","1988-03-08","", 40.922,  0.882,"Iberdrola","ANAV","Westinghouse",_S],
    ["Cofrentes",   "Cofrentes","Unit 1","Spain","operating","BWR","BWR-6",    1064,1118,"1975-08-14","1984-03-11","1985-03-11","", 39.244, -1.068,"Iberdrola","Iberdrola","GE",_S],

    # ── SWEDEN ─────────────────────────────────────────────────────────────────
    ["Forsmark-1",   "Forsmark",  "Unit 1","Sweden","operating","BWR","BWR",  984, 1020,"1973-06-01","1980-04-10","1984-12-10","", 60.405, 18.170,"Vattenfall","Vattenfall","ASEA Atom",_S],
    ["Forsmark-3",   "Forsmark",  "Unit 3","Sweden","operating","BWR","BWR",  1167,1200,"1979-01-01","1985-08-18","1985-08-18","", 60.405, 18.170,"Vattenfall","Vattenfall","ASEA Atom",_S],
    ["Ringhals-3",   "Ringhals",  "Unit 3","Sweden","operating","PWR","PWR",   1063,1099,"1972-09-01","1981-05-07","1981-09-07","", 57.257, 12.106,"Vattenfall","Ringhals","Westinghouse",_S],

    # ── SWITZERLAND ────────────────────────────────────────────────────────────
    ["Beznau-1",   "Beznau",  "Unit 1","Switzerland","operating","PWR","PWR",  365, 380,"1965-09-01","1969-09-17","1969-12-09","", 47.523,  8.116,"Axpo","Axpo","Westinghouse",_S],
    ["Leibstadt",  "Leibstadt","Unit 1","Switzerland","operating","BWR","BWR",  1220,1285,"1974-01-01","1984-09-28","1984-12-15","", 47.603,  8.181,"KKL","KKL","GE",_S],
    ["Gosgen",     "Gosgen",   "Unit 1","Switzerland","operating","PWR","PWR",   970,1020,"1973-06-01","1979-09-12","1979-11-01","", 47.367,  7.961,"KKG","KKG","KWU",_S],

    # ── TURKEY ─────────────────────────────────────────────────────────────────
    ["Akkuyu-1","Akkuyu","Unit 1","Turkey","under construction","VVER","VVER-1200",1114,1200,"2018-04-03","","","", 36.144, 33.541,"Akkuyu Nuclear","Rosatom","Rosatom",_S],
    ["Akkuyu-2","Akkuyu","Unit 2","Turkey","under construction","VVER","VVER-1200",1114,1200,"2020-04-08","","","", 36.144, 33.541,"Akkuyu Nuclear","Rosatom","Rosatom",_S],
    ["Akkuyu-3","Akkuyu","Unit 3","Turkey","under construction","VVER","VVER-1200",1114,1200,"2021-03-10","","","", 36.144, 33.541,"Akkuyu Nuclear","Rosatom","Rosatom",_S],
    ["Akkuyu-4","Akkuyu","Unit 4","Turkey","under construction","VVER","VVER-1200",1114,1200,"2022-07-21","","","", 36.144, 33.541,"Akkuyu Nuclear","Rosatom","Rosatom",_S],

    # ── UAE ────────────────────────────────────────────────────────────────────
    ["Barakah-1","Barakah","Unit 1","UAE","operating","PWR","APR1400",1345,1400,"2012-07-18","2020-08-19","2021-04-06","", 23.968, 52.227,"ENEC","Nawah","KEPCO",_S],
    ["Barakah-2","Barakah","Unit 2","UAE","operating","PWR","APR1400",1345,1400,"2013-04-16","2021-09-14","2022-03-24","", 23.968, 52.227,"ENEC","Nawah","KEPCO",_S],
    ["Barakah-3","Barakah","Unit 3","UAE","operating","PWR","APR1400",1345,1400,"2014-09-24","2023-02-24","2023-10-14","", 23.968, 52.227,"ENEC","Nawah","KEPCO",_S],
    ["Barakah-4","Barakah","Unit 4","UAE","under construction","PWR","APR1400",1345,1400,"2015-09-02","","","", 23.968, 52.227,"ENEC","Nawah","KEPCO",_S],

    # ── UKRAINE ────────────────────────────────────────────────────────────────
    ["Khmelnitsky-1","Khmelnitsky","Unit 1","Ukraine","operating","VVER","VVER-1000",950,1000,"1981-11-01","1987-12-22","1987-12-22","", 50.300, 26.648,"Energoatom","Energoatom","Rosatom",_S],
    ["Rivne-3",      "Rivne",     "Unit 3","Ukraine","operating","VVER","VVER-1000",950,1000,"1980-02-22","1986-12-21","1987-11-21","", 51.325, 25.892,"Energoatom","Energoatom","Rosatom",_S],
    ["South Ukraine-1","South Ukraine","Unit 1","Ukraine","operating","VVER","VVER-1000",950,1000,"1977-11-01","1982-10-27","1983-12-31","", 47.839, 31.216,"Energoatom","Energoatom","Rosatom",_S],
    ["Zaporizhzhia-1","Zaporizhzhia","Unit 1","Ukraine","operating","VVER","VVER-1000",950,1000,"1981-04-01","1985-12-10","1985-12-10","", 47.506, 34.585,"Energoatom","Energoatom","Rosatom",_S],
    ["Zaporizhzhia-5","Zaporizhzhia","Unit 5","Ukraine","operating","VVER","VVER-1000",950,1000,"1985-11-01","1989-10-18","1989-10-18","", 47.506, 34.585,"Energoatom","Energoatom","Rosatom",_S],

    # ── UNITED KINGDOM ─────────────────────────────────────────────────────────
    ["Heysham-2A",     "Heysham-2",     "Unit A","United Kingdom","operating","GCR","AGR",  615, 660,"1980-08-01","1988-03-01","1989-04-01","", 54.032, -2.910,"EDF","EDF","GEC",_S],
    ["Torness-A",      "Torness",       "Unit A","United Kingdom","operating","GCR","AGR",  615, 660,"1980-08-01","1988-05-23","1988-05-23","", 55.966, -2.437,"EDF","EDF","GEC",_S],
    ["Sizewell-B",     "Sizewell",      "Unit B","United Kingdom","operating","PWR","PWR",  1198,1258,"1988-07-18","1995-02-14","1995-02-14","", 52.213,  1.618,"EDF","EDF","Westinghouse",_S],
    ["Hinkley Point C-1","Hinkley Point C","Unit 1","United Kingdom","under construction","PWR","EPR",1630,1720,"2018-12-11","","","", 51.205, -3.143,"EDF/CGN","EDF","Framatome",_S],
    ["Hinkley Point C-2","Hinkley Point C","Unit 2","United Kingdom","under construction","PWR","EPR",1630,1720,"2019-12-11","","","", 51.205, -3.143,"EDF/CGN","EDF","Framatome",_S],
    ["Wylfa Newydd-1", "Wylfa Newydd",  "Unit 1","United Kingdom","proposed","PWR","ABWR",   1380,1455,"","","","", 53.418, -4.473,"Horizon","Hitachi","Hitachi",_S],

    # ── UNITED STATES ──────────────────────────────────────────────────────────
    ["Palo Verde-1",   "Palo Verde",  "Unit 1","United States","operating","PWR","System 80",1311,1412,"1976-05-25","1985-11-26","1986-01-28","", 33.388,-112.862,"APS","APS","CE",_S],
    ["Palo Verde-2",   "Palo Verde",  "Unit 2","United States","operating","PWR","System 80",1311,1412,"1978-05-25","1986-04-19","1986-09-19","", 33.388,-112.862,"APS","APS","CE",_S],
    ["Palo Verde-3",   "Palo Verde",  "Unit 3","United States","operating","PWR","System 80",1311,1412,"1979-11-01","1987-11-26","1988-01-08","", 33.388,-112.862,"APS","APS","CE",_S],
    ["Browns Ferry-1", "Browns Ferry","Unit 1","United States","operating","BWR","BWR-4",   1210,1251,"1967-09-12","1973-08-01","1974-08-01","", 34.704,-87.119,"TVA","TVA","GE",_S],
    ["Browns Ferry-3", "Browns Ferry","Unit 3","United States","operating","BWR","BWR-4",   1210,1251,"1968-07-01","1977-03-01","1977-03-01","", 34.704,-87.119,"TVA","TVA","GE",_S],
    ["Grand Gulf-1",   "Grand Gulf",  "Unit 1","United States","operating","BWR","BWR-6",   1497,1533,"1974-09-04","1984-07-01","1985-07-01","", 32.008,-91.051,"Entergy","Entergy","GE",_S],
    ["Peach Bottom-2", "Peach Bottom","Unit 2","United States","operating","BWR","BWR-4",   1339,1373,"1968-01-31","1974-03-01","1974-07-05","", 39.759,-76.269,"Exelon","Exelon","GE",_S],
    ["Peach Bottom-3", "Peach Bottom","Unit 3","United States","operating","BWR","BWR-4",   1339,1373,"1968-09-25","1974-07-26","1974-12-23","", 39.759,-76.269,"Exelon","Exelon","GE",_S],
    ["Vogtle-1",       "Vogtle",      "Unit 1","United States","operating","PWR","PWR",     1217,1281,"1976-08-01","1987-03-27","1987-05-01","", 33.143,-81.762,"Georgia Power","Southern Nuclear","Westinghouse",_S],
    ["Vogtle-3",       "Vogtle",      "Unit 3","United States","operating","PWR","AP1000",  1117,1250,"2009-03-12","2023-04-01","2023-07-31","", 33.143,-81.762,"Georgia Power","Southern Nuclear","Westinghouse",_S],
    ["Vogtle-4",       "Vogtle",      "Unit 4","United States","operating","PWR","AP1000",  1117,1250,"2013-11-19","2024-03-01","2024-04-29","", 33.143,-81.762,"Georgia Power","Southern Nuclear","Westinghouse",_S],
    ["Turkey Point-3", "Turkey Point","Unit 3","United States","operating","PWR","PWR",      760, 800,"1967-04-27","1972-11-14","1972-12-14","", 25.433,-80.332,"FPL","FPL","Westinghouse",_S],
    ["Diablo Canyon-1","Diablo Canyon","Unit 1","United States","operating","PWR","PWR",    1122,1151,"1968-04-22","1984-11-28","1985-05-07","", 35.211,-120.854,"PG&E","PG&E","Westinghouse",_S],
    ["Diablo Canyon-2","Diablo Canyon","Unit 2","United States","operating","PWR","PWR",    1118,1162,"1970-12-09","1985-08-26","1986-03-13","", 35.211,-120.854,"PG&E","PG&E","Westinghouse",_S],
    # Planned
    ["Natrium-1",  "Kemmerer", "Unit 1","United States","proposed","SFR","Natrium",   345, 345,"","","","", 41.792,-110.538,"TerraPower","TerraPower","TerraPower/GEH",_S],
    ["CP-1",       "Carbon Free","Unit 1","United States","proposed","SMR-LWR","BWRX-300",300,300,"","","","", 33.000,-83.000,"Southern","Southern","GE Hitachi",_S],

    # ── BANGLADESH ─────────────────────────────────────────────────────────────
    ["Rooppur-1","Rooppur","Unit 1","Bangladesh","under construction","VVER","VVER-1200",1114,1200,"2017-11-30","","","", 24.065, 89.047,"BAEC","BAEC","Rosatom",_S],
    ["Rooppur-2","Rooppur","Unit 2","Bangladesh","under construction","VVER","VVER-1200",1114,1200,"2018-07-14","","","", 24.065, 89.047,"BAEC","BAEC","Rosatom",_S],

    # ── POLAND ─────────────────────────────────────────────────────────────────
    ["Lubiatowo-1","Lubiatowo-Kopalino","Unit 1","Poland","planned","PWR","AP1000",1117,1250,"","","","", 54.783, 17.850,"PEJ","PEJ","Westinghouse",_S],
    ["Lubiatowo-2","Lubiatowo-Kopalino","Unit 2","Poland","planned","PWR","AP1000",1117,1250,"","","","", 54.783, 17.850,"PEJ","PEJ","Westinghouse",_S],

    # ── GERMANY (shutdown context) ─────────────────────────────────────────────
    ["Emsland",    "Emsland",    "Unit 1","Germany","shutdown","PWR","PWR-Konvoi",1329,1400,"1982-08-12","1988-04-14","1988-06-20","2023-04-15", 52.470,  7.323,"PreussenElektra","PreussenElektra","KWU",_S],
    ["Isar-2",     "Isar",       "Unit 2","Germany","shutdown","PWR","PWR-Konvoi",1365,1475,"1982-09-15","1988-01-22","1988-04-09","2023-04-15", 48.603, 12.295,"PreussenElektra","PreussenElektra","KWU",_S],
]

# Country context table (GDP ~2023 USD, population ~2024)
COUNTRIES = [
    ["Argentina",      "Latin America",   "Upper middle income",    646075000000,  13935,  46200000,  145, 0.07, 50,   3],
    ["Armenia",        "Eurasia",         "Upper middle income",     19518000000,   6474,   3000000,    7, 0.28, 44,   1],
    ["Belgium",        "Europe",          "High income",            584697000000,  50114,  11600000,   85, 0.47, 68,   7],
    ["Brazil",         "Latin America",   "Upper middle income",   2173666000000,  10109, 216000000,  690, 0.02, 42,   2],
    ["Bulgaria",       "Europe",          "Upper middle income",     89580000000,  13326,   6500000,   45, 0.35, 44,   2],
    ["Canada",         "North America",   "High income",           2140086000000,  53372,  40000000,  600, 0.15, 60,  19],
    ["China",          "Asia",            "Upper middle income",  17794782000000,  12614,1410000000, 9450, 0.05, 41,  65],
    ["Czech Republic", "Europe",          "High income",            340459000000,  31820,  10900000,   85, 0.37, 36,   6],
    ["Egypt",          "Africa",          "Lower middle income",    395926000000,   3698, 110000000,  210, 0.00,  0,   0],
    ["Finland",        "Europe",          "High income",            300588000000,  53654,   5600000,   90, 0.30, 50,   5],
    ["France",         "Europe",          "High income",           3030904000000,  44460,  68100000,  485, 0.65, 68,  56],
    ["Germany",        "Europe",          "High income",           4082000000000,  48718,  84300000,  545, 0.00, 62,   0],
    ["India",          "Asia",            "Lower middle income",   3549919000000,   2485,1428000000, 1900, 0.03, 30,  22],
    ["Japan",          "Asia",            "High income",           4212945000000,  33834, 124500000,  980, 0.08, 50,  33],
    ["Mexico",         "Latin America",   "Upper middle income",   1365000000000,  10624, 130000000,  310, 0.04, 34,   2],
    ["Netherlands",    "Europe",          "High income",            999000000000,  57768,  17900000,  115, 0.04, 55,   1],
    ["Pakistan",       "Asia",            "Lower middle income",    338000000000,   1394, 236000000,  160, 0.05, 30,   6],
    ["Poland",         "Europe",          "High income",            811229000000,  22112,  36800000,  175, 0.00,  0,   0],
    ["Romania",        "Europe",          "Upper middle income",    348000000000,  17862,  19000000,   65, 0.19, 30,   2],
    ["Russia",         "Eurasia",         "Upper middle income",   2021420000000,  13817, 143800000, 1170, 0.20, 44,  37],
    ["Slovakia",       "Europe",          "High income",            132000000000,  24192,   5500000,   30, 0.57, 36,   5],
    ["South Africa",   "Africa",          "Upper middle income",    380000000000,   6193,  60400000,  235, 0.06, 44,   2],
    ["South Korea",    "Asia",            "High income",           1712793000000,  33147,  51700000,  590, 0.28, 46,  26],
    ["Spain",          "Europe",          "High income",           1582000000000,  32788,  48400000,  250, 0.20, 50,   7],
    ["Sweden",         "Europe",          "High income",            581000000000,  55360,  10500000,  140, 0.30, 50,   6],
    ["Switzerland",    "Europe",          "High income",            905000000000, 103199,   8700000,   65, 0.33, 55,   4],
    ["Turkey",         "Europe",          "Upper middle income",   1108022000000,  12985,  85300000,  335, 0.00,  0,   0],
    ["UAE",            "Middle East",     "High income",            504173000000,  51426,   9800000,  160, 0.20,  4,   4],
    ["Ukraine",        "Eurasia",         "Lower middle income",    173000000000,   4500,  37000000,  150, 0.55, 36,  15],
    ["United Kingdom", "Europe",          "High income",           3340032000000,  48913,  68300000,  315, 0.14, 68,   9],
    ["United States",  "North America",   "High income",          27360935000000,  81695, 334900000, 4300, 0.18, 55,  93],
    ["Bangladesh",     "Asia",            "Lower middle income",    437415000000,   2688, 171000000,   95, 0.00,  0,   0],
    ["Armenia",        "Eurasia",         "Upper middle income",     19518000000,   6474,   3000000,    7, 0.28, 44,   1],
]

POLICY_DOCS = [
    ["policy-us-001", "United States","DOE advanced nuclear strategy","strategy","Advanced nuclear fuel and demonstration policy","2024-01-01","Advanced reactors, SMR demonstrations, HALEU fuel supply, licensing modernization, clean firm power and industrial heat are recurring policy priorities."],
    ["policy-cn-001", "China","State nuclear expansion plan","strategy","Nuclear expansion and advanced reactor program","2024-01-01","Large PWR buildout continues alongside HTR-PM demonstration, fast reactor development and energy security framing."],
    ["policy-fr-001", "France","French energy planning document","strategy","Nuclear renaissance and EPR2 program","2024-01-01","France announced construction of six EPR2 units and potential for additional reactors. Energy sovereignty and decarbonization are primary drivers."],
    ["policy-ru-001", "Russia","Rosatom export strategy","technology","Fast reactor and closed fuel cycle development","2024-01-01","Fast reactor deployment, sodium-cooled technology, MOX fuel and closed fuel cycle strategy are emphasized."],
    ["policy-ca-001", "Canada","OPG SMR deployment program","project","Darlington SMR deployment BWRX-300","2024-01-01","SMR deployment, BWRX-300 licensing, grid reliability and clean electricity targets are emphasized."],
    ["policy-uk-001", "United Kingdom","UK nuclear strategy","strategy","Hinkley Point C and future nuclear","2024-01-01","Hinkley Point C EPR construction, SMR program evaluation, energy security and net zero targets."],
    ["policy-pl-001", "Poland","Polish nuclear energy program","strategy","First nuclear power plant program","2024-01-01","Energy security, coal replacement, AP1000 technology selection, supply chain development and EU financing."],
    ["policy-in-001", "India","Nuclear power expansion","strategy","DAE long-term nuclear expansion program","2024-01-01","Domestic PHWR fleet expansion, PFBR fast breeder reactor, Kudankulam expansion and thorium fuel cycle development."],
    ["policy-ar-001", "Argentina","CNEA nuclear plan","technology","CAREM SMR and nuclear expansion","2024-01-01","CAREM small modular reactor development, domestic engineering capability and long nuclear experience are highlighted."],
    ["policy-kr-001", "South Korea","KEPCO export strategy","strategy","APR1400 technology export and domestic expansion","2024-01-01","APR1400 export success (UAE), Shin Hanul expansion, SMR development (i-SMR) and hydrogen production."],
]


def create_dirty_sample_data() -> None:
    sample = config.RAW / "sample"
    sample.mkdir(parents=True, exist_ok=True)

    reactors = pd.DataFrame(RAW_REACTORS, columns=[
        "reactor_name", "plant_name", "unit_name", "country", "status", "reactor_type",
        "design_name", "net_capacity_mwe", "gross_capacity_mwe", "construction_start_date",
        "grid_connection_date", "commercial_operation_date", "shutdown_date", "latitude",
        "longitude", "owner", "operator", "vendor", "source_name"
    ])

    # Inject intentional dirty data to demonstrate cleaning pipeline
    reactors = pd.concat([reactors, reactors.iloc[[0]]], ignore_index=True)  # duplicate
    reactors["net_capacity_mwe"] = reactors["net_capacity_mwe"].astype(object)
    reactors.loc[len(reactors) - 1, "net_capacity_mwe"] = "1,345"           # comma in number
    reactors.loc[3, "status"] = "Under-Construction "                        # inconsistent format
    reactors.loc[12, "net_capacity_mwe"] = None                              # missing value

    reactors.to_csv(sample / "dirty_reactors_raw.csv", index=False)

    # Deduplicate COUNTRIES (Armenia appears twice by mistake above)
    seen = set()
    unique_countries = []
    for row in COUNTRIES:
        if row[0] not in seen:
            seen.add(row[0])
            unique_countries.append(row)

    countries = pd.DataFrame(unique_countries, columns=[
        "country", "region", "income_group", "gdp_current_usd", "gdp_per_capita",
        "population", "electricity_generation_twh", "nuclear_share_fraction",
        "nuclear_experience_years", "historical_completed_reactors"
    ])
    countries.to_csv(sample / "dirty_country_context_raw.csv", index=False)

    docs = pd.DataFrame(POLICY_DOCS, columns=[
        "document_id", "country", "source_name", "document_type", "title", "date", "text"
    ])
    docs.to_csv(sample / "policy_documents_raw.csv", index=False)
