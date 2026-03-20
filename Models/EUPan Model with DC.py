#%%
import pandas as pd
import numpy as np
file_path = "Input Final.xlsx"

excel_data = pd.ExcelFile(file_path, engine='openpyxl')

Sets_data = excel_data.parse('Sets')

TechData_data = excel_data.parse('TechData')
Emission_data = excel_data.parse('Emission')
LoadShed_data = excel_data.parse('Load Shedding')

Country_data=excel_data.parse('Trans')
ComY_data=excel_data.parse('Transmission')
CO2_data=excel_data.parse('Fuel Cost')

Clustering_data=excel_data.parse('Clustering12')

New_Country_data=excel_data.parse('Trans')
df_TransE = excel_data.parse('Trans', header=None, usecols="G:AM", skiprows=3, nrows=33)
df_TransC = excel_data.parse('Trans', header=None, usecols="G:AM", skiprows=39, nrows=33)


df_emTarget = excel_data.parse('EmTarget', header=None, usecols="B:AI", skiprows=2, nrows=6)
df_Fuel = excel_data.parse('Fuel Cost', header=None, usecols="B:H", skiprows=3, nrows=15)
df_LandAV = excel_data.parse('Land', header=None, usecols="A:D", skiprows=2, nrows=33)

df_CAPEX = excel_data.parse('TechData', header=None, usecols="A:G", skiprows=2, nrows=15)
df_VOM = excel_data.parse('TechData', header=None, usecols="Q:W", skiprows=2, nrows=15)
df_FOM = excel_data.parse('TechData', header=None, usecols="I:O", skiprows=2, nrows=15)

#df_BR=excel_data.parse('Building rate', header=None, usecols="A:FJ", skiprows=2, nrows=15)
df_BR=excel_data.parse('Building rate', header=None, usecols="A:FJ", skiprows=23, nrows=15)
df_InitCap=excel_data.parse('Initial Capacity', header=None, usecols="A:AH", skiprows=1, nrows=15)
df_LoadGrowth=excel_data.parse('Load Growth', header=None, usecols="K:Q", skiprows=2, nrows=33)
df_Trans1 = excel_data.parse('Transmission', header=None, usecols="C:AI", skiprows=2, nrows=33)

df_AV=excel_data.parse('AV12', header=None, usecols="A:CW", skiprows=2, nrows=288)
df_Dem=excel_data.parse('Demand_Cluster12', header=None, usecols="A:AI", skiprows=1, nrows=288)
df_Price=excel_data.parse('Price', header=None, usecols="A:AI", skiprows=1, nrows=288)
df_DCProfile=excel_data.parse('DC', header=None, usecols="N:P", skiprows=1, nrows=288)



df_PriceGrowth=excel_data.parse('Price Growth', header=None, usecols="K:Q", skiprows=2, nrows=33)

#df_Target=excel_data.parse('Target', header=None, usecols="A:GQ", skiprows=2, nrows=15)
df_Targetmin=excel_data.parse('Target', header=None, usecols="A:GQ", skiprows=21, nrows=5)
df_Targetmax=excel_data.parse('Target', header=None, usecols="A:GQ", skiprows=30, nrows=5)

AI_demand=excel_data.parse('DC')
AI_demand2=excel_data.parse('DC')

#%%
from pyomo.environ import *
from pyomo.environ import SolverFactory
from pyomo.environ import value
def build_model(hl_max):
    
    model = ConcreteModel()


    t_data = Sets_data.iloc[0, 2:8].values
    h_data = Sets_data.iloc[1, 2:26].values
    k_data = Sets_data.iloc[2, 2:14].values
    c_data = Sets_data.iloc[3, 2:35].values
    j_data = Sets_data.iloc[4, 2:17].values
    jre_data = Sets_data.iloc[5, 2:6].values
    jes_data = Sets_data.iloc[6, 2:4].values
    jccs_data = Sets_data.iloc[7, 2:4].values


    # ============================================================
# 🔴 SET DEFINITIONS (Index Sets of the Optimization Model)
# ============================================================
# This section defines all static and dynamic index sets used
# throughout the model. These sets determine the dimensionality
# of parameters, variables, and constraints.
# ============================================================
    model.t = Set(initialize=t_data, doc='Set for year: 2025, 2030, 2035, 2050, 2045, 2050')
    model.h = Set (initialize=h_data, doc='Set for hour 1:24')
    model.c = Set (initialize=c_data, doc='Set for country: AL, AT, .... UK')
    model.k = Set (initialize=k_data, doc='Set for cluster K1:K12')
    model.j = Set (initialize=j_data, doc='Set for generation technology')
    model.jre = Set (initialize=jre_data, doc='Set for renewable technology')
    model.jes = Set (initialize=jes_data, doc='Set for storage technology')
    model.jccs = Set (initialize=jccs_data, doc='Set for carbon capture technology')
    model.r=Set (initialize=['FLAP', 'CEE', 'Nordic', 'Baltic', 'South', 'NW'])

    Country1_data=ComY_data.iloc[38:215,2].values
    Country2_data=ComY_data.iloc[38:215,3].values
    Distance_data=ComY_data.iloc[38:215,4]
    Candidate_line=ComY_data.iloc[38:215,5]
    Type_line=ComY_data.iloc[38:215,6].values
    Neighbourhood_Countries = list(zip(Country1_data,Country2_data,Distance_data))
    model.Ty = Set(initialize=['HVDC','HVDC-S', 'OHL', 'UG'], doc='Set for tranmsission line')

    model.hl = Param(initialize=2, mutable=True, doc='Slack parameter length of capacity expansion horizon')

    C1_data=Country_data.iloc[1:155,1].values
    C2_data=Country_data.iloc[1:155,2].values
    Neighbourhood_Regions = list(zip(C1_data,C2_data))


    TransDistance_data=list(zip(C1_data,C2_data))

    ldd_data = Country_data.iloc[1:155, 3]
    Distance_dict = dict(zip(TransDistance_data, ldd_data))

    model.N = Set(dimen=2, initialize=[(c,c1) for c in model.c for c1 in model.c if (c,c1) in Neighbourhood_Regions],doc='Dynamic set for making connection between neighboring countries' )


    ids = [f"id_{i}" for i in range(1, len(Country1_data) + 1)]
    model.ids=Set(initialize=ids, doc='Set for ID of trasnmission project for counteies where they have more than one candidate line')
    # Create list of triples (c, c1, id_)
    triples = list(zip(Type_line,Country1_data, Country2_data, ids))

    # Create dictionary mapping triple -> Candidate_line value
    line_param_dict = dict(zip(triples, Candidate_line))
    Distance_dict1 = dict(zip(triples, Distance_data))

    model.NN = Set(dimen=4, initialize=triples)

    Country_order = {country: i + 1 for i, country in enumerate(model.c)}
    model.ord_c = Param(model.c, initialize=Country_order)



    #%%
    # ============================================================
