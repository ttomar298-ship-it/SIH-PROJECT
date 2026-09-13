import os
import pandas as pd

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RAW_DIR = os.path.join(BASE_DIR, "backend", "data", "raw")
os.makedirs(RAW_DIR, exist_ok=True)

# 1. DILRMP State Land Records Data
DILRMP_DATA = """Sl. No.,State/UT,Total RORs,Total No. of Villages,Villages of CLR Completed (No.),Villages of CLR Completed (%)
1,Andman and Nicobar Islands,120449,205,205,100
2,Andhra Pradesh,27294315,17564,17344,98.75
3,Assam,4378822,23033,19687,85.47
4,Bihar,42533351,45949,45743,99.55
5,Chandigarh,5392,25,25,100
6,Chhattisgarh,22154450,19818,19672,99.26
7,Goa,789875,425,425,100
8,Gujarat,11940832,18389,18387,99.99
9,Haryana,4929960,7100,6885,96.97
10,Himachal Pradesh,1187349,21067,20922,99.31
11,Jammu and Kashmir,6591042,6850,6828,99.68
12,Jharkhand,2414830,32945,32707,99.28
13,Karnataka,16845472,30715,29404,95.73
14,Kerala,14281074,1674,1674,100
15,Ladakh,249,247,71,28.51
16,Lakshadweep,72425,24,24,100
17,Madhya Pradesh,45642133,55693,55678,99.97
18,Maharashtra,24007776,44798,44781,99.96
19,Manipur,611343,2715,548,20.18
20,Mizoram,356587,911,495,54.34
21,Nagaland,107830,1600,512,32
22,Nct of Delhi,67010,207,196,94.69
23,Odisha,14562018,51788,51726,99.88
24,Puducherry,298219,130,130,100
25,Punjab,5671959,13016,12731,97.81
26,Rajasthan,12228999,48719,47417,97.33
27,Sikkim,182596,421,413,98.1
28,Tamil Nadu,23201068,16810,16797,99.92
29,Telangana,12919557,10947,10190,93.08
30,Dadra and Nagar Haveli and Daman and Diu,96352,100,98,98
31,Tripura,1306362,897,897,100
32,Uttarakhand,1522960,16691,15820,94.78
33,Uttar Pradesh,22566485,109096,105593,96.79
34,West Bengal,48593416,42423,42240,99.57"""

