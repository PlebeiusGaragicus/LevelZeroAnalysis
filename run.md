```

(venv) myca@jupiter LevelZeroAnalysis % python3 fire_wait_times.py


------------------------------------------
>> loading dataset:  condensed-large
full_path='/Users/myca/My Drive/DATA/INTTERRA/condensed-large.csv'


------------------------------------------ DATA IMPORT:
/Users/myca/Downloads/[911-DATA-ANALYSIS]/LevelZeroAnalysis/fire_wait_times.py:21: DtypeWarning: Columns (19,27) have mixed types. Specify dtype option on import or set low_memory=False.
  data = pd.read_csv(full_path)
   unit     incident         incidentDate  ...    apparatusType enroutePriority arrivedPriority
0  M326  RP210000001  2021-01-01 00:04:10  ...              ALS             NaN             NaN
1    E1  RP210000001  2021-01-01 00:04:10  ...           Engine           Code3           Code3
2  M318  RP210000002  2021-01-01 00:06:19  ...              ALS             NaN             NaN
3    T4  RP210000002  2021-01-01 00:06:19  ...  Truck or aerial           Code3           Code3
4  M322  RP210000003  2021-01-01 00:06:44  ...              ALS             NaN             NaN

[5 rows x 50 columns]


------------------------------------------ MERGED ARRIVALS:
                    pfr_arrival         amr_arrival  wait_seconds
incident                                                         
MD210000003                 NaT 2021-02-12 17:07:15           0.0
MD210000004                 NaT                 NaT           0.0
MD210000008 2021-03-31 17:21:11 2021-03-31 17:16:48           0.0
MD210000010                 NaT 2021-06-12 14:13:16           0.0
MD210000011 2021-06-26 10:43:02 2021-06-26 10:43:40          38.0
MD210000014 2021-07-18 07:23:59 2021-07-18 07:24:32          33.0
MD210000019                 NaT                 NaT           0.0
MD210000023                 NaT                 NaT           0.0
MD210000028 2021-12-05 05:45:46 2021-12-05 05:29:40           0.0
MD210000029 2021-12-05 07:13:12                 NaT           0.0
>> exporting to:  /Users/myca/My Drive/DATA/INTTERRA/export- merged arrivals.csv


------------------------------------------ WAIT TIMES:
                    pfr_arrival         amr_arrival  wait_seconds  wait_time_minutes
incident                                                                            
MD230000008 2023-05-17 14:18:45 2023-05-17 14:20:27         102.0                1.7
MD230000020 2023-06-05 18:01:28 2023-06-05 18:03:17         109.0                1.8
MD230000032 2023-06-26 22:28:12 2023-06-26 22:29:26          74.0                1.2
MD230000048 2023-07-28 17:20:29 2023-07-28 17:23:19         170.0                2.8
RA210001124 2021-06-29 23:34:06 2021-06-29 23:37:26         200.0                3.3
>> exporting to:  /Users/myca/My Drive/DATA/INTTERRA/export- wait times.csv


------------------------------------------ INCIDENTS BY WEEK:
/Users/myca/Downloads/[911-DATA-ANALYSIS]/LevelZeroAnalysis/fire_wait_times.py:85: SettingWithCopyWarning: 
A value is trying to be set on a copy of a slice from a DataFrame.
Try using .loc[row_indexer,col_indexer] = value instead

See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
  incidents_waited_5['year_week'] = incidents_waited_5['pfr_arrival'].dt.isocalendar().year.astype(str) + '-W' + incidents_waited_5['pfr_arrival'].dt.isocalendar().week.astype(str).str.zfill(2)
/Users/myca/Downloads/[911-DATA-ANALYSIS]/LevelZeroAnalysis/fire_wait_times.py:86: SettingWithCopyWarning: 
A value is trying to be set on a copy of a slice from a DataFrame.
Try using .loc[row_indexer,col_indexer] = value instead

See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
  incidents_waited_10['year_week'] = incidents_waited_10['pfr_arrival'].dt.isocalendar().year.astype(str) + '-W' + incidents_waited_10['pfr_arrival'].dt.isocalendar().week.astype(str).str.zfill(2)
/Users/myca/Downloads/[911-DATA-ANALYSIS]/LevelZeroAnalysis/fire_wait_times.py:87: SettingWithCopyWarning: 
A value is trying to be set on a copy of a slice from a DataFrame.
Try using .loc[row_indexer,col_indexer] = value instead

See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
  incidents_waited_15['year_week'] = incidents_waited_15['pfr_arrival'].dt.isocalendar().year.astype(str) + '-W' + incidents_waited_15['pfr_arrival'].dt.isocalendar().week.astype(str).str.zfill(2)
    year_week  waited_15_plus  waited_10_plus  waited_5_plus  total_incidents
0    2020-W53               2               7             12              109
1    2021-W01               6              11             45              308
2    2021-W02              13              19             50              277
3    2021-W03               5               9             29              265
4    2021-W04               5               9             34              272
5    2021-W05               3               6             35              277
6    2021-W06              41              94            213              455
7    2021-W07              44              69            137              393
8    2021-W08               3               6             41              296
9    2021-W09               6              14             36              273
10   2021-W10               9              15             38              290
11   2021-W11               8              15             43              239
12   2021-W12               2               8             31              227
13   2021-W13               4               5             41              245
14   2021-W14               4               9             29              250
15   2021-W15               7              10             48              284
16   2021-W16              10              17             58              316
17   2021-W17               3              16             36              303
18   2021-W18               9              15             52              331
19   2021-W19               7              13             46              316
20   2021-W20               6              13             46              292
21   2021-W21              10              19             65              366
22   2021-W22              10              16             81              411
23   2021-W23               4              11             58              301
24   2021-W24               6              18             73              347
25   2021-W25              14              32            117              479
26   2021-W26              14              46            147              519
27   2021-W27               7              18             80              397
28   2021-W28              13              35            101              402
29   2021-W29              11              24             96              412
30   2021-W30               4              18             97              422
31   2021-W31              13              21             76              378
32   2021-W32               6              18            106              464
33   2021-W33              12              24             74              386
34   2021-W34               5               9             64              325
35   2021-W35               8              20             76              363
36   2021-W36              11              21             97              422
37   2021-W37               2              15             66              352
38   2021-W38               4              21             97              429
39   2021-W39               7              17             64              333
40   2021-W40              14              28            100              400
41   2021-W41              10              15             72              340
42   2021-W42              10              20             72              336
43   2021-W43               9              23            100              406
44   2021-W44               9              22             73              323
45   2021-W45              11              22             60              333
46   2021-W46               8              18             45              275
47   2021-W47               7              14             49              265
48   2021-W48               7              14             60              301
49   2021-W49               9              18            100              380
50   2021-W50              15              26             96              347
51   2021-W51               7              16             50              283
52   2021-W52              14              34            102              380
53   2022-W01              11              24             83              363
54   2022-W02               8              14             74              351
55   2022-W03               4              16             61              298
56   2022-W04               5              17             70              338
57   2022-W05               3               5             44              295
58   2022-W06               5              10             54              282
59   2022-W07               5               9             57              287
60   2022-W08               5              14             75              310
61   2022-W09              10              22             57              305
62   2022-W10               4              17             61              299
63   2022-W11               8              15             67              296
64   2022-W12               6              16             62              289
65   2022-W13               5               9             55              271
66   2022-W14               5              11             40              257
67   2022-W15               9              14             57              288
68   2022-W16              13              27             77              310
69   2022-W17               8              22             91              383
70   2022-W18              10              18             69              351
71   2022-W19              10              16             73              387
72   2022-W20              15              27             93              412
73   2022-W21              14              22             98              395
74   2022-W22              15              39            108              388
75   2022-W23              11              19            101              370
76   2022-W24               9              20             85              353
77   2022-W25              15              34            121              428
78   2022-W26              13              23             91              361
79   2022-W27              12              20             86              346
80   2022-W28              19              42            119              379
81   2022-W29              13              33            105              390
82   2022-W30              19              57            148              462
83   2022-W31              14              33            129              441
84   2022-W32              16              39            122              374
85   2022-W33              12              30            103              391
86   2022-W34              14              37            143              453
87   2022-W35              13              30            131              436
88   2022-W36              13              41            133              391
89   2022-W37              10              27            109              389
90   2022-W38              22              56            149              433
91   2022-W39              23              52            140              409
92   2022-W40              25              55            164              448
93   2022-W41              14              26            108              394
94   2022-W42              14              30             99              369
95   2022-W43               3              18            109              376
96   2022-W44              16              52            159              437
97   2022-W45              15              24            119              386
98   2022-W46              21              49            175              483
99   2022-W47              18              56            178              476
100  2022-W48              27              76            218              504
101  2022-W49              26              70            216              513
102  2022-W50              22              61            206              517
103  2022-W51              49             108            252              560
104  2022-W52              34              77            233              506
105  2023-W01              18              53            149              467
106  2023-W02              21              42            115              388
107  2023-W03              14              31            115              386
108  2023-W04              13              34            134              403
109  2023-W05              11              34            132              410
110  2023-W06              11              43            143              415
111  2023-W07              27              62            181              480
112  2023-W08             120             178            309              540
113  2023-W09              32              63            189              484
114  2023-W10              19              56            156              449
115  2023-W11              48              99            229              473
116  2023-W12              35              75            202              468
117  2023-W13              28              48            149              412
118  2023-W14              25              55            141              408
119  2023-W15              33              65            173              436
120  2023-W16              32              65            195              466
121  2023-W17              31              65            191              482
122  2023-W18              28              66            167              479
123  2023-W19              19              46            155              424
124  2023-W20              35              74            209              493
125  2023-W21              22              48            164              460
126  2023-W22              27              47            144              398
127  2023-W23              33              62            178              486
128  2023-W24              25              50            157              447
129  2023-W25              34              78            201              473
130  2023-W26              19              48            152              450
131  2023-W27              30              65            162              473
132  2023-W28              23              71            200              520
133  2023-W29              27              61            169              454
134  2023-W30              24              50            167              431
135  2023-W31              24              61            180              467
136  2023-W32              36              85            230              527
137  2023-W33              49             114            289              604
138  2023-W34              37              80            183              484
139  2023-W35              39              82            193              505
140  2023-W36              25              54            158              451
>> exporting to:  /Users/myca/My Drive/DATA/INTTERRA/export- incidents by week.csv


------------------------------------------ DATA VISUALIZATION:
ANALYSIS FOR DATASET: condensed-large
------------------------------------------
total_incidents=350613
average_wait_time=47.4 seconds
waited 5+ minutes on 15852 incidents
waited 10+ minutes on 5042 incidents
waited 15+ minutes on 2272 incidents

```