# 🔴 Reading input from Excel File and Map with Parameters
# ============================================================
# ============================================================
    
    CAPEX_data = {
        (j, t): df_CAPEX.iloc[i, 1 + t_idx]
        for i, j in enumerate(df_CAPEX.iloc[:, 0])
        for t_idx, t in enumerate(model.t)
    }

    VOM_data = {
        (j, t): df_VOM.iloc[i, 1 + t_idx]
        for i, j in enumerate(df_VOM.iloc[:, 0])
        for t_idx, t in enumerate(model.t)
    }

    FOM_data = {
        (j, t): df_FOM.iloc[i, 1 + t_idx]
        for i, j in enumerate(df_FOM.iloc[:, 0])
        for t_idx, t in enumerate(model.t)
    }

    eta_data =TechData_data.iloc[20:35, 1].values
    eta_df = TechData_data.iloc[20:35, [0, 1]]
    eta_map = {str(k).strip(): v for k, v in zip(eta_df.iloc[:, 0], eta_df.iloc[:, 1])}


    de_data =TechData_data.iloc[20:35, 6].values
    de_df = TechData_data.iloc[20:35, [5, 6]]
    de_map = {str(k).strip(): v for k, v in zip(de_df.iloc[:, 0], de_df.iloc[:, 1])}


    Cf_data =TechData_data.iloc[20:35, 11].values
    Cf_df = TechData_data.iloc[20:35, [10, 11]]
    Cf_map = {str(k).strip(): v for k, v in zip(Cf_df.iloc[:, 0], Cf_df.iloc[:, 1])}



    Pmin_data =TechData_data.iloc[20:35, 17].values
    Pmin_df = TechData_data.iloc[20:35, [16, 17]]
    Pmin_map = {str(k).strip(): v for k, v in zip(Pmin_df.iloc[:, 0], Pmin_df.iloc[:, 1])}

    Pmax_data =TechData_data.iloc[20:35, 21].values
    Pmax_df = TechData_data.iloc[20:35, [20, 21]]
    Pmax_map = {str(k).strip(): v for k, v in zip(Pmax_df.iloc[:, 0], Pmax_df.iloc[:, 1])}


    ConY_data =TechData_data.iloc[39:54, 1].values
    ConY_df = TechData_data.iloc[39:54, [0, 1]]
    ConY_map = {str(k).strip(): v for k, v in zip(ConY_df.iloc[:, 0], ConY_df.iloc[:, 1])}

    LT_data =TechData_data.iloc[39:54, 6].values
    LT_df = TechData_data.iloc[39:54, [5, 6]]
    LT_map = {str(k).strip(): v for k, v in zip(LT_df.iloc[:, 0], LT_df.iloc[:, 1])}

    DL_data =TechData_data.iloc[39:54, 11].values
    DL_df = TechData_data.iloc[39:54, [10, 11]]
    DL_map = {str(k).strip(): v for k, v in zip(DL_df.iloc[:, 0], DL_df.iloc[:, 1])}

    RU_data =TechData_data.iloc[59:74, 1].values
    RU_df = TechData_data.iloc[59:74, [0, 1]]
    RU_map = {str(k).strip(): v for k, v in zip(RU_df.iloc[:, 0], RU_df.iloc[:, 1])}


    EmFactor_data =Emission_data.iloc[3:18, 1].values
    EmFactor_df = Emission_data.iloc[3:18, [0, 1]]
    EmFactor_map = {str(k).strip(): v for k, v in zip(EmFactor_df.iloc[:, 0], EmFactor_df.iloc[:, 1])}



    LS_data =LoadShed_data.iloc[4:37, 1].values
    LS_df = LoadShed_data.iloc[4:37, [0, 1]]
    LS_map = {str(k).strip(): v for k, v in zip(LS_df.iloc[:, 0], LS_df.iloc[:, 1])}



    CVoLL_data =LoadShed_data.iloc[4:37, 10].values
    CVoLL_df = LoadShed_data.iloc[4:37, [9, 10]]
    CVoLL_map = {str(k).strip(): v for k, v in zip(CVoLL_df.iloc[:, 0], CVoLL_df.iloc[:, 1])}


    WF_data =Clustering_data.iloc[0:13, 2].values
    WF_df = Clustering_data.iloc[0:13, [1, 2]]
    WF_map = {str(k).strip(): v for k, v in zip(WF_df.iloc[:, 0], WF_df.iloc[:, 1])}


    Carbon_data =CO2_data.iloc[20:26, 3].values
    Carbon_df = CO2_data.iloc[20:26, [2, 3]]
    Carbon_map = {(k): v for k, v in zip(Carbon_df.iloc[:, 0], Carbon_df.iloc[:, 1])}


    Data12=ComY_data.iloc[38:215,8]
    Commition_data={(NN): Data12.iloc[i]
              for i, NN in enumerate(model.NN)}



    jre_filtered = ["Solar", "WindOn", "WindOff"]


    AV_data = {
        (k, h, c, e): df_AV.iloc[i, 2 + 3 * c_idx + e_idx]
        for i, (k, h) in enumerate(zip(df_AV.iloc[:, 0], df_AV.iloc[:, 1]))
        for c_idx, c in enumerate(model.c)
        for e_idx, e in enumerate(jre_filtered) 
    }

    Dem_data = {
        (k, h, c): df_Dem.iloc[i, 2 + c_idx]
        for i, (k, h) in enumerate(zip(df_Dem.iloc[:, 0], df_Dem.iloc[:, 1]))
        for c_idx, c in enumerate(model.c) 
    }

    Price_data = {
        (k, h, c): df_Price.iloc[i, 2 + c_idx]
        for i, (k, h) in enumerate(zip(df_Price.iloc[:, 0], df_Price.iloc[:, 1]))
        for c_idx, c in enumerate(model.c) 
    }
    Land_data = {
        (c, e): df_LandAV.iloc[i, 1 + e_idx]
        for i, c in enumerate(df_LandAV.iloc[:, 0])  # ← FIXED
        for e_idx, e in enumerate(jre_filtered)
    }



    EmTarget_data = {
        (t, c): df_emTarget.iloc[i, 1 + c_idx]
        for i, t in enumerate(df_emTarget.iloc[:, 0])
        for c_idx, c in enumerate(model.c)
    }


    FuelCost_data = {
        (j, t): df_Fuel.iloc[i, 1 + t_idx]
        for i, j in enumerate(df_Fuel.iloc[:, 0])
        for t_idx, t in enumerate(model.t)
    }


    Growth_data = {
        (c, t): df_LoadGrowth.iloc[i, 1 + t_idx]
        for i, c in enumerate(df_LoadGrowth.iloc[:, 0])
        for t_idx, t in enumerate(model.t)
    }


    PriceGrowth_data = {
        (c, t): df_PriceGrowth.iloc[i, 1 + t_idx]
        for i, c in enumerate(df_PriceGrowth.iloc[:, 0])
        for t_idx, t in enumerate(model.t)
    }


    t_idx1 = [2, 3, 4, 5,6]   # updated list
    n_t = len(t_idx1)

    BR_data = {
        (j, c, t): df_BR.iloc[i, 1 + c_idx*n_t + t_idx1.index(t)]
        for i, j in enumerate(df_BR.iloc[:, 0])   # technologies (rows)
        for c_idx, c in enumerate(model.c)        # countries
        for t in t_idx1                            # t = 1..5
    }



    t_idx2 = [1, 2, 3, 4, 5, 6]   # updated list
    n_t = len(t_idx2)
    '''
    Target_data = {
        (j, c, t): df_Target.iloc[i, 1 + c_idx*n_t + t_idx2.index(t)]
        for i, j in enumerate(df_Target.iloc[:, 0])   # technologies (rows)
        for c_idx, c in enumerate(model.c)        # countries
        for t in t_idx2                            # t = 1..5
    }
    '''
    Target_dataMin = {
        (j, c, t): df_Targetmin.iloc[i, 1 + c_idx*n_t + t_idx2.index(t)]
        for i, j in enumerate(df_Targetmin.iloc[:, 0])   # technologies (rows)
        for c_idx, c in enumerate(model.c)        # countries
        for t in t_idx2                            # t = 1..5
    }

    Target_dataMax = {
        (j, c, t): df_Targetmax.iloc[i, 1 + c_idx*n_t + t_idx2.index(t)]
        for i, j in enumerate(df_Targetmax.iloc[:, 0])   # technologies (rows)
        for c_idx, c in enumerate(model.c)        # countries
        for t in t_idx2                            # t = 1..5
    }

    ICap_data = {
        (j, c): df_InitCap.iloc[i, 1 + c_idx]
        for i, j in enumerate(df_InitCap.iloc[:, 0])
        for c_idx, c in enumerate(model.c)
    }


    Trans_data1 = {
        (g_row, g_col): df_Trans1.iloc[i, j]
        for i, g_row in enumerate(model.c)
        for j, g_col in enumerate(model.c) 
       if df_Trans1.iloc[i, j] > 0
       }




    TransE_data = {
        (g_row, g_col): df_TransE.iloc[i, j]
        for i, g_row in enumerate(model.c)
        for j, g_col in enumerate(model.c) 
       
       }

    TransC_data = {
        (g_row, g_col): df_TransC.iloc[i, j]
        for i, g_row in enumerate(model.c)
        for j, g_col in enumerate(model.c) 
       
       }
    
    AI_data =AI_demand.iloc[0:33, 1].values
    AI_df = AI_demand.iloc[0:33, [0, 1]]
    AI_map = {(k).strip(): v for k, v in zip(AI_df.iloc[:, 0], 0.75*AI_df.iloc[:, 1])}

    DCDem_data = {
        (row[13], row[14]): row[15] for idx, row in df_DCProfile.iterrows()
    }

     # IEA_Base
    AI_CAP =AI_demand.iloc[0:6, 5].values
    AICAP_df = AI_demand.iloc[0:6, 4:6]
    AICAP_map = {int(k): v for k, v in zip(AICAP_df.iloc[:, 0], 0.75*AICAP_df.iloc[:, 1])}


    #IEA_Lift Off
    AI_CAP1 =AI_demand.iloc[0:6, 6].values
    AICAP1_df = AI_demand.iloc[0:6, 4:7]
    AICAP1_map = {int(k): v for k, v in zip(AICAP1_df.iloc[:, 0], 0.75*AICAP1_df.iloc[:, 2])}


    #IEA_High Efficiency
    AI_CAP2 =AI_demand.iloc[0:6, 7].values
    AICAP2_df = AI_demand.iloc[0:6, 4:8]
    AICAP2_map = {int(k): v for k, v in zip(AICAP2_df.iloc[:, 0], 0.75*AICAP2_df.iloc[:, 3])}

    #IEA_Headwinds
    AI_CAP3 =AI_demand.iloc[0:6, 8].values
    AICAP3_df = AI_demand.iloc[0:6, 4:9]
    AICAP3_map = {int(k): v for k, v in zip(AICAP3_df.iloc[:, 0], 0.75*AICAP3_df.iloc[:, 4])}

    #IEA_Pessimistic - Deflation
    AI_CAP4 =AI_demand.iloc[0:6, 9].values
    AICAP4_df = AI_demand.iloc[0:6, 4:10]
    AICAP4_map = {int(k): v for k, v in zip(AICAP4_df.iloc[:, 0], 0.75*AICAP4_df.iloc[:, 5])}

    #IEA_Pessimistic - Med
    AI_CAP5 =AI_demand.iloc[0:6, 10].values
    AICAP5_df = AI_demand.iloc[0:6, 4:11]
    AICAP5_map = {int(k): v for k, v in zip(AICAP5_df.iloc[:, 0], 0.75*AICAP5_df.iloc[:, 6])}

    #IEA_Pessimistic - End
    AI_CAP6 =AI_demand.iloc[0:6, 11].values
    AICAP6_df = AI_demand.iloc[0:6, 4:12]
    AICAP6_map = {int(k): v for k, v in zip(AICAP6_df.iloc[:, 0], 0.75*AICAP6_df.iloc[:, 7])}







    # ICIS_Base
    AI_CAP11 =AI_demand2.iloc[10:16, 5].values
    AICAP11_df = AI_demand2.iloc[10:16, 4:6]
    AICAP11_map = {int(k): v for k, v in zip(AICAP11_df.iloc[:, 0], 0.75*AICAP11_df.iloc[:, 1])}


    #ICIS_Collops Off
    AI_CAP12 =AI_demand2.iloc[10:16, 6].values
    AICAP12_df = AI_demand2.iloc[10:16, 4:7]
    AICAP12_map = {int(k): v for k, v in zip(AICAP12_df.iloc[:, 0], 0.75*AICAP12_df.iloc[:, 2])}


    #ICIS_High Efficiency
    AI_CAP13 =AI_demand2.iloc[10:16, 7].values
    AICAP13_df = AI_demand2.iloc[10:16, 4:8]
    AICAP13_map = {int(k): v for k, v in zip(AICAP13_df.iloc[:, 0], 0.75*AICAP13_df.iloc[:, 3])}

    #ICIS_Headwinds
    AI_CAP14 =AI_demand2.iloc[10:16, 8].values
    AICAP14_df = AI_demand2.iloc[0:6, 4:9]
    AICAP14_map = {int(k): v for k, v in zip(AICAP14_df.iloc[:, 0], 0.75*AICAP14_df.iloc[:, 4])}

    #ICIS_Pessimistic - Deflation
    AI_CAP15 =AI_demand2.iloc[10:16, 9].values
    AICAP15_df = AI_demand2.iloc[10:16, 4:10]
    AICAP15_map = {int(k): v for k, v in zip(AICAP15_df.iloc[:, 0], 0.75*AICAP15_df.iloc[:, 5])}
    
    #ICIS_Pessimistic - Med
    AI_CAP16 =AI_demand2.iloc[10:16, 10].values
    AICAP16_df = AI_demand2.iloc[10:16, 4:11]
    AICAP16_map = {int(k): v for k, v in zip(AICAP16_df.iloc[:, 0], 0.75*AICAP16_df.iloc[:, 6])}

    #ICIS_Pessimistic - End
    AI_CAP17 =AI_demand2.iloc[10:16, 11].values
    AICAP17_df = AI_demand2.iloc[10:16, 4:12]
    AICAP17_map = {int(k): v for k, v in zip(AICAP17_df.iloc[:, 0], 0.75*AICAP17_df.iloc[:, 7])}




    # McKinsey_Base
    AI_CAP21 = AI_demand2.iloc[20:28, 5].values
    AICAP21_df = AI_demand2.iloc[20:26, 4:6]
    AICAP21_map = {int(k): v for k, v in zip(AICAP21_df.iloc[:, 0], 0.75 * AICAP21_df.iloc[:, 1])}


    # McKinsey_Lift Off
    AI_CAP22 = AI_demand2.iloc[20:28, 6].values
    AICAP22_df = AI_demand2.iloc[20:26, 4:7]
    AICAP22_map = {int(k): v for k, v in zip(AICAP22_df.iloc[:, 0], 0.75 * AICAP22_df.iloc[:, 2])}


    # McKinsey_High Efficiency
    AI_CAP23 = AI_demand2.iloc[20:28, 7].values
    AICAP23_df = AI_demand2.iloc[20:26, 4:8]
    AICAP23_map = {int(k): v for k, v in zip(AICAP23_df.iloc[:, 0], 0.75 * AICAP23_df.iloc[:, 3])}


    # McKinsey_Headwinds
    AI_CAP24 = AI_demand2.iloc[20:28, 8].values
    AICAP24_df = AI_demand2.iloc[20:26, 4:9]
    AICAP24_map = {int(k): v for k, v in zip(AICAP24_df.iloc[:, 0], 0.75 * AICAP24_df.iloc[:, 4])}
    
    
    #McKinsey_Pessimistic - Deflation
    AI_CAP25 =AI_demand2.iloc[20:28, 9].values
    AICAP25_df = AI_demand2.iloc[20:26, 4:10]
    AICAP25_map = {int(k): v for k, v in zip(AICAP25_df.iloc[:, 0], 0.75*AICAP25_df.iloc[:, 5])}
    
    #McKinsey_Pessimistic - Med
    AI_CAP26 =AI_demand2.iloc[20:28, 10].values
    AICAP26_df = AI_demand2.iloc[20:26, 4:11]
    AICAP26_map = {int(k): v for k, v in zip(AICAP26_df.iloc[:, 0], 0.75*AICAP26_df.iloc[:, 6])}

    #MsKinsey_Pessimistic - End
    AI_CAP27 =AI_demand2.iloc[20:28, 11].values
    AICAP27_df = AI_demand2.iloc[20:26, 4:12]
    AICAP27_map = {int(k): v for k, v in zip(AICAP27_df.iloc[:, 0], 0.75*AICAP27_df.iloc[:, 7])}

    

    #%%
    # ============================================================