# 2. MoSPI Real Infrastructure Projects in Andhra Pradesh
MOSPI_RAW = [
    {"name": "Interim Terminal Building at Vijayawada Airport", "sector": "Civil Aviation", "start": "2020-04-01", "target": "2023-03-01", "actual": "2023-03-01", "orig_cost": 611.8, "rev_cost": 611.8, "district": "Krishna", "lat": 16.5305, "lon": 80.7968},
    {"name": "Ext and Str. of Existing Runway 08/26 at Tirupati Airport", "sector": "Civil Aviation", "start": "2017-08-01", "target": "2020-02-01", "actual": "2021-12-01", "orig_cost": 177.1, "rev_cost": 177.1, "district": "Chittoor", "lat": 13.6324, "lon": 79.5434},
    {"name": "Construction of Permanent Campus for IISER at Jangalapalli", "sector": "Higher Education", "start": "2019-09-01", "target": "2022-09-01", "actual": "2023-01-01", "orig_cost": 588.72, "rev_cost": 588.72, "district": "Chittoor", "lat": 13.6828, "lon": 79.5100},
    {"name": "Construction of Permanent Campus for NITAP Phase 1b at Tadepalligudem", "sector": "Higher Education", "start": "2019-02-01", "target": "2020-09-01", "actual": "2022-06-01", "orig_cost": 186.0, "rev_cost": 205.0, "district": "West Godavari", "lat": 16.8150, "lon": 81.5270},
    {"name": "Construction of Permanent Campus for IIT Tirupati at Merlapaka", "sector": "Higher Education", "start": "2019-02-01", "target": "2020-06-01", "actual": "2022-12-01", "orig_cost": 655.34, "rev_cost": 655.34, "district": "Chittoor", "lat": 13.6288, "lon": 79.4192},
    {"name": "Residential Complex and OPD Block, AIIMS Mangalagiri", "sector": "Health and Family Welfare", "start": "2017-08-01", "target": "2019-03-01", "actual": "2021-03-01", "orig_cost": 272.19, "rev_cost": 272.54, "district": "Guntur", "lat": 16.4350, "lon": 80.5600},
    {"name": "Hospital and Teaching Block - AIIMS Guntur", "sector": "Health and Family Welfare", "start": "2018-03-01", "target": "2020-06-01", "actual": "2021-06-01", "orig_cost": 601.02, "rev_cost": 601.02, "district": "Guntur", "lat": 16.4400, "lon": 80.5700},
    {"name": "Development of Coastal Terminal at Krishnapatnam Port", "sector": "Petroleum", "start": "2017-07-01", "target": "2021-02-01", "actual": "2023-03-01", "orig_cost": 580.2, "rev_cost": 580.2, "district": "Nellore", "lat": 14.2500, "lon": 80.1200},
    {"name": "Sulphur Forming Unit in SRU", "sector": "Petroleum", "start": "2020-10-01", "target": "2021-08-01", "actual": "2021-08-01", "orig_cost": 210.94, "rev_cost": 210.94, "district": "Visakhapatnam", "lat": 17.6868, "lon": 83.2185},
    {"name": "RUF Pitch Loading Gantry", "sector": "Petroleum", "start": "2020-10-01", "target": "2022-11-01", "actual": "2022-11-01", "orig_cost": 332.61, "rev_cost": 332.61, "district": "Visakhapatnam", "lat": 17.6900, "lon": 83.2200},
    {"name": "220 KV Grid Supply Visakhapatnam", "sector": "Petroleum", "start": "2020-10-01", "target": "2021-03-01", "actual": "2021-08-01", "orig_cost": 303.4, "rev_cost": 303.4, "district": "Visakhapatnam", "lat": 17.7000, "lon": 83.2100},
    {"name": "SWRO II with LLPH Facilities", "sector": "Petroleum", "start": "2019-09-01", "target": "2020-07-01", "actual": "2021-09-01", "orig_cost": 196.26, "rev_cost": 196.26, "district": "Visakhapatnam", "lat": 17.6950, "lon": 83.2250},
    {"name": "Visakh Refinery Modernisation Project (VRMP)", "sector": "Petroleum", "start": "2016-07-01", "target": "2020-07-01", "actual": "2022-07-01", "orig_cost": 20928.0, "rev_cost": 26264.0, "district": "Visakhapatnam", "lat": 17.7100, "lon": 83.2300},
    {"name": "LPG BP Project Chittoor", "sector": "Petroleum", "start": "2019-07-01", "target": "2022-07-01", "actual": "2022-07-01", "orig_cost": 167.0, "rev_cost": 167.0, "district": "Chittoor", "lat": 13.2172, "lon": 79.1003},
    {"name": "Revamping of Vijayawada Terminal for Conversion to TOP", "sector": "Petroleum", "start": "2018-10-01", "target": "2021-10-01", "actual": "2022-03-01", "orig_cost": 316.2, "rev_cost": 316.2, "district": "Krishna", "lat": 16.5062, "lon": 80.6480},
    {"name": "Grass Root Petroleum TOP at Chutapuram", "sector": "Petroleum", "start": "2018-08-01", "target": "2021-04-01", "actual": "2021-12-01", "orig_cost": 466.0, "rev_cost": 466.0, "district": "Anantapur", "lat": 14.6819, "lon": 77.6006},
    {"name": "Revamping of Facilities at Vizag Coastal Terminal", "sector": "Petroleum", "start": "2018-04-01", "target": "2022-04-01", "actual": "2023-02-01", "orig_cost": 355.0, "rev_cost": 355.0, "district": "Visakhapatnam", "lat": 17.7150, "lon": 83.2400},
    {"name": "Rail Fed Depot at Guntakal", "sector": "Petroleum", "start": "2017-08-01", "target": "2021-04-01", "actual": "2021-03-01", "orig_cost": 384.58, "rev_cost": 384.58, "district": "Anantapur", "lat": 15.1667, "lon": 77.3667},
    {"name": "KG-DWN-98/2 Cluster II Deepwater Development Project", "sector": "Petroleum", "start": "2016-03-01", "target": "2020-06-01", "actual": "2022-06-01", "orig_cost": 34012.0, "rev_cost": 25090.0, "district": "East Godavari", "lat": 16.9891, "lon": 82.2475},
    {"name": "Multi Modal Logistics Park at Kakinada Port", "sector": "Railways", "start": "2016-08-01", "target": "2019-03-01", "actual": "2022-03-01", "orig_cost": 234.5, "rev_cost": 235.0, "district": "East Godavari", "lat": 16.9604, "lon": 82.2381},
    {"name": "Multi Modal Logistics Park at Visakhapatnam", "sector": "Railways", "start": "2013-01-01", "target": "2018-03-01", "actual": "2021-12-01", "orig_cost": 387.7, "rev_cost": 487.13, "district": "Visakhapatnam", "lat": 17.7200, "lon": 83.2500},
    {"name": "Kottavalasa - Koraput Railway Line Doubling", "sector": "Railways", "start": "2015-04-01", "target": "2022-03-01", "actual": "2024-03-01", "orig_cost": 2499.71, "rev_cost": 2499.71, "district": "Vizianagaram", "lat": 18.1167, "lon": 83.4167},
    {"name": "Vijayawada - Gudur 3rd Railway Line Project", "sector": "Railways", "start": "2015-04-01", "target": "2023-12-01", "actual": "2024-06-01", "orig_cost": 3246.26, "rev_cost": 3548.68, "district": "Krishna", "lat": 16.5100, "lon": 80.6500},
    {"name": "Vijayawada - Gudivada - Bhimavaram - Narsapur Doubling & Electrification", "sector": "Railways", "start": "2012-03-01", "target": "2020-03-01", "actual": "2022-03-01", "orig_cost": 1503.71, "rev_cost": 3377.0, "district": "West Godavari", "lat": 16.5400, "lon": 81.5200},
    {"name": "Gudur - Durgarajapatnam Port Railway Link", "sector": "Railways", "start": "2011-04-01", "target": "2016-03-01", "actual": "2022-03-01", "orig_cost": 761.37, "rev_cost": 761.37, "district": "Nellore", "lat": 14.1500, "lon": 79.8500},
    {"name": "Cumbum - Proddatur Railway Project", "sector": "Railways", "start": "2013-04-01", "target": "2018-03-01", "actual": "2023-03-01", "orig_cost": 829.0, "rev_cost": 829.0, "district": "Kadapa", "lat": 14.7500, "lon": 78.5500},
    {"name": "Duvvada - Vijayawada 3rd Line Railway Capacity Augmentation", "sector": "Railways", "start": "2015-04-01", "target": "2020-03-01", "actual": "2023-03-01", "orig_cost": 3873.07, "rev_cost": 3873.07, "district": "Visakhapatnam", "lat": 17.7000, "lon": 83.1500},
    {"name": "Guntur - Guntakal Railway Line Doubling (SCR)", "sector": "Railways", "start": "2016-04-01", "target": "2022-03-01", "actual": "2024-03-01", "orig_cost": 3631.0, "rev_cost": 3887.48, "district": "Guntur", "lat": 16.3000, "lon": 80.4500},
    {"name": "Nadikude - Srikalahasti New Broad Gauge Line", "sector": "Railways", "start": "2011-04-01", "target": "2021-03-01", "actual": "2024-03-01", "orig_cost": 2288.7, "rev_cost": 2643.25, "district": "Guntur", "lat": 16.5800, "lon": 79.9500},
    {"name": "Kotipalli - Narsapur New Railway Line (SCR)", "sector": "Railways", "start": "2001-12-01", "target": "2009-03-01", "actual": "2024-03-01", "orig_cost": 1045.2, "rev_cost": 2120.16, "district": "East Godavari", "lat": 16.6900, "lon": 82.0200},
    {"name": "Nandyal - Yerraguntla New Broad Gauge Line (SCR)", "sector": "Railways", "start": "1996-03-01", "target": "2009-02-01", "actual": "2020-03-01", "orig_cost": 164.36, "rev_cost": 1050.0, "district": "Kurnool", "lat": 15.4800, "lon": 78.4800},
    {"name": "Rehabilitation of New NH-544e Kodikonda - Madakasira", "sector": "Road Transport and Highways", "start": "2018-03-01", "target": "2018-11-01", "actual": "2021-07-01", "orig_cost": 504.19, "rev_cost": 504.19, "district": "Anantapur", "lat": 14.1000, "lon": 77.2500},
    {"name": "Rehabilitation and Upgradation of NH-565 Dornala - Tokapalli", "sector": "Road Transport and Highways", "start": "2018-01-01", "target": "2018-08-01", "actual": "2021-08-01", "orig_cost": 418.03, "rev_cost": 418.03, "district": "Prakasam", "lat": 15.9000, "lon": 79.1000},
    {"name": "Upgradation of NH-544dd Kalyandurg Section", "sector": "Road Transport and Highways", "start": "2018-03-01", "target": "2018-08-01", "actual": "2021-11-01", "orig_cost": 289.67, "rev_cost": 289.67, "district": "Anantapur", "lat": 14.5500, "lon": 77.1000},
    {"name": "Rehabilitation of NH-326a Srikakulam Section", "sector": "Road Transport and Highways", "start": "2018-03-01", "target": "2018-08-01", "actual": "2021-12-01", "orig_cost": 228.32, "rev_cost": 228.32, "district": "Srikakulam", "lat": 18.3000, "lon": 83.9000},
    {"name": "Rehabilitation and Upgradation of NH-340 Rayachoti Section", "sector": "Road Transport and Highways", "start": "2017-01-01", "target": "2017-08-01", "actual": "2021-06-01", "orig_cost": 319.28, "rev_cost": 319.28, "district": "Kadapa", "lat": 14.0500, "lon": 78.7500},
    {"name": "Construction of 4-lane Bypass to Vizianagaram Town on NH-43", "sector": "Road Transport and Highways", "start": "2017-02-01", "target": "2017-11-01", "actual": "2021-10-01", "orig_cost": 429.43, "rev_cost": 429.43, "district": "Vizianagaram", "lat": 18.1200, "lon": 83.4000},
    {"name": "Upgradation of Machilipatnam to Avanigadda NH-216 Section", "sector": "Road Transport and Highways", "start": "2016-11-01", "target": "2017-08-01", "actual": "2021-08-01", "orig_cost": 376.25, "rev_cost": 376.25, "district": "Krishna", "lat": 16.1800, "lon": 81.1300},
    {"name": "Rehabilitation of Existing NH-167 Adoni - Alur Section", "sector": "Road Transport and Highways", "start": "2016-11-01", "target": "2017-05-01", "actual": "2021-06-01", "orig_cost": 290.15, "rev_cost": 290.15, "district": "Kurnool", "lat": 15.6300, "lon": 77.2700},
    {"name": "Rehabilitation of Repalle to Eeppurpalem Section NH-216", "sector": "Road Transport and Highways", "start": "2017-01-01", "target": "2018-01-01", "actual": "2022-04-01", "orig_cost": 576.48, "rev_cost": 576.48, "district": "Guntur", "lat": 16.0200, "lon": 80.8500},
    {"name": "Four Laning of Gundugolanu - Devarapalli - Kovvuru NH-16 Section", "sector": "Road Transport and Highways", "start": "2018-03-01", "target": "2021-03-01", "actual": "2021-10-01", "orig_cost": 1532.62, "rev_cost": 2499.0, "district": "West Godavari", "lat": 16.9000, "lon": 81.4000},
    {"name": "Six Laning of Narasannapeta - Ranastalam Section of NH-16", "sector": "Road Transport and Highways", "start": "2017-12-01", "target": "2020-06-01", "actual": "2021-07-01", "orig_cost": 1323.15, "rev_cost": 1323.15, "district": "Srikakulam", "lat": 18.2500, "lon": 83.7500},
    {"name": "Six Laning of NH-140 Chittoor to Mallavaram Section", "sector": "Road Transport and Highways", "start": "2018-03-01", "target": "2020-03-01", "actual": "2021-09-01", "orig_cost": 1550.98, "rev_cost": 1550.98, "district": "Chittoor", "lat": 13.3500, "lon": 79.2000},
    {"name": "Six Laning of Anandapuram - Pendurthi - Anakapalli NH-16", "sector": "Road Transport and Highways", "start": "2018-02-01", "target": "2020-02-01", "actual": "2021-10-01", "orig_cost": 1959.0, "rev_cost": 1959.0, "district": "Visakhapatnam", "lat": 17.6800, "lon": 83.0000},
    {"name": "Dedicated Port Access Highway to Krishnapatnam Port", "sector": "Road Transport and Highways", "start": "2018-03-01", "target": "2020-03-01", "actual": "2022-03-01", "orig_cost": 314.43, "rev_cost": 314.43, "district": "Nellore", "lat": 14.2800, "lon": 80.0800},
    {"name": "6-Laning of Vijayawada Bypass from Gollapudi to Chinnakakani", "sector": "Road Transport and Highways", "start": "2019-11-01", "target": "2021-02-01", "actual": "2023-06-01", "orig_cost": 1601.1, "rev_cost": 1601.1, "district": "Krishna", "lat": 16.5200, "lon": 80.6000},
    {"name": "6-Laning of Vijayawada Bypass Chinna Avutupalli to Gollapudi", "sector": "Road Transport and Highways", "start": "2019-11-01", "target": "2021-02-01", "actual": "2023-06-01", "orig_cost": 1226.88, "rev_cost": 1226.88, "district": "Krishna", "lat": 16.5500, "lon": 80.6800},
    {"name": "Six Laning of Ranastalam - Anandapuram Section of NH-16", "sector": "Road Transport and Highways", "start": "2017-03-01", "target": "2020-03-01", "actual": "2022-03-01", "orig_cost": 1041.62, "rev_cost": 1187.1, "district": "Visakhapatnam", "lat": 17.9000, "lon": 83.4500},
    {"name": "Four Laning of NH-9 Vijayawada to Machilipatnam Corridor", "sector": "Road Transport and Highways", "start": "2016-01-01", "target": "2018-11-01", "actual": "2021-12-01", "orig_cost": 1134.97, "rev_cost": 1134.97, "district": "Krishna", "lat": 16.3500, "lon": 80.9000},
    {"name": "Vijayawada - Gundugolanu Section NH-16 Expansion", "sector": "Road Transport and Highways", "start": "2014-09-01", "target": "2017-02-01", "actual": "2021-03-01", "orig_cost": 1684.0, "rev_cost": 1684.0, "district": "Krishna", "lat": 16.7000, "lon": 80.9500},
    {"name": "Six Laning of Nellore - Chilkaluripet NH-16 Highway", "sector": "Road Transport and Highways", "start": "2011-11-01", "target": "2014-05-01", "actual": "2021-06-01", "orig_cost": 1535.0, "rev_cost": 1535.0, "district": "Nellore", "lat": 14.4426, "lon": 79.9865},
    {"name": "Tirupati - Tiruttani - Chennai Highway Corridor (NH-205)", "sector": "Road Transport and Highways", "start": "2011-04-01", "target": "2013-10-01", "actual": "2021-03-01", "orig_cost": 571.0, "rev_cost": 571.0, "district": "Chittoor", "lat": 13.5000, "lon": 79.6000},
    {"name": "Visakhapatnam Steel Plant Coke Oven Battery-5", "sector": "Steel", "start": "2011-12-01", "target": "2017-12-01", "actual": "2022-03-01", "orig_cost": 2858.0, "rev_cost": 2558.0, "district": "Visakhapatnam", "lat": 17.6500, "lon": 83.1800},
    {"name": "Polavaram National Multipurpose Irrigation Project", "sector": "Water Resources", "start": "2009-02-01", "target": "2020-03-01", "actual": "2024-06-01", "orig_cost": 10151.04, "rev_cost": 55548.87, "district": "West Godavari", "lat": 17.2500, "lon": 81.6500},
]

def main():
    # Save DILRMP data
    dilrmp_file = os.path.join(RAW_DIR, "dilrmp_land_records.csv")
    with open(dilrmp_file, "w", encoding="utf-8") as f:
        f.write(DILRMP_DATA)
    print(f"Saved DILRMP dataset to {dilrmp_file}")

    # Save MoSPI Real Projects data
    mospi_file = os.path.join(RAW_DIR, "mospi_real_projects.csv")
    df_mospi = pd.DataFrame(MOSPI_RAW)
    df_mospi.to_csv(mospi_file, index=False)
    print(f"Saved MoSPI real projects dataset to {mospi_file} ({len(df_mospi)} projects)")

if __name__ == "__main__":
    main()