# 🔵 PARAMETER DEFINITIONS (Model Input Data)
# ============================================================
# This section defines all exogenous data of the model.
# Parameters represent technical, economic, and demand data
# and remain fixed during optimization.
# ============================================================

    model.dur=Param(initialize=5, doc='Duration of time periods (year)')
    model.cc_fix= Param(model.j,model.t, initialize=CAPEX_data, doc='Capital Cost of Technology j at year t (EURO/kW)')
    model.VOM= Param(model.j,model.t, initialize=VOM_data, doc='Variable Operation Cost of Technology j at year t (EURO/MWh)')
    model.FOM= Param(model.j,model.t, initialize=FOM_data, doc='Fixed Operation Cost of Technology j at year t (EURO/KW-yr)')
    model.eta =Param(model.j, initialize=eta_map, doc='Efficiency of Technology j (%)')
    model.de=Param(model.j,initialize=de_map, doc='De-rating Factor of Technology j(%)')
    model.CF= Param(model.j,initialize=Cf_map, doc='Capacity Factor of Technology j(%)')
    model.Pmin= Param(model.j,initialize=Pmin_map, doc='Minimum Power Generation of Technology j as percentage of rated power (%)')
    model.Pmax= Param(model.j,initialize=Pmax_map, doc='Maximum Power Generation of Technology j as percentage of rated power (%)')
    #model.ConY= Param(model.j,initialize=ConY_map)
    model.ComY=Param(model.NN, initialize=Commition_data, doc='Construction time of Technology j (year)')
    model.LT= Param(model.j,initialize=LT_map,  doc='Effective Life-time of Technology j (year)')
    model.DL= Param(model.j,initialize=DL_map, doc='Self Consumption/ loss of technology j (%)')
    model.RU= Param(model.j,initialize=RU_map, doc='Ramp-up of power  output for technology j as percentage of rated output (%)')
    model.RD= Param(model.j,initialize=RU_map, doc='Ramp-down of power output for technology j as percentage of rated output (%)')
    model.yc= Param(model.j,initialize=EmFactor_map, doc='Emission Factor of Technology j')
    model.CVoLL=Param(model.c,initialize=CVoLL_map, doc='Value of Lost of Load in country c (EURO/MWh)')
    model.WF=Param(model.k,initialize=WF_map, doc='Weight of Cluster k')
    model.ct= Param(model.t, initialize=Carbon_map, doc='Carbon Cost (EURO/ton CO2)')
    model.AV= Param(model.k, model.h, model.c, model.jre, initialize=AV_data, mutable=True, doc='Availability of renewable technology at cluster k, hour h, country c, technology jre')


    hydro_av_c = {
        'AL': 0.45,  # Albania
        'AT': 0.48,  # Austria
        'BE': 0.3,  # Belgium
        'BA': 0.28,  # Bosnia and Herzegovina
        'BG': 0.40,  # Bulgaria
        'HR': 0.45,  # Croatia
        'CZ': 0.42,  # Czech Republic
        'DK': 0,  # Denmark
        'EE': 0,  # Estonia
        'FI': 0.45,  # Finland
        'FR': 0.24,  # France
        'DE': 0.48,  # Germany
        'GR': 0.2,  # Greece
        'HU': 0.46,  # Hungary
        'IE': 0.54,  # Ireland
        'IT': 0.38,  # Italy
        'LV': 0.4,  # Latvia
        'LT': 0.43,  # Lithuania
        'LU': 0.41,  # Luxembourg
        'ME': 0.45,  # Montenegro
        'NL': 0,  # Netherlands
        'MK': 0.32,  # North Macedonia
        'NO': 0.48,  # Norway
        'PL': 0.28,  # Poland
        'PT': 0.38,  # Portugal
        'RO': 0.32,  # Romania
        'RS': 0.45,  # Serbia
        'SI': 0.45,  # Slovenia
        'SK': 0.48,  # Slovakia
        'ES': 0.42,  # Spain
        'SE': 0.52,  # Sweden
        'CH': 0.48,  # Switzerland
        'UK': 0.40   # United Kingdom
    }



    for k in model.k:
        for h in model.h:      # only because AV is indexed by h
            for c in model.c:
                model.AV[k, h, c, 'Hydro'] = hydro_av_c[c]

                   
    model.Dem=Param(model.k,model.h,model.c, initialize=Dem_data, doc='Electricity demand at cluster k hour h and country c (MWh) at 2025')

    model.LandAV=Param(model.c,model.jre, initialize=Land_data, doc='Land Availability for renewable at country c and technology jre (GW/km2)')
    model.EmTarget=Param(model.t,model.c, initialize=EmTarget_data, doc='Carbon budget at country c (kton CO2)')
    model.FC=Param(model.j,model.t,initialize=FuelCost_data, doc='Fuel Cost for technology j at year t (EURO/MWh)')
    model.growth=Param(model.c,model.t,initialize=Growth_data, doc='Demand grwoth rate at country c for year t')

    model.BR=Param(model.j,model.c,model.t, initialize=BR_data, doc='Building rate for technology j at country c at year t (GW)')
    model.ICap=Param(model.j,model.c,initialize=ICap_data, doc='Initial capacity for technology j at country c  (MW)')
    model.Self=Param(model.jes, initialize={'Battery':0.0125, 'PumpHy':0}, doc='Self charge for storage')


    model.PLmaxe=Param(model.c,model.c,initialize=TransE_data, doc='Existing cross-border technology between neighboring countries in MW')
    model.PLmaxc=Param(model.c,model.c,initialize=TransC_data,doc='Candidate cross-border technology between neighboring countries in MW')
    model.NE = Set(dimen=2,initialize=model.PLmaxe.keys(), doc='Set of region pairs with nonzero pipeline distances')

    model.TICP = Param(
        model.Ty,
        initialize={
            'HVDC': 458,
            'HVDC-S': 1368,
            'OHL': 288,
            'UG': 1368
        },
        doc='1000 Eur/MW.km transmission line'
    )

    model.TL = Param(
        model.Ty,
        initialize={
            'HVDC': 0.00005,
            'HVDC-S': 0.00007,
            'OHL': 0.0001,
            'UG': 0.00008
        },
        doc='% loss of transmission line with different type (HVDC, Underground Cable, Overhead Line, UnderSea Cable)'
    )

    model.Dist=Param(model.N,initialize=Distance_dict, doc='km distance between neighboring countries')


    model.TargetMin= Param(model.j,model.c,model.t, initialize=Target_dataMin, doc='Minimum Building rate for technology and storage according to TYNDP')
    model.TargetMax= Param(model.j,model.c,model.t, initialize=Target_dataMax, doc='Minimum Building rate for technology and storage according to TYNDP')



    def dfc_init(model, t):
        r = 0.06
        return round((1 / (1 + r)) ** (5 * (t - 1)), 2)

    model.dfc = Param(model.t, initialize=dfc_init, doc="Discount factor for capital costs at 5-year intervals")


    def dfo_init(model, t):
        r = 0.06
        return round(sum(1 / (1 + r)**(5*(t - 1) + k) for k in range(1, 6)), 2)
    model.dfo = Param(model.t, initialize=dfo_init, doc="Discount factor for OPEX over each 5-year block")


    def TPowerDem_init(model, c, t, k, h):
        return ((1+model.growth[c,t]) * model.Dem[k,h,c])
    model.TDem = Param(model.c, model.t, model.k, model.h, initialize=TPowerDem_init, doc='Final houry demand for country c at year t, cluster k and hour h for future years (MWh)')

    def AnnualDemand_init(model, c, t):
        return sum(
            model.TDem[c, t, k, h] * model.WF[k]
            for k in model.k
            for h in model.h
        )

    model.AnnualDemand = Param(model.c, model.t, initialize=AnnualDemand_init)


    model.Curt=Param(initialize=200, doc='Penalty for renewable curtailment (EURO/MWh)')

    model.DCProfile=Param(model.k,model.h,initialize=DCDem_data, doc='Normalized data centre load profile (p.u)')
    model.IntCap=Param(model.c,initialize=AI_map, doc='Initial Capacity for Data Centre at Coutry c (MW)')
    
    
    model.GF=Param(model.c, initialize=0,mutable=True, doc='Growth factor for data centre capacity between 2025 and 2030')

    GF_c = {
    'AL': 0.0000,
    'AT': 0.1378,
    'BE': 0.0944,
    'BA': 0.0000,
    'BG': 0.0069,
    'HR': 0.0759,
    'CZ': 0.0095,
    'DK': 0.0486,
    'EE': 0.0069,
    'FI': 0.1251,
    'FR': 0.1040,
    'DE': 0.0990,
    'GR': 0.4875,
    'HU': 0.0222,
    'IE': 0.0577,
    'IT': 0.2981,
    'LV': 0.0069,
    'LT': 0.0122,
    'LU': 0.0090,
    'ME': 0.0000,
    'NL': 0.0455,
    'MK': 0.0000,
    'NO': 0.1432,
    'PL': 0.0650,
    'PT': 0.9314,
    'RO': 0.1014,
    'RS': 0.0000,
    'SI': 0.0069,
    'SK': 0.0562,
    'ES': 0.3050,
    'SE': 0.1216,
    'CH': 0.0155,
    'UK': 0.0786
}

    for c in model.c:
      model.GF[c] = GF_c[c]


    # ============================================================
# 🟣 DATA-CENTRE CAPACITY PATHWAYS – SCENARIO DEFINITION
# ============================================================
# This section defines the data-centre capacity expansion
# pathways for the 21 analysed scenarios.
#
# Each scenario represents a different planning assumption
# (e.g., demand growth).
#
# To run a specific scenario, only the corresponding constraints
# need to be activated or modified. The core model formulation,
# input parameters, and sets remain unchanged.
#
# ============================================================
    #IEA Scenarios
    
    model.TotCap=Param(model.t,initialize=AICAP_map, doc='Data Centre Capacity Target at year t (MW) for IEA Base Scenario')
    model.TotCap1=Param(model.t,initialize=AICAP1_map, doc='Data Centre Capacity Target at year t (MW) for IEA Lift-Off Scenario')
    model.TotCap2=Param(model.t,initialize=AICAP2_map, doc='Data Centre Capacity Target at year t (MW) for IEA High-Eff Scenario')
    model.TotCap3=Param(model.t,initialize=AICAP3_map, doc='Data Centre Capacity Target at year t (MW) for IEA Headwinds Scenario')
    model.TotCap4=Param(model.t,initialize=AICAP4_map, doc='Data Centre Capacity Target at year t (MW) for IEA Pessimistic Def Scenario')
    model.TotCap5=Param(model.t,initialize=AICAP5_map, doc='Data Centre Capacity Target at year t (MW) for IEA Pessimistic Med Scenario')
    model.TotCap6=Param(model.t,initialize=AICAP6_map, doc='Data Centre Capacity Target at year t (MW) for IEA Pessimistic End Scenario')
    
    # ICIS Scenarios

    model.TotCap11=Param(model.t,initialize=AICAP11_map, doc='Data Centre Capacity Target at year t (MW) for ICIS Base Scenario')
    model.TotCap12=Param(model.t,initialize=AICAP12_map, doc='Data Centre Capacity Target at year t (MW) for ICIS Lift-Off Scenario')
    model.TotCap13=Param(model.t,initialize=AICAP13_map, doc='Data Centre Capacity Target at year t (MW) for ICIS High-Eff Scenario')
    model.TotCap14=Param(model.t,initialize=AICAP14_map, doc='Data Centre Capacity Target at year t (MW) for ICIS Headwinds Scenario')
    model.TotCap15=Param(model.t,initialize=AICAP15_map, doc='Data Centre Capacity Target at year t (MW) for ICIS Pessimistic Def Scenario')
    model.TotCap16=Param(model.t,initialize=AICAP16_map, doc='Data Centre Capacity Target at year t (MW) for ICIS Pessimistic Med Scenario')
    model.TotCap17=Param(model.t,initialize=AICAP17_map, doc='Data Centre Capacity Target at year t (MW) for ICIS Pessimistic End Scenario')
    
    
    # McKinsey Scenarios

    model.TotCap21=Param(model.t,initialize=AICAP21_map, doc='Data Centre Capacity Target at year t (MW) for McKinsey Base Scenario')
    model.TotCap22=Param(model.t,initialize=AICAP22_map, doc='Data Centre Capacity Target at year t (MW) for McKinsey Lift-Off Scenario')
    model.TotCap23=Param(model.t,initialize=AICAP23_map, doc='Data Centre Capacity Target at year t (MW) for McKinsey High-Eff Scenario')
    model.TotCap24=Param(model.t,initialize=AICAP24_map, doc='Data Centre Capacity Target at year t (MW) for McKinsey Headwinds Scenario')
    model.TotCap25=Param(model.t,initialize=AICAP25_map, doc='Data Centre Capacity Target at year t (MW) for McKinsey Pessimistic Def Scenario')
    model.TotCap26=Param(model.t,initialize=AICAP26_map, doc='Data Centre Capacity Target at year t (MW) for McKinsey Pessimistic Med Scenario')
    model.TotCap27=Param(model.t,initialize=AICAP27_map, doc='Data Centre Capacity Target at year t (MW) for McKinsey Pessimistic End Scenario')



    #%%
    
    # ============================================================
# 🟢 DECISION VARIABLES
# ============================================================
# This section defines all endogenous decision variables of
# the optimization model. 
# ============================================================
    
    
    model.E = Set(dimen=2, initialize=[(c,c1) for (c,c1) in model.N if c < c1])

    model.Y = Var(model.E, model.t, within=Binary, doc='Binary variable for new tranmsission line between two neighboring countries at year t')
    model.AY = Var(model.E, model.t, within=Integers, doc='Available cross-border line between negiboring countries ')


    model.TotalDem=Var(model.c,model.t,model.k,model.h, domain=NonNegativeReals, doc='Total demand including base and demand associated with AI in country c year t cluster k and hour h (MWh)' )
   
    model.CapAI=Var(model.t,model.c,domain=NonNegativeReals, doc='Installed capacity of Data Centre in year t at country c (MW)' )
    model.CapNewAI=Var(model.t,model.c,domain=NonNegativeReals, doc='New capacity of Data Centre in year t at country c (MW)')
    model.DCapNewAI=Var(model.t,model.c,domain=NonNegativeReals, doc='Decommissioned capacity of Data Centre in year t at country c (MW)')

    model.ProfileDC=Var(model.c,model.t,model.k,model.h, domain=NonNegativeReals, doc='Final Data Centre load profile in country c year t cluster k and hour h (MWh)')

    model.PL=Var(model.E,model.t,model.k,model.h, within=Reals, doc='Power Flow between country c,c1 at  year t cluster k and hour h (MWh)')
    model.PLI=Var(model.c,model.c,model.t, within=NonNegativeReals, doc='New Cross-border tranmsission line invetsemtn between countries at year t (MW)')
    model.L=Var(model.c,model.c,model.t, within=NonNegativeReals, doc='Available Cross-border tranmsission line invetsemtn between countries at year t (MW)')

    model.PG = Var(model.j, model.c, model.t, model.k, model.h, domain=NonNegativeReals, doc='Power generation from technology j at year t cluster k and hour h (MWh)')
    model.PeakDemand = Var(model.t, domain=NonNegativeReals, doc='Whole-system Peak demand at year t (MWh)')

    model.CAP = Var(model.j, model.c, model.t, domain=NonNegativeReals, doc='Available capacity of technology j in country c at year t (MW)')

    model.DCAP = Var(model.j, model.c, model.t, domain=NonNegativeReals, doc='Decommissioned capacity of technology j in country c at year t (MW)')

    model.CAPnew = Var(model.j, model.c, model.t, domain=NonNegativeReals, doc='New investment capacity of technology j in country c at year t (MWh)')

    model.CH = Var(model.j, model.c, model.t, model.k, model.h, domain=NonNegativeReals, doc='Charging value by storage tecnology jes in country c at year t cluster k and hour h (MWh)')
    model.DC = Var(model.j, model.c, model.t, model.k, model.h, domain=NonNegativeReals, doc='Discharging value by storage tecnology jes in country c at year t cluster k and hour h (MWh)')
    model.LC = Var(model.c, model.t, model.k, model.h, domain=NonNegativeReals, doc='Value of renewable curtailment in country c at year t cluster k and hour h (MWh)')
    model.LS = Var(model.c, model.t, model.k, model.h, domain=NonNegativeReals, doc='Value of lost of load in country c at year t cluster k and hour h (MWh)')
    model.Rup = Var(model.j, model.c, model.t, model.k, model.h, domain=NonNegativeReals, doc='Ramp-up generation by technology j in country c at year t cluster k and hour h (MWh)')
    model.Rdown = Var(model.j, model.c, model.t, model.k, model.h, domain=NonNegativeReals, doc='Ramp-down generation by technology j in country c at year t cluster k and hour h (MWh)')
    model.Vf = Var(model.j, model.c, model.t, domain=NonNegativeReals, doc='Fuel consumption by technology j in country c at year t cluster k and hour h (MWh)')
    model.S = Var(model.jes, model.c, model.t, model.k, model.h, domain=NonNegativeReals, doc='Stored energy by technology jes in country c at year t cluster k and hour h (MWh)')
    model.Sinit = Var(model.jes, model.c, model.t, domain=NonNegativeReals, doc='Initial stored energy by technology j in country c at year t cluster k and hour h (MWh)')
    model.Slack=Var(model.t,model.c,within=NonNegativeReals, doc='Slack variable for overshooting from the carbon budget')

    model.em=Var(model.t,model.c,within=Reals, doc=' Total emission at year t in country c (ton CO2)')
    model.TIC=Var( within=NonNegativeReals, doc=' Total transmission invetsment cost (EURO)')
    model.FCC=Var(model.t,within=NonNegativeReals, doc=' CAPEX for generation/storage invetsment cost at year t (EURO)')
    model.FuelC=Var(model.t,within=NonNegativeReals, doc=' Fuel cost at year t (EURO)')
    model.FOC=Var(model.t,within=NonNegativeReals, doc=' Variable O&M cost at year t (EURO)')
    model.FFC=Var(model.t,within=NonNegativeReals, doc=' Fixed opweration cost at year t (EURO)')
    model.CC=Var(model.t,within=Reals, doc=' Carbon cost at year t (EURO)')
    model.VOLL=Var(model.t,within=NonNegativeReals, doc='Value of lost of load cost at year t (EURO)' )
    model.ccurt=Var(model.t, within=NonNegativeReals, doc='Renewable curtailment cost at year t (EURO)')
    model.ENS = Var(model.c, model.t, within=NonNegativeReals, doc='Energy not-supplied at coutry c at year t (MWh)')
    
    model.tt=RangeSet(1,hl_max)



    #%% --------------------------------------------------------------------------------Objective Function--------------------------------------------
    from pyomo.environ import value
    
   # 🟢 CAPEX calculation for generation and storage technology Eq.1
    def FCC_rule(model, t):
        return (
           0.001* model.FCC[t] == 0.001* sum(model.dfc[t] *model.cc_fix[j,t] * model.CAPnew[j, c, t]
                for j in model.j
                for c in model.c
            )
        )

    model.FCCConstraint = Constraint(model.tt, rule=FCC_rule)

   # 🟢 Fixed Operation Cost calculation Eq.2
    def FFC_rule(model, t):
            return (
                0.001*model.FFC[t] == 0.001*sum(model.dfo[t]*model.FOM[j,t] * model.CAP[j,c,t] 
                    for j in model.j
                    for c in model.c
                )
                )
    model.FFCConstraint = Constraint(model.tt, rule=FFC_rule)

    # 🟢 Variable Operation Cost calculation Eq.3
    def FOC_rule(model, t):
            return 0.001*model.FOC[t] == 0.001*sum(model.dfo[t]*
                model.WF[k] * model.VOM[j,t] * model.PG[j, c, t, k, h]
                for j in model.j if j not in model.jes
                for c in model.c
                for k in model.k
                for h in model.h
            )+0.001*sum(model.dfo[t]*
                model.WF[k] * model.VOM[j,t] * model.CH[j, c, t, k, h]
                for j in model.jes 
                for c in model.c
                for k in model.k
                for h in model.h
            )
    model.FOCConstraint = Constraint(model.tt, rule=FOC_rule)

    # 🟢 Fuel Cost calculation Eq.4
    def Fuel_rule(model,t):
        return 0.001*model.FuelC[t]== 0.001 *sum(model.dfo[t]*
            model.FC[j,t] * model.Vf[j, c, t]
            for j in model.j 
            for c in model.c      
        )
    model.FuelConstraint = Constraint(model.tt, rule=Fuel_rule)
 
    # 🟢 Carbon Cost calculation Eq.5  (For basecase run where the AI not included, the Slack part should be turn off)
    def CC_rule(model,t):
        return 0.001 *model.CC[t] ==0.001 * sum(
            model.dfo[t]* ((model.em[t,c]*model.ct[t])+300*1000*model.Slack[t,c]) for c in model.c
          )
    model.CCConstraint = Constraint(model.tt,rule=CC_rule)

    # 🟢 VOLL Cost calculation Eq.6
    def VOLL_rule(model,t):
        return 0.001 *model.VOLL[t]==0.001 *sum (model.dfo[t]*model.WF[k]*model.CVoLL[c]*model.LS[c,t,k,h] for c in model.c for k in model.k for h in model.h)
    model.VOLLConstraint=Constraint(model.tt, rule=VOLL_rule)
    
    
    # 🟢 Curtailment Cost calculation Eq.7
    def Curt_rule(model,t):
        return 0.001 *model.ccurt[t]==0.001 *sum (model.dfo[t]*model.WF[k]*model.Curt*model.LC[c,t,k,h] for c in model.c for k in model.k for h in model.h)
    model.CurtConstraint=Constraint(model.tt, rule=Curt_rule)


   # 🟢 CAPEX calculation for transmission Eq.8
    def TIC_rule(model):
         return 0.001 * model.TIC == 0.001 * sum(
                model.dfc[t] * 1671 * model.Dist[c, c1]/2 *model.PLmaxc[c, c1] *(model.Y[c,c1,t]-model.Y[c,c1,t-1])
                for c in model.c
                for c1 in model.c
                if (c, c1) in model.E
                for t in model.tt if t>1    
        )
    model.TICConstraint = Constraint( rule=TIC_rule)


    # 🟢 Total Objective Function Eq.9
    def objective_rule(model):
        return ( sum(
            1000*model.FCC[t]+ 
            1000*model.FFC[t]+ 
            model.FOC[t]+ 
            model.FuelC[t]+ 
            model.CC[t]+
            model.VOLL[t]+ 
            model.ccurt[t]
            for t in model.tt)+
            +model.TIC
        )                   
    model.TC = Objective(rule=objective_rule, sense=minimize)


    #%% ------------------------------------------------------------------Trasnmission------------------------------------------------
    # 🟢 Each transmission already constructed, its status remain 1 by the end of planning horizon Eq.10
    def LinePersistence_rule(model, c, c1):
            return sum (model.Y[c,c1,t] for t in model.tt) <= 1
    model.LinePersistence = Constraint(model.E,  rule=LinePersistence_rule)

    # 🟢 There is no candidate line that can be installed by t0 Eq.11
    def NoBuildFirstYear_rule(model, c, c1):
        return model.Y[c,c1,model.t.first()] == 0
    model.NoBuildFirstYear = Constraint(model.E, rule=NoBuildFirstYear_rule)

    # 🟢 The total available cross-border status between countries is calculated by Eq.12
    def LineAV_rule(model, c, c1, t):
        return model.AY[c,c1,t] == sum(
            model.Y[c,c1,tau] for tau in model.tt if tau <= t
        )
    model.LineAV = Constraint(model.E, model.tt, rule=LineAV_rule)


    # 🟢 New cross-border capacity equal to the maximum allowable capacity when it corresponding binery variable is 1 as Eq.13
    def PLI_rule(model, c, c1, t):
        return model.PLI[c,c1,t] == model.PLmaxc[c,c1] * model.Y[c,c1,t]
    model.PLIdef = Constraint(model.E, model.tt, rule=PLI_rule)




    # 🟢 Total  MW capacity of croo-border between neighboring countries is calculated by Eq.14
    def CapacityAccumulation_rule(model, c, c1, t):
        if t == model.t.first():
            return model.L[c,c1,t] == model.PLmaxe[c,c1]
        else:
            return model.L[c,c1,t] == model.L[c,c1,t-1] + model.PLI[c,c1,t]
    model.CapacityAccumulation = Constraint(model.E, model.tt, rule=CapacityAccumulation_rule)


    # 🟢  The transmission capacity in the forward direction is equal to the transmission capacity in the reverse direction by Eq.15
    def TrInvest2_rule(model,c,c1,t):
        if  (c,c1) in model.N:
            return model.L[c,c1,t]==model.L[c1,c,t]
        return Constraint.Skip
    model.TrInvest2Con= Constraint(model.E,model.tt,rule=TrInvest2_rule)


    # 🟢  The power flow is limitted to upper installed cross-border capacity by Eq.16
    def TrCapacity_rule(model,c,c1,t,k,h):
        if (c,c1) in model.E:
            return model.PL[c,c1,t,k,h]<= model.L[c,c1,t]
        return Constraint.Skip
    model.TrCapacityCon=Constraint(model.E,model.tt,model.k,model.h, rule=TrCapacity_rule)

    # 🟢  The power flow is limitted to lower installed cross-border capacity by Eq.17
    def TrCapacity_rule2(model,c,c1,t,k,h):
        if (c,c1) in model.E:
            return model.PL[c,c1,t,k,h]>=-model.L[c,c1,t]
        return Constraint.Skip
    model.TrCapacityCon2=Constraint(model.E,model.tt,model.k,model.h, rule=TrCapacity_rule2)


    #%%---------------------------------------------------------------------------Data Centre Constraints
    
    #The capacity of data centre by 2030 are extrapolated according to current capacity and national national growth trends. 
    #This means the model treats the 2030 capacity as an
    #input. Using these projected capacities, the corresponding
    # Growth Factor (GF) is calculated for each country.
    
    GF = (1.26)**5
     
    # 🟢  The initial capacity of data centre in each country is cacluated by Eq.18
    def Cap2025_rule(model, c):
        return model.CapAI[1,c] == model.IntCap[c]

    model.Cap2025CON = Constraint(model.c, rule=Cap2025_rule)

    # 🟢  The capacity of data centre by 2030 in each country is cacluated by Eq.19
    def Cap2030_exact_growth_rule(model, c):
        return model.CapAI[2,c] == (1+model.GF[c]) * model.IntCap[c]

    model.Cap2030GrowthCON = Constraint(model.c, rule=Cap2030_exact_growth_rule)

     # 🟢  The optimal capacity of data centre post- 2030 in each country is cacluated by Eq.20, the last sentence (Decommissioned capacity) is only actived in Pessimistic scenarios
    def DC_Availablity_rule(model,t,c):
        if t in [3,4,5,6]:
            return model.CapAI[t,c]==(model.CapAI[t-1,c])+model.CapNewAI[t,c]#-model.DCapNewAI[t,c]
        return Constraint.Skip
       
    model.DCAVailCON=Constraint(model.tt,model.c,rule=DC_Availablity_rule)

   # 🟢 Data-Centre Capacity Post-2030
# ============================================================
# The capacity of data centres beyond 2030 in each country
# is limited by an **upper bound**, as specified in Eq. 21.
#
# Details:
#   - The right-hand side (RHS) of Eq. 21 is denoted as TotalCapX.
#   - 'X' should be adjusted according to the chosen scenario.
#   - By default, TotalCapX is set to the IEA Base scenario.
#
    def DC_Capacity(model,t):
        if t in [3,4,5,6]:
            return sum(model.CapAI[t,c] for c in model.c)<=1.2*1000*model.TotCap[t]
        return Constraint.Skip
    model.DCCapCON=Constraint(model.tt,rule=DC_Capacity)
 
    # 🟢  The capacity of data centre post- 2030 in each country is restricted by lower value as by Eq.22
    def DC_Capacity1(model,t):
        if t in [3,4,5,6]:
            return sum(model.CapAI[t,c] for c in model.c)>=1000*model.TotCap[t]
        return Constraint.Skip
        
    model.DCCapCON1=Constraint(model.tt,rule=DC_Capacity1)


    def DC_Capacity3(model,t,c):
        if t in [3,4,5,6]:
            return model.CapAI[t,c] <= 0.2*1000*model.TotCap[t]
        return Constraint.Skip
        
    model.DCCapCON3=Constraint(model.tt,model.c,rule=DC_Capacity3)
    
   # ============================================================
# 📌 Minimum Data-Centre Capacity Constraint
# ============================================================
# In the event of a collapse or drop in data-centre capacity,
# each country is assumed to maintain its minimum baseline capacity.
    def DC_Capacity4(model,t,c):
        if t in [3,4,5,6] :
            return model.CapAI[t,c] >= model.IntCap[c]
        return Constraint.Skip
        
    model.DCCapCON4=Constraint(model.tt,model.c,rule=DC_Capacity4)


    # 🟢  The final energy consumption by data centre is calculated by Eq.24
    def DC_Profile_rule(model,c,t,k,h):
            return model.ProfileDC[c,t,k,h]==model.CapAI[t, c]*model.DCProfile[k,h]

    model.DCProfileCON1=Constraint(model.c,model.tt, model.k,model.h, rule=DC_Profile_rule)
     
    # 🟢  The total system energy consumption including base and Data Centre demand is calculated by Eq.25
    def tot_demand(model,c,t,k,h):
        return model.TotalDem[c,t,k,h]==model.ProfileDC[c,t,k,h]+model.TDem[c, t, k, h]

    model.TotDemCON1=Constraint(model.c,model.tt,model.k,model.h, rule=tot_demand)


    #%%
    #🟢 Electricity Balance Eq. 26
# ⚡ Transmission Line Simplification
# ============================================================
# For simplification, all transmission lines are assumed
# to be of HVDC 
#
# Key assumptions:
#   - Transmission losses are set to 0.05% per kilometer.
#   - Under the baseline (without Data cenntre), the model.TotalDem[c, t, k, h] should be replaced with model.TDem[c, t, k, h]

    def elec_balance_rule(model, c, t, k, h):
        lhs = (
            sum(model.PG[j, c, t, k, h]*(1-model.DL[j]) for j in model.j) +
            sum(model.PL[i, j, t, k, h]*(1-0.0005*model.Dist[i, j]) for (i, j) in model.E if j==c) -
            sum(model.PL[i, j, t, k, h] for (i, j) in model.E if i==c)+
            sum(model.DC[j, c, t, k, h] for j in model.jes) -model.LC[c, t, k, h]
        )

        rhs = (
            sum(model.CH[j, c, t, k, h] for j in model.jes) -
            model.LS[c, t, k, h] + 
            model.TotalDem[c, t, k, h]
        )

        return lhs == rhs

    model.ElecBalance = Constraint(model.c, model.tt, model.k, model.h, rule=elec_balance_rule)




    #%% 
    #🟢 Capacity expansion constraints Eq.27
    from pyomo.environ import value

    def ElecInv_rule(model, j, c, t):
            tp = int(value(model.LT[j]) / 5)
            return model.CAP[j, c, t] == (
                (model.ICap[j, c] if t == 1 else 0)
                + (model.CAP[j, c, t-1] if t > 1 else 0)
                + model.CAPnew[j, c, t]
                - model.DCAP[j, c, t]
                - (model.CAPnew[j, c, t - tp] if t > tp else 0)
            )

    model.ElecInv = Constraint(model.j, model.c, model.tt, rule=ElecInv_rule)


   #🟢 Maximum target for renewable, storae and nuclear in the line with TYNDP buildout policy Eq.28, This value for lift-off scneario is 1.25
    def Target_CapMax_rule(model,j,c,t):
        if t in [2,3,4,5,6] and j in ['Nuclear', 'WindOn', 'WindOff', 'Battery', 'Solar']:
            return model.CAP[j,c,t]<=1.1*model.TargetMax[j,c,t]
        return Constraint.Skip
               
    model.TargetMaxCON= Constraint(model.j, model.c,model.tt, rule=Target_CapMax_rule)


    def Target_CapMin_rule(model,j,c,t):
        if t in [2,3,4,5,6] and j in [ 'WindOn', 'WindOff', 'Solar']:
            return model.CAP[j,c,t]>=model.TargetMin[j,c,t]
        return Constraint.Skip
               
    #model.TargetMinCON= Constraint(model.j, model.c,model.t, rule=Target_CapMin_rule)

            
           
    #🟢 No Building rate coal, oil, and pumphydro during the planning horizon 
    for c in model.c:
        for t in model.t:
            model.CAPnew['PumpHy', c, t].setub(0)
            model.CAPnew['Coal', c, t].setub(0)
            model.CAPnew['Oil', c, t].setub(0)
           
    
    #🟢 Building rate for thermal unit in 5-year interval for gas, biomass, h2ccgt, and CCS Eq. 29
    def Build2_rule(model, j, c, t):
        if t in [2, 3, 4, 5, 6]:

            # Hydro-specific rule
            if j in ['Hydro']:
                return model.CAPnew[j, c, t] <= 1000 * model.BR[j, c, t]

            # BiomassCCS and Gas
            elif j in ['BiomassCCS', 'Gas']:
                return model.CAPnew[j, c, t] <= 1050 * model.BR[j, c, t]

            # Other dispatchable technologies
            elif j not in ['WindOff', 'WindOn', 'Battery', 'Solar']:
                return model.CAPnew[j, c, t] <= 1050 * model.BR[j, c, t]

            # VRE / storage
            else:
                return Constraint.Skip

        # First period
        else:
            return model.CAPnew[j, c, 1] == 0

    model.Build2Con = Constraint(model.j, model.c, model.t, rule=Build2_rule)
   
    

    #🟢 Land availability for solar, and wind capacity Eq. 30
    def LandAvailability_rule(model,jre,c,t):
        if jre in ['Solar', 'WindOn', 'WindOff']:
            return model.CAP[jre,c,t]<= (1000*model.LandAV[c,jre]+model.ICap[jre,c])
        return Constraint.Skip
    model.LandAVCon=Constraint(model.jre,model.c, model.tt, rule=LandAvailability_rule)

    #%%
    #🟢 Minimum generation, must-run Eq. 31
    def ThermalCap1_rule(model,j,c,t,k,h):
        if j  in ['Nuclear']:
            return model.PG[j,c,t,k,h]>= model.Pmin[j]*model.CAP[j,c,t]
        return Constraint.Skip
    model.ThermalCap1Con=Constraint(model.j,model.c,model.tt,model.k,model.h,rule=ThermalCap1_rule)
    
    #🟢 Maximum generation Eq. 32
    def ThermalCap2_rule(model,j,c,t,k,h):
        if  j in ['H2CCGT','Nuclear','CCGTCCS', 'Biomass', 'BiomassCCS','CCGT', 'Oil', 'Gas', 'Coal']:
            return model.PG[j,c,t,k,h]<= model.Pmax[j]*model.CAP[j,c,t]
        return Constraint.Skip
    model.ThermalCap2Con=Constraint(model.j,model.c,model.tt,model.k,model.h,rule=ThermalCap2_rule)

     #🟢 No generation for storage technology 
    def StorageG_rule(model,jes,c,t,k,h):
        return model.PG[jes,c,t,k,h]==0
    model.GenStorCon=Constraint(model.jes,model.c,model.tt,model.k,model.h,rule=StorageG_rule)

     #🟢 Generation for renewable based on the availability Eq. 33
    def ReCap_rule(model,jre,c,t,k,h):
            return model.PG[jre,c,t,k,h]==model.AV[k,h,c,jre]*model.CAP[jre,c,t]
    model.ReCapCon=Constraint(model.jre,model.c,model.tt,model.k,model.h, rule=ReCap_rule)



     #🟢 Maximum bound of renewable curtialment Eq. 34
    def Curtailment_rule (model,c,t,k,h):
            return model.LC[c,t,k,h]<= sum (model.PG[jre,c,t,k,h] for jre in model.jre if jre in ['Solar', 'WindOn', 'WindOff'] )    
    model.CurtailCon=Constraint( model.c,model.tt,model.k,model.h, rule=Curtailment_rule)
    #%%
    #🟢 Ramp-up limit Eq. 36
    def ThermalRampUp_rule(model, j,c,t,k,h):
        if h > 1 and j in ['H2CCGT','Nuclear','CCGTCCS', 'Biomass', 'BiomassCCS','CCGT', 'Oil', 'Gas', 'Coal']:
            return model.PG[j,c,t,k,h] - model.PG[j,c,t,k,h-1] <= model.RU[j]*model.CAP[j,c,t]
        return Constraint.Skip
    model.RampCON=Constraint(model.j,model.c,model.tt,model.k,model.h, rule=ThermalRampUp_rule)
     
    #🟢 Ramp-down limit Eq. 37
    def ThermalRampDn_rule(model, j,c,t,k,h):
        if h > 1 and j in ['H2CCGT','Nuclear','CCGTCCS', 'Biomass', 'BiomassCCS','CCGT', 'Oil', 'Gas', 'Coal']:
            return  model.PG[j,c,t,k,h-1]-model.PG[j,c,t,k,h] <= model.RD[j]*model.CAP[j,c,t]
        return Constraint.Skip
    model.RampDnCON=Constraint(model.j,model.c,model.tt,model.k,model.h, rule=ThermalRampDn_rule)
       

    #%% Energy Storage
    
    #🟢 Charging value by storage is limitted by upper bound as Eq. 38
    def ChargeBound_rule(model,jes,c,k,h,t):
            return model.CH[jes,c,t,k,h]<=model.CAP[jes,c,t]
    model.ChargeBoundCon=Constraint(model.jes,model.c,model.k,model.h,model.tt, rule=ChargeBound_rule)
   
    #🟢 Discharging value by storage is limitted by upper bound as Eq. 39
    def DischargeBound_rule(model,jes,c,k,h,t):
            return model.DC[jes,c,t,k,h]<=model.CAP[jes,c,t]
    model.DischargeBoundCon=Constraint(model.jes,model.c,model.k,model.h,model.tt, rule=DischargeBound_rule)

    #🟢 Storage level is calculated as Eq. 40
    def StorageLevel_rule(model, jes, c, t, k, h):
        return model.S[jes, c, t, k, h] == (
            (1-model.Self[jes])*(model.S[jes, c, t,k, h-1] if h > 1 else model.Sinit[jes, c, t])
            + model.eta[jes] * model.CH[jes, c, t, k, h]
            - model.DC[jes, c, t, k, h] / model.eta[jes]
        )

    model.StorageLevelCon = Constraint(model.jes, model.c, model.tt, model.k, model.h, rule=StorageLevel_rule)


    #🟢 Final Storage level by end of the day is calculated as Eq. 41
    def s_final_rule(model, jes,c,t,k,h):
            return model.S[jes, c,t,k,24] == 0
      
    model.SFinalConstraint = Constraint(model.jes,model.c, model.tt,model.k, model.h,  rule=s_final_rule)


    #🟢 Initial Storage level by end of the day is calculated as Eq. 42
    def StorageLeve2_rule(model, jes, c, t):
                return model.Sinit[jes, c, t]==0.5*model.CAP[jes,c,t]

    model.StorageLevel2Con = Constraint(model.jes, model.c, model.tt, rule=StorageLeve2_rule)


   #🟢 Conver power to energy for battery and pumphydro storage according to charging duration time  Eq. 43
    def StorageMax_rule1(model, jes, c, t, k, h):
       if jes in ['Battery']:
            return model.S[jes, c, t, k, h] <=4*model.CAP[jes,c,t]
       return model.S[jes, c, t, k, h] <=8*model.CAP[jes,c,t]
    model.StorageMaxCon1 = Constraint(model.jes, model.c, model.tt, model.k, model.h, rule=StorageMax_rule1)
    #%%PEAK DEMAND
    
    #🟢 Whole-system peak demand is calculated by Eq. 44
    def PeakDemand_rule(model,t,k,h):
            return model.PeakDemand[t]>= sum(model.TotalDem[c, t, k, h] for c in model.c)
    model.PeakDemandCon=Constraint(model.tt,model.k,model.h, rule=PeakDemand_rule)

    #🟢 Reserve margin is calculated by Eq. 45
    def Reserve_rule(model,t):
            return sum(model.de[j]*model.CAP[j,c,t] for j in model.j for c in model.c)>= (1+0.08)*model.PeakDemand[t]                  
    model.ReserveCon= Constraint(model.tt, rule=Reserve_rule)
    #%%
    #🟢 Emission pollution is calculated by Eq. 46
    def ElecEmissions_rule(model, t,c):
            return 0.001*model.em[t,c] == 0.001*sum(
                model.WF[k] * model.yc[j] * model.PG[j, c, t, k, h]
                for j in model.j 
                for k in model.k
                for h in model.h
            )
    model.ElecEmissionsCon = Constraint(model.tt,model.c, rule=ElecEmissions_rule)

    # Emission pollution is limitted by the upper bound by Eq. 47
    def Em_target_rule(model,t,c):
      return 0.001 *model.em[t,c]   <= 0.001 *1000*(model.EmTarget[t,c] +model.Slack[t,c])
    model.EmTargetConstraint=Constraint(model.tt,model.c, rule=Em_target_rule)
    
    def Additional_target_rule(model,t,c):
      return 0.001 *model.Slack[t,c]   <= 0.001 *0.2*model.EmTarget[t,c] 
    model.AdditioanlConstraint=Constraint(model.tt,model.c, rule=Additional_target_rule)


    #%%
    # 🟢 Fuel consumption for power generation is calculated by Eq. 48

    def FuelCpnsumption_rule(model,j,c,t):
        if j in ['H2CCGT','Nuclear','CCGTCCS', 'Biomass', 'BiomassCCS','CCGT', 'Oil', 'Gas', 'Coal']:
            return model.Vf[j,c,t]==sum(model.WF[k]*model.PG[j,c,t,k,h]/model.eta[j] for k in model.k for h in model.h)
        return Constraint.Skip
        
    model.FuelCon=Constraint(model.j,model.c,model.tt, rule=FuelCpnsumption_rule)

    #%%Load shedding
      
    # 🟢 Energy not-supplied is calculated by Eq. 49
    def ENS_def_rule(model, c, t):
        return model.ENS[c, t] == sum(
            model.LS[c, t, k, h] * model.WF[k]
            for k in model.k
            for h in model.h
        )

    model.ENS_Def = Constraint(model.c, model.t, rule=ENS_def_rule)
      
    # 🟢 Energy not-supplied is converted to LOLE as calculated by Eq. 50 where the LOLE for each coutry should less than 3 hour per year
    def ENS_limit_rule(model, c, t):
        return model.ENS[c, t] <= (3/8760) * model.AnnualDemand[c, t]

    model.ENS_Limit = Constraint(model.c, model.t, rule=ENS_limit_rule)
    return model
                                                                                                  
    #%% Solving the Rolling Horizon Optimisation Problem with 6 sequential windows
hl_init = 2
hl_max  = 6
step    = 1

fixed_values = {}

hl = hl_init

while hl <= hl_max:

    # --- BUILD MODEL FOR CURRENT HORIZON ---
    model = build_model(hl)     
                                

    for (var_name, idx), val in fixed_values.items():
        getattr(model, var_name)[idx].fix(val)

    # --- SOLVE ---
    opt = SolverFactory('gurobi')
    opt.options['Threads']     = 30
    opt.options['Presolve']    = 0
    opt.options['TimeLimit']   = 28000
    opt.options['MIPGap']      = 0.01
    opt.options['LogFile']     = "opt.log"

    results = opt.solve(model, tee=True)
    last_model = model

    # --- SAVE DECISIONS FOR CURRENT HORIZON ---
    for (j, c, t) in model.CAPnew.index_set():
        if t <= hl:                       # store decisions up to current horizon
            fixed_values[("CAPnew", (j, c, t))] = value(model.CAPnew[j, c, t])
            fixed_values[("CAP", (j, c, t))] = value(model.CAP[j, c, t])
            fixed_values[("DCAP", (j,c,t))] = value(model.DCAP[j,c,t])
            fixed_values[("CapAI", (t,c))] = value(model.CapAI[t,c])

    for (c, c1, t) in model.Y.index_set():
        if t <= hl:
            fixed_values[("Y", (c, c1, t))] = value(model.Y[c, c1, t])
            fixed_values[("AY", (c, c1, t))] = value(model.AY[c, c1, t])
            fixed_values[("L", (c, c1, t))] = value(model.L[c, c1, t])
            fixed_values[("PLI", (c, c1, t))] = value(model.PLI[c, c1, t])

    # increase horizon
    hl += step



model = last_model
from openpyxl import Workbook

wb = Workbook()


#Saving results
all_variables = []

objective_value = model.TC()  
all_variables.append({"Name": "Objective", "Index": "-", "Value": objective_value})

for var in model.component_objects(Var, active=True):
    var_name = var.name
    for index in var:
        value = var[index]()
        if value is not None and abs(value) > 1e-6:  
            all_variables.append({
                "Name": var_name,
                "Index": index,
                "Value": value
            })

df = pd.DataFrame(all_variables)
df.to_excel("EUPanIEA Base.xlsx", index=False, sheet_name="All Data")


#%% Saving all variables and results 
import pandas as pd
from pyomo.environ import value

# ---------- PeakDemand (t) ----------
data_peak = []
for t in model.t:
    data_peak.append({
        't': t,
        'PeakDemand': value(model.PeakDemand[t])
    })
df_peak = pd.DataFrame(data_peak)

# ---------- CAP (j,c,t) ----------
data_cap = []
for j in model.j:
    for c in model.c:
        for t in model.t:
            data_cap.append({
                'j': j,
                'c': c,
                't': t,
                'CAP': value(model.CAP[j, c, t])
            })
df_cap = pd.DataFrame(data_cap)

# ---------- DCAP (j,c,t) ----------
data_dcap = []
for j in model.j:
    for c in model.c:
        for t in model.t:
            data_dcap.append({
                'j': j,
                'c': c,
                't': t,
                'DCAP': value(model.DCAP[j, c, t])
            })
df_dcap = pd.DataFrame(data_dcap)

# ---------- CAPnew (j,c,t) ----------
data_capnew = []
for j in model.j:
    for c in model.c:
        for t in model.t:
            data_capnew.append({
                'j': j,
                'c': c,
                't': t,
                'CAPnew': value(model.CAPnew[j, c, t])
            })
df_capnew = pd.DataFrame(data_capnew)

# ---------- Save to Excel ----------
with pd.ExcelWriter('results_IEA_Base.xlsx', engine='openpyxl') as writer:
    df_peak.to_excel(writer, sheet_name='PeakDemand', index=False)
    df_cap.to_excel(writer, sheet_name='CAP', index=False)
    df_dcap.to_excel(writer, sheet_name='DCAP', index=False)
    df_capnew.to_excel(writer, sheet_name='CAPnew', index=False)

from pyomo.environ import value

# ---------- CH weighted by WF[k] ----------
data_ch = []

for j in ['PumpHy','Battery']:
    for c in model.c:
        for t in model.t:
            for k in model.k:
                for h in model.h:
                    data_ch.append({
                        'j': j,
                        'c': c,
                        't': t,
                        'k': k,
                        'h': h,
                        'Storage Charge': value(model.CH[j, c, t, k, h]) * value(model.WF[k])
                    })

df_ch = pd.DataFrame(data_ch)

# ---------- Save to Excel ----------
with pd.ExcelWriter('results_IEA_Base.xlsx', engine='openpyxl', mode='a') as writer:
    df_ch.to_excel(writer, sheet_name='Storage Charge', index=False)


data_dis = []

for j in ['PumpHy','Battery']:
    for c in model.c:
        for t in model.t:
            for k in model.k:
                for h in model.h:
                    data_dis.append({
                        'j': j,
                        'c': c,
                        't': t,
                        'k': k,
                        'h': h,
                        'Storage Discharge': value(model.DC[j, c, t, k, h]) * value(model.WF[k])
                    })

df_dis = pd.DataFrame(data_dis)

# ---------- Save to Excel ----------
with pd.ExcelWriter('results_IEA_Base.xlsx', engine='openpyxl', mode='a') as writer:
    df_dis.to_excel(writer, sheet_name='Storage Discharge', index=False)
    


data_SOC = []   
for j in ['PumpHy','Battery']:
    for c in model.c:
        for t in model.t:
            for k in model.k:
                for h in model.h:
                    data_SOC.append({
                        'j': j,
                        'c': c,
                        't': t,
                        'k': k,
                        'h': h,
                        'Storage SOC': value(model.S[j, c, t, k, h]) * value(model.WF[k])
                    })

df_SOC = pd.DataFrame(data_SOC)

# ---------- Save to Excel ----------
with pd.ExcelWriter('results_IEA_Base.xlsx', engine='openpyxl', mode='a') as writer:
    df_SOC.to_excel(writer, sheet_name='Storage SOC', index=False)    
    
from pyomo.environ import value

# ---------- PG weighted by WF[k] ----------
data_pg = []

for j in model.j:
    for c in model.c:
        for t in model.t:
            for k in model.k:
                for h in model.h:
                    data_pg.append({
                        'j': j,
                        'c': c,
                        't': t,
                        'k': k,
                        'h': h,
                        'Generation': value(model.PG[j, c, t, k, h]) * value(model.WF[k])
                    })

df_pg = pd.DataFrame(data_pg)

# ---------- Save to Excel ----------
with pd.ExcelWriter('results_IEA_Base.xlsx', engine='openpyxl', mode='a') as writer:
    df_pg.to_excel(writer, sheet_name='Generation', index=False)   

import pandas as pd
from pyomo.environ import value

# ---------- PL (From, To, t, k, h) ----------
data_pl = []

for (c_from, c_to) in model.E:
    for t in model.t:
        for k in model.k:
            for h in model.h:
                data_pl.append({
                    'From': c_from,
                    'To': c_to,
                    't': t,
                    'k': k,
                    'h': h,
                    'PL': value(model.PL[c_from, c_to, t, k, h])
                })

df_pl = pd.DataFrame(data_pl)

# ---------- Save to Excel ----------
with pd.ExcelWriter('results_IEA_Base.xlsx', engine='openpyxl', mode='a') as writer:
    df_pl.to_excel(writer, sheet_name='PL', index=False)

import pandas as pd
from pyomo.environ import value

# ---------- em (t, c) ----------
data_em = []

for t in model.t:
    for c in model.c:
        data_em.append({
            't': t,
            'c': c,
            'Emission': value(model.em[t, c])
        })

df_em = pd.DataFrame(data_em)

# ---------- Save to Excel ----------
with pd.ExcelWriter('results_IEA_Base.xlsx', engine='openpyxl', mode='a') as writer:
    df_em.to_excel(writer, sheet_name='Emission', index=False)


import pandas as pd
from pyomo.environ import value

# ---------- Vf (j, c, t) ----------
data_vf = []

for j in ['H2CCGT','Nuclear','CCGTCCS', 'Biomass', 'BiomassCCS','CCGT', 'Oil', 'Gas', 'Coal']:
    for c in model.c:
        for t in model.t:
            data_vf.append({
                'j': j,
                'c': c,
                't': t,
                'Fuel Consumption': value(model.Vf[j, c, t])
            })

df_vf = pd.DataFrame(data_vf)

# ---------- Save to Excel ----------
with pd.ExcelWriter('results_IEA_Base.xlsx', engine='openpyxl', mode='a') as writer:
    df_vf.to_excel(writer, sheet_name='Fuel Consumption', index=False)

import pandas as pd
from pyomo.environ import value

# ---------- Financial variables ----------
data_fin = []

# TIC (no t index)
data_fin.append({
    'Variable': 'TIC',
    't': '',
    'Value': value(model.TIC)
})

# Variables with t index
for t in model.t:
    data_fin.append({'Variable': 'FCC',   't': t, 'Value': value(model.FCC[t])})
    data_fin.append({'Variable': 'FuelC', 't': t, 'Value': value(model.FuelC[t])})
    data_fin.append({'Variable': 'FOC',   't': t, 'Value': value(model.FOC[t])})
    data_fin.append({'Variable': 'FFC',   't': t, 'Value': value(model.FFC[t])})
    data_fin.append({'Variable': 'CC',    't': t, 'Value': value(model.CC[t])})
    data_fin.append({'Variable': 'VOLL',  't': t, 'Value': value(model.VOLL[t])})
    data_fin.append({'Variable': 'ccurt', 't': t, 'Value': value(model.ccurt[t])})

df_fin = pd.DataFrame(data_fin)

# ---------- Save to Excel ----------
with pd.ExcelWriter('results_IEA_Base.xlsx', engine='openpyxl', mode='a') as writer:
    df_fin.to_excel(writer, sheet_name='Financial', index=False)

import pandas as pd
from pyomo.environ import value

# ---------- TDem parameter weighted by WF[k] ----------
data_TotalDem = []

for c in model.c:
    for t in model.t:
        for k in model.k:
            for h in model.h:
                data_TotalDem.append({
                    'c': c,
                    't': t,
                    'k': k,
                    'h': h,
                    'Base Demand': value(model.TotalDem[c, t, k, h]) * value(model.WF[k])
                })

df_TotalDem = pd.DataFrame(data_TotalDem)

# ---------- Save to Excel ----------
with pd.ExcelWriter('results_IEA_Base.xlsx', engine='openpyxl', mode='a') as writer:
    df_TotalDem.to_excel(writer, sheet_name='Total Demand', index=False)


data_AIDem = []

for c in model.c:
    for t in model.t:
        for k in model.k:
            for h in model.h:
                data_AIDem.append({
                    'c': c,
                    't': t,
                    'k': k,
                    'h': h,
                    'Base Demand': value(model.ProfileDC[c, t, k, h]) * value(model.WF[k])
                })

df_AIDem = pd.DataFrame(data_AIDem)

# ---------- Save to Excel ----------
with pd.ExcelWriter('results_IEA_Base.xlsx', engine='openpyxl', mode='a') as writer:
    df_AIDem.to_excel(writer, sheet_name='AI Demand', index=False)

data_curt = []
    
for c in model.c:
    for t in model.t:
        for k in model.k:
            for h in model.h:
                data_curt.append({
                    'c': c,
                    't': t,
                    'k': k,
                    'h': h,
                    'Curtailment': value(model.LC[c, t, k, h]) * value(model.WF[k])
                })

df_curt = pd.DataFrame(data_curt)

# ---------- Save to Excel ----------
with pd.ExcelWriter('results_IEA_Base.xlsx', engine='openpyxl', mode='a') as writer:
    df_curt.to_excel(writer, sheet_name='Curtailment', index=False) 
