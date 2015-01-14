'''isotopomer metabolomics analysis class'''

from analysis.analysis_base import *
from stage02_isotopomer_query import *
from stage02_isotopomer_io import *
# Dependencies
import operator, json, csv
from copy import copy
# Dependencies from 3rd party
import scipy.io
from numpy import histogram, mean, std, loadtxt
import matplotlib as mpl
import matplotlib.pyplot as plt
import h5py
from resources.molmass import Formula
# Dependencies from cobra
from cobra.io.sbml import create_cobra_model_from_sbml_file
from cobra.io.sbml import write_cobra_model_to_sbml_file
from cobra.io.mat import save_matlab_model
from cobra.manipulation.modify import convert_to_irreversible, revert_to_reversible
from cobra.flux_analysis.objective import update_objective
from cobra.flux_analysis.variability import flux_variability_analysis
from cobra.flux_analysis.parsimonious import optimize_minimal_flux
from cobra.flux_analysis import flux_variability_analysis, single_deletion
from cobra.core.Reaction import Reaction
from cobra.core.Metabolite import Metabolite

class stage02_isotopomer_dependencies():
    def __init__(self):
        self.calculate = base_calculate();
        #variables:
        self.isotopomer_rxns_net_irreversible = {
                'ptrc_to_4abut_1':{'reactions':['PTRCTA','ABUTD'],
                                   'stoichiometry':[1,1]},
                'ptrc_to_4abut_2':{'reactions':['GGPTRCS','GGPTRCO','GGGABADr','GGGABAH'],
                                   'stoichiometry':[1,1,1,1]},
                'glu_DASH_L_to_acg5p':{'reactions':['ACGS','ACGK'],
                                   'stoichiometry':[1,1]},
                '2obut_and_pyr_to_3mop':{'reactions':['ACHBS','KARA2','DHAD2'],
                                   'stoichiometry':[1,1,1]},
                'pyr_to_23dhmb':{'reactions':['ACLS','KARA1_reverse'],
                                   'stoichiometry':[1,1]},
                #'met_DASH_L_and_ptrc_to_spmd_and_5mta':{'reactions':['METAT','ADMDC','SPMS'],
                #                   'stoichiometry':[1,1,1]}, #cannot be lumped
                'chor_and_prpp_to_3ig3p':{'reactions':['ANS','ANPRT','PRAIi','IGPS'],
                                   'stoichiometry':[1,1,1,1]},
                'hom_DASH_L_and_cyst_DASH_L_to_pyr_hcys_DASH_L':{'reactions':['HSST','SHSL1','CYSTL'],
                                   'stoichiometry':[1,1,1]},
                'e4p_and_pep_to_3dhq':{'reactions':['DDPA','DHQS'],
                                   'stoichiometry':[1,1]},
                'aspsa_to_sl2a6o':{'reactions':['DHDPS','DHDPRy','THDPS'],
                                   'stoichiometry':[1,1,1]},
                'glu_DASH_L_to_glu5sa':{'reactions':['GLU5K','G5SD'],
                                   'stoichiometry':[1,1]},
                'g1p_to_glycogen':{'reactions':['GLGC','GLCS1'],
                                   'stoichiometry':[1,1]},
                'thr_DASH_L_to_gly':{'reactions':['THRD','GLYAT_reverse'],
                                   'stoichiometry':[1,1]}, #need to remove deadend mets: athr-L: ATHRDHr, ATHRDHr_reverse; aact: AACTOOR, AOBUTDs
                'dhap_to_lac_DASH_D':{'reactions':['MGSA','LGTHL','GLYOX'],
                                   'stoichiometry':[1,1,1]},
                'hom_DASH_L_to_thr_DASH_L':{'reactions':['HSK','THRS'],
                                   'stoichiometry':[1,1]},
                '3pg_to_ser_DASH_L':{'reactions':['PGCD','PSERT','PSP_L'],
                                   'stoichiometry':[1,1,1]},
                'prpp_to_his_DASH_L':{'reactions':['ATPPRT','PRATPP','PRAMPC','PRMICI','IG3PS','IGPDH','HSTPT','HISTP','HISTD'],
                                   'stoichiometry':[1,1,1,1,1,1,1,1,1]},
                'UMPSYN_aerobic':{'reactions':['ASPCT','DHORTS_reverse','DHORD2','ORPT_reverse','OMPDC'],
                                   'stoichiometry':[1,1,1,1,1]},
                #'UMPSYN_anaerobic':{'reactions':['ASPCT','DHORTS_reverse','DHORD5','ORPT_reverse','OMPDC'],
                #                   'stoichiometry':[1,1,1,1,1]},
                'IMPSYN_1':{'reactions':['GLUPRT','PRAGSr','PRFGS','PRAIS'],
                                   'stoichiometry':[1,1,1,1]},
                'IMPSYN_2':{'reactions':['AIRC2','AIRC3_reverse','PRASCSi','ADSL2r'],
                                   'stoichiometry':[1,1,1,1]},
                'IMPSYN_3':{'reactions':['AICART','IMPC_reverse'],
                                   'stoichiometry':[1,1]},
                'imp_to_gmp':{'reactions':['IMPD','GMPS2'],
                                   'stoichiometry':[1,1]},
                'imp_to_amp':{'reactions':['ADSS','ADSL1r'],
                                   'stoichiometry':[1,1]},
                #'utp_to_dump_anaerobic':{'reactions':['RNTR4c2','DUTPDP'],
                #                   'stoichiometry':[1,1]},
                'udp_to_dump_aerobic':{'reactions':['RNDR4','NDPK6','DUTPDP'],
                                   'stoichiometry':[1,1,1]},
                #'dtmp_to_dttp':{'reactions':['DTMPK','NDPK4'],
                #                   'stoichiometry':[1,1]}, #cannot be lumped
                'COASYN':{'reactions':['ASP1DC','MOHMT','DPR','PANTS','PNTK','PPNCL2','PPCDC','PTPATi','DPCOAK'],
                                   'stoichiometry':[1,1,1,1,1,1,1,1,1]},
                'FADSYN_1':{'reactions':['GTPCII2','DHPPDA2','APRAUR','PMDPHT','RBFSb'],
                                   'stoichiometry':[1,1,1,1,1]},
                'FADSYN_2':{'reactions':['RBFSa','DB4PS'],
                                   'stoichiometry':[1,1]},
                'FADSYN_3':{'reactions':['RBFK','FMNAT'],
                                   'stoichiometry':[1,1]},
                'NADSYN_aerobic':{'reactions':['ASPO6','QULNS','NNDPR','NNATr','NADS1','NADK'],
                                   'stoichiometry':[1,1,1,1,1,1]},
                #'NADSYN_anaerobic':{'reactions':['ASPO5','QULNS','NNDPR','NNATr','NADS1','NADK'],
                #                   'stoichiometry':[1,1,1,1,1,1]},
                #'NADSALVAGE':{'reactions':['NADPPPS','NADN','NNAM','NAMNPP','NMNN','NMNDA','NMNAT','NADDP','ADPRDP'],
                #                   'stoichiometry':[1,1,1,1,1,1,1,1,1]}, #cannot be lumped
                'THFSYN':{'reactions':['GTPCI','DNTPPA','DNMPPA','DHNPA2r','HPPK2','ADCS','ADCL','DHPS2','DHFS'],
                                   'stoichiometry':[1,1,1,1,1,1,1,1,1]},
                'GTHSYN':{'reactions':['GLUCYS','GTHS'],
                                   'stoichiometry':[1,1]},
                'GLYCPHOSPHOLIPID_1':{'reactions':['DASYN181','AGPAT181','G3PAT181'],'stoichiometry':[1,1,1]},
                'GLYCPHOSPHOLIPID_2':{'reactions':['PSSA181','PSD181'],'stoichiometry':[1,1]},
                'GLYCPHOSPHOLIPID_3':{'reactions':['PGSA160','PGPP160'],'stoichiometry':[1,1]},
                'GLYCPHOSPHOLIPID_4':{'reactions':['DASYN161','AGPAT161','G3PAT161'],'stoichiometry':[1,1,1]},
                'GLYCPHOSPHOLIPID_5':{'reactions':['PGSA181','PGPP181'],'stoichiometry':[1,1]},
                'GLYCPHOSPHOLIPID_6':{'reactions':['PSD161','PSSA161'],'stoichiometry':[1,1]},
                'GLYCPHOSPHOLIPID_7':{'reactions':['PSSA160','PSD160'],'stoichiometry':[1,1]},
                'GLYCPHOSPHOLIPID_8':{'reactions':['DASYN160','AGPAT160','G3PAT160'],'stoichiometry':[1,1,1]},
                'GLYCPHOSPHOLIPID_9':{'reactions':['PGSA161','PGPP161'],'stoichiometry':[1,1]},
                'MOLYBDOPTERIN_1':{'reactions':['MPTAT','MPTS','CPMPS'],'stoichiometry':[1,1,1]},
                'MOLYBDOPTERIN_2':{'reactions':['MOCDS','MOGDS'],'stoichiometry':[1,1]},
                'MOLYBDOPTERIN_3':{'reactions':['MOADSUx','MPTSS'],'stoichiometry':[1,1]},
                'COFACTOR_1':{'reactions':['GLUTRR','G1SAT','GLUTRS'],'stoichiometry':[1,1,1]},
                'COFACTOR_2':{'reactions':['DHNAOT4','UPPDC1','DHNCOAT','DHNCOAS','SEPHCHCS','SUCBZS','SUCBZL','PPPGO3','FCLT','CPPPGO','SHCHCS3'],'stoichiometry':[1,1,1,1,1,1,1,1,1,1,1]},
                'COFACTOR_3':{'reactions':['TYRL','AMMQLT8','HEMEOS','UPP3MT','SHCHD2','SHCHF','ENTCS','CBLAT'],'stoichiometry':[1,1,1,1,1,1,1,1]},
                'VITB6':{'reactions':['E4PD','PERD','OHPBAT','PDX5PS','PDX5PO2'],'stoichiometry':[1,1,1,1,1]},
                #'THIAMIN':{'reactions':['AMPMS2','PMPK','THZPSN3','TMPPP','TMPK'],'stoichiometry':[1,1,1,1,1]}, # original pathway without correction
                'THIAMIN':{'reactions':['AMPMS3','PMPK','THZPSN3','TMPPP','TMPK'],'stoichiometry':[1,1,1,1,1]},
                'COFACTOR_4':{'reactions':['I4FE4ST','I4FE4SR','I2FE2SS2'],'stoichiometry':[1,1,1]},
                'COFACTOR_5':{'reactions':['BMOGDS1','BMOGDS2','BMOCOS'],'stoichiometry':[1,1,1]},
                'COFACTOR_6':{'reactions':['DMPPS','GRTT','DMATT'],'stoichiometry':[1,1,1]},
                'COFACTOR_7':{'reactions':['MECDPS','DXPRIi','MEPCT','CDPMEK','MECDPDH5'],'stoichiometry':[1,1,1,1,1]},
                'COFACTOR_8':{'reactions':['LIPOS','LIPOCT'],'stoichiometry':[1,1]},
                'COFACTOR_9':{'reactions':['OMMBLHX','OMPHHX','OPHHX','HBZOPT','DMQMT','CHRPL','OMBZLM','OPHBDC','OHPHM'],'stoichiometry':[1,1,1,1,1,1,1,1,1]},
                'COFACTOR_10':{'reactions':['SERASr','DHBD','UPP3S','HMBS','ICHORT','DHBS'],'stoichiometry':[1,1,1,1,1,1]},
                'COFACTOR_11':{'reactions':['PMEACPE','EGMEACPR','DBTS','AOXSr2','I2FE2SR','OPMEACPD','MALCOAMT','AMAOTr','OPMEACPS','OPMEACPR','OGMEACPD','OGMEACPR','OGMEACPS','EPMEACPR','BTS5'],'stoichiometry':[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]},
                'CELLENV_1':{'reactions':['UAMAGS','UAPGR','UAGPT3','PAPPT3','GLUR_reverse','UAGCVT','UAMAS','UDCPDP','UGMDDS','UAAGDS'],'stoichiometry':[1,1,1,1,1,1,1,1,1,1]},
                'CELLENV_2':{'reactions':['3HAD181','3OAR181','3OAS181','EAR181x'],'stoichiometry':[1,1,1,1]},
                'CELLENV_3':{'reactions':['3HAD160','3OAR160','EAR160x','3OAS160'],'stoichiometry':[1,1,1,1]},
                'CELLENV_4':{'reactions':['EAR120x','3OAR120','3HAD120','3OAS120','EAR100x'],'stoichiometry':[1,1,1,1,1]},
                'CELLENV_5':{'reactions':['G1PACT','UAGDP','PGAMT_reverse','GF6PTA'],'stoichiometry':[1,1,1,1]},
                'CELLENV_6':{'reactions':['3OAR40','EAR40x','3OAS60','3OAR60','3HAD80','3OAS80','3OAR80','EAR60x','3HAD60','EAR80x','3HAD40'],'stoichiometry':[1,1,1,1,1,1,1,1,1,1,1]},
                'CELLENV_7':{'reactions':['3HAD161','EAR161x','3OAS161','3OAR161','3OAS141','3HAD141','3OAR121','EAR121x','3HAD121','EAR141x','T2DECAI','3OAR141','3OAS121'],'stoichiometry':[1,1,1,1,1,1,1,1,1,1,1,1,1]},
                'CELLENV_8':{'reactions':['TDPGDH','TDPDRR','TDPDRE','G1PTT'],'stoichiometry':[1,1,1,1]},
                'CELLENV_9':{'reactions':['3OAS140','3OAR140'],'stoichiometry':[1,1]},
                'CELLENV_10':{'reactions':['3HAD140','EAR140x'],'stoichiometry':[1,1]},
                'CELLENV_11':{'reactions':['3OAR100','3HAD100','3OAS100'],'stoichiometry':[1,1,1]},
                'LIPOPOLYSACCHARIDE_1':{'reactions':['COLIPAabcpp','COLIPAabctex','EDTXS1','EDTXS2','GALT1','GLCTR1','GLCTR2','GLCTR3','HEPK1','HEPK2','HEPT1','HEPT2','HEPT3','HEPT4','LPADSS','MOAT','MOAT2','MOAT3C','RHAT1','TDSK','USHD'],'stoichiometry':[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]},
                'LIPOPOLYSACCHARIDE_2':{'reactions':['AGMHE','GMHEPAT','GMHEPK','GMHEPPA','S7PI'],'stoichiometry':[1,1,1,1,1]},
                'LIPOPOLYSACCHARIDE_3':{'reactions':['U23GAAT','UHGADA','UAGAAT'],'stoichiometry':[1,1,1]},
                'LIPOPOLYSACCHARIDE_4':{'reactions':['KDOPP','KDOCT2','KDOPS'],'stoichiometry':[1,1,1]},
                'ASTPathway':{'reactions':['AST','SADH','SGDS','SGSAD','SOTA'],'stoichiometry':[1,1,1,1,1]}
                };
    #model reduction functions
    def load_ALEWt(self,anoxic = False):
        '''load iJO1366 with the following changes:
	    1. update to AMPMS2 to account for carbon monoxide
	    2. changes to uptake bounds for glucose M9 media
	    3. constrain the model to use 'PFK' instead of 'F6PA', 'DHAPT' when grown on glucose
	    4. constrain the model to use the physiologically perferred glutamate synthesis enzymes
	    5. depending on oxygen availability, constrain the model to use the correct RNR enzymes
	    6. depending on oxygen availability, constrain the model to use the correct Dihydroorotate dehydrogenase (PyrD) enzymes
	    7. constrain fatty acid biosynthesis to use the physiologically preferred enzymes'''
        ijo1366_sbml = "data\\iJO1366.xml"
        # Read in the sbml file and define the model conditions
        cobra_model = create_cobra_model_from_sbml_file(ijo1366_sbml, print_time=True)
        # Update AMPMS2
        coc = Metabolite('co_c','CO','carbon monoxide','c');
        cop = Metabolite('co_p','CO','carbon monoxide','p');
        coe = Metabolite('co_e','CO','carbon monoxide','e');
        cobra_model.add_metabolites([coc,cop,coe])
        ampms2_mets = {};
        ampms2_mets[cobra_model.metabolites.get_by_id('air_c')] = -1;
        ampms2_mets[cobra_model.metabolites.get_by_id('amet_c')] = -1;
        ampms2_mets[cobra_model.metabolites.get_by_id('dad_DASH_5_c')] = 1;
        ampms2_mets[cobra_model.metabolites.get_by_id('met_DASH_L_c')] = 1;
        ampms2_mets[cobra_model.metabolites.get_by_id('4ampm_c')] = 1;
        ampms2_mets[cobra_model.metabolites.get_by_id('h_c')] = 3;
        ampms2_mets[cobra_model.metabolites.get_by_id('for_c')] = 1;
        ampms2_mets[cobra_model.metabolites.get_by_id('co_c')] = 1;
        ampms2 = Reaction('AMPMS3');
        ampms2.add_metabolites(ampms2_mets);
        copp_mets = {};
        copp_mets[cobra_model.metabolites.get_by_id('co_c')] = -1;
        copp_mets[cobra_model.metabolites.get_by_id('co_p')] = 1;
        copp = Reaction('COtpp');
        copp.add_metabolites(copp_mets);
        coex_mets = {};
        coex_mets[cobra_model.metabolites.get_by_id('co_p')] = -1;
        coex_mets[cobra_model.metabolites.get_by_id('co_e')] = 1;
        coex = Reaction('COtex');
        coex.add_metabolites(coex_mets);
        cotrans_mets = {};
        cotrans_mets[cobra_model.metabolites.get_by_id('co_e')] = -1;
        cotrans = Reaction('EX_co_LPAREN_e_RPAREN_');
        cotrans.add_metabolites(cotrans_mets);
        cobra_model.add_reactions([ampms2,copp,coex,cotrans]);
        cobra_model.remove_reactions(['AMPMS2']);
        # Define the model conditions:
        system_boundaries = [x.id for x in cobra_model.reactions if x.boundary == 'system_boundary'];
        for b in system_boundaries:
                cobra_model.reactions.get_by_id(b).lower_bound = 0.0;
                cobra_model.reactions.get_by_id(b).upper_bound = 0.0;
        # Reset demand reactions
        demand = ['DM_4CRSOL',
                'DM_5DRIB',
                'DM_AACALD',
                'DM_AMOB',
                'DM_MTHTHF',
                'DM_OXAM'];
        for d in demand:
                cobra_model.reactions.get_by_id(d).lower_bound = 0.0;
                cobra_model.reactions.get_by_id(d).upper_bound = 1000.0;
        # Change the objective
        update_objective(cobra_model,{'Ec_biomass_iJO1366_WT_53p95M':1.0})
        # Assign KOs

        # Specify media composition (M9 glucose):
        cobra_model.reactions.get_by_id('EX_glc_LPAREN_e_RPAREN_').lower_bound = -10.0;
        cobra_model.reactions.get_by_id('EX_o2_LPAREN_e_RPAREN_').lower_bound = -18.0;
        #uptake = ['EX_cl_LPAREN_e_RPAREN_',
        #            'EX_so4_LPAREN_e_RPAREN_',
        #            'EX_ca2_LPAREN_e_RPAREN_',
        #            'EX_pi_LPAREN_e_RPAREN_',
        #            'EX_fe2_LPAREN_e_RPAREN_',
        #            'EX_cu2_LPAREN_e_RPAREN_',
        #            'EX_zn2_LPAREN_e_RPAREN_',
        #            'EX_cbl1_LPAREN_e_RPAREN_',
        #            'EX_mobd_LPAREN_e_RPAREN_',
        #            'EX_ni2_LPAREN_e_RPAREN_',
        #            'EX_mn2_LPAREN_e_RPAREN_',
        #            'EX_k_LPAREN_e_RPAREN_',
        #            'EX_nh4_LPAREN_e_RPAREN_',
        #            'EX_cobalt2_LPAREN_e_RPAREN_',
        #            'EX_mg2_LPAREN_e_RPAREN_'];
        uptake = ['EX_ca2_LPAREN_e_RPAREN_',
                    'EX_cbl1_LPAREN_e_RPAREN_',
                    'EX_cl_LPAREN_e_RPAREN_',
                    'EX_co2_LPAREN_e_RPAREN_',
                    'EX_cobalt2_LPAREN_e_RPAREN_',
                    'EX_cu2_LPAREN_e_RPAREN_',
                    'EX_fe2_LPAREN_e_RPAREN_',
                    'EX_fe3_LPAREN_e_RPAREN_',
                    'EX_h_LPAREN_e_RPAREN_',
                    'EX_h2o_LPAREN_e_RPAREN_',
                    'EX_k_LPAREN_e_RPAREN_',
                    'EX_mg2_LPAREN_e_RPAREN_',
                    'EX_mn2_LPAREN_e_RPAREN_',
                    'EX_mobd_LPAREN_e_RPAREN_',
                    'EX_na1_LPAREN_e_RPAREN_',
                    'EX_nh4_LPAREN_e_RPAREN_',
                    'EX_ni2_LPAREN_e_RPAREN_',
                    'EX_pi_LPAREN_e_RPAREN_',
                    'EX_sel_LPAREN_e_RPAREN_',
                    'EX_slnt_LPAREN_e_RPAREN_',
                    'EX_so4_LPAREN_e_RPAREN_',
                    'EX_tungs_LPAREN_e_RPAREN_',
                    'EX_zn2_LPAREN_e_RPAREN_'];
        for u in uptake:
            cobra_model.reactions.get_by_id(u).lower_bound = -1000.0;
        # Specify allowed secretion products
        secrete = ['EX_meoh_LPAREN_e_RPAREN_',
                    'EX_5mtr_LPAREN_e_RPAREN_',
                    'EX_h_LPAREN_e_RPAREN_',
                    'EX_co2_LPAREN_e_RPAREN_',
                    'EX_co_LPAREN_e_RPAREN_',
                    'EX_h2o_LPAREN_e_RPAREN_',
                    'EX_ac_LPAREN_e_RPAREN_',
                    'EX_fum_LPAREN_e_RPAREN_',
                    'EX_for_LPAREN_e_RPAREN_',
                    'EX_etoh_LPAREN_e_RPAREN_',
                    'EX_lac_DASH_L_LPAREN_e_RPAREN_',
                    'EX_pyr_LPAREN_e_RPAREN_',
                    'EX_succ_LPAREN_e_RPAREN_'];
        for s in secrete:
            cobra_model.reactions.get_by_id(s).upper_bound = 1000.0;
        # Constrain specific reactions
        noFlux = ['F6PA', 'DHAPT'];
        ammoniaExcess = ['GLUDy']; # PMCID: 196288
        # RNR control (DOI:10.1111/j.1365-2958.2006.05493.x)
        # Dihydroorotate dehydrogenase (PyrD) (DOI:10.1016/S0076-6879(78)51010-0, PMID: 199252, DOI:S0969212602008316 [pii])
        aerobic = ['RNDR1', 'RNDR2', 'RNDR3', 'RNDR4', 'DHORD2', 'ASPO6','LCARR','PFL','FRD2','FRD3']; # see DOI:10.1111/j.1365-2958.2011.07593.x; see DOI:10.1089/ars.2006.8.773 for a review
        anaerobic = ['RNTR1c2', 'RNTR2c2', 'RNTR3c2', 'RNTR4c2', 'DHORD5', 'ASPO5','PDH','SUCDi']; # see DOI:10.1074/jbc.274.44.31291, DOI:10.1128/JB.00440-07
        if anaerobic:
            rxnList = noFlux + ammoniaExcess + anaerobic;
            for rxn in rxnList:
                cobra_model.reactions.get_by_id(rxn).lower_bound = 0.0;
                cobra_model.reactions.get_by_id(rxn).upper_bound = 0.0;
        else:
            rxnList = noFlux + ammoniaExcess + aerobic;
            for rxn in rxnList:
                cobra_model.reactions.get_by_id(rxn).lower_bound = 0.0;
                cobra_model.reactions.get_by_id(rxn).upper_bound = 0.0;
        # Set the direction for specific reactions
        # Fatty acid biosynthesis: DOI: 10.1016/j.ymben.2010.10.007, PMCID: 372925
        fattyAcidSynthesis = ['ACCOAC', 'ACOATA', 'HACD1', 'HACD2', 'HACD3', 'HACD4', 'HACD5', 'HACD6', 'HACD7', 'HACD8', 'KAS14', 'KAS15', 'MACPD', 'MCOATA', '3OAR100', '3OAR120', '3OAR121', '3OAR140', '3OAR141', '3OAR160', '3OAR161', '3OAR180', '3OAR181', '3OAR40', '3OAR60', '3OAR80']
        fattyAcidOxidation = ['ACACT1r', 'ACACT2r', 'ACACT3r', 'ACACT4r', 'ACACT5r', 'ACACT6r', 'ACACT7r', 'ACACT8r', 'ACOAD1f', 'ACOAD2f', 'ACOAD3f', 'ACOAD4f', 'ACOAD5f', 'ACOAD6f', 'ACOAD7f', 'ACOAD8f', 'CTECOAI6', 'CTECOAI7', 'CTECOAI8', 'ECOAH1', 'ECOAH2', 'ECOAH3', 'ECOAH4', 'ECOAH5', 'ECOAH6', 'ECOAH7', 'ECOAH8']
        ndpk = ['NDPK1','NDPK2','NDPK3','NDPK4','NDPK5','NDPK7','NDPK8'];
        rxnList = fattyAcidSynthesis + fattyAcidOxidation;
        for rxn in rxnList:
            cobra_model.reactions.get_by_id(rxn).lower_bound = 0.0;
            cobra_model.reactions.get_by_id(rxn).upper_bound = 1000.0;

        return cobra_model;
    def reduce_model(self,cobra_model,cobra_model_outFileName=None):
        '''reduce model'''
        # Input: cobra_model
        # Output: cobra_model 
        #         the lower and upper bounds have been set to 0.0
        #         for all reactions that cannot carry a flux
        cobra_model.optimize()
        sol_f = cobra_model.solution.f

        fva_data = flux_variability_analysis(cobra_model, fraction_of_optimum=0.9,
                                              objective_sense='maximize', the_reactions=None,
                                              allow_loops=True, solver='gurobi',
                                              the_problem='return', tolerance_optimality=1e-6,
                                              tolerance_feasibility=1e-6, tolerance_barrier=1e-8,
                                              lp_method=1, lp_parallel=0, new_objective=None,
                                              relax_b=None, error_reporting=None,
                                              number_of_processes=1, copy_model=False);
        #with open("data\\ijo1366_irrev_fva.json", 'w') as outfile:
        #    json.dump(data, outfile, indent=4);

        #fva_data = json.load(open("data\\ijo1366_irrev_fva.json"));

        # Reduce model
        rxns_noflux = [];
        for k,v in fva_data.iteritems():
            if v['minimum'] == 0.0 and v['maximum'] == 0.0:
                cobra_model.reactions.get_by_id(k).lower_bound = 0.0;
                cobra_model.reactions.get_by_id(k).upper_bound = 0.0;
                rxns_noflux.append(k);

        if cobra_model_outFileName:
            write_cobra_model_to_sbml_file(cobra_model,cobra_model_outFileName)

        cobra_model.optimize()
        sol_reduced_f = cobra_model.solution.f

        # Check that the reduced model is consistent with the original model
        if not sol_f == sol_reduced_f:
            print 'reduced model is inconsistent with the original model'
            print 'original model solution: ' + str(sol_f)
            print 'reduced model solution: ' + str(sol_reduced_f)
    def reduce_model_pfba(self,cobra_model,cobra_model_outFileName=None,fba_outFileName=None,subs=[]):
        '''reduce model using pfba'''
        # Input: cobra_model
        #        cobra_model_outFileName
        #        subs = string of specific subsystems to reduce
        # Output: cobra_model 
        #         the lower and upper bounds have been set to 0.0
        #         for all reactions that cannot carry a flux
        cobra_model.optimize()
        sol_f = cobra_model.solution.f

        # Find minimal flux solution:
        pfba = optimize_minimal_flux(cobra_model,True,solver='gurobi');

        # Reduce model
        rxns_noflux = [];
        # set lb and ub for all reactions with 0 flux to 0;
        for k,v in cobra_model.solution.x_dict.iteritems():
            if (v < 0.0 or v == 0.0) and cobra_model.reactions.get_by_id(k).subsystem in subs:
                cobra_model.reactions.get_by_id(k).lower_bound = 0.0;
                cobra_model.reactions.get_by_id(k).upper_bound = 0.0;
                rxns_noflux.append(k);

        if cobra_model_outFileName:
            write_cobra_model_to_sbml_file(cobra_model,cobra_model_outFileName)

        if pfba_outFileName:
            # Write pfba solution to file
            with open(pfba_outFileName,mode='wb') as outfile:
                writer = csv.writer(outfile)
                writer.writerow(['Reaction','Flux'])
                for k,v in cobra_model.solution.x_dict.iteritems():
                    writer.writerow([k,v]);

        cobra_model.optimize()
        sol_reduced_f = cobra_model.solution.f

        # Check that the reduced model is consistent with the original model
        if not sol_f == sol_reduced_f:
            print 'reduced model is inconsistent with the original model'
            print 'original model solution: ' + str(sol_f)
            print 'reduced model solution: ' + str(sol_reduced_f)
    def add_net_reaction(self,cobra_model_IO, rxn_dict_I,remove_reverse=False):
        '''add a net reaction to the model after removing
        the individual reactions'''
        # input: rxn_dict_I = dictionary of net reaction ids and
        #                       corresponding list of individual reaction ids
        # output: cobra_model_IO = individual reactions replaced with a
        #                           net reaction

        cobra_model_IO.optimize();
        sol_orig = cobra_model_IO.solution.f;
        print "original model solution", sol_orig

        try:
            cobra_model_tmp = cobra_model_IO.copy2();
        except KeyError as e:
            print e; 

        # make net reactions:
        rxn_dict_net = {};
        for k,v in rxn_dict_I.iteritems():
            rxn_net = make_net_reaction(cobra_model_tmp, k, v['reactions'],v['stoichiometry']);
            if rxn_net:
                rxn_net.lower_bound = 0.0;
                rxn_net.upper_bound = 1000.0;
                rxn_net.objective_coefficient = 0.0;
            else:
                print 'an error occured in add_net_reaction'
                exit(-1)

            #rxn_net.reversibility = False;
            rxn_dict_net[k] = (v['reactions'],rxn_net);

        # add replace individual reactions with net reaction
        for k,v in rxn_dict_net.iteritems():
            cobra_model_IO.remove_reactions(v[0]);
            # remove the reverse reaction if it exists for irreversible models
            if remove_reverse:
                for rxn in v[0]:
                    if '_reverse' in rxn:
                        rxn_rev = rxn.replace('_reverse','')
                        if cobra_model_IO.reactions.has_id(rxn_rev): cobra_model_IO.remove_reactions(rxn_rev);
                    else:
                        rxn_rev = rxn+'_reverse';
                        if cobra_model_IO.reactions.has_id(rxn_rev): cobra_model_IO.remove_reactions(rxn_rev);
            cobra_model_IO.add_reaction(v[1]);
            cobra_model_IO.optimize();
            sol_new = cobra_model_IO.solution.f;
            print k, sol_new
    def make_net_reaction(self,cobra_model_I, rxn_id_I, rxn_list_I,stoich_list_I):
        '''generate a net reaction from a list of individual reactions'''
        # input: rxn_list_I = list of reaction IDs
        # output: rxn_net_O = net reaction (cobra Reaction object)
        from cobra.core.Reaction import Reaction

        #rxn_net_O = cobra_model_I.reactions.get_by_id(rxn_list_I[0]);
        #for r in rxn_list_I[1:]:
        #    if cobra_model_I.reactions.get_by_id(r).reversibility:
        #        print r + " is reversible!";
        #        print "continue?"
        #    rxn_net_O += cobra_model_I.reactions.get_by_id(r);

        # check input:
        if not len(stoich_list_I) == len(rxn_list_I):
            print "error in " + rxn_id_I + ": there are " + str(len(rxn_list_I)) + " rxn ids and " + str(len(stoich_list_I)) + " coefficients";
            exit(-1);

        rxn_net_O = Reaction(rxn_id_I);
        for i,r in enumerate(rxn_list_I):
            mets = {};
            metlist = [];
            metlist = cobra_model_I.reactions.get_by_id(r).products + cobra_model_I.reactions.get_by_id(r).reactants;
            for met in metlist:
                mets[met] = cobra_model_I.reactions.get_by_id(r).get_coefficient(met)*stoich_list_I[i];
            rxn_net_O.add_metabolites(mets);
            rxn_net_O.subsystem = cobra_model_I.reactions.get_by_id(r).subsystem; #copy over the subsystem
    
        # check net reaction
        #if not rxn_net_O.check_mass_balance():  
            #print "error: " + rxn_id_I + " is not elementally balanced";

        #print rxn_net_O.id;
        #print rxn_net_O.build_reaction_string();
        return rxn_net_O;
    def get_solBySub(self,cobra_model_I,sol_I,sub_I):

        sol_O = {};
        for k,v in sol_I.iteritems():
            try:
                if cobra_model_I.reactions.get_by_id(k).subsystem == sub_I:
                    sol_O[k] = v;
            except:
                print k + ' reaction not found'

        return sol_O;
    def groupBySameFlux(self,cobra_model_I,sol_I):

        flux_list = [];
        for r,f in sol_I.iteritems():
            if not f in flux_list and float(f)>0.0:
                flux_list.append(f)
            
        sameFlux_O = {};
        for f in flux_list:
            rxn_list = [];
            for r,v in sol_I.iteritems():
                if v==f:
                    rxn_list.append(r);
            stoich = [1]*len(rxn_list)
            rxnName = '';
            for rxn in rxn_list:
                rxnName = rxnName + rxn + '_';
            rxnName = rxnName[:-1];
            # check that the reaction name is less than 225 characters
            if len(rxnName)>224:
                rxnName = rxnName[:224];
            sameFlux_O[rxnName] = {'reactions':rxn_list,
                               'stoichiometry':stoich,
                                'flux':f};
            #netRxn = make_net_reaction(cobra_model_copy,rxnName,rxn_list,stoich)
            #sameFlux_O[rxnName] = {'reactions':rxn_list,
            #                   'stoichiometry':stoich,
            #                    'flux':f,
            #                    'net':netRxn};

        return sameFlux_O
    def add_net_reaction_subsystem(self,cobra_model_IO,sol_I,subs_I):
        '''make net reactions for specific subsystems grouped 
        by reactions that have the same flux from pfba'''
        #input: cobra_model
        #       sol_I = pfba solution
        #       sub_I = list of model subsystems
        #output: cobra_model
    
        # convert model to irreversible
        # convert_to_irreversible(cobra_model_IO);
        # Make net reactions for pathways outside of the scope
        # of the isotopomer model
        for s in subs_I:
            sol = get_solBySub(cobra_model_IO,sol_I,s)
            sameFlux = groupBySameFlux(cobra_model_IO,sol)
            netRxns = {};
            for k,v in sameFlux.iteritems():
                if len(v['reactions'])>1: 
                    netRxns[k] = v;
            add_net_reaction(cobra_model_IO,netRxns);
            # add subsystem information back in
            for k in sameFlux.iterkeys():
                cobra_model_IO.reactions.get_by_id(k).subsystem = s
            remove_noflux_reactions(cobra_model_IO,sol_I,subs_I)
        # convert model back to reversible
        # revert_to_reversible(cobra_model_IO);
    def remove_noflux_reactions(self,cobra_model,sol=None,subs=[]):
        '''remove noflux reactions'''
        # Input: cobra_model
        #        sol = pfba solution
        #        subs = string of specific subsystems to reduce
        # Output: cobra_model 
        #         if the lower and upper bounds are zero, the reactions
        #         are removed
        cobra_model.optimize()
        sol_f = cobra_model.solution.f
    
        # Reduce model
        rxns_noflux = [];
        # set lb and ub for all reactions with 0 flux to 0;
        if sol:
            if subs:
                for k,v in sol.iteritems():
                    try:
                        if (float(v) < 0.0 or float(v) == 0.0) and cobra_model.reactions.get_by_id(k).subsystem in subs:
                            cobra_model.reactions.get_by_id(k).lower_bound = 0.0;
                            cobra_model.reactions.get_by_id(k).upper_bound = 0.0;
                            cobra_model.remove_reactions(k)
                            rxns_noflux.append(k);
                    except:
                        print 'reaction is not in model: ' + k
            else:
                for k,v in sol.iteritems():
                    try:
                        if (float(v) < 0.0 or float(v) == 0.0):
                            cobra_model.reactions.get_by_id(k).lower_bound = 0.0;
                            cobra_model.reactions.get_by_id(k).upper_bound = 0.0;
                            cobra_model.remove_reactions(k)
                            rxns_noflux.append(k);
                    except:
                        print 'reaction is not in model: ' + k
        else:
            if subs:
                for r in cobra_model.reactions:
                    if r.lower_bound == 0.0 and r.upper_bound == 0.0 and cobra_model.reactions.get_by_id(r.id).subsystem in subs:
                        cobra_model.remove_reactions(r.id)
            else:
                for r in cobra_model.reactions:
                    if r.lower_bound == 0.0 and r.upper_bound == 0.0:
                        cobra_model.remove_reactions(r.id)
                
        cobra_model.optimize()
        sol_reduced_f = cobra_model.solution.f

        # Check that the reduced model is consistent with the original model
        if not sol_f == sol_reduced_f:
            print 'reduced model is inconsistent with the original model'
            print 'original model solution: ' + str(sol_f)
            print 'reduced model solution: ' + str(sol_reduced_f)
    def get_reactionsInfo(self,cobra_model):
        '''return the number of reactions and the number of reactions 
        that cannot carry a flux (i.e. lb and ub of 0.0)'''
        nrxn_O = len(cobra_model.reactions);
        nrxn_noflux_O = 0;
        for r in cobra_model.reactions:
            if r.lower_bound == 0.0 and r.upper_bound == 0.0:
                nrxn_noflux_O += 1;
        return nrxn_O, nrxn_noflux_O
    #model reduction iteration functions
    def makeIsotopomerModel_iteration01(self,pfba_file,netrxn_irreversible_model_filename,fva_reduced_model_filename,reduced_lbub_filename):
        '''iteration 1:
        identification of reactions that can be lumped in pathways outside the model scope'''
        cobra_model = self.load_ALEWt();
        # Make the model irreversible for downstream manipulations:
        convert_to_irreversible(cobra_model);
        # Add lumped isotopomer reactions
        self.add_net_reaction(cobra_model,isotopomer_rxns_net_irreversible);
        # Find minimal flux solution:
        pfba = optimize_minimal_flux(cobra_model,True,solver='gurobi');
        # Write pfba solution to file
        with open(pfba_file,mode='wb') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(['Reaction','Flux'])
            for k,v in cobra_model.solution.x_dict.iteritems():
                writer.writerow([k,v]);
        # Read in pfba solution 
        pfba_sol = {};
        with open(pfba_file,mode='r') as infile:
            dictreader = csv.DictReader(infile)
            for r in dictreader:
                pfba_sol[r['Reaction']] = r['Flux'];
        # Make net reactions for pathways outside of the scope
        # of the isotopomer model
        subs = ['Cell Envelope Biosynthesis',
	        'Glycerophospholipid Metabolism',
	        'Lipopolysaccharide Biosynthesis / Recycling',
	        'Membrane Lipid Metabolism',
	        'Murein Biosynthesis'
            'Murein Recycling',
            'Cofactor and Prosthetic Group Biosynthesis',
            #'Transport, Inner Membrane',
            #'Transport, Outer Membrane',
            #'Transport, Outer Membrane Porin',
            'tRNA Charging',
            'Unassigned',
            'Exchange',
            'Inorganic Ion Transport and Metabolism',
            'Nitrogen Metabolism'];
        self.add_net_reaction_subsystem(cobra_model,pfba_sol,subs);
        self.remove_noflux_reactions(cobra_model,pfba_sol,['Transport, Outer Membrane Porin','Transport, Inner Membrane','Transport, Outer Membrane'])
        revert_to_reversible(cobra_model);
        # write model to sbml
        write_cobra_model_to_sbml_file(cobra_model,netrxn_irreversible_model_filename)
        # Reduce model using FVA:
        self.reduce_model(cobra_model,fva_reduced_model_filename)
        # Remove all reactions with 0 flux
        self.remove_noflux_reactions(cobra_model);
        with open(reduced_lbub_filename,mode='wb') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(['Reaction','Formula','LB','UB','Subsystem'])
            for r in cobra_model.reactions:
                writer.writerow([r.id,
                                 r.build_reaction_string(),
                                r.lower_bound,
                                r.upper_bound,
                                r.subsystem]);
    def makeIsotopomerModel_iteration02(self,pfba_filename,fva_reduced_model_filename,netrxn_irreversible_model_filename,reduced_lbub_filename):
        '''iteration 2:
        addition of finalized lumped reactions that are in pathways that are within the scope of the model
        and reduction by removing reactions with zero optimal minimal flux outside the scope of the model'''
        cobra_model = load_ALEWt();
        # Make the model irreversible for downstream manipulations:
        convert_to_irreversible(cobra_model);
        cobra_model.optimize();
        # Add lumped isotopomer reactions
        self.add_net_reaction(cobra_model,isotopomer_rxns_net_irreversible,True);
        cobra_model.optimize();
        # Find minimal flux solution:
        pfba = optimize_minimal_flux(cobra_model,True,solver='gurobi');
        # Write pfba solution to file
        with open(pfba_filename,mode='wb') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(['Reaction','Flux','Subsystem'])
            for k,v in cobra_model.solution.x_dict.iteritems():
                writer.writerow([k,v,cobra_model.reactions.get_by_id(k).subsystem]);
        # Read in pfba solution 
        pfba_sol = {};
        with open(pfba_filename,mode='r') as infile:
            dictreader = csv.DictReader(infile)
            for r in dictreader:
                pfba_sol[r['Reaction']] = r['Flux'];
        # remove noflux reactions for pathways outside of the scope
        # of the isotopomer model
        subs = ['Cell Envelope Biosynthesis',
	        'Glycerophospholipid Metabolism',
	        'Lipopolysaccharide Biosynthesis / Recycling',
	        'Membrane Lipid Metabolism',
	        'Murein Biosynthesis'
            'Murein Recycling',
            'Cofactor and Prosthetic Group Biosynthesis',
            'Transport, Inner Membrane',
            'Transport, Outer Membrane',
            'Transport, Outer Membrane Porin',
            'tRNA Charging',
            'Unassigned',
            #'Exchange',
            'Inorganic Ion Transport and Metabolism',
            'Nitrogen Metabolism',
            'Alternate Carbon Metabolism'];
        self.remove_noflux_reactions(cobra_model,pfba_sol,subs)
        # Reduce model using FVA:
        self.reduce_model(cobra_model,fva_reduced_model_filename)
        # Reset secretion products that may have been turned off
        secrete = ['EX_meoh_LPAREN_e_RPAREN_',
                    'EX_5mtr_LPAREN_e_RPAREN_',
                    'EX_h_LPAREN_e_RPAREN_',
                    'EX_co2_LPAREN_e_RPAREN_',
                    'EX_co_LPAREN_e_RPAREN_',
                    'EX_h2o_LPAREN_e_RPAREN_',
                    'EX_ac_LPAREN_e_RPAREN_',
                    'EX_fum_LPAREN_e_RPAREN_',
                    'EX_for_LPAREN_e_RPAREN_',
                    'EX_etoh_LPAREN_e_RPAREN_',
                    'EX_lac_DASH_L_LPAREN_e_RPAREN_',
                    'EX_pyr_LPAREN_e_RPAREN_',
                    'EX_succ_LPAREN_e_RPAREN_'];
        for s in secrete:
            cobra_model.reactions.get_by_id(s).upper_bound = 1000.0;
        # Remove all reactions with 0 flux
        r1,r2 = self.get_reactionsInfo(cobra_model);
        while r2 !=0:
            self.remove_noflux_reactions(cobra_model);
            r1,r2 = self.get_reactionsInfo(cobra_model);
            print r1,r2;
        # write model to sbml
        write_cobra_model_to_sbml_file(cobra_model,netrxn_irreversible_model_filename)
        with open(reduced_lbub_filename,mode='wb') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(['Reaction','Formula','LB','UB','Subsystem'])
            for r in cobra_model.reactions:
                writer.writerow([r.id,
                                 r.build_reaction_string(),
                                r.lower_bound,
                                r.upper_bound,
                                r.subsystem]);
    def makeIsotopomerModel_cobraMAT(self,model_filename,xml_filename,mat_filename,csv_filename,isotopomer_mapping_filename,ko_list=[],flux_dict={},description=None):
        '''iteration 3:
        Remove reactions that are thermodynamically unfavorable and add isotopomer data'''
        # Read in the sbml file and define the model conditions
        cobra_model = create_cobra_model_from_sbml_file(model_filename, print_time=True)
        # Modify glucose uptake:
        if cobra_model.reactions.has_id('EX_glc_LPAREN_e_RPAREN__reverse'):
            lb,ub = cobra_model.reactions.get_by_id('EX_glc_LPAREN_e_RPAREN__reverse').lower_bound,cobra_model.reactions.get_by_id('EX_glc_LPAREN_e_RPAREN__reverse').upper_bound;
            EX_glc_mets = {};
            EX_glc_mets[cobra_model.metabolites.get_by_id('glc_DASH_D_e')] = -1;
            EX_glc = Reaction('EX_glc_LPAREN_e_RPAREN_');
            EX_glc.add_metabolites(EX_glc_mets);
            cobra_model.add_reaction(EX_glc)
            cobra_model.reactions.get_by_id('EX_glc_LPAREN_e_RPAREN_').lower_bound = -ub;
            cobra_model.reactions.get_by_id('EX_glc_LPAREN_e_RPAREN_').upper_bound = lb;
            cobra_model.remove_reactions(['EX_glc_LPAREN_e_RPAREN__reverse'])
        ## Remove thermodynamically infeasible reactions:
        #infeasible = [];
        #loops = [];
        #cobra_model.remove_reactions(infeasible + loops);
        # Apply KOs, if any:
        for ko in ko_list:
            cobra_model.reactions.get_by_id(ko).lower_bound = 0.0;
            cobra_model.reactions.get_by_id(ko).upper_bound = 0.0;
        # Apply flux constraints, if any:
        for rxn,flux in flux_dict.iteritems():
            cobra_model.reactions.get_by_id(rxn).lower_bound = flux['lb'];
            cobra_model.reactions.get_by_id(rxn).upper_bound = flux['ub'];
        # Change description, if any:
        if description:
            cobra_model.description = description;
        # Read in isotopomer model
        isotopomer_mapping = self.read_isotopomer_mapping_csv(isotopomer_mapping_filename); #broken
        isotopomer_str = self.build_isotopomer_str(isotopomer_mapping);
        # write model to sbml
        write_cobra_model_to_sbml_file(cobra_model,xml_filename)
        # Add isotopomer field to model
        for r in cobra_model.reactions:
            if isotopomer_str.has_key(r.id):
                cobra_model.reactions.get_by_id(r.id).isotopomer = isotopomer_str[r.id];
            else:
                cobra_model.reactions.get_by_id(r.id).isotopomer = '';
        # Add null basis:
        cobra_model_array = cobra_model.to_array_based_model();
        N = self.calculate.null(cobra_model_array.S.todense()) #convert S from sparse to full and compute the nullspace
        cobra_model.N = N;
        # solve and save pFBA for later use:
        optimize_minimal_flux(cobra_model,True,solver='gurobi');
        # add match field:
        match = numpy.zeros(len(cobra_model.reactions));
        cobra_model.match = match;
        # write model to mat
        save_matlab_model_isotopomer(cobra_model,mat_filename);
        with open(csv_filename,mode='wb') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(['Reaction','Formula','LB','UB','Genes','Subsystem','Isotopomer'])
            for r in cobra_model.reactions:
                writer.writerow([r.id,
                                 r.build_reaction_string(),
                                r.lower_bound,
                                r.upper_bound,
                                r.gene_reaction_rule,
                                r.subsystem,
                                r.isotopomer]);
    #ecoli_INCA modifications
    def expand_ecoliINCA01(self,model_id_I,mapping_id_I,date_I,model_id_O,mapping_id_O):
        '''expand the INCA Ecoli model to account for additional metabolites'''

        query = stage02_isotopomer_query()
        # get the xml model
        cobra_model_sbml = ''
        cobra_model_sbml = query.get_row_modelID_dataStage02IsotopomerModels(model_id_I);
        # load the model
        if cobra_model_sbml:
            if cobra_model_sbml['file_type'] == 'sbml':
                with open('data\\cobra_model_tmp.xml','wb') as file:
                    file.write(cobra_model_sbml['model_file']);
                    file.close()
                cobra_model = None;
                cobra_model = create_cobra_model_from_sbml_file('data\\cobra_model_tmp.xml', print_time=True);
            elif cobra_model_sbml['file_type'] == 'json':
                with open('data\\cobra_model_tmp.json','wb') as file:
                    file.write(cobra_model_sbml['model_file']);
                    file.close()
                cobra_model = None;
                cobra_model = load_json_model('data\\cobra_model_tmp.json');
            else:
                print 'file_type not supported'

        #get the atomMapping_reactions
        atomMappingReactions = query.get_rows_mappingID_dataStage02IsotopomerAtomMappingReactions(mapping_id_I);
        #change the mapping_id
        for cnt,row in enumerate(atomMappingReactions):
            atomMappingReactions[cnt]['mapping_id']=mapping_id_O;

        #expand the model to include glyoxylate shunt:
        #get metabolites not in the model
        met_row = {}
        met_row = query.get_row_modelIDAndMetID_dataStage02IsotopomerModelMetabolites('140407_iDM2014','glx_c');
        glx = Metabolite(met_row['met_id'],met_row['formula'],met_row['met_name'],'c')
        glx.charge = met_row['charge']
        #get metabolites in the model
        icit = cobra_model.metabolites.get_by_id('icit_c')
        succ = cobra_model.metabolites.get_by_id('succ_c')
        accoa = cobra_model.metabolites.get_by_id('accoa_c')
        mal = cobra_model.metabolites.get_by_id('mal_DASH_L_c')
        #make ICL
        rxn_mets = {};
        rxn_mets[icit] = -1;
        rxn_mets[succ] = 1;
        rxn_mets[glx] = 1;
        rxn = Reaction('ICL');
        rxn.add_metabolites(rxn_mets);
        cobra_model.add_reactions([rxn]);
        cobra_model.reactions.get_by_id(rxn.id).lower_bound = 0.0;
        cobra_model.reactions.get_by_id(rxn.id).upper_bound = 1000;
        cobra_model.repair();
        #append the new atom mappings
        row_tmp = {};
        row_tmp['mapping_id']=mapping_id_O;
        row_tmp['rxn_id']='ICL';
        row_tmp['rxn_description']='';
        row_tmp['rxn_equation']='';
        row_tmp['reactants_stoichiometry_tracked']=[-1]
        row_tmp['products_stoichiometry_tracked']=[1,1]
        row_tmp['reactants_ids_tracked']=['icit_c']
        row_tmp['products_ids_tracked']=['glx_c','succ_c']
        row_tmp['reactants_elements_tracked']=[["C", "C", "C", "C", "C", "C"]]
        row_tmp['products_elements_tracked']=[["C", "C"], ["C", "C", "C", "C"]]
        row_tmp['reactants_positions_tracked']=[[0, 1, 2, 3, 4, 5]]
        row_tmp['products_positions_tracked']=[[0, 1], [0, 1, 2, 3]]
        row_tmp['reactants_mapping']=['abcdef']
        row_tmp['products_mapping']=['ab','fcde']
        row_tmp['used_']=True
        row_tmp['comment_']='added'
        atomMappingReactions.append(row_tmp);
        #make MALS
        rxn_mets = {};
        rxn_mets[glx] = -1;
        rxn_mets[accoa] = -1;
        rxn_mets[mal] = 1;
        rxn = Reaction('MALS');
        rxn.add_metabolites(rxn_mets);
        cobra_model.add_reactions([rxn]);
        cobra_model.reactions.get_by_id(rxn.id).lower_bound = 0.0;
        cobra_model.reactions.get_by_id(rxn.id).upper_bound = 1000;
        cobra_model.repair();
        #append the new atom mappings
        row_tmp = {};
        row_tmp['mapping_id']=mapping_id_O;
        row_tmp['rxn_id']='MALS';
        row_tmp['rxn_description']='';
        row_tmp['rxn_equation']='';
        row_tmp['reactants_stoichiometry_tracked']=[-1,-1]
        row_tmp['products_stoichiometry_tracked']=[1]
        row_tmp['reactants_ids_tracked']=['accoa_c','glx_c']
        row_tmp['products_ids_tracked']=['mal_DASH_L_c']
        row_tmp['reactants_elements_tracked']=[["C", "C"], ["C", "C"]]
        row_tmp['products_elements_tracked']=[["C", "C", "C", "C"]]
        row_tmp['reactants_positions_tracked']=[[0, 1], [0, 1]]
        row_tmp['products_positions_tracked']=[[0, 1, 2, 3]]
        row_tmp['reactants_mapping']=['ab','cd']
        row_tmp['products_mapping']=['cdba']
        row_tmp['used_']=True
        row_tmp['comment_']='added'
        atomMappingReactions.append(row_tmp);

        #add in glucose transporters and intracellular glc 
        #get metabolites not in the model
        met_row = {}
        met_row = query.get_row_modelIDAndMetID_dataStage02IsotopomerModelMetabolites('140407_iDM2014',"glc_DASH_D_c");
        glc_c = Metabolite(met_row['met_id'],met_row['formula'],met_row['met_name'],'c')
        glc_c.charge = met_row['charge']
        met_row = {}
        met_row = query.get_row_modelIDAndMetID_dataStage02IsotopomerModelMetabolites('140407_iDM2014',"glc_DASH_D_e");
        glc_e = Metabolite(met_row['met_id'],met_row['formula'],met_row['met_name'],'e')
        glc_e.charge = met_row['charge']
        glcext = Metabolite('glc_DASH_D_e.ext',met_row['formula'],met_row['met_name'],'e')
        glcext.charge = met_row['charge']
        glcpre = Metabolite('glc_DASH_D_e.pre',met_row['formula'],met_row['met_name'],'e')
        glcpre.charge = met_row['charge']
        #get metabolites in the model
        pep = cobra_model.metabolites.get_by_id('pep_c')
        pyr = cobra_model.metabolites.get_by_id('pyr_c')
        g6p = cobra_model.metabolites.get_by_id('g6p_c')
        #make EX_glc_LPAREN_e_RPAREN_
        rxn_mets = {};
        rxn_mets[glcext] = -1;
        rxn_mets[glc_e] = 1;
        rxn = Reaction('EX_glc_LPAREN_e_RPAREN_');
        cobra_model.remove_reactions(['EX_glc_LPAREN_e_RPAREN_']);
        rxn.add_metabolites(rxn_mets);
        cobra_model.add_reactions([rxn]);
        cobra_model.reactions.get_by_id(rxn.id).lower_bound = 0.0;
        cobra_model.reactions.get_by_id(rxn.id).upper_bound = 1000;
        cobra_model.repair();
        #append the new atom mappings
        row_tmp = {};
        row_tmp['mapping_id']=mapping_id_O;
        row_tmp['rxn_id']='EX_glc_LPAREN_e_RPAREN_';
        row_tmp['rxn_description']='';
        row_tmp['rxn_equation']='';
        row_tmp['reactants_stoichiometry_tracked']=[-1]
        row_tmp['products_stoichiometry_tracked']=[1]
        row_tmp['reactants_ids_tracked']=['glc_DASH_D_e.ext']
        row_tmp['products_ids_tracked']=['glc_DASH_D_e']
        row_tmp['reactants_elements_tracked']=[["C", "C", "C", "C", "C", "C"]]
        row_tmp['products_elements_tracked']=[["C", "C", "C", "C", "C", "C"]]
        row_tmp['reactants_positions_tracked']=[[0, 1, 2, 3, 4, 5]]
        row_tmp['products_positions_tracked']=[[0, 1, 2, 3, 4, 5]]
        row_tmp['reactants_mapping']=['abcdef']
        row_tmp['products_mapping']=['abcdef']
        row_tmp['used_']=True
        row_tmp['comment_']='added'
        atomMappingReactions.append(row_tmp);
        #make EX_glc_LPAREN_e_RPAREN__pre
        rxn_mets = {};
        rxn_mets[glcpre] = -1;
        rxn_mets[glc_e] = 1;
        rxn = Reaction('EX_glc_LPAREN_e_RPAREN__pre');
        cobra_model.remove_reactions(['v60']);
        rxn.add_metabolites(rxn_mets);
        cobra_model.add_reactions([rxn]);
        cobra_model.reactions.get_by_id(rxn.id).lower_bound = 0.0;
        cobra_model.reactions.get_by_id(rxn.id).upper_bound = 1000;
        cobra_model.repair();
        #append the new atom mappings
        row_tmp = {};
        row_tmp['mapping_id']=mapping_id_O;
        row_tmp['rxn_id']='EX_glc_LPAREN_e_RPAREN__pre';
        row_tmp['rxn_description']='';
        row_tmp['rxn_equation']='';
        row_tmp['reactants_stoichiometry_tracked']=[-1]
        row_tmp['products_stoichiometry_tracked']=[1]
        row_tmp['reactants_ids_tracked']=['glc_DASH_D_e.pre']
        row_tmp['products_ids_tracked']=['glc_DASH_D_e']
        row_tmp['reactants_elements_tracked']=[["C", "C", "C", "C", "C", "C"]]
        row_tmp['products_elements_tracked']=[["C", "C", "C", "C", "C", "C"]]
        row_tmp['reactants_positions_tracked']=[[0, 1, 2, 3, 4, 5]]
        row_tmp['products_positions_tracked']=[[0, 1, 2, 3, 4, 5]]
        row_tmp['reactants_mapping']=['abcdef']
        row_tmp['products_mapping']=['abcdef']
        row_tmp['used_']=True
        row_tmp['comment_']='added'
        atomMappingReactions.append(row_tmp);
        #make GLCptspp  "glc_DASH_D_p + pep_c --> g6p_c + pyr_c"
        rxn_mets = {};
        rxn_mets[glc_e] = -1;
        rxn_mets[pep] = -1;
        rxn_mets[g6p] = 1;
        rxn_mets[pyr] = 1;
        rxn = Reaction('GLCptspp');
        rxn.add_metabolites(rxn_mets);
        cobra_model.add_reactions([rxn]);
        cobra_model.reactions.get_by_id(rxn.id).lower_bound = 0.0;
        cobra_model.reactions.get_by_id(rxn.id).upper_bound = 1000;
        cobra_model.repair();
        #append the new atom mappings
        row_tmp = {};
        row_tmp['mapping_id']=mapping_id_O;
        row_tmp['rxn_id']='GLCptspp';
        row_tmp['rxn_description']='';
        row_tmp['rxn_equation']='';
        row_tmp['reactants_stoichiometry_tracked']=[-1,-1]
        row_tmp['products_stoichiometry_tracked']=[1,1]
        row_tmp['reactants_ids_tracked']=['glc_DASH_D_e','pep_c']
        row_tmp['products_ids_tracked']=['g6p_c','pyr_c']
        row_tmp['reactants_elements_tracked']=[["C", "C", "C", "C", "C", "C"],["C", "C", "C"]]
        row_tmp['products_elements_tracked']=[["C", "C", "C", "C", "C", "C"],["C", "C", "C"]]
        row_tmp['reactants_positions_tracked']=[[0, 1, 2, 3, 4, 5],[0, 1, 2]]
        row_tmp['products_positions_tracked']=[[0, 1, 2, 3, 4, 5],[0, 1, 2]]
        row_tmp['reactants_mapping']=['abcdef','ghi']
        row_tmp['products_mapping']=['abcdef','ghi']
        row_tmp['used_']=True
        row_tmp['comment_']='added'
        atomMappingReactions.append(row_tmp);
        #make GLCt2pp "glc_DASH_D_p + h_p --> glc_DASH_D_c + h_c" 
        rxn_mets = {};
        rxn_mets[glc_e] = -1;
        rxn_mets[glc_c] = 1;
        rxn = Reaction('GLCt2pp');
        rxn.add_metabolites(rxn_mets);
        cobra_model.add_reactions([rxn]);
        cobra_model.reactions.get_by_id(rxn.id).lower_bound = 0.0;
        cobra_model.reactions.get_by_id(rxn.id).upper_bound = 1000.0;
        cobra_model.repair();
        #append the new atom mappings
        row_tmp = {};
        row_tmp['mapping_id']=mapping_id_O;
        row_tmp['rxn_id']='GLCt2pp';
        row_tmp['rxn_description']='';
        row_tmp['rxn_equation']='';
        row_tmp['reactants_stoichiometry_tracked']=[-1]
        row_tmp['products_stoichiometry_tracked']=[1]
        row_tmp['reactants_ids_tracked']=['glc_DASH_D_e']
        row_tmp['products_ids_tracked']=['glc_DASH_D_c']
        row_tmp['reactants_elements_tracked']=[["C", "C", "C", "C", "C", "C"]]
        row_tmp['products_elements_tracked']=[["C", "C", "C", "C", "C", "C"]]
        row_tmp['reactants_positions_tracked']=[[0, 1, 2, 3, 4, 5]]
        row_tmp['products_positions_tracked']=[[0, 1, 2, 3, 4, 5]]
        row_tmp['reactants_mapping']=['abcdef']
        row_tmp['products_mapping']=['abcdef']
        row_tmp['used_']=True
        row_tmp['comment_']='added'
        atomMappingReactions.append(row_tmp);
        #make HEX1 "atp_c + glc_DASH_D_c --> g6p_c + h_c + adp_c"  
        rxn_mets = {};
        rxn_mets[glc_c] = -1;
        rxn_mets[g6p] = 1;
        rxn = Reaction('HEX1');
        rxn.add_metabolites(rxn_mets);
        cobra_model.add_reactions([rxn]);
        cobra_model.reactions.get_by_id(rxn.id).lower_bound = 0.0;
        cobra_model.reactions.get_by_id(rxn.id).upper_bound = 1000.0;
        cobra_model.repair();
        #append the new atom mappings
        row_tmp = {};
        row_tmp['mapping_id']=mapping_id_O;
        row_tmp['rxn_id']='HEX1';
        row_tmp['rxn_description']='';
        row_tmp['rxn_equation']='';
        row_tmp['reactants_stoichiometry_tracked']=[-1]
        row_tmp['products_stoichiometry_tracked']=[1]
        row_tmp['reactants_ids_tracked']=['glc_DASH_D_c']
        row_tmp['products_ids_tracked']=['g6p_c']
        row_tmp['reactants_elements_tracked']=[["C", "C", "C", "C", "C", "C"]]
        row_tmp['products_elements_tracked']=[["C", "C", "C", "C", "C", "C"]]
        row_tmp['reactants_positions_tracked']=[[0, 1, 2, 3, 4, 5]]
        row_tmp['products_positions_tracked']=[[0, 1, 2, 3, 4, 5]]
        row_tmp['reactants_mapping']=['abcdef']
        row_tmp['products_mapping']=['abcdef']
        row_tmp['used_']=True
        row_tmp['comment_']='added'
        atomMappingReactions.append(row_tmp);

        ##expand the model
        #acon = Metabolite('acon_DASH_C_c','C6H3O6','cis-Aconitate','c');
        #cit = cobra_model.metabolites.get_by_id('cit_c')
        #icit = cobra_model.metabolites.get_by_id('icit_c')
        #e4p = cobra_model.metabolites.get_by_id('e4p_c')
        #r5p = cobra_model.metabolites.get_by_id('r5p_c')
        #phe = cobra_model.metabolites.get_by_id('phe_DASH_L_c')
        #his = cobra_model.metabolites.get_by_id('his_DASH_L_c')
        #phpyr = Metabolite('phpyr_c','C9H7O3','Phenylpyruvate','c');
        #prpp = Metabolite('prpp_c','C5H8O14P3','5-Phospho-alpha-D-ribose 1-diphosphate','c');
        ## update selected reactions to account for new metabolites
        #for rxn,row in enumerate(atomMappingReactions):
        #    if row['rxn_id'] == 'ACONTa_ACONTb':
        #        #split ACONTa_ACONTb
        #        aconta_mets = {};
        #        aconta_mets[cit] = -1;
        #        aconta_mets[acon] = 1;
        #        aconta = Reaction('ACONTa');
        #        aconta.add_metabolites(aconta_mets);
        #        cobra_model.remove_reactions(['ACONTa_ACONTb']);
        #        cobra_model.add_reactions([aconta]);
        #        cobra_model.repair();
        #        # Update the mapping ids
        #        atomMappingReactions[rxn]['products_ids_tracked']=['acon_DASH_C_c']
        #        atomMappingReactions[rxn]['comment_']='updated'
        #    elif row['rxn_id'] == 'PheSYN':
        #        #split PheSYN to add in phpyr

        #        # Update the mapping_ids
        #        atomMappingReactions[rxn]['mapping_id']=mapping_id_O;
        #        atomMappingReactions[rxn]['rxn_id']=rxn_ids[rxn];
        #        atomMappingReactions[rxn]['rxn_description']='';
        #        atomMappingReactions[rxn]['rxn_equation']='';
        #        atomMappingReactions[rxn]['reactants_stoichiometry_tracked']=[]
        #        atomMappingReactions[rxn]['products_stoichiometry_tracked']=[]
        #        atomMappingReactions[rxn]['reactants_ids_tracked']=[]
        #        atomMappingReactions[rxn]['products_ids_tracked']=[]
        #        atomMappingReactions[rxn]['reactants_elements_tracked']=[]
        #        atomMappingReactions[rxn]['products_elements_tracked']=[]
        #        atomMappingReactions[rxn]['reactants_positions_tracked']=[]
        #        atomMappingReactions[rxn]['products_positions_tracked']=[]
        #        atomMappingReactions[rxn]['reactants_mapping']=[]
        #        atomMappingReactions[rxn]['products_mapping']=[]
        #        atomMappingReactions[rxn]['used_']=True
        #        atomMappingReactions[rxn]['comment_']=None
        #    elif row['rxn_id'] == 'HisSYN':
        #        # split HisSYN to add in prpp
        #        #cobra_model.reactions.get_by_id(rxn_ids[rxn])
        #        #cobra_model.reactions.get_by_id(rxn_ids[rxn])
        #        # Update the mapping_ids
        #        atomMappingReactions[rxn]['reactants_ids_tracked']=[r.replace('r5p_c','prpp_c') for r in atomMappingReactions[rxn]['reactants_ids_tracked']]

        #        # combine TKT1a and TKT1b
        #        # combine TKT2a and TKT2b
        #        # split PPC_PPCK
        #        # split PTAr_ACKr_ACS

        ## add in ACONTb
        #acontb_mets = {};
        #acontb_mets[acon] = -1;
        #acontb_mets[icit] = 1;
        #acontb = Reaction('ACONTb');
        #acontb.add_metabolites(acontb_mets);
        #cobra_model.add_reactions([acontb]);
        #cobra_model.repair();
        ## add in ACONTb mapping
        #row={};
        #row['mapping_id']=mapping_id_O;
        #row['rxn_id']='ACONTb';
        #row['rxn_description']='';
        #row['rxn_equation']='';
        #row['reactants_stoichiometry_tracked']=[-1]
        #row['products_stoichiometry_tracked']=[1]
        #row['reactants_ids_tracked']=['acon_DASH_C_c']
        #row['products_ids_tracked']=['icit_c']
        #row['reactants_elements_tracked']=[["C", "C", "C", "C", "C", "C"]]
        #row['products_elements_tracked']=[["C", "C", "C", "C", "C", "C"]]
        #row['reactants_positions_tracked']=[[0, 1, 2, 3, 4, 5]]
        #row['products_positions_tracked']=[[0, 1, 2, 3, 4, 5]]
        #row['reactants_mapping']=['abcdef']
        #row['products_mapping']=['abcdef']
        #row['used_']=True
        #row['comment_']='added'
        #atomMappingReactions.append(row)    
        ## add in e4p_to_phpyr

        ## add in r5p_to_prp 
        #r5p_to_prpp_mets = {};
        #r5p_to_prpp_mets[e4p] = -1;
        #r5p_to_prpp_mets[prpp] = 1;
        #r5p_to_prpp = Reaction('r5p_to_prpp');
        #r5p_to_prpp.add_metabolites(r5p_to_prpp_mets);
        #cobra_model.add_reactions([r5p_to_prpp]);
        #cobra_model.repair(); 
        ## add in r5p_to_prpp mapping
        #row={};
        #row['mapping_id']=mapping_id_O;
        #row['rxn_id']='r5p_to_prpp';
        #row['rxn_description']='';
        #row['rxn_equation']='';
        #row['reactants_stoichiometry_tracked']=[-1]
        #row['products_stoichiometry_tracked']=[1]
        #row['reactants_ids_tracked']=['r5p_c']
        #row['products_ids_tracked']=['prpp_c']
        #row['reactants_elements_tracked']=[["C", "C", "C", "C", "C"]]
        #row['products_elements_tracked']=[["C", "C", "C", "C", "C"]]
        #row['reactants_positions_tracked']=[[0, 1, 2, 3, 4]]
        #row['products_positions_tracked']=[[0, 1, 2, 3, 4]]
        #row['reactants_mapping']=['abcde']
        #row['products_mapping']=['abcde']
        #row['used_']=True
        #row['comment_']='added'
        #atomMappingReactions.append(row)   
    
        # write the model to a temporary file
        save_json_model(cobra_model,'data\\cobra_model_tmp.json')
        
        # add the model information to the database
        io = stage02_isotopomer_io()
        dataStage02IsotopomerModelRxns_data = [];
        dataStage02IsotopomerModelMets_data = [];
        dataStage02IsotopomerModels_data,\
            dataStage02IsotopomerModelRxns_data,\
            dataStage02IsotopomerModelMets_data = io._parse_model_json(model_id_O, date_I, 'data\\cobra_model_tmp.json')
        io.add_data_stage02_isotopomer_modelMetabolites(dataStage02IsotopomerModelMets_data);
        io.add_data_stage02_isotopomer_modelReactions(dataStage02IsotopomerModelRxns_data);
        io.add_data_stage02_isotopomer_models(dataStage02IsotopomerModels_data);

        #add atomMappingReactions to the database
        io.add_data_stage02_isotopomer_atomMappingReactions(atomMappingReactions);
    def expand_ecoliINCA02(self,experiment_id_I,model_id_I,mapping_id_I,date_I,model_id_O,mapping_id_O):
        '''expand the INCA Ecoli model to account for additional metabolites'''

        query = stage02_isotopomer_query()
        # get the xml model
        cobra_model_sbml = ''
        cobra_model_sbml = query.get_row_modelID_dataStage02IsotopomerModels(model_id_I);
        # load the model
        if cobra_model_sbml:
            if cobra_model_sbml['file_type'] == 'sbml':
                with open('data\\cobra_model_tmp.xml','wb') as file:
                    file.write(cobra_model_sbml['model_file']);
                    file.close()
                cobra_model = None;
                cobra_model = create_cobra_model_from_sbml_file('data\\cobra_model_tmp.xml', print_time=True);
            elif cobra_model_sbml['file_type'] == 'json':
                with open('data\\cobra_model_tmp.json','wb') as file:
                    file.write(cobra_model_sbml['model_file']);
                    file.close()
                cobra_model = None;
                cobra_model = load_json_model('data\\cobra_model_tmp.json');
            else:
                print 'file_type not supported'

        #get the atomMapping_reactions
        atomMappingReactions = query.get_rows_mappingID_dataStage02IsotopomerAtomMappingReactions(mapping_id_I);
        #change the mapping_id
        for cnt,row in enumerate(atomMappingReactions):
            atomMappingReactions[cnt]['mapping_id']=mapping_id_O;
        accoa = cobra_model.metabolites.get_by_id('accoa_c')

        #expand the model to include ATPSYN:
        #get metabolites not in the model
        met_row = {}
        met_row = query.get_row_modelIDAndMetID_dataStage02IsotopomerModelMetabolites('140407_iDM2014','atp_c');
        atp = Metabolite(met_row['met_id'],met_row['formula'],met_row['met_name'],'c')
        atp.charge = met_row['charge']
        #get metabolites in the model
        r5p = cobra_model.metabolites.get_by_id('r5p_c')
        fthf = cobra_model.metabolites.get_by_id('10fthf_c')
        gly = cobra_model.metabolites.get_by_id('gly_c')
        co2 = cobra_model.metabolites.get_by_id('co2_c')
        glu = cobra_model.metabolites.get_by_id('glu_DASH_L_c')
        gln = cobra_model.metabolites.get_by_id('gln_DASH_L_c')
        asp = cobra_model.metabolites.get_by_id('asp_DASH_L_c')
        fum = cobra_model.metabolites.get_by_id('fum_c')
        #make ATPSYN (irreversible)
        rxn_mets = {};
        rxn_mets[r5p] = -1;
        rxn_mets[fthf] = -1;
        rxn_mets[gly] = -1;
        rxn_mets[co2] = -1;
        rxn_mets[fthf] = -1;
        rxn_mets[gln] = -1;
        rxn_mets[asp] = -1;
        rxn_mets[asp] = -1;
        rxn_mets[atp] = 1;
        rxn_mets[glu] = 1;
        rxn_mets[fum] = 1;
        rxn_mets[fum] = 1;
        rxn = Reaction('ATPSYN');
        rxn.add_metabolites(rxn_mets);
        cobra_model.add_reactions([rxn]);
        cobra_model.reactions.get_by_id(rxn.id).lower_bound = 0.0;
        cobra_model.reactions.get_by_id(rxn.id).upper_bound = 1000;
        cobra_model.repair();

        #expand the model to include GTPSYN:
        #get metabolites not in the model
        met_row = {}
        met_row = query.get_row_modelIDAndMetID_dataStage02IsotopomerModelMetabolites('140407_iDM2014','gtp_c');
        gtp = Metabolite(met_row['met_id'],met_row['formula'],met_row['met_name'],'c')
        gtp.charge = met_row['charge']
        #get metabolites in the model
        r5p = cobra_model.metabolites.get_by_id('r5p_c')
        fthf = cobra_model.metabolites.get_by_id('10fthf_c')
        gly = cobra_model.metabolites.get_by_id('gly_c')
        co2 = cobra_model.metabolites.get_by_id('co2_c')
        glu = cobra_model.metabolites.get_by_id('glu_DASH_L_c')
        gln = cobra_model.metabolites.get_by_id('gln_DASH_L_c')
        asp = cobra_model.metabolites.get_by_id('asp_DASH_L_c')
        fum = cobra_model.metabolites.get_by_id('fum_c')
        #make GTPSYN (irreversible)
        rxn_mets = {};
        rxn_mets[r5p] = -1;
        rxn_mets[fthf] = -1;
        rxn_mets[gly] = -1;
        rxn_mets[co2] = -1;
        rxn_mets[fthf] = -1;
        rxn_mets[gln] = -1;
        rxn_mets[gln] = -1;
        rxn_mets[asp] = -1;
        rxn_mets[gtp] = 1;
        rxn_mets[glu] = 1;
        rxn_mets[glu] = 1;
        rxn_mets[fum] = 1;
        rxn = Reaction('GTPSYN');
        rxn.add_metabolites(rxn_mets);
        cobra_model.add_reactions([rxn]);
        cobra_model.reactions.get_by_id(rxn.id).lower_bound = 0.0;
        cobra_model.reactions.get_by_id(rxn.id).upper_bound = 1000;
        cobra_model.repair();

        #expand the model to include VPMATr_reverse and VPMATr:
        #get metabolites not in the model
        met_row = {}
        met_row = query.get_row_modelIDAndMetID_dataStage02IsotopomerModelMetabolites('140407_iDM2014','3mob_c');
        mob3 = Metabolite(met_row['met_id'],met_row['formula'],met_row['met_name'],'c')
        mob3.charge = met_row['charge']
        #get metabolites in the model
        val = cobra_model.metabolites.get_by_id('val_DASH_L_c')
        ala = cobra_model.metabolites.get_by_id('ala_DASH_L_c')
        pyr = cobra_model.metabolites.get_by_id('pyr_c')
        #make VPMATr_reverse (irreversible)
        rxn_mets = {};
        rxn_mets[val] = -1;
        rxn_mets[pyr] = -1;
        rxn_mets[mob3] = 1;
        rxn_mets[ala] = 1;
        rxn = Reaction('VPMATr_reverse');
        rxn.add_metabolites(rxn_mets);
        cobra_model.add_reactions([rxn]);
        cobra_model.reactions.get_by_id(rxn.id).lower_bound = 0.0;
        cobra_model.reactions.get_by_id(rxn.id).upper_bound = 1000;
        cobra_model.repair();
        #make VPMATr (irreversible)
        rxn_mets = {};
        rxn_mets[mob3] = -1;
        rxn_mets[ala] = -1;
        rxn_mets[val] = 1;
        rxn_mets[pyr] = 1;
        rxn = Reaction('VPMATr');
        rxn.add_metabolites(rxn_mets);
        cobra_model.add_reactions([rxn]);
        cobra_model.reactions.get_by_id(rxn.id).lower_bound = 0.0;
        cobra_model.reactions.get_by_id(rxn.id).upper_bound = 1000;
        cobra_model.repair();

        #expand the model to include COASYN:
        #get metabolites not in the model
        met_row = {}
        met_row = query.get_row_modelIDAndMetID_dataStage02IsotopomerModelMetabolites('140407_iDM2014','coa_c');
        coa = Metabolite(met_row['met_id'],met_row['formula'],met_row['met_name'],'c')
        coa.charge = met_row['charge']
        #get metabolites in the model
        cys = cobra_model.metabolites.get_by_id('cys_DASH_L_c')
        mlthf = cobra_model.metabolites.get_by_id('mlthf_c')
        #make COASYN (irreversible)
        rxn_mets = {};
        rxn_mets[atp] = -1;
        rxn_mets[mlthf] = -1;
        rxn_mets[mob3] = -1;
        rxn_mets[asp] = -1;
        rxn_mets[cys] = -1;
        rxn_mets[coa] = 1;
        rxn_mets[co2] = 1;
        rxn_mets[co2] = 1;
        rxn = Reaction('COASYN');
        rxn.add_metabolites(rxn_mets);
        cobra_model.add_reactions([rxn]);
        cobra_model.reactions.get_by_id(rxn.id).lower_bound = 0.0;
        cobra_model.reactions.get_by_id(rxn.id).upper_bound = 1000;
        cobra_model.repair();

        #expand the model to include FADSYN:
        #get metabolites not in the model
        met_row = {}
        met_row = query.get_row_modelIDAndMetID_dataStage02IsotopomerModelMetabolites('140407_iDM2014','fad_c');
        fad = Metabolite(met_row['met_id'],met_row['formula'],met_row['met_name'],'c')
        fad.charge = met_row['charge']
        #get metabolites in the model
        ru5p = cobra_model.metabolites.get_by_id('ru5p_DASH_D_c')
        #make FADSYN (irreversible)
        rxn_mets = {};
        rxn_mets[gtp] = -1;
        rxn_mets[ru5p] = -1;
        rxn_mets[ru5p] = -1;
        rxn_mets[atp] = -1;
        rxn_mets[fad] = 1;
        rxn_mets[co2] = 1;
        rxn_mets[co2] = 1;
        rxn_mets[co2] = 1;
        rxn = Reaction('FADSYN');
        rxn.add_metabolites(rxn_mets);
        cobra_model.add_reactions([rxn]);
        cobra_model.reactions.get_by_id(rxn.id).lower_bound = 0.0;
        cobra_model.reactions.get_by_id(rxn.id).upper_bound = 1000;
        cobra_model.repair();
        
        #expand the model to include CBMKr and CBMKr_reverse:
        #get metabolites not in the model
        met_row = {}
        met_row = query.get_row_modelIDAndMetID_dataStage02IsotopomerModelMetabolites('140407_iDM2014','cbp_c');
        cbp = Metabolite(met_row['met_id'],met_row['formula'],met_row['met_name'],'c')
        cbp.charge = met_row['charge']
        #make CBMKr (irreversible)
        rxn_mets = {};
        rxn_mets[co2] = -1;
        rxn_mets[cbp] = 1;
        rxn = Reaction('CBMKr');
        rxn.add_metabolites(rxn_mets);
        cobra_model.add_reactions([rxn]);
        cobra_model.reactions.get_by_id(rxn.id).lower_bound = 0.0;
        cobra_model.reactions.get_by_id(rxn.id).upper_bound = 1000;
        cobra_model.repair();
        #make CBMKr_reverse (irreversible)
        rxn_mets = {};
        rxn_mets[cbp] = -1;
        rxn_mets[co2] = 1;
        rxn = Reaction('CBMKr_reverse');
        rxn.add_metabolites(rxn_mets);
        cobra_model.add_reactions([rxn]);
        cobra_model.reactions.get_by_id(rxn.id).lower_bound = 0.0;
        cobra_model.reactions.get_by_id(rxn.id).upper_bound = 1000;
        cobra_model.repair();

        #expand the model to include UTPSYN:
        #get metabolites not in the model
        met_row = {}
        met_row = query.get_row_modelIDAndMetID_dataStage02IsotopomerModelMetabolites('140407_iDM2014','utp_c');
        utp = Metabolite(met_row['met_id'],met_row['formula'],met_row['met_name'],'c')
        utp.charge = met_row['charge']
        #make UTPSYN (irreversible)
        rxn_mets = {};
        rxn_mets[r5p] = -1;
        rxn_mets[cbp] = -1;
        rxn_mets[asp] = -1;
        rxn_mets[utp] = 1;
        rxn_mets[co2] = 1;
        rxn = Reaction('UTPSYN');
        rxn.add_metabolites(rxn_mets);
        cobra_model.add_reactions([rxn]);
        cobra_model.reactions.get_by_id(rxn.id).lower_bound = 0.0;
        cobra_model.reactions.get_by_id(rxn.id).upper_bound = 1000;
        cobra_model.repair();

        # update selected reactions to account for coa_c
        cobra_model.reactions.get_by_id("ArgSYN").add_metabolites({coa:1});
        cobra_model.reactions.get_by_id("CS").add_metabolites({coa:1});
        cobra_model.reactions.get_by_id("LeuSYN").add_metabolites({coa:1});
        cobra_model.reactions.get_by_id("PDH").add_metabolites({coa:-1});
        cobra_model.reactions.get_by_id("PTAr_ACKr_ACS").add_metabolites({coa:1});
        cobra_model.reactions.get_by_id("PTAr_ACKr_ACS_reverse").add_metabolites({coa:-1});
        cobra_model.reactions.get_by_id("SERAT_CYSS").add_metabolites({coa:1});
        cobra_model.reactions.get_by_id("THRD_GLYAT").add_metabolites({coa:-1});
        cobra_model.reactions.get_by_id("MALS").add_metabolites({coa:1});

        # update selected mappings to account for coa_c
        for rxn,row in enumerate(atomMappingReactions):
            if row['rxn_id'] == 'ArgSYN':
                atomMappingReactions[rxn]['reactants_stoichiometry_tracked']=[-1,-1,-1,-1,-1]
                atomMappingReactions[rxn]['products_stoichiometry_tracked']=[1,1,1,1,1]
                atomMappingReactions[rxn]['reactants_ids_tracked']=['glu_DASH_L_c','co2_c','gln_DASH_L_c','asp_DASH_L_c','accoa_c']
                atomMappingReactions[rxn]['products_ids_tracked']=['arg_DASH_L_c','akg_c','fum_c','ac_c','coa_c']
                atomMappingReactions[rxn]['reactants_mapping']=['abcde','f','ghijk','lmno','ABCDEFGHIJKLMNOPQRSTUpq']
                atomMappingReactions[rxn]['products_mapping']=['abcdef','ghijk','lmno','pq','ABCDEFGHIJKLMNOPQRSTU']
                atomMappingReactions[rxn]['reactants_elements_tracked']=[]
                atomMappingReactions[rxn]['products_elements_tracked']=[]
                atomMappingReactions[rxn]['reactants_positions_tracked']=[]
                atomMappingReactions[rxn]['products_positions_tracked']=[]
                for cnt,mapping in enumerate(atomMappingReactions[rxn]['reactants_mapping']):
                    positions = []
                    elements = []
                    for pos,element in enumerate(mapping):
                        positions.append(pos);
                        elements.append('C');
                    atomMappingReactions[rxn]['reactants_elements_tracked'].append(elements)
                    atomMappingReactions[rxn]['reactants_positions_tracked'].append(positions)
                for cnt,mapping in enumerate(atomMappingReactions[rxn]['products_mapping']):
                    positions = []
                    elements = []
                    for pos,element in enumerate(mapping):
                        positions.append(pos);
                        elements.append('C');
                    atomMappingReactions[rxn]['products_elements_tracked'].append(elements)
                    atomMappingReactions[rxn]['products_positions_tracked'].append(positions)


            elif row['rxn_id'] == 'CS':
                atomMappingReactions[rxn]['reactants_stoichiometry_tracked']=[-1,-1]
                atomMappingReactions[rxn]['products_stoichiometry_tracked']=[1,1]
                atomMappingReactions[rxn]['reactants_ids_tracked']=['oaa_c','accoa_c']
                atomMappingReactions[rxn]['products_ids_tracked']=['cit_c','coa_c']
                atomMappingReactions[rxn]['reactants_mapping']=['abcd','ABCDEFGHIJKLMNOPQRSTUef']
                atomMappingReactions[rxn]['products_mapping']=['dcbfea','ABCDEFGHIJKLMNOPQRSTU']
                atomMappingReactions[rxn]['reactants_elements_tracked']=[]
                atomMappingReactions[rxn]['products_elements_tracked']=[]
                atomMappingReactions[rxn]['reactants_positions_tracked']=[]
                atomMappingReactions[rxn]['products_positions_tracked']=[]
                for cnt,mapping in enumerate(atomMappingReactions[rxn]['reactants_mapping']):
                    positions = []
                    elements = []
                    for pos,element in enumerate(mapping):
                        positions.append(pos);
                        elements.append('C');
                    atomMappingReactions[rxn]['reactants_elements_tracked'].append(elements)
                    atomMappingReactions[rxn]['reactants_positions_tracked'].append(positions)
                for cnt,mapping in enumerate(atomMappingReactions[rxn]['products_mapping']):
                    positions = []
                    elements = []
                    for pos,element in enumerate(mapping):
                        positions.append(pos);
                        elements.append('C');
                    atomMappingReactions[rxn]['products_elements_tracked'].append(elements)
                    atomMappingReactions[rxn]['products_positions_tracked'].append(positions)

            elif row['rxn_id'] == 'LeuSYN':
                atomMappingReactions[rxn]['reactants_stoichiometry_tracked']=[-1,-1,-1,-1]
                atomMappingReactions[rxn]['products_stoichiometry_tracked']=[1,1,1,1,1]
                atomMappingReactions[rxn]['reactants_ids_tracked']=['accoa_c','pyr_c','pyr_c','glu_DASH_L_c']
                atomMappingReactions[rxn]['products_ids_tracked']=['leu_DASH_L_c','co2_c','co2_c','akg_c','coa_c']
                atomMappingReactions[rxn]['reactants_mapping']=['ABCDEFGHIJKLMNOPQRSTUab','cde','fgh','ijklm']
                atomMappingReactions[rxn]['products_mapping']=['abdghe','c','f','ijklm','ABCDEFGHIJKLMNOPQRSTU']
                atomMappingReactions[rxn]['reactants_elements_tracked']=[]
                atomMappingReactions[rxn]['products_elements_tracked']=[]
                atomMappingReactions[rxn]['reactants_positions_tracked']=[]
                atomMappingReactions[rxn]['products_positions_tracked']=[]
                for cnt,mapping in enumerate(atomMappingReactions[rxn]['reactants_mapping']):
                    positions = []
                    elements = []
                    for pos,element in enumerate(mapping):
                        positions.append(pos);
                        elements.append('C');
                    atomMappingReactions[rxn]['reactants_elements_tracked'].append(elements)
                    atomMappingReactions[rxn]['reactants_positions_tracked'].append(positions)
                for cnt,mapping in enumerate(atomMappingReactions[rxn]['products_mapping']):
                    positions = []
                    elements = []
                    for pos,element in enumerate(mapping):
                        positions.append(pos);
                        elements.append('C');
                    atomMappingReactions[rxn]['products_elements_tracked'].append(elements)
                    atomMappingReactions[rxn]['products_positions_tracked'].append(positions)

            elif row['rxn_id'] == 'PDH':
                atomMappingReactions[rxn]['reactants_stoichiometry_tracked']=[-1,-1]
                atomMappingReactions[rxn]['products_stoichiometry_tracked']=[1,1]
                atomMappingReactions[rxn]['reactants_ids_tracked']=['pyr_c','coa_c']
                atomMappingReactions[rxn]['products_ids_tracked']=['accoa_c','co2_c']
                atomMappingReactions[rxn]['reactants_mapping']=['abc','ABCDEFGHIJKLMNOPQRSTU']
                atomMappingReactions[rxn]['products_mapping']=['ABCDEFGHIJKLMNOPQRSTUbc','a']
                atomMappingReactions[rxn]['reactants_elements_tracked']=[]
                atomMappingReactions[rxn]['products_elements_tracked']=[]
                atomMappingReactions[rxn]['reactants_positions_tracked']=[]
                atomMappingReactions[rxn]['products_positions_tracked']=[]
                for cnt,mapping in enumerate(atomMappingReactions[rxn]['reactants_mapping']):
                    positions = []
                    elements = []
                    for pos,element in enumerate(mapping):
                        positions.append(pos);
                        elements.append('C');
                    atomMappingReactions[rxn]['reactants_elements_tracked'].append(elements)
                    atomMappingReactions[rxn]['reactants_positions_tracked'].append(positions)
                for cnt,mapping in enumerate(atomMappingReactions[rxn]['products_mapping']):
                    positions = []
                    elements = []
                    for pos,element in enumerate(mapping):
                        positions.append(pos);
                        elements.append('C');
                    atomMappingReactions[rxn]['products_elements_tracked'].append(elements)
                    atomMappingReactions[rxn]['products_positions_tracked'].append(positions)

            elif row['rxn_id'] == 'PTAr_ACKr_ACS':
                atomMappingReactions[rxn]['reactants_stoichiometry_tracked']=[-1]
                atomMappingReactions[rxn]['products_stoichiometry_tracked']=[1,1]
                atomMappingReactions[rxn]['reactants_ids_tracked']=['accoa_c']
                atomMappingReactions[rxn]['products_ids_tracked']=['ac_c','coa_c']
                atomMappingReactions[rxn]['reactants_mapping']=['ABCDEFGHIJKLMNOPQRSTUab']
                atomMappingReactions[rxn]['products_mapping']=['ab','ABCDEFGHIJKLMNOPQRSTU']
                atomMappingReactions[rxn]['reactants_elements_tracked']=[]
                atomMappingReactions[rxn]['products_elements_tracked']=[]
                atomMappingReactions[rxn]['reactants_positions_tracked']=[]
                atomMappingReactions[rxn]['products_positions_tracked']=[]
                for cnt,mapping in enumerate(atomMappingReactions[rxn]['reactants_mapping']):
                    positions = []
                    elements = []
                    for pos,element in enumerate(mapping):
                        positions.append(pos);
                        elements.append('C');
                    atomMappingReactions[rxn]['reactants_elements_tracked'].append(elements)
                    atomMappingReactions[rxn]['reactants_positions_tracked'].append(positions)
                for cnt,mapping in enumerate(atomMappingReactions[rxn]['products_mapping']):
                    positions = []
                    elements = []
                    for pos,element in enumerate(mapping):
                        positions.append(pos);
                        elements.append('C');
                    atomMappingReactions[rxn]['products_elements_tracked'].append(elements)
                    atomMappingReactions[rxn]['products_positions_tracked'].append(positions)

            elif row['rxn_id'] == 'PTAr_ACKr_ACS_reverse':
                atomMappingReactions[rxn]['reactants_stoichiometry_tracked']=[-1,-1]
                atomMappingReactions[rxn]['products_stoichiometry_tracked']=[1]
                atomMappingReactions[rxn]['reactants_ids_tracked']=['ac_c','coa_c']
                atomMappingReactions[rxn]['products_ids_tracked']=['accoa_c']
                atomMappingReactions[rxn]['reactants_mapping']=['ab','ABCDEFGHIJKLMNOPQRSTU']
                atomMappingReactions[rxn]['products_mapping']=['ABCDEFGHIJKLMNOPQRSTUab']
                atomMappingReactions[rxn]['reactants_elements_tracked']=[]
                atomMappingReactions[rxn]['products_elements_tracked']=[]
                atomMappingReactions[rxn]['reactants_positions_tracked']=[]
                atomMappingReactions[rxn]['products_positions_tracked']=[]
                for cnt,mapping in enumerate(atomMappingReactions[rxn]['reactants_mapping']):
                    positions = []
                    elements = []
                    for pos,element in enumerate(mapping):
                        positions.append(pos);
                        elements.append('C');
                    atomMappingReactions[rxn]['reactants_elements_tracked'].append(elements)
                    atomMappingReactions[rxn]['reactants_positions_tracked'].append(positions)
                for cnt,mapping in enumerate(atomMappingReactions[rxn]['products_mapping']):
                    positions = []
                    elements = []
                    for pos,element in enumerate(mapping):
                        positions.append(pos);
                        elements.append('C');
                    atomMappingReactions[rxn]['products_elements_tracked'].append(elements)
                    atomMappingReactions[rxn]['products_positions_tracked'].append(positions)

            elif row['rxn_id'] == 'SERAT_CYSS':
                atomMappingReactions[rxn]['reactants_stoichiometry_tracked']=[-1,-1]
                atomMappingReactions[rxn]['products_stoichiometry_tracked']=[1,1,1]
                atomMappingReactions[rxn]['reactants_ids_tracked']=['ser_DASH_L_c','accoa_c']
                atomMappingReactions[rxn]['products_ids_tracked']=['cys_DASH_L_c','ac_c','coa_c']
                atomMappingReactions[rxn]['reactants_mapping']=['abc','ABCDEFGHIJKLMNOPQRSTUde']
                atomMappingReactions[rxn]['products_mapping']=['abc','de','ABCDEFGHIJKLMNOPQRSTU']
                atomMappingReactions[rxn]['reactants_elements_tracked']=[]
                atomMappingReactions[rxn]['products_elements_tracked']=[]
                atomMappingReactions[rxn]['reactants_positions_tracked']=[]
                atomMappingReactions[rxn]['products_positions_tracked']=[]
                for cnt,mapping in enumerate(atomMappingReactions[rxn]['reactants_mapping']):
                    positions = []
                    elements = []
                    for pos,element in enumerate(mapping):
                        positions.append(pos);
                        elements.append('C');
                    atomMappingReactions[rxn]['reactants_elements_tracked'].append(elements)
                    atomMappingReactions[rxn]['reactants_positions_tracked'].append(positions)
                for cnt,mapping in enumerate(atomMappingReactions[rxn]['products_mapping']):
                    positions = []
                    elements = []
                    for pos,element in enumerate(mapping):
                        positions.append(pos);
                        elements.append('C');
                    atomMappingReactions[rxn]['products_elements_tracked'].append(elements)
                    atomMappingReactions[rxn]['products_positions_tracked'].append(positions)

            elif row['rxn_id'] == 'THRD_GLYAT':
                atomMappingReactions[rxn]['reactants_stoichiometry_tracked']=[-1,-1]
                atomMappingReactions[rxn]['products_stoichiometry_tracked']=[1,1]
                atomMappingReactions[rxn]['reactants_ids_tracked']=['thr_DASH_L_c','coa_c']
                atomMappingReactions[rxn]['products_ids_tracked']=['gly_c','accoa_c']
                atomMappingReactions[rxn]['reactants_mapping']=['abcd','ABCDEFGHIJKLMNOPQRSTU']
                atomMappingReactions[rxn]['products_mapping']=['ab','ABCDEFGHIJKLMNOPQRSTUcd']
                atomMappingReactions[rxn]['reactants_elements_tracked']=[]
                atomMappingReactions[rxn]['products_elements_tracked']=[]
                atomMappingReactions[rxn]['reactants_positions_tracked']=[]
                atomMappingReactions[rxn]['products_positions_tracked']=[]
                for cnt,mapping in enumerate(atomMappingReactions[rxn]['reactants_mapping']):
                    positions = []
                    elements = []
                    for pos,element in enumerate(mapping):
                        positions.append(pos);
                        elements.append('C');
                    atomMappingReactions[rxn]['reactants_elements_tracked'].append(elements)
                    atomMappingReactions[rxn]['reactants_positions_tracked'].append(positions)
                for cnt,mapping in enumerate(atomMappingReactions[rxn]['products_mapping']):
                    positions = []
                    elements = []
                    for pos,element in enumerate(mapping):
                        positions.append(pos);
                        elements.append('C');
                    atomMappingReactions[rxn]['products_elements_tracked'].append(elements)
                    atomMappingReactions[rxn]['products_positions_tracked'].append(positions)

            elif row['rxn_id'] == 'MALS':
                atomMappingReactions[rxn]['reactants_stoichiometry_tracked']=[-1,-1]
                atomMappingReactions[rxn]['products_stoichiometry_tracked']=[1,1]
                atomMappingReactions[rxn]['reactants_ids_tracked']=['accoa_c','glx_c']
                atomMappingReactions[rxn]['products_ids_tracked']=['mal_DASH_L_c','coa_c']
                atomMappingReactions[rxn]['reactants_mapping']=['ABCDEFGHIJKLMNOPQRSTUab','cd']
                atomMappingReactions[rxn]['products_mapping']=['cdba','ABCDEFGHIJKLMNOPQRSTU']
                atomMappingReactions[rxn]['reactants_elements_tracked']=[]
                atomMappingReactions[rxn]['products_elements_tracked']=[]
                atomMappingReactions[rxn]['reactants_positions_tracked']=[]
                atomMappingReactions[rxn]['products_positions_tracked']=[]
                for cnt,mapping in enumerate(atomMappingReactions[rxn]['reactants_mapping']):
                    positions = []
                    elements = []
                    for pos,element in enumerate(mapping):
                        positions.append(pos);
                        elements.append('C');
                    atomMappingReactions[rxn]['reactants_elements_tracked'].append(elements)
                    atomMappingReactions[rxn]['reactants_positions_tracked'].append(positions)
                for cnt,mapping in enumerate(atomMappingReactions[rxn]['products_mapping']):
                    positions = []
                    elements = []
                    for pos,element in enumerate(mapping):
                        positions.append(pos);
                        elements.append('C');
                    atomMappingReactions[rxn]['products_elements_tracked'].append(elements)
                    atomMappingReactions[rxn]['products_positions_tracked'].append(positions)

        # update BOF
        met_row = {}
        met_row = query.get_row_modelIDAndMetID_dataStage02IsotopomerModelMetabolites('140407_iDM2014','adp_c');
        adp = Metabolite(met_row['met_id'],met_row['formula'],met_row['met_name'],'c')
        adp.charge = met_row['charge']
        cobra_model.reactions.get_by_id("Ec_Biomass_INCA").add_metabolites({coa:2.51,
              atp:-53.95,gtp:-0.20912,fad:-0.000223,utp:-0.1401});

        # write the model to a temporary file
        save_json_model(cobra_model,'data\\cobra_model_tmp.json')
        
        # add the model information to the database
        io = stage02_isotopomer_io()
        dataStage02IsotopomerModelRxns_data = [];
        dataStage02IsotopomerModelMets_data = [];
        dataStage02IsotopomerModels_data,\
            dataStage02IsotopomerModelRxns_data,\
            dataStage02IsotopomerModelMets_data = io._parse_model_json(model_id_O, date_I, 'data\\cobra_model_tmp.json')
        io.add_data_stage02_isotopomer_modelMetabolites(dataStage02IsotopomerModelMets_data);
        io.add_data_stage02_isotopomer_modelReactions(dataStage02IsotopomerModelRxns_data);
        io.add_data_stage02_isotopomer_models(dataStage02IsotopomerModels_data);

        #add atomMappingReactions to the database
        io.add_data_stage02_isotopomer_atomMappingReactions(atomMappingReactions);
        
        # expand atomMappingReactions
        imm = stage02_isotopomer_metaboliteMapping()
        irm = stage02_isotopomer_reactionMapping()
        mappingUtilities = stage02_isotopomer_mappingUtilities()

        # make atomMappingMetabolites
        mappingUtilities.make_missingMetaboliteMappings(experiment_id_I,model_id_I=[model_id_O],
                                    mapping_id_rxns_I=[mapping_id_O],
                                    mapping_id_mets_I=[],#mapping_id_mets_I=[mapping_id_I],
                                    mapping_id_new_I=mapping_id_O);

        # update symmetric metabolites
        imm.get_metaboliteMapping(mapping_id_O,'succ_c')
        imm.make_symmetric()
        imm.update_metaboliteMapping()
        imm.clear_metaboliteMapping()
        imm.get_metaboliteMapping(mapping_id_O,'fum_c')
        imm.make_symmetric()
        imm.update_metaboliteMapping()
        imm.clear_metaboliteMapping()
        imm.get_metaboliteMapping(mapping_id_O,'26dap_DASH_M_c')
        imm.make_symmetric()
        imm.update_metaboliteMapping()
        imm.clear_metaboliteMapping()

        ## update _elements and _positions-_tracked
        #irm.get_reactionMapping(mapping_id_O,'ArgSYN')
        #irm.checkAndCorrect_elementsAndPositions();
        #irm.update_reactionMapping()
        #irm.clear_reactionMapping()
        #irm.get_reactionMapping(mapping_id_O,'CS')
        #irm.checkAndCorrect_elementsAndPositions();
        #irm.update_reactionMapping()
        #irm.clear_reactionMapping()
        #irm.get_reactionMapping(mapping_id_O,'LeuSYN')
        #irm.checkAndCorrect_elementsAndPositions();
        #irm.update_reactionMapping()
        #irm.clear_reactionMapping()
        #irm.get_reactionMapping(mapping_id_O,'PDH')
        #irm.checkAndCorrect_elementsAndPositions();
        #irm.update_reactionMapping()
        #irm.clear_reactionMapping()
        #irm.get_reactionMapping(mapping_id_O,'PTAr_ACKr_ACS')
        #irm.checkAndCorrect_elementsAndPositions();
        #irm.update_reactionMapping()
        #irm.clear_reactionMapping()
        #irm.get_reactionMapping(mapping_id_O,'PTAr_ACKr_ACS_reverse')
        #irm.checkAndCorrect_elementsAndPositions();
        #irm.update_reactionMapping()
        #irm.clear_reactionMapping()
        #irm.get_reactionMapping(mapping_id_O,'SERAT_CYSS')
        #irm.checkAndCorrect_elementsAndPositions();
        #irm.update_reactionMapping()
        #irm.clear_reactionMapping()
        #irm.get_reactionMapping(mapping_id_O,'THRD_GLYAT')
        #irm.checkAndCorrect_elementsAndPositions();
        #irm.update_reactionMapping()
        #irm.clear_reactionMapping()
        #irm.get_reactionMapping(mapping_id_O,'MALS')
        #irm.checkAndCorrect_elementsAndPositions();
        #irm.update_reactionMapping()
        #irm.clear_reactionMapping()

        #make default base metabolites
        imm.get_metaboliteMapping(mapping_id_O,'asp_DASH_L_c')
        imm.make_defaultBaseMetabolites()
        imm.update_metaboliteMapping()
        imm.clear_metaboliteMapping()
        imm.get_metaboliteMapping(mapping_id_O,'cys_DASH_L_c')
        imm.make_defaultBaseMetabolites()
        imm.update_metaboliteMapping()
        imm.clear_metaboliteMapping()
        imm.get_metaboliteMapping(mapping_id_O,'ru5p_DASH_D_c')
        imm.make_defaultBaseMetabolites()
        imm.update_metaboliteMapping()
        imm.clear_metaboliteMapping()
        #add in PRS to the network?
        #if not, substitute r5p_c for prpp_c
        #substitute co2_c for for_c
        #substitute phe_DASH_L_c for phpyr_c
        #ATPSYN
        irm.make_trackedCompoundReaction(mapping_id_O,model_id_O,'ATPSYN',
	        [{'r5p_c':'C'},{'10fthf_c':'C'},{'gly_c':'C'},{'co2_c':'C'},{'10fthf_c':'C'}],
            [],
            [],
            'atp_c',
            [],
            [])
        irm.add_productMapping(['atp_c'])
        irm.make_trackedCompoundReaction(mapping_id_O,model_id_O,'ATPSYN',
	        [{'gln_DASH_L_c':'C'}],
            [],
            [],
            'glu_DASH_L_c',
            [],
            [])
        irm.make_trackedCompoundReaction(mapping_id_O,model_id_O,'ATPSYN',
	        [{'asp_DASH_L_c':'C'}],
            [],
            [],
            'fum_c',
            [],
            [])
        irm.make_trackedCompoundReaction(mapping_id_O,model_id_O,'ATPSYN',
	        [{'asp_DASH_L_c':'C'}],
            [],
            [],
            'fum_c',
            [],
            [])
        irm.add_reactionMapping()
        irm.clear_reactionMapping()
        #GTPSYN
        irm.make_trackedCompoundReaction(mapping_id_O,model_id_O,'GTPSYN',
	        [{'r5p_c':'C'},{'10fthf_c':'C'},{'gly_c':'C'},{'co2_c':'C'},{'10fthf_c':'C'}],
            [],
            [],
            'gtp_c',
            [],
            [])
        irm.make_trackedCompoundReaction(mapping_id_O,model_id_O,'GTPSYN',
	        [{'gln_DASH_L_c':'C'}],
            [],
            [],
            'glu_DASH_L_c',
            [],
            [])
        irm.make_trackedCompoundReaction(mapping_id_O,model_id_O,'GTPSYN',
	        [{'gln_DASH_L_c':'C'}],
            [],
            [],
            'glu_DASH_L_c',
            [],
            [])
        irm.make_trackedCompoundReaction(mapping_id_O,model_id_O,'GTPSYN',
	        [{'asp_DASH_L_c':'C'}],
            [],
            [],
            'fum_c',
            [],
            [])
        irm.add_productMapping(['gtp_c'])
        irm.add_reactionMapping()
        irm.clear_reactionMapping()
        #VPAMTr_reverse
        irm.make_trackedCompoundReaction(mapping_id_O,model_id_O,'VPAMTr_reverse',
	        [{'val_DASH_L_c':'C'}],
            [],
            [],
            '3mob_c',
            [],
            [])
        irm.make_trackedCompoundReaction(mapping_id_O,model_id_O,'VPAMTr_reverse',
	        [{'pyr_c':'C'}],
            [],
            [],
            'ala_DASH_L_c',
            [],
            [])
        irm.add_productMapping(['3mob_c'])
        irm.add_reactionMapping()
        irm.clear_reactionMapping()
        #VPAMTr
        irm.make_trackedCompoundReaction(mapping_id_O,model_id_O,'VPAMTr',
	        [{'3mob_c':'C'}],
            [],
            [],
            'val_DASH_L_c',
            [],
            [])
        irm.make_trackedCompoundReaction(mapping_id_O,model_id_O,'VPAMTr',
	        [{'ala_DASH_L_c':'C'}],
            [],
            [],
            'pyr_c',
            [],
            [])
        irm.add_reactionMapping()
        irm.clear_reactionMapping()
        #COASYN
        irm.make_trackedCompoundReaction(mapping_id_O,model_id_O,'COASYN',
	        [{'atp_c':'C'},{'mlthf_c':'C'},{'3mob_c':'C'},{'asp_DASH_L_c':'C'},{'cys_DASH_L_c':'C'}],
            [{'asp_DASH_L_c':3},{'cys_DASH_L_c':4}],
            [{'co2_c':0},{'co2_c':0}],
            'coa_c',
            [{'co2_c':'C'},{'co2_c':'C'}],
            ['co2_c','co2_c'])
        #reverse product mapping for 3mob_c in database!
        irm.update_productMapping(['coa_c'])
        irm.add_reactionMapping()
        irm.clear_reactionMapping()
        #ACCOA_psuedo
        irm.make_trackedBinaryReaction('full04','140407_iDM2014','accoa_c_base_met_ids',
	        [{'coa_c':'C'},{'ac_c':'C'}],
            'accoa_c')
        irm.update_productMapping(['accoa_c'])
        irm.clear_reactionMapping()
        #FADSYN
        irm.make_trackedCompoundReaction(mapping_id_O,model_id_O,'FADSYN',
	        [{'gtp_c':'C'},{'ru5p_DASH_D_c':'C'},{'ru5p_DASH_D_c':'C'},{'atp_c':'C'}],
            [{'gtp_c':0},{'ru5p_DASH_D_c':1},{'ru5p_DASH_D_c':2}],
            [{'10fthf_c':0},{'co2_c':0},{'co2_c':0}],
            'fad_c',
            [{'10fthf_c':'C'},{'co2_c':'C'},{'co2_c':'C'}],
            ['co2_c','co2_c','co2_c'])
        irm.add_productMapping(['fad_c'])
        irm.add_reactionMapping()
        irm.clear_reactionMapping()
        #CBMKr
        irm.make_trackedCompoundReaction(mapping_id_O,model_id_O,'CBMKr',
	        [{'co2_c':'C'}],
            [],
            [],
            'cbp_c',
            [],
            [])
        irm.add_productMapping(['cbp_c'])
        irm.add_reactionMapping()
        irm.clear_reactionMapping()
        #CBMKr_reverse
        irm.make_trackedCompoundReaction(mapping_id_O,model_id_O,'CBMKr_reverse',
	        [{'cbp_c':'C'}],
            [],
            [],
            'co2_c',
            [],
            [])
        irm.add_reactionMapping()
        irm.clear_reactionMapping()
        #UTPSYN
        irm.make_trackedCompoundReaction(mapping_id_O,model_id_O,'UTPSYN',
	        [{'r5p_c':'C'},{'cbp_c':'C'},{'asp_DASH_L_c':'C'}],
            [{'asp_DASH_L_c':2}],
            [{'co2_c':0}],
            'utp_c',
            [{'co2_c':'C'}],
            ['co2_c'])
        irm.add_productMapping(['utp_c'])
        irm.add_reactionMapping()
        irm.clear_reactionMapping()
    #ecoli_RL2013 modifications (TODO)
    def expand_ecoliRL2013_01(self,experiment_id_I,model_id_I,mapping_id_I,date_I,model_id_O,mapping_id_O):
        '''expand the INCA Ecoli model to account for additional metabolites'''

        query = stage02_isotopomer_query()
        # get the xml model
        cobra_model_sbml = ''
        cobra_model_sbml = query.get_row_modelID_dataStage02IsotopomerModels(model_id_I);
        # load the model
        if cobra_model_sbml:
            if cobra_model_sbml['file_type'] == 'sbml':
                with open('data\\cobra_model_tmp.xml','wb') as file:
                    file.write(cobra_model_sbml['model_file']);
                    file.close()
                cobra_model = None;
                cobra_model = create_cobra_model_from_sbml_file('data\\cobra_model_tmp.xml', print_time=True);
            elif cobra_model_sbml['file_type'] == 'json':
                with open('data\\cobra_model_tmp.json','wb') as file:
                    file.write(cobra_model_sbml['model_file']);
                    file.close()
                cobra_model = None;
                cobra_model = load_json_model('data\\cobra_model_tmp.json');
            else:
                print 'file_type not supported'

        #get the atomMapping_reactions
        atomMappingReactions = query.get_rows_mappingID_dataStage02IsotopomerAtomMappingReactions(mapping_id_I);
        #change the mapping_id
        for cnt,row in enumerate(atomMappingReactions):
            atomMappingReactions[cnt]['mapping_id']=mapping_id_O;

        #add in glucose transporters and intracellular glc 
        #get metabolites not in the model
        met_row = {}
        met_row = query.get_row_modelIDAndMetID_dataStage02IsotopomerModelMetabolites('140407_iDM2014',"atp_c");
        atp = Metabolite(met_row['met_id'],met_row['formula'],met_row['met_name'],'c')
        atp.charge = met_row['charge']
        met_row = {}
        met_row = query.get_row_modelIDAndMetID_dataStage02IsotopomerModelMetabolites('140407_iDM2014',"glc_DASH_D_c");
        glc_c = Metabolite(met_row['met_id'],met_row['formula'],met_row['met_name'],'c')
        glc_c.charge = met_row['charge']
        met_row = {}
        met_row = query.get_row_modelIDAndMetID_dataStage02IsotopomerModelMetabolites('140407_iDM2014',"glc_DASH_D_e");
        glc_e = Metabolite(met_row['met_id'],met_row['formula'],met_row['met_name'],'e')
        glc_e.charge = met_row['charge']
        glcext = Metabolite('glc_DASH_D_e.ext',met_row['formula'],met_row['met_name'],'e')
        glcext.charge = met_row['charge']
        glcpre = Metabolite('glc_DASH_D_e.pre',met_row['formula'],met_row['met_name'],'e')
        glcpre.charge = met_row['charge']
        #get metabolites in the model
        pep = cobra_model.metabolites.get_by_id('pep_c')
        pyr = cobra_model.metabolites.get_by_id('pyr_c')
        g6p = cobra_model.metabolites.get_by_id('g6p_c')
        #make EX_glc_LPAREN_e_RPAREN_
        rxn_mets = {};
        rxn_mets[glcext] = -1;
        rxn_mets[glc_e] = 1;
        rxn = Reaction('EX_glc_LPAREN_e_RPAREN_');
        cobra_model.remove_reactions(['EX_glc_LPAREN_e_RPAREN_']);
        rxn.add_metabolites(rxn_mets);
        cobra_model.add_reactions([rxn]);
        cobra_model.reactions.get_by_id(rxn.id).lower_bound = 0.0;
        cobra_model.reactions.get_by_id(rxn.id).upper_bound = 1000;
        cobra_model.repair();
        #append the new atom mappings
        row_tmp = {};
        row_tmp['mapping_id']=mapping_id_O;
        row_tmp['rxn_id']='EX_glc_LPAREN_e_RPAREN_';
        row_tmp['rxn_description']='';
        row_tmp['rxn_equation']='';
        row_tmp['reactants_stoichiometry_tracked']=[-1]
        row_tmp['products_stoichiometry_tracked']=[1]
        row_tmp['reactants_ids_tracked']=['glc_DASH_D_e.ext']
        row_tmp['products_ids_tracked']=['glc_DASH_D_e']
        row_tmp['reactants_elements_tracked']=[["C", "C", "C", "C", "C", "C"]]
        row_tmp['products_elements_tracked']=[["C", "C", "C", "C", "C", "C"]]
        row_tmp['reactants_positions_tracked']=[[0, 1, 2, 3, 4, 5]]
        row_tmp['products_positions_tracked']=[[0, 1, 2, 3, 4, 5]]
        row_tmp['reactants_mapping']=['abcdef']
        row_tmp['products_mapping']=['abcdef']
        row_tmp['used_']=True
        row_tmp['comment_']='added'
        atomMappingReactions.append(row_tmp);
        ##make EX_glc_LPAREN_e_RPAREN__pre
        #rxn_mets = {};
        #rxn_mets[glcpre] = -1;
        #rxn_mets[glc_e] = 1;
        #rxn = Reaction('EX_glc_LPAREN_e_RPAREN__pre');
        #cobra_model.remove_reactions(['v60']);
        #rxn.add_metabolites(rxn_mets);
        #cobra_model.add_reactions([rxn]);
        #cobra_model.reactions.get_by_id(rxn.id).lower_bound = 0.0;
        #cobra_model.reactions.get_by_id(rxn.id).upper_bound = 1000;
        #cobra_model.repair();
        ##append the new atom mappings
        #row_tmp = {};
        #row_tmp['mapping_id']=mapping_id_O;
        #row_tmp['rxn_id']='EX_glc_LPAREN_e_RPAREN__pre';
        #row_tmp['rxn_description']='';
        #row_tmp['rxn_equation']='';
        #row_tmp['reactants_stoichiometry_tracked']=[-1]
        #row_tmp['products_stoichiometry_tracked']=[1]
        #row_tmp['reactants_ids_tracked']=['glc_DASH_D_e.pre']
        #row_tmp['products_ids_tracked']=['glc_DASH_D_e']
        #row_tmp['reactants_elements_tracked']=[["C", "C", "C", "C", "C", "C"]]
        #row_tmp['products_elements_tracked']=[["C", "C", "C", "C", "C", "C"]]
        #row_tmp['reactants_positions_tracked']=[[0, 1, 2, 3, 4, 5]]
        #row_tmp['products_positions_tracked']=[[0, 1, 2, 3, 4, 5]]
        #row_tmp['reactants_mapping']=['abcdef']
        #row_tmp['products_mapping']=['abcdef']
        #row_tmp['used_']=True
        #row_tmp['comment_']='added'
        #atomMappingReactions.append(row_tmp);
        #make GLCptspp  "glc_DASH_D_p + pep_c --> g6p_c + pyr_c"
        rxn_mets = {};
        rxn_mets[glc_e] = -1;
        rxn_mets[pep] = -1;
        rxn_mets[g6p] = 1;
        rxn_mets[pyr] = 1;
        rxn = Reaction('GLCptspp');
        rxn.add_metabolites(rxn_mets);
        cobra_model.add_reactions([rxn]);
        cobra_model.reactions.get_by_id(rxn.id).lower_bound = 0.0;
        cobra_model.reactions.get_by_id(rxn.id).upper_bound = 1000;
        cobra_model.repair();
        #append the new atom mappings
        row_tmp = {};
        row_tmp['mapping_id']=mapping_id_O;
        row_tmp['rxn_id']='GLCptspp';
        row_tmp['rxn_description']='';
        row_tmp['rxn_equation']='';
        row_tmp['reactants_stoichiometry_tracked']=[-1,-1]
        row_tmp['products_stoichiometry_tracked']=[1,1]
        row_tmp['reactants_ids_tracked']=['glc_DASH_D_e','pep_c']
        row_tmp['products_ids_tracked']=['g6p_c','pyr_c']
        row_tmp['reactants_elements_tracked']=[["C", "C", "C", "C", "C", "C"],["C", "C", "C"]]
        row_tmp['products_elements_tracked']=[["C", "C", "C", "C", "C", "C"],["C", "C", "C"]]
        row_tmp['reactants_positions_tracked']=[[0, 1, 2, 3, 4, 5],[0, 1, 2]]
        row_tmp['products_positions_tracked']=[[0, 1, 2, 3, 4, 5],[0, 1, 2]]
        row_tmp['reactants_mapping']=['abcdef','ghi']
        row_tmp['products_mapping']=['abcdef','ghi']
        row_tmp['used_']=True
        row_tmp['comment_']='added'
        atomMappingReactions.append(row_tmp);
        #make GLCt2pp "glc_DASH_D_p + h_p --> glc_DASH_D_c + h_c" 
        rxn_mets = {};
        rxn_mets[glc_e] = -1;
        rxn_mets[glc_c] = 1;
        rxn = Reaction('GLCt2pp');
        rxn.add_metabolites(rxn_mets);
        cobra_model.add_reactions([rxn]);
        cobra_model.reactions.get_by_id(rxn.id).lower_bound = 0.0;
        cobra_model.reactions.get_by_id(rxn.id).upper_bound = 1000.0;
        cobra_model.repair();
        #append the new atom mappings
        row_tmp = {};
        row_tmp['mapping_id']=mapping_id_O;
        row_tmp['rxn_id']='GLCt2pp';
        row_tmp['rxn_description']='';
        row_tmp['rxn_equation']='';
        row_tmp['reactants_stoichiometry_tracked']=[-1]
        row_tmp['products_stoichiometry_tracked']=[1]
        row_tmp['reactants_ids_tracked']=['glc_DASH_D_e']
        row_tmp['products_ids_tracked']=['glc_DASH_D_c']
        row_tmp['reactants_elements_tracked']=[["C", "C", "C", "C", "C", "C"]]
        row_tmp['products_elements_tracked']=[["C", "C", "C", "C", "C", "C"]]
        row_tmp['reactants_positions_tracked']=[[0, 1, 2, 3, 4, 5]]
        row_tmp['products_positions_tracked']=[[0, 1, 2, 3, 4, 5]]
        row_tmp['reactants_mapping']=['abcdef']
        row_tmp['products_mapping']=['abcdef']
        row_tmp['used_']=True
        row_tmp['comment_']='added'
        atomMappingReactions.append(row_tmp);
        #make HEX1 "atp_c + glc_DASH_D_c --> g6p_c + h_c + adp_c"  
        rxn_mets = {};
        rxn_mets[glc_c] = -1;
        rxn_mets[atp] = -1;
        rxn_mets[g6p] = 1;
        rxn = Reaction('HEX1');
        rxn.add_metabolites(rxn_mets);
        cobra_model.add_reactions([rxn]);
        cobra_model.reactions.get_by_id(rxn.id).lower_bound = 0.0;
        cobra_model.reactions.get_by_id(rxn.id).upper_bound = 1000.0;
        cobra_model.repair();
        #append the new atom mappings
        row_tmp = {};
        row_tmp['mapping_id']=mapping_id_O;
        row_tmp['rxn_id']='HEX1';
        row_tmp['rxn_description']='';
        row_tmp['rxn_equation']='';
        row_tmp['reactants_stoichiometry_tracked']=[-1]
        row_tmp['products_stoichiometry_tracked']=[1]
        row_tmp['reactants_ids_tracked']=['glc_DASH_D_c']
        row_tmp['products_ids_tracked']=['g6p_c']
        row_tmp['reactants_elements_tracked']=[["C", "C", "C", "C", "C", "C"]]
        row_tmp['products_elements_tracked']=[["C", "C", "C", "C", "C", "C"]]
        row_tmp['reactants_positions_tracked']=[[0, 1, 2, 3, 4, 5]]
        row_tmp['products_positions_tracked']=[[0, 1, 2, 3, 4, 5]]
        row_tmp['reactants_mapping']=['abcdef']
        row_tmp['products_mapping']=['abcdef']
        row_tmp['used_']=True
        row_tmp['comment_']='added'
        atomMappingReactions.append(row_tmp);

        # add in PRPPS	phosphoribosylpyrophosphate synthetase	atp[c] + r5p[c]  <=> amp[c] + h[c] + prpp[c] 
        #get metabolites not in the model
        met_row = {}
        met_row = query.get_row_modelIDAndMetID_dataStage02IsotopomerModelMetabolites('140407_iDM2014',"prpp_c");
        prpp = Metabolite(met_row['met_id'],met_row['formula'],met_row['met_name'],'c')
        prpp.charge = met_row['charge']
        r5p = cobra_model.metabolites.get_by_id('r5p_c')
        # expand the model
        rxn_mets = {};
        rxn_mets[r5p] = -1;
        rxn_mets[atp] = -1;
        rxn_mets[prpp] = 1;
        rxn = Reaction('PRPPS');
        rxn.add_metabolites(rxn_mets);
        cobra_model.add_reactions([rxn]);
        cobra_model.repair(); 
        # add in rxn mapping
        row={};
        row['mapping_id']=mapping_id_O;
        row['rxn_id']='PRPPS';
        row['rxn_description']='';
        row['rxn_equation']='';
        row['reactants_stoichiometry_tracked']=[-1]
        row['products_stoichiometry_tracked']=[1]
        row['reactants_ids_tracked']=['r5p_c']
        row['products_ids_tracked']=['prpp_c']
        row['reactants_elements_tracked']=[["C", "C", "C", "C", "C"]]
        row['products_elements_tracked']=[["C", "C", "C", "C", "C"]]
        row['reactants_positions_tracked']=[[0, 1, 2, 3, 4]]
        row['products_positions_tracked']=[[0, 1, 2, 3, 4]]
        row['reactants_mapping']=['abcde']
        row['products_mapping']=['abcde']
        row['used_']=True
        row['comment_']='added'
        atomMappingReactions.append(row) 

        ##expand the model
        #acon = Metabolite('acon_DASH_C_c','C6H3O6','cis-Aconitate','c');
        #cit = cobra_model.metabolites.get_by_id('cit_c')
        #icit = cobra_model.metabolites.get_by_id('icit_c')
        #e4p = cobra_model.metabolites.get_by_id('e4p_c')
        #phe = cobra_model.metabolites.get_by_id('phe_DASH_L_c')
        his = cobra_model.metabolites.get_by_id('his_DASH_L_c')
        #phpyr = Metabolite('phpyr_c','C9H7O3','Phenylpyruvate','c');
        # update selected reactions to account for new metabolites
        for rxn,row in enumerate(atomMappingReactions):
            if row['rxn_id'] == 'HisSYN':
                # split HisSYN to add in prpp
                cobra_model.reactions.get_by_id(row['rxn_id']).subtract_metabolites({atp:-1,r5p:-1})
                cobra_model.reactions.get_by_id(row['rxn_id']).add_metabolites({prpp:-1})
                # Update the mapping_ids
                atomMappingReactions[rxn]['reactants_ids_tracked']=[r.replace('r5p_c','prpp_c') for r in atomMappingReactions[rxn]['reactants_ids_tracked']]  
    
        # write the model to a temporary file
        save_json_model(cobra_model,'data\\cobra_model_tmp.json')
        
        # add the model information to the database
        io = stage02_isotopomer_io()
        dataStage02IsotopomerModelRxns_data = [];
        dataStage02IsotopomerModelMets_data = [];
        dataStage02IsotopomerModels_data,\
            dataStage02IsotopomerModelRxns_data,\
            dataStage02IsotopomerModelMets_data = io._parse_model_json(model_id_O, date_I, 'data\\cobra_model_tmp.json')
        io.add_data_stage02_isotopomer_modelMetabolites(dataStage02IsotopomerModelMets_data);
        io.add_data_stage02_isotopomer_modelReactions(dataStage02IsotopomerModelRxns_data);
        io.add_data_stage02_isotopomer_models(dataStage02IsotopomerModels_data);

        #add atomMappingReactions to the database
        io.add_data_stage02_isotopomer_atomMappingReactions(atomMappingReactions);

        # expand atomMappingReactions
        imm = stage02_isotopomer_metaboliteMapping()
        irm = stage02_isotopomer_reactionMapping()
        mappingUtilities = stage02_isotopomer_mappingUtilities()

        # make atomMappingMetabolites
        mappingUtilities.make_missingMetaboliteMappings(experiment_id_I,model_id_I=[model_id_O],
                                    mapping_id_rxns_I=[mapping_id_O],
                                    mapping_id_mets_I=[],
                                    mapping_id_new_I=mapping_id_O);

        # update symmetric metabolites
        imm.get_metaboliteMapping(mapping_id_O,'succ_c')
        imm.make_symmetric()
        imm.update_metaboliteMapping()
        imm.clear_metaboliteMapping()
        imm.get_metaboliteMapping(mapping_id_O,'fum_c')
        imm.make_symmetric()
        imm.update_metaboliteMapping()
        imm.clear_metaboliteMapping()
        imm.get_metaboliteMapping(mapping_id_O,'26dap_DASH_M_c')
        imm.make_symmetric()
        imm.update_metaboliteMapping()
        imm.clear_metaboliteMapping()
    #analysis functions
    def load_isotopomer_matlab(self,matlab_data,isotopomer_data=None):
        '''Load 13CFlux isotopomer simulation data from matlab file'''
        # load measured isotopomers from MATLAB file into numpy array
        # load names and calculated isotopomers from MATLAB file into numpy array
        names = scipy.io.loadmat(matlab_data)['output']['names'][0][0];
        calculated_ave = scipy.io.loadmat(matlab_data)['output']['ave'][0][0];
        calculated_stdev = scipy.io.loadmat(matlab_data)['output']['stdev'][0][0];
        # load residuals from MATLAB file into numpy array
        residuals = scipy.io.loadmat(matlab_data)['residuals'];
        if isotopomer_data:
            measured_dict = json.load(open(isotopomer_data,'r'));
            measured_names = [];
            measured_ave = [];
            measured_stdev = [];
            # extract data to lists
            for frag,data in measured_dict['fragments'].iteritems():
                for name in data['data_names']:
                    measured_names.append(name);
                for ave in data['data_ave']:
                    measured_ave.append(ave);
                for stdev in data['data_stdev']:
                    measured_stdev.append(stdev);
            # convert lists to dict
            measured_dict = {};
            for i,name in enumerate(measured_names):
                measured_dict[name]={'measured_ave':measured_ave[i],
                                       'measured_stdev':measured_stdev[i]};
            # match measured names to calculated names
            measured_ave = [];
            measured_stdev = [];
            residuals = [];
            for i,name in enumerate(names):
                if measured_dict.has_key(name[0][0]):
                    measured_ave.append(measured_dict[name[0][0]]['measured_ave']);
                    measured_stdev.append(measured_dict[name[0][0]]['measured_stdev']);
                    residuals.append(measured_dict[name[0][0]]['measured_ave']-calculated_ave[i][0]);
                else:
                    measured_ave.append(None);
                    measured_stdev.append(None);
                    residuals.append(None);
        else:
            measured_ave_tmp = scipy.io.loadmat(matlab_data)['toCompare'];
            measured_ave = [];
            for d in measured_ave_tmp:
                measured_ave.append(d[0]);
            measured_stdev = numpy.zeros(len(measured_ave));
        # combine into a dictionary
        isotopomer = {};
        for i in range(len(names)):
            isotopomer[names[i][0][0]] = {'measured_ave':measured_ave[i], #TODO: extract out by fragment names
                                    'measured_stdev':measured_stdev[i],
                                    'calculated_ave':calculated_ave[i][0],
                                    'calculated_stdev':calculated_stdev[i][0],
                                    'residuals':residuals[i]};

        return isotopomer;
    def load_confidenceIntervals_matlab(self,matlab_data,cobra_model_matlab,cobra_model_name):
        '''Load confidence intervals from matlab file'''
        # load confidence intervals from MATLAB file into numpy array
        cimin_h5py = h5py.File(matlab_data)['ci']['minv'][0];
        cimax_h5py = h5py.File(matlab_data)['ci']['maxv'][0];
        cimin = numpy.array(cimin_h5py);
        cimax = numpy.array(cimax_h5py);
        # load cobramodel
        rxns = scipy.io.loadmat(cobra_model_matlab)[cobra_model_name]['rxns'][0][0]
        # combine cimin, cimax, and rxns into dictionary
        ci = {};
        for i in range(len(cimin)):
            ci[rxns[i][0][0]] = {'minv':cimin[i],'maxv':cimax[i]};

        return ci;
    def compare_isotopomers_calculated(self,isotopomer_1, isotopomer_2):
        '''compare two calculated isotopomer distributions'''
        # extract into lists
        absDif_list = [];
        ssr_1_list = [];
        ssr_2_list = [];
        bestFit_list = [];
        frag_list = [];
        ssr_1 = 0.0; # sum of squared residuals (threshold of 10e1, Antoniewicz poster, co-culture, Met Eng X)
        ssr_2 = 0.0;
        measured_1_list = [];
        measured_2_list = [];
        calculatedAve_1_list = [];
        calculatedAve_2_list = [];
        measuredStdev_1_list = [];
        measuredStdev_2_list = [];
        for frag,data in isotopomer_1.iteritems():
            absDif = 0.0;
            sr_1 = 0.0;
            sr_2 = 0.0;
            bestFit = None;
            absDif = fabs(isotopomer_1[frag]['calculated_ave'] - isotopomer_2[frag]['calculated_ave']);
            sr_1 = pow(isotopomer_1[frag]['calculated_ave']-isotopomer_1[frag]['measured_ave'],2);
            sr_2 = pow(isotopomer_2[frag]['calculated_ave']-isotopomer_2[frag]['measured_ave'],2);
            if sr_1>sr_2: bestFit = '2';
            elif sr_1<sr_2: bestFit = '1';
            elif sr_1==sr_2: bestFit = None;
            absDif_list.append(absDif);
            ssr_1_list.append(sr_1);
            ssr_2_list.append(sr_2);
            bestFit_list.append(bestFit);
            frag_list.append(frag);
            ssr_1 += sr_1;
            ssr_2 += sr_2;
            measured_1_list.append(isotopomer_1[frag]['measured_ave'])
            measured_2_list.append(isotopomer_2[frag]['measured_ave'])
            calculatedAve_1_list.append(isotopomer_1[frag]['calculated_ave']);
            calculatedAve_2_list.append(isotopomer_2[frag]['calculated_ave']);
            measuredStdev_1_list.append(isotopomer_1[frag]['measured_stdev']);
            measuredStdev_2_list.append(isotopomer_2[frag]['measured_stdev']);

        # calculate the correlation coefficient
        # 1. between measured vs. calculated (1 and 2)
        # 2. between calculated 1 vs. calculated 2
        r_measuredVsCalculated_1 = None;
        r_measuredVsCalculated_2 = None;
        r_measured1VsMeasured2 = None;
        p_measuredVsCalculated_1 = None;
        p_measuredVsCalculated_2 = None;
        p_measured1VsMeasured2 = None;

        r_measuredVsCalculated_1, p_measuredVsCalculated_1 = scipy.stats.pearsonr(measured_1_list,calculatedAve_1_list);
        r_measuredVsCalculated_2, p_measuredVsCalculated_2 = scipy.stats.pearsonr(measured_2_list,calculatedAve_2_list);
        r_measured1VsMeasured2, p_measured1VsMeasured2 = scipy.stats.pearsonr(calculatedAve_1_list,calculatedAve_2_list);

        # wrap stats into a dictionary
        isotopomer_comparison_stats = {};
        isotopomer_comparison_stats = dict(zip(('r_measuredVsCalculated_1', 'p_measuredVsCalculated_1',
            'r_measuredVsCalculated_2', 'p_measuredVsCalculated_2',
            'r_measured1VsMeasured2', 'p_measured1VsMeasured2',
            'ssr_1,ssr_2'),
                                               (r_measuredVsCalculated_1, p_measuredVsCalculated_1,
            r_measuredVsCalculated_2, p_measuredVsCalculated_2,
            r_measured1VsMeasured2, p_measured1VsMeasured2,
            ssr_1,ssr_2)));

        ## zip, sort, unzip # does not appear to sort correctly!
        #zipped = zip(absDif_list,ssr_1_list,ssr_2_list,bestFit_list,frag_list,
        #             measured_1_list,measured_2_list,calculatedAve_1_list,calculatedAve_2_list,
        #             measuredStdev_1_list,measuredStdev_2_list);
        #zipped.sort();
        #zipped.reverse();
        #absDif_list,ssr_1_list,sst_2_list,bestFit_list,frag_list,\
        #             measured_1_list,measured_2_list,calculatedAve_1_list,calculatedAve_2_list,\
        #             measuredStdev_1_list,measuredStdev_2_list = zip(*zipped);
        # restructure into a list of dictionaries for easy parsing or data base viewing
        isotopomer_comparison = [];
        for i in range(len(absDif_list)):
            isotopomer_comparison.append({'isotopomer_absDif':absDif_list[i],
                                           'isotopomer_1_sr':ssr_1_list[i],
                                           'isotopomer_2_sr':ssr_2_list[i],
                                           'bestFit':bestFit_list[i],
                                           'frag':frag_list[i],
                                           'measured_1_ave':measured_1_list[i],
                                           'measured_2_ave':measured_2_list[i],
                                           'measured_1_stdev':measuredStdev_1_list[i],
                                           'measured_2_stdev':measuredStdev_2_list[i],
                                           'calculated_1_ave':calculatedAve_1_list[i],
                                           'calculated_2_ave':calculatedAve_2_list[i]});

        return isotopomer_comparison,isotopomer_comparison_stats;
    def compare_ci_calculated(self,ci_1,ci_2):
        '''compare 2 calculated confidence intervals'''
        # extract into lists
        rxns_1_list = [];
        rxns_2_list = [];
        ciminv_1_list = [];
        ciminv_2_list = [];
        cimaxv_1_list = [];
        cimaxv_2_list = [];
        cirange_1_list = [];
        cirange_2_list = [];
        cirange_1_sum = 0.0;
        cirange_2_sum = 0.0;
        # ci_1:
        for k,v in ci_1.iteritems():
            rxns_1_list.append(k);
            ciminv_1_list.append(v['minv']);
            cimaxv_1_list.append(v['maxv']);
            cirange_1_list.append(v['maxv']-v['minv']);
            cirange_1_sum += v['maxv']-v['minv'];
        ## zip, sort, unzip
        #zipped1 = zip(rxns_1_list,ciminv_1_list,cimaxv_1_list,cirange_1_list);
        #zipped1.sort();
        #rxns_1_list,ciminv_1_list,cimaxv_1_list,cirange_1_list = zip(*zipped1);
        # ci_2:
        for k,v in ci_2.iteritems():
            rxns_2_list.append(k);
            ciminv_2_list.append(v['minv']);
            cimaxv_2_list.append(v['maxv']);
            cirange_2_list.append(v['maxv']-v['minv']);
            cirange_2_sum += v['maxv']-v['minv'];
        ## zip, sort, unzip
        #zipped2 = zip(rxns_2_list,ciminv_2_list,cimaxv_2_list,cirange_2_list);
        #zipped2.sort();
        #rxns_2_list,ciminv_2_list,cimaxv_2_list,cirange_2_list = zip(*zipped2);
        # compare by rxn_id
        cirange_absDev_list = [];
        rxns_combined_list = [];
        ciminv_1_combined_list = [];
        ciminv_2_combined_list = [];
        cimaxv_1_combined_list = [];
        cimaxv_2_combined_list = [];
        cirange_1_combined_list = [];
        cirange_2_combined_list = [];
        cirange_1_combined_sum = 0.0;
        cirange_2_combined_sum = 0.0;
        for i in range(len(rxns_1_list)):
            for j in range(len(rxns_2_list)):
                if rxns_1_list[i] == rxns_2_list[j]:
                    rxns_combined_list.append(rxns_1_list[i]);
                    cirange_absDev_list.append(fabs(cirange_1_list[i]-cirange_2_list[j]));
                    ciminv_1_combined_list.append(ciminv_1_list[i]);
                    ciminv_2_combined_list.append(ciminv_2_list[j]);
                    cimaxv_1_combined_list.append(cimaxv_1_list[i]);
                    cimaxv_2_combined_list.append(cimaxv_2_list[j]);
                    cirange_1_combined_list.append(cirange_1_list[i]);
                    cirange_2_combined_list.append(cirange_2_list[j]);
                    cirange_1_combined_sum += cirange_1_list[i]
                    cirange_2_combined_sum += cirange_2_list[j]
        ## zip, sort, unzip
        #zippedCombined = zip(cirange_absDev_list,rxns_combined_list,ciminv_1_combined_list,ciminv_2_combined_list,cimaxv_1_combined_list,cimaxv_2_combined_list,cirange_1_combined_list,cirange_2_combined_list);
        #zippedCombined.sort();
        #zippedCombined.reverse();
        #cirange_absDev_list,rxns_combined_list,ciminv_1_combined_list,ciminv_2_combined_list,cimaxv_1_combined_list,cimaxv_2_combined_list,cirange_1_combined_list,cirange_2_combined_list = zip(*zippedCombined);
        # restructure into a list of dictionaries for easy parsing or data base viewing
        ci_comparison = [];
        for i in range(len(cirange_absDev_list)):
            ci_comparison.append({'cirange_absDev_list':cirange_absDev_list[i],
                                  'rxns_combined_list':rxns_combined_list[i],
                                  'ciminv_1_combined_list':ciminv_1_combined_list[i],
                                  'ciminv_2_combined_list':ciminv_2_combined_list[i],
                                  'cimaxv_1_combined_list':cimaxv_1_combined_list[i],
                                  'cimaxv_2_combined_list':cimaxv_2_combined_list[i],
                                  'cirange_1_combined_list':cirange_1_combined_list[i],
                                  'cirange_2_combined_list':cirange_2_combined_list[i]});

        return ci_comparison,cirange_1_sum,cirange_2_sum,cirange_1_combined_sum,cirange_2_combined_sum;
    def plot_compare_isotopomers_calculated(self,isotopomer_comparison,isotopomer_comparison_stats):
        '''Plot 1: isotopomer fitting comparison
        Plot 2: isotopomer residual comparison'''
        io = base_exportData(isotopomer_comparison);
        # Plot 1 and Plot 2:
        io.write_dict2tsv('data//data.tsv');
    def plot_ci_calculated(self,ci):
        '''plot confidence intervals from fluxomics experiment using escher'''
        data = [];
        flux1 = {};
        flux2 = {};
        for k,v in ci.iteritems():
            flux1[k] = v['minv'];
            flux2[k] = v['maxv'];
        data.append(flux1);
        data.append(flux2);
        io = base_exportData(data);
        io.write_dict2json('visualization\\escher\\ci.json');
    def export_modelWithFlux(self,cobra_model_xml_I,ci_list_I,cobra_model_xml_O):
        '''update model lower_bound/upper_bound with calculated flux confidence intervals'''

        cobra_model = create_cobra_model_from_sbml_file(cobra_model_xml_I);

        rxns_add = [];
        rxns_omitted = [];
        rxns_break = [];

        system_boundaries = [x.id for x in cobra_model.reactions if x.boundary == 'system_boundary'];
        objectives = [x.id for x in cobra_model.reactions if x.objective_coefficient == 1];

        for i,ci_I in enumerate(ci_list_I):
            print 'add flux from ci ' + str(i);
            for rxn in cobra_model.reactions:
                if rxn.id in ci_I.keys() and not(rxn.id in system_boundaries)\
                    and not(rxn.id in objectives):
                    cobra_model_copy = cobra_model.copy();
                    # check for reactions that break the model:
                    if ci_I[rxn.id]['minv'] > 0:
                        cobra_model_copy.reactions.get_by_id(rxn.id).lower_bound = ci_I[rxn.id]['minv'];
                    if ci_I[rxn.id]['maxv'] > 0 and ci_I[rxn.id]['maxv'] > ci_I[rxn.id]['minv']:
                        cobra_model_copy.reactions.get_by_id(rxn.id).upper_bound = ci_I[rxn.id]['maxv'];
                    cobra_model_copy.optimize(solver='gurobi');
                    if not cobra_model_copy.solution.f:
                        print rxn.id + ' broke the model!'
                        rxns_break.append(rxn.id);
                    else: 
                        if ci_I[rxn.id]['minv'] > 0:
                            cobra_model.reactions.get_by_id(rxn.id).lower_bound = ci_I[rxn.id]['minv'];
                        if ci_I[rxn.id]['maxv'] > 0 and ci_I[rxn.id]['maxv'] > ci_I[rxn.id]['minv']:
                            cobra_model.reactions.get_by_id(rxn.id).upper_bound = ci_I[rxn.id]['maxv'];
                        rxns_add.append(rxn.id);
                else:
                    rxns_omitted.append(rxn.id);

        write_cobra_model_to_sbml_file(cobra_model,cobra_model_xml_O)

class stage02_isotopomer_metaboliteMapping():
    """Class to standardize metabolite mapping:

    A mapped metabolite takes the following form:
    'met_id' + 'nMet_id' + '_' + 'element' + nElement
    
    Input:
    met_ids_elements_I = [{met_id:element},...]
                         [{'f6p_c':'C'},{'f6p_c':'C'},{'f6p_c':'H'},{'f6p_c':'H'},{'ac_c':'C'},{'utp_c':'C'}]
                         NOTE: The order matters if using multiple elements! will need to further test in future versions
                         
    Base metabolites: default base metabolite is co2 for carbon and oh for hydrogen
    Base reaction: co2 + oh- + h+ = ch2o + o2"""

    def __init__(self,
            mapping_id_I=None,
            #met_name_I=None,
            met_id_I=None,
            #formula_I=None,
            met_elements_I=[],
            met_atompositions_I=[],
            met_symmetry_elements_I=[],
            met_symmetry_atompositions_I=[],
            used__I=True,
            comment__I=None,
            met_mapping_I=[],
            base_met_ids_I=[],
            base_met_elements_I=[],
            base_met_atompositions_I=[],
            base_met_symmetry_elements_I=[],
            base_met_symmetry_atompositions_I=[],
            base_met_indices_I=[]):
        #self.session = Session();
        self.stage02_isotopomer_query = stage02_isotopomer_query();
        self.calculate = base_calculate();
        self.metaboliteMapping={};
        self.metaboliteMapping['mapping_id']=mapping_id_I;
        #self.metaboliteMapping['met_name']=met_name_I;
        self.metaboliteMapping['met_id']=met_id_I;
        #self.metaboliteMapping['formula']=formula_I;
        self.metaboliteMapping['met_elements']=met_elements_I;
        self.metaboliteMapping['met_atompositions']=met_atompositions_I;
        self.metaboliteMapping['met_symmetry_elements']=met_symmetry_elements_I;
        self.metaboliteMapping['met_symmetry_atompositions']=met_symmetry_atompositions_I;
        self.metaboliteMapping['used_']=used__I;
        self.metaboliteMapping['comment_']=comment__I;
        self.metaboliteMapping['met_mapping']=met_mapping_I;
        self.metaboliteMapping['base_met_ids']=base_met_ids_I;
        self.metaboliteMapping['base_met_elements']=base_met_elements_I;
        self.metaboliteMapping['base_met_atompositions']=base_met_atompositions_I;
        self.metaboliteMapping['base_met_symmetry_elements']=base_met_symmetry_elements_I;
        self.metaboliteMapping['base_met_symmetry_atompositions']=base_met_symmetry_atompositions_I;
        self.metaboliteMapping['base_met_indices']=base_met_indices_I;
    def make_elementsAndPositionsTracked(self,met_id_I,element_I,n_elements_I):
        #Input: met_id_I,element_I,n_elements_I
        #Output: mapping_O,positions_O,elements_O
        #E.g: make_elementsTracked('fdp','C',6)
        mapping_O = [];
        positions_O = [];
        elements_O = [];
        for elements_cnt in range(n_elements_I):
            mapping = '[' + met_id_I + '_'  + element_I + str(elements_cnt) + ']';
            mapping_O.append(mapping);
            positions_O.append(elements_cnt);
            elements_O.append(element_I);
        return mapping_O,positions_O,elements_O;
    def make_trackedMetabolite(self,mapping_id_I,model_id_I,met_id_element_I,met_index_I=None):
        '''Make an unique atom mapping for the given metabolite and element'''
        currentElementPos = 0;
        mapping_O = [];
        positions_O = [];
        elements_O = [];
        base_met_ids_O = [];
        base_met_elements_O = [];
        base_met_atompositions_O = [];
        base_met_symmetry_elements_O = [];
        base_met_symmetry_atompositions_O = [];
        base_met_indices_O = [];
        for k,v in met_id_element_I.iteritems():
            # check if the metabolite is already in the database
            met_data = {}
            met_data = self.stage02_isotopomer_query.get_rows_mappingIDAndMetID_dataStage02IsotopomerAtomMappingMetabolites(mapping_id_I,k)
            #NOTE: need to add in a constraint to make sure that the elements in the database and the elments in the input match!
            if met_data and met_data.has_key('met_elements') and v==met_data['met_elements'][0]:
                nElements = len(met_data['met_elements']);
            else:
                # get the formula for the met_id
                formula_I = self.stage02_isotopomer_query.get_formula_modelIDAndMetID_dataStage02IsotopomerModelMetabolites(model_id_I,k);
                # get the number of elements
                if not Formula(formula_I)._elements.has_key(v): break; #check if the element is even contained in the formula
                if Formula(formula_I)._elements[v].has_key(0):
                    nElements = Formula(formula_I)._elements[v][0]; #get the # of the elements
            # make the tracking
            nMet = 0;
            if met_index_I: nMet = met_index_I
            mapping,positions,elements = self.make_elementsAndPositionsTracked(k+str(nMet),v,nElements);
            positions_corrected = [currentElementPos+pos for pos in positions];
            currentElementPos += max(positions)+1;
            mapping_O.append(mapping);
            positions_O.extend(positions_corrected);
            elements_O.extend(elements);
            base_met_ids_O.append(k)
            base_met_elements_O.append(elements)
            base_met_atompositions_O.append(positions)
            base_met_indices_O.append(nMet)
        self.metaboliteMapping['mapping_id']=mapping_id_I
        self.metaboliteMapping['met_id']=k
        self.metaboliteMapping['met_elements']=elements_O
        self.metaboliteMapping['met_atompositions']=positions_O
        self.metaboliteMapping['met_mapping']=mapping_O
        self.metaboliteMapping['base_met_ids']=base_met_ids_O
        self.metaboliteMapping['base_met_elements']=base_met_elements_O
        self.metaboliteMapping['base_met_atompositions']=base_met_atompositions_O
        self.metaboliteMapping['base_met_indices']=base_met_indices_O
    def make_compoundTrackedMetabolite(self,mapping_id_I,model_id_I,met_ids_elements_I,met_id_O,met_ids_indices_I = []):
        '''Make an unique atom mapping for the given metabolite based on base metabolites and elements'''
        #Input:
        #   metIDs_elements_I = [{met_id:element},..]
        # met_ids_elements_I = [{'f6p_c':'C'},{'ac_c':'C'},{'utp_c':'C'}}]
        #   metIDs_elements_I = [met_id:{elements=[string,...],stoichiometry:float}},..]
        # met_ids_elements_I = [{'f6p_c':{'elements':['C'],'stoichiometry':1}},{'ac_c':{'elements':['C'],'stoichiometry':1}},{'utp_c':{'elements':['C'],'stoichiometry':1}}]
        # make_compoundTrackedMetabolite('full04','140407_iDM2014',met_ids_elements_I,'uacgam_c')
        currentElementPos = 0;
        mapping_O = [];
        positions_O = [];
        elements_O = [];
        base_met_ids_O = [];
        base_met_elements_O = [];
        base_met_atompositions_O = [];
        base_met_symmetry_elements_O = [];
        base_met_symmetry_atompositions_O = [];
        base_met_indices_O = [];
        # get unique met_ids
        met_ids_all = [];
        for row in met_ids_elements_I:
            for k,v in row.iteritems():
                met_ids_all.append(k);
        met_ids_unique = list(set(met_ids_all))
        met_ids_cnt = {};
        met_ids_elements = {};
        for met_id in met_ids_unique:
            met_ids_cnt[met_id] = 0;
            met_ids_elements[met_id] = [];
        # make the compound mapping
        for row_cnt,row in enumerate(met_ids_elements_I):
            for k,v in row.iteritems():
                # check if the metabolite is already in the database
                met_data = {}
                met_data = self.stage02_isotopomer_query.get_rows_mappingIDAndMetID_dataStage02IsotopomerAtomMappingMetabolites(mapping_id_I,k)
                #NOTE: need to add in a constraint to make sure that the elements in the database and the elments in the input match!
                if met_data and met_data.has_key('met_elements') and v==met_data['met_elements'][0]:
                    nElements = len(met_data['met_elements']);
                else:
                    # get the formula for the met_id
                    formula_I = self.stage02_isotopomer_query.get_formula_modelIDAndMetID_dataStage02IsotopomerModelMetabolites(model_id_I,k);
                    # get the number of elements
                    if not Formula(formula_I)._elements.has_key(v): break; #check if the element is even contained in the formula
                    if Formula(formula_I)._elements[v].has_key(0):
                        nElements = Formula(formula_I)._elements[v][0]; #get the # of the elements
                # determine the metabolite index
                nMets = met_ids_cnt[k];
                if met_ids_indices_I: nMets = met_ids_indices_I[row_cnt]
                # make the tracking
                mapping,positions,elements = self.make_elementsAndPositionsTracked(k+str(nMets),v,nElements);
                positions_corrected = [currentElementPos+pos for pos in positions];
                currentElementPos += max(positions)+1;
                # add to the compound tracking
                mapping_O.append(mapping);
                positions_O.extend(positions_corrected);
                elements_O.extend(elements);
                base_met_ids_O.append(k)
                base_met_elements_O.append(elements)
                base_met_atompositions_O.append(positions)
                base_met_indices_O.append(nMets)
            met_ids_cnt[k] += 1; # needed to ensure a unique metabolite mapping if the same met_id is used multiple times
        self.metaboliteMapping['mapping_id']=mapping_id_I
        self.metaboliteMapping['met_id']=met_id_O
        self.metaboliteMapping['met_elements']=elements_O
        self.metaboliteMapping['met_atompositions']=positions_O
        self.metaboliteMapping['met_mapping']=mapping_O
        self.metaboliteMapping['base_met_ids']=base_met_ids_O
        self.metaboliteMapping['base_met_elements']=base_met_elements_O
        self.metaboliteMapping['base_met_atompositions']=base_met_atompositions_O
        self.metaboliteMapping['base_met_indices']=base_met_indices_O
    def append_baseMetabolites_toMetabolite(self,model_id_I,met_ids_elements_I,met_id_O=None):
        '''Append a base metabolite to the current metabolite'''
        #get the currentElementPos
        currentElementPos = max(self.metaboliteMapping['met_atompositions'])+1;
        # get unique met_ids
        met_ids_unique = list(set(self.metaboliteMapping['base_met_ids']))
        met_ids_cnt = {};
        met_ids_elements = {};
        for met_id in met_ids_unique:
            met_ids_cnt[met_id] = 0;
            met_ids_elements[met_id] = [];
        for met_id_cnt,met_id in enumerate(self.metaboliteMapping['base_met_ids']):
            # determine the number of met_ids
            met_ids_cnt[met_id]+=1
            # determine the unique elements
            if not self.metaboliteMapping['met_elements'][0] in met_ids_elements[met_id]:
                met_ids_elements[met_id].append(self.metaboliteMapping['met_elements'][met_id_cnt][0]);
        # add the mapping for the new metabolites
        for row in met_ids_elements_I:
            for k,v in row.iteritems():
                # check if the metabolite is already in the database
                met_data = {}
                met_data = self.stage02_isotopomer_query.get_rows_mappingIDAndMetID_dataStage02IsotopomerAtomMappingMetabolites(self.metaboliteMapping['mapping_id'],k)
                #NOTE: need to add in a constraint to make sure that the elements in the database and the elments in the input match!
                if met_data and met_data.has_key('met_elements') and v==met_data['met_elements'][0]:
                    nElements = len(met_data['met_elements']);
                else:
                    # get the formula for the met_id
                    formula_I = self.stage02_isotopomer_query.get_formula_modelIDAndMetID_dataStage02IsotopomerModelMetabolites(model_id_I,k);
                    # get the number of elements
                    if not Formula(formula_I)._elements.has_key(v): break; #check if the element is even contained in the formula
                    if Formula(formula_I)._elements[v].has_key(0):
                        nElements = Formula(formula_I)._elements[v][0]; #get the # of the elements
                # adjust the metabolite number if the same metabolite already exists
                nMets = met_ids_cnt[k];
                met_id_mapping = k+nMets;
                # make the tracking
                mapping,positions,elements = self.make_elementsAndPositionsTracked(met_id_mapping,v,nElements);
                positions_corrected = [currentElementPos+pos for pos in positions];
                currentElementPos += max(positions)+1;
                # add to the compound tracking
                self.metaboliteMapping['met_mapping'].append(mapping);
                self.metaboliteMapping['met_atompositions'].extend(positions_corrected);
                self.metaboliteMapping['met_elements'].extend(elements);
                self.metaboliteMapping['base_met_ids'].append(k)
                self.metaboliteMapping['base_met_elements'].append(elements)
                self.metaboliteMapping['base_met_atompositions'].append(positions)
                self.metaboliteMapping['base_met_indices'].append(met_ids_cnt[k]);
                met_ids_cnt[met_id]+=1;
        if met_id_O: self.metaboliteMapping['met_id']=met_id_O
    def pop_baseMetabolite_fromMetabolite(self,model_id_I,met_id_element_I,met_id_O=None):
        '''Remove a base metabolite from the current metabolite:
        metabolites are removed FILO;
        NOTE: this can lead to problems downstream when the mapping
        is reconstructed from the base metabolites if multiple elements are used'''
        #Input:
        #   met_id_element_I = {met_id:element}
        '''Unit Test:
        '''
        met_mapping = self.metaboliteMapping['met_mapping'];
        base_met_ids = self.metaboliteMapping['base_met_ids'];
        base_met_elements = self.metaboliteMapping['base_met_elements'];
        base_met_atompositions = self.metaboliteMapping['base_met_atompositions'];
        base_met_indices = self.metaboliteMapping['base_met_indices'];
        #base_met_symmetry_elements=self.metaboliteMapping['base_met_symmetry_elements'];
        #base_met_symmetry_atompositions=self.metaboliteMapping['base_met_symmetry_atompositions'];
        met_mapping.reverse();
        base_met_ids.reverse();
        base_met_elements.reverse();
        base_met_atompositions.reverse();
        base_met_indices.reverse();
        #base_met_symmetry_elements.reverse();
        #base_met_symmetry_atompositions.reverse();
        self.metaboliteMapping['met_mapping']=[]
        self.metaboliteMapping['base_met_ids']=[]
        self.metaboliteMapping['base_met_elements']=[]
        self.metaboliteMapping['base_met_atompositions']=[]
        self.metaboliteMapping['base_met_indices']=[]
        #self.metaboliteMapping['base_met_symmetry_elements']=[]
        #self.metaboliteMapping['base_met_symmetry_atompositions']=[]
        for met_id_remove,v in met_id_element_I.iteritems():
            removed = False
            for met_cnt,met_id in enumerate(base_met_ids):
                if met_id_remove == met_id and v==base_met_elements[met_cnt][0] and not removed:
                    removed = True;
                else: 
                    self.metaboliteMapping['met_mapping'].insert(0,met_mapping[met_cnt]);
                    self.metaboliteMapping['base_met_ids'].insert(0,base_met_ids[met_cnt]);
                    self.metaboliteMapping['base_met_elements'].insert(0,base_met_elements[met_cnt]);
                    self.metaboliteMapping['base_met_atompositions'].insert(0,base_met_atompositions[met_cnt]);
                    self.metaboliteMapping['base_met_indices'].insert(0,base_met_indices[met_cnt])
                    #self.metaboliteMapping['base_met_symmetry_elements'].insert(0,base_met_symmetry_elements[met_cnt]);
                    #self.metaboliteMapping['base_met_symmetry_atompositions'].insert(0,base_met_symmetry_atompositions[met_cnt]);
        '''v1: removes ALL base metabolites that match the met_id'''
        #for met_id_remove in met_ids_I:
        #    for met_cnt,met_id in enumerate(base_met_ids):
        #        if met_id_remove != met_id:
        #            self.metaboliteMapping['met_mapping'].append(met_mapping[met_cnt]);
        #            self.metaboliteMapping['base_met_ids'].append(base_met_ids[met_cnt]);
        #            self.metaboliteMapping['base_met_elements'].append(base_met_elements[met_cnt]);
        #            self.metaboliteMapping['base_met_atompositions'].append(base_met_atompositions[met_cnt]);
        #            #self.metaboliteMapping['base_met_symmetry_elements'].append(base_met_symmetry_elements[met_cnt]);
        #            #self.metaboliteMapping['base_met_symmetry_atompositions'].append(base_met_symmetry_atompositions[met_cnt]);
        if met_id_O: self.metaboliteMapping['met_id']=met_id_O
        self.update_trackedMetabolite_fromBaseMetabolites(model_id_I);
    def remove_baseMetabolite_fromMetabolite(self,model_id_I,met_id_element_I,met_id_O=None,met_index_I=None):
        '''Remove a base metabolite from the current metabolite:
        metabolites are removed FIFO if the index is not specified;'''
        #Input:
        #   met_id_element = {met_id:element}
        '''Unit Test:'''

        met_mapping = self.metaboliteMapping['met_mapping'];
        base_met_ids = self.metaboliteMapping['base_met_ids'];
        base_met_elements = self.metaboliteMapping['base_met_elements'];
        base_met_atompositions = self.metaboliteMapping['base_met_atompositions'];
        base_met_indices = self.metaboliteMapping['base_met_indices'];
        #base_met_symmetry_elements=self.metaboliteMapping['base_met_symmetry_elements'];
        #base_met_symmetry_atompositions=self.metaboliteMapping['base_met_symmetry_atompositions'];
        self.metaboliteMapping['met_mapping']=[]
        self.metaboliteMapping['base_met_ids']=[]
        self.metaboliteMapping['base_met_elements']=[]
        self.metaboliteMapping['base_met_atompositions']=[]
        self.metaboliteMapping['base_met_indices']=[]
        #self.metaboliteMapping['base_met_symmetry_elements']=[]
        #self.metaboliteMapping['base_met_symmetry_atompositions']=[]
        for met_id_remove,v in met_id_element_I.iteritems():
            removed = False
            for met_cnt,met_id in enumerate(base_met_ids):
                if met_index_I:
                    if met_index_I == base_met_indices[met_cnt] and met_id_remove == met_id and v==base_met_elements[met_cnt][0] and not removed:
                        removed = True
                    else: 
                        self.metaboliteMapping['met_mapping'].append(met_mapping[met_cnt]);
                        self.metaboliteMapping['base_met_ids'].append(base_met_ids[met_cnt]);
                        self.metaboliteMapping['base_met_elements'].append(base_met_elements[met_cnt]);
                        self.metaboliteMapping['base_met_atompositions'].append(base_met_atompositions[met_cnt]);
                        self.metaboliteMapping['base_met_indices'].append(base_met_indices[met_cnt]);
                        #self.metaboliteMapping['base_met_symmetry_elements'].append(base_met_symmetry_elements[met_cnt]);
                        #self.metaboliteMapping['base_met_symmetry_atompositions'].append(base_met_symmetry_atompositions[met_cnt]);
                else:
                    if met_id_remove == met_id and v==base_met_elements[met_cnt][0] and not removed:
                        removed = True
                    else: 
                        self.metaboliteMapping['met_mapping'].append(met_mapping[met_cnt]);
                        self.metaboliteMapping['base_met_ids'].append(base_met_ids[met_cnt]);
                        self.metaboliteMapping['base_met_elements'].append(base_met_elements[met_cnt]);
                        self.metaboliteMapping['base_met_atompositions'].append(base_met_atompositions[met_cnt]);
                        self.metaboliteMapping['base_met_indices'].append(base_met_indices[met_cnt]);
                        #self.metaboliteMapping['base_met_symmetry_elements'].append(base_met_symmetry_elements[met_cnt]);
                        #self.metaboliteMapping['base_met_symmetry_atompositions'].append(base_met_symmetry_atompositions[met_cnt]);
        '''v1: removes ALL base metabolites that match the met_id'''
        #for met_id_remove in met_ids_I:
        #    for met_cnt,met_id in enumerate(base_met_ids):
        #        if met_id_remove != met_id:
        #            self.metaboliteMapping['met_mapping'].append(met_mapping[met_cnt]);
        #            self.metaboliteMapping['base_met_ids'].append(base_met_ids[met_cnt]);
        #            self.metaboliteMapping['base_met_elements'].append(base_met_elements[met_cnt]);
        #            self.metaboliteMapping['base_met_atompositions'].append(base_met_atompositions[met_cnt]);
        #            #self.metaboliteMapping['base_met_symmetry_elements'].append(base_met_symmetry_elements[met_cnt]);
        #            #self.metaboliteMapping['base_met_symmetry_atompositions'].append(base_met_symmetry_atompositions[met_cnt]);
        if met_id_O: self.metaboliteMapping['met_id']=met_id_O
        self.update_trackedMetabolite_fromBaseMetabolites(model_id_I);
    def extract_baseMetabolite_fromMetabolite(self,model_id_I,met_id_element_I,met_index_I=None):
        '''Returns a base metabolites from the current metabolite:
        returns metabolites in FIFO'''
        base_metaboliteMapping = stage02_isotopomer_metaboliteMapping();
        base_met_ids = self.metaboliteMapping['base_met_ids'];
        met_id_remove = {};
        met_index = None
        for k,v in met_id_element_I.iteritems():
            for met_cnt,met_id in enumerate(base_met_ids):
                if met_index_I:
                    if met_index_I == self.metaboliteMapping['base_met_indices'][met_cnt] and k == met_id and v==self.metaboliteMapping['base_met_elements'][met_cnt][0]:
                        met_id_remove = {k:self.metaboliteMapping['base_met_elements'][met_cnt][0]};
                        met_index = met_index_I;
                        break;
                else:
                    if k == met_id and v==self.metaboliteMapping['base_met_elements'][met_cnt][0]:
                        met_id_remove = {k:self.metaboliteMapping['base_met_elements'][met_cnt][0]};
                        met_index = self.metaboliteMapping['base_met_indices'][met_cnt]
                        break;
        base_metaboliteMapping.make_trackedMetabolite(self.metaboliteMapping['mapping_id'],model_id_I,met_id_remove,met_index);
        return base_metaboliteMapping
    def update_trackedMetabolite_fromBaseMetabolites(self,model_id_I):
        '''update mapping, elements, and atompositions from base metabolites;
        NOTE: issues may arise in the number assigned to each metabolite if multiple elements are used'''
        # get unique met_ids
        met_ids_unique = list(set(self.metaboliteMapping['base_met_ids']))
        met_ids_cnt = {};
        met_ids_elements = {};
        for met_id in met_ids_unique:
            met_ids_cnt[met_id] = 0;
            met_ids_elements[met_id] = [];
        # make the input structure
        met_ids_elements_I = [];
        for met_id_cnt,met_id in enumerate(self.metaboliteMapping['base_met_ids']):
            met_ids_elements_I.append({met_id:self.metaboliteMapping['base_met_elements'][met_id_cnt][0]})
        self.make_compoundTrackedMetabolite(self.metaboliteMapping['mapping_id'],model_id_I,met_ids_elements_I,self.metaboliteMapping['met_id'],self.metaboliteMapping['base_met_indices'])
    def make_newMetaboliteMapping(self):
        '''Make a new mapping for the metabolite that switches out the names of the base metabolites
        for the current metabolite'''
        mapping_O= [];
        elements = list(set(self.metaboliteMapping['met_elements']))
        element_cnt = {};
        for element in elements:
            element_cnt[element] = 0;
        for met_element in self.metaboliteMapping['met_elements']:
            mapping = '[' + self.metaboliteMapping['met_id'] + '_'  + met_element + str(element_cnt[met_element]) + ']';
            mapping_O.append(mapping);
            element_cnt[met_element]+=1
        return mapping_O
    def make_defaultBaseMetabolites(self):
        '''Add default base metabolite to the metabolite'''
        self.metaboliteMapping['base_met_ids']=[];
        self.metaboliteMapping['base_met_elements']=[];
        self.metaboliteMapping['base_met_atompositions']=[];
        self.metaboliteMapping['base_met_symmetry_elements']=[];
        self.metaboliteMapping['base_met_symmetry_atompositions']=[];
        self.metaboliteMapping['base_met_indices']=[];
        compartment = self.metaboliteMapping['met_id'].split('_')[-1]
        for cnt,element in enumerate(self.metaboliteMapping['met_elements']):
            if element == 'C':
                self.metaboliteMapping['base_met_ids'].append('co2'+'_'+compartment);
                self.metaboliteMapping['base_met_elements'].append([element]);
                self.metaboliteMapping['base_met_atompositions'].append([0]);
                self.metaboliteMapping['base_met_indices'].append(cnt);
            elif element == 'H':
                self.metaboliteMapping['base_met_ids'].append('h'+'_'+element);
                self.metaboliteMapping['base_met_elements'].append([element]);
                self.metaboliteMapping['base_met_atompositions'].append([0]);
                self.metaboliteMapping['base_met_indices'].append(cnt);
            else: print "element not yet supported"
    def convert_arrayMapping2StringMapping(self):
        '''Convert an array representation of a mapping to a string representation'''
        arrayMapping = self.metaboliteMapping['met_mapping']
        stringMapping = ''
        for mapping in self.metaboliteMapping['met_mapping']:
            stringMapping+=''.join(mapping)
        return stringMapping;
    def convert_stringMapping2ArrayMapping(self):
        '''Convert a string representation of a mapping to an array representation'''
        
        stringMapping = self.metaboliteMapping['met_mapping']
        if '[' in self.metaboliteMapping['met_mapping']:
            stringMapping = self.metaboliteMapping['met_mapping'].split('][');
            stringMapping = [m.replace('[','') for m in stringMapping];
            stringMapping = [m.replace(']','') for m in stringMapping];
        else:
            stringMapping = [m for m in stringMapping];
        # add in '[]'
        arrayMapping = [];
        for m in stringMapping:
            arrayMapping.append('['+m+']')
        return arrayMapping;
    def add_metaboliteMapping(self,
            mapping_id_I=None,
            met_id_I=None,
            met_elements_I=None,
            met_atompositions_I=None,
            met_symmetry_elements_I=None,
            met_symmetry_atompositions_I=None,
            used__I=True,
            comment__I=None):
        '''Add tracked metabolite to the database'''
        if mapping_id_I: self.metaboliteMapping['mapping_id']=mapping_id_I;
        if met_id_I: self.metaboliteMapping['met_id']=met_id_I;
        if met_elements_I: self.metaboliteMapping['met_elements']=met_elements_I;
        if met_atompositions_I: self.metaboliteMapping['met_atompositions']=met_atompositions_I;
        if met_symmetry_elements_I: self.metaboliteMapping['met_symmetry_elements']=met_symmetry_elements_I;
        if met_symmetry_atompositions_I: self.metaboliteMapping['met_symmetry_atompositions']=met_symmetry_atompositions_I;
        if used__I: self.metaboliteMapping['used_']=used__I;
        if comment__I: self.metaboliteMapping['comment_']=comment__I;
        #add data to the database
        #row = None;
        #row = data_stage02_isotopomer_atomMappingMetabolites(self.metaboliteMapping['mapping_id'],
        #    self.metaboliteMapping['met_id'],
        #    self.metaboliteMapping['met_elements'],
        #    self.metaboliteMapping['met_atompositions'],
        #    self.metaboliteMapping['met_symmetry_elements'],
        #    self.metaboliteMapping['met_symmetry_atompositions'],
        #    self.metaboliteMapping['used_'],
        #    self.metaboliteMapping['comment_'],
        #    self.make_newMetaboliteMapping(),
        #    self.metaboliteMapping['base_met_ids'],
        #    self.metaboliteMapping['base_met_elements'],
        #    self.metaboliteMapping['base_met_atompositions'],
        #    self.metaboliteMapping['base_met_symmetry_elements'],
        #    self.metaboliteMapping['base_met_symmetry_atompositions'],
        #    self.metaboliteMapping['base_met_indices']);
        #self.session.add(row);
        #self.session.commit();
        data = self.metaboliteMapping;
        data['met_mapping'] = self.make_newMetaboliteMapping();
        self.stage02_isotopomer_query.add_data_dataStage02IsotopomerAtomMappingMetabolites([data]);
    def update_metaboliteMapping(self,
            mapping_id_I=None,
            met_id_I=None,
            met_elements_I=None,
            met_atompositions_I=None,
            met_symmetry_elements_I=None,
            met_symmetry_atompositions_I=None,
            used__I=True,
            comment__I=None):
        '''Add tracked metabolite to the database'''
        if mapping_id_I: self.metaboliteMapping['mapping_id']=mapping_id_I;
        if met_id_I: self.metaboliteMapping['met_id']=met_id_I;
        if met_elements_I: self.metaboliteMapping['met_elements']=met_elements_I;
        if met_atompositions_I: self.metaboliteMapping['met_atompositions']=met_atompositions_I;
        if met_symmetry_elements_I: self.metaboliteMapping['met_symmetry_elements']=met_symmetry_elements_I;
        if met_symmetry_atompositions_I: self.metaboliteMapping['met_symmetry_atompositions']=met_symmetry_atompositions_I;
        if used__I: self.metaboliteMapping['used_']=used__I;
        if comment__I: self.metaboliteMapping['comment_']=comment__I;
        self.metaboliteMapping['met_mapping']=self.make_newMetaboliteMapping()
        #add update data in the database
        self.stage02_isotopomer_query.update_rows_dataStage02IsotopomerAtomMappingMetabolites([self.metaboliteMapping]);
    def get_metaboliteMapping(self,mapping_id_I,met_id_I):
        '''Get tracked metabolite from the database'''
        row = {}
        row = self.stage02_isotopomer_query.get_rows_mappingIDAndMetID_dataStage02IsotopomerAtomMappingMetabolites(mapping_id_I,met_id_I);
        self.metaboliteMapping=row;
    def get_baseMetabolites(self):
        '''Get base metabolite from the database for the current metabolite'''
        row = {}
        row = self.stage02_isotopomer_query.get_rows_mappingIDAndMetID_dataStage02IsotopomerAtomMappingMetabolites(self.metaboliteMapping['mapping_id'],self.metaboliteMapping['met_id']);
        self.metaboliteMapping['base_met_ids']=row['base_met_ids'];
        self.metaboliteMapping['base_met_elements']=row['base_met_elements']
        self.metaboliteMapping['base_met_atompositions']=row['base_met_atompositions']
        self.metaboliteMapping['base_met_symmetry_elements']=row['base_met_symmetry_elements']
        self.metaboliteMapping['base_met_symmetry_atompositions']=row['base_met_symmetry_atompositions']
        ## if the current base_met_indices are already set, add to them
        ## NOTE: works only if the base metabolite is also the current metabolite
        #if len(self.metaboliteMapping['base_met_indices'])==1:
        #    currentIndex = self.metaboliteMapping['base_met_indices'][0]
        #    self.metaboliteMapping['base_met_indices'] = [currentIndex + i for i in row['base_met_indices']];
        ## else ensure that all met_id/base_met_index pairs are unique
        #else:
        #    self.metaboliteMapping['base_met_indices']=row['base_met_indices']
        self.metaboliteMapping['base_met_indices']=row['base_met_indices']
    def clear_metaboliteMapping(self):
        self.metaboliteMapping={};
        self.metaboliteMapping['mapping_id']=None;
        #self.metaboliteMapping['met_name']=None;
        self.metaboliteMapping['met_id']=None;
        #self.metaboliteMapping['formula']=None;
        self.metaboliteMapping['met_elements']=None;
        self.metaboliteMapping['met_atompositions']=None;
        self.metaboliteMapping['met_symmetry_elements']=None;
        self.metaboliteMapping['met_symmetry_atompositions']=None;
        self.metaboliteMapping['used_']=True;
        self.metaboliteMapping['comment_']=None;
        self.metaboliteMapping['met_mapping']=None;
        self.metaboliteMapping['base_met_ids']=None;
        self.metaboliteMapping['base_met_elements']=None;
        self.metaboliteMapping['base_met_atompositions']=None;
        self.metaboliteMapping['base_met_symmetry_elements']=None;
        self.metaboliteMapping['base_met_symmetry_atompositions']=None;
        self.metaboliteMapping['base_met_indices']=None;
    def make_symmetric(self,met_symmetry_elements_I=[],met_symmetry_atompositions_I=[]):
        '''Make the current metabolite symmetric
        default = 180 symmetry'''
        if met_symmetry_elements_I and met_symmetry_atompositions_I:
            self.metaboliteMapping['met_symmetry_elements']=met_symmetry_elements_I;
            self.metaboliteMapping['met_symmetry_atompositions']=met_symmetry_atompositions_I;
        else:
            self.metaboliteMapping['met_symmetry_elements']=[m for m in reversed(self.metaboliteMapping['met_elements'])];
            self.metaboliteMapping['met_symmetry_atompositions']=[m for m in reversed(self.metaboliteMapping['met_atompositions'])];
    def copy_metaboliteMappingDict(self):
        '''Copy the current metabolite mapping'''
        copy_metaboliteMapping = {};
        copy_metaboliteMapping['mapping_id']=self.metaboliteMapping['mapping_id']
        #copy_metaboliteMapping['met_name']=self.metaboliteMapping['met_name']
        copy_metaboliteMapping['met_id']=self.metaboliteMapping['met_id']
        #copy_metaboliteMapping['formula']=self.metaboliteMapping['formula']
        copy_metaboliteMapping['met_elements']=self.metaboliteMapping['met_elements']
        copy_metaboliteMapping['met_atompositions']=self.metaboliteMapping['met_atompositions']
        copy_metaboliteMapping['met_symmetry_elements']=self.metaboliteMapping['met_symmetry_elements']
        copy_metaboliteMapping['met_symmetry_atompositions']=self.metaboliteMapping['met_symmetry_atompositions']
        copy_metaboliteMapping['used_']=self.metaboliteMapping['used_']
        copy_metaboliteMapping['comment_']=self.metaboliteMapping['comment_']
        copy_metaboliteMapping['met_mapping']=self.metaboliteMapping['met_mapping']
        copy_metaboliteMapping['base_met_ids']=self.metaboliteMapping['base_met_ids']
        copy_metaboliteMapping['base_met_elements']=self.metaboliteMapping['base_met_elements']
        copy_metaboliteMapping['base_met_atompositions']=self.metaboliteMapping['base_met_atompositions']
        copy_metaboliteMapping['base_met_symmetry_elements']=self.metaboliteMapping['base_met_symmetry_elements']
        copy_metaboliteMapping['base_met_symmetry_atompositions']=self.metaboliteMapping['base_met_symmetry_atompositions']
        copy_metaboliteMapping['base_met_indices']=self.metaboliteMapping['base_met_indices'];
        return copy_metaboliteMapping
    def copy_metaboliteMapping(self):
        '''Copy the current metabolite mapping'''
        return self;

class stage02_isotopomer_reactionMapping():
    def __init__(self,
            mapping_id_I=None,
            rxn_id_I=None,
            rxn_description_I=None,
            reactants_stoichiometry_tracked_I=[],
            products_stoichiometry_tracked_I=[],
            reactants_ids_tracked_I=[],
            products_ids_tracked_I=[],
            reactants_elements_tracked_I=[],
            products_elements_tracked_I=[],
            reactants_positions_tracked_I=[],
            products_positions_tracked_I=[],
            reactants_mapping_I=[],
            products_mapping_I=[],
            rxn_equation_I=None,
            used__I=None,
            comment__I=None,
            reactants_metaboliteMappings_I=[],
            products_metaboliteMappings_I=[]):
        #self.session = Session();
        self.stage02_isotopomer_query = stage02_isotopomer_query();
        self.calculate = base_calculate();
        self.reactionMapping={}
        self.reactionMapping['mapping_id']=mapping_id_I
        self.reactionMapping['rxn_id']=rxn_id_I
        self.reactionMapping['rxn_description']=rxn_description_I
        self.reactionMapping['reactants_stoichiometry_tracked']=reactants_stoichiometry_tracked_I
        self.reactionMapping['products_stoichiometry_tracked']=products_stoichiometry_tracked_I
        self.reactionMapping['reactants_ids_tracked']=reactants_ids_tracked_I
        self.reactionMapping['products_ids_tracked']=products_ids_tracked_I
        self.reactionMapping['reactants_elements_tracked']=reactants_elements_tracked_I
        self.reactionMapping['products_elements_tracked']=products_elements_tracked_I
        self.reactionMapping['reactants_positions_tracked']=reactants_positions_tracked_I
        self.reactionMapping['products_positions_tracked']=products_positions_tracked_I
        self.reactionMapping['reactants_mapping']=reactants_mapping_I
        self.reactionMapping['products_mapping']=products_mapping_I
        self.reactionMapping['rxn_equation']=rxn_equation_I
        self.reactionMapping['used_']=used__I
        self.reactionMapping['comment_']=comment__I
        self.reactionMapping['reactants_metaboliteMappings']=reactants_metaboliteMappings_I
        self.reactionMapping['products_metaboliteMappings']=products_metaboliteMappings_I
        self.reactants_base_met_ids=[];
        self.reactants_base_met_elements=[];
        self.reactants_base_met_atompositions=[];
        self.reactants_base_met_symmetry_elements=[];
        self.reactants_base_met_symmetry_atompositions=[];
        self.reactants_base_met_indices=[];
        self.products_base_met_ids=[];
        self.products_base_met_elements=[];
        self.products_base_met_atompositions=[];
        self.products_base_met_symmetry_elements=[];
        self.products_base_met_symmetry_atompositions=[];
        self.products_base_met_indices=[];
    def make_trackedCompoundReaction_fromRow(self,mapping_id_I,model_id_I,rxn_id_I,
            rxn_description_I=None,
            reactants_stoichiometry_tracked_I=[],
            products_stoichiometry_tracked_I=[],
            reactants_ids_tracked_I=[],
            products_ids_tracked_I=[],
            reactants_mapping_I=[],
            products_mapping_I=[],
            rxn_equation_I=None,
            used__I=True,
            comment__I=None):
        
        irm = stage02_isotopomer_reactionMapping(
            mapping_id_I=mapping_id_I,
            rxn_id_I=rxn_id_I,
            rxn_description_I=rxn_id_I,
            reactants_stoichiometry_tracked_I=reactants_stoichiometry_tracked_I,
            products_stoichiometry_tracked_I=products_stoichiometry_tracked_I,
            reactants_ids_tracked_I=reactants_ids_tracked_I,
            products_ids_tracked_I=products_ids_tracked_I,
            reactants_mapping_I=reactants_mapping_I,
            products_mapping_I=products_mapping_I,
            rxn_equation_I=rxn_equation_I,
            used__I=used__I,
            comment__I=comment__I);
        irm.reactionMapping['reactants_elements_tracked']=None;
        irm.reactionMapping['reactants_positions_tracked']=None;
        irm.reactionMapping['products_elements_tracked']=None;
        irm.reactionMapping['products_positions_tracked']=None;
        irm.checkAndCorrect_elementsAndPositions();
        
        self.reactionMapping['mapping_id']=irm.reactionMapping['mapping_id']
        self.reactionMapping['rxn_id']=irm.reactionMapping['rxn_id']
        self.reactionMapping['rxn_description']=irm.reactionMapping['rxn_description']
        self.reactionMapping['rxn_equation']=irm.reactionMapping['rxn_equation']
        self.reactionMapping['used_']=irm.reactionMapping['used_']
        self.reactionMapping['comment_']=irm.reactionMapping['comment_']
        for reactant_id_cnt,reactant_id in enumerate(irm.reactionMapping['reactants_ids_tracked']):
            self.reactionMapping['reactants_stoichiometry_tracked'].append(irm.reactionMapping['reactants_stoichiometry_tracked'][reactant_id_cnt])
            self.reactionMapping['reactants_ids_tracked'].append(irm.reactionMapping['reactants_ids_tracked'][reactant_id_cnt])
            self.reactionMapping['reactants_elements_tracked'].append(irm.reactionMapping['reactants_elements_tracked'][reactant_id_cnt])
            self.reactionMapping['reactants_positions_tracked'].append(irm.reactionMapping['reactants_positions_tracked'][reactant_id_cnt])
            self.reactionMapping['reactants_mapping'].append(irm.reactionMapping['reactants_mapping'][reactant_id_cnt])
            self.reactionMapping['products_mapping'].append(irm.reactionMapping['products_mapping'][reactant_id_cnt])
        for product_id_cnt,product_id in enumerate(irm.reactionMapping['products_ids_tracked']):
            self.reactionMapping['products_stoichiometry_tracked'].append(irm.reactionMapping['products_stoichiometry_tracked'][product_id_cnt])
            self.reactionMapping['products_ids_tracked'].append(irm.reactionMapping['products_ids_tracked'][product_id_cnt])
            self.reactionMapping['products_elements_tracked'].append(irm.reactionMapping['products_elements_tracked'][product_id_cnt])
            self.reactionMapping['products_positions_tracked'].append(irm.reactionMapping['products_positions_tracked'][product_id_cnt])
            self.reactionMapping['products_mapping'].append(irm.reactionMapping['products_mapping'][product_id_cnt])

        self.make_reactantsAndProductsMetaboliteMappings(reactionMapping_I=irm.reactionMapping);
    def make_trackedBinaryReaction(self,mapping_id_I,model_id_I,rxn_id_I,reactant_ids_elements_I,product_id_I):
        '''Make a binary reaction of the form A + B + ... = C'''
        #Input
        # reactant_ids_elements_I = [met_id:{elements=[string,...],stoichiometry:float}},..]
        # product_ids_elements_I = {met_id:{elements=[string,...],stoichiometry:float}}}
        # e.g. met_ids_elements_I = [{'f6p_c':'C'},{'ac_c':'C'},{'utp_c','C'}]
        # e.g. irm.make_trackedBinaryReaction('full04','140407_iDM2014','rxn01',met_ids_elements_I,'uacgam_c')

        imm = stage02_isotopomer_metaboliteMapping();
        # get unique met_ids
        reactant_ids_all = [];
        for row in reactant_ids_elements_I:
            for k,v in row.iteritems():
                reactant_ids_all.append(k);
        reactant_ids_unique = list(set(reactant_ids_all))
        reactant_ids_cnt = {};
        for reactant_id in reactant_ids_unique:
            reactant_ids_cnt[reactant_id] = 0;
        # make the reactants mapping
        reactants_stoichiometry_tracked_O = [];
        reactants_ids_tracked_O = [];
        reactants_elements_tracked_O = [];
        reactants_positions_tracked_O = [];
        reactants_mapping_O = [];
        reactants_metaboliteMappings_O = [];
        for row in reactant_ids_elements_I:
            for k,v in row.iteritems():
                imm.make_trackedMetabolite(mapping_id_I,model_id_I,{k:v},reactant_ids_cnt[k]);
                reactants_elements_tracked_O.append(imm.metaboliteMapping['met_elements']);
                reactants_positions_tracked_O.append(imm.metaboliteMapping['met_atompositions']);
                reactants_mapping_O.append(imm.convert_arrayMapping2StringMapping());
                reactants_stoichiometry_tracked_O.append(-1.0);
                reactants_ids_tracked_O.append(k);
                reactants_metaboliteMappings_O.append(copy(imm.copy_metaboliteMapping()));
                imm.clear_metaboliteMapping()
                reactant_ids_cnt[k]+=1
        # make the products mapping
        products_stoichiometry_tracked_O = [];
        products_ids_tracked_O = [];
        products_elements_tracked_O = [];
        products_positions_tracked_O = [];
        products_mapping_O = [];
        products_metaboliteMappings_O = [];
        if product_id_I:
            imm.make_compoundTrackedMetabolite(mapping_id_I,model_id_I,reactant_ids_elements_I,product_id_I);
            products_elements_tracked_O.append(imm.metaboliteMapping['met_elements']);
            products_positions_tracked_O.append(imm.metaboliteMapping['met_atompositions']);
            products_mapping_O.append(imm.convert_arrayMapping2StringMapping());
            products_stoichiometry_tracked_O.append(1.0);
            products_ids_tracked_O.append(product_id_I);
            products_metaboliteMappings_O.append(copy(imm.copy_metaboliteMapping()));
        # save the reaction
        self.reactionMapping['mapping_id']=mapping_id_I
        self.reactionMapping['rxn_id']=rxn_id_I
        self.reactionMapping['rxn_description']=None
        self.reactionMapping['reactants_stoichiometry_tracked']=reactants_stoichiometry_tracked_O
        self.reactionMapping['products_stoichiometry_tracked']=products_stoichiometry_tracked_O
        self.reactionMapping['reactants_ids_tracked']=reactants_ids_tracked_O
        self.reactionMapping['products_ids_tracked']=products_ids_tracked_O
        self.reactionMapping['reactants_elements_tracked']=reactants_elements_tracked_O
        self.reactionMapping['products_elements_tracked']=products_elements_tracked_O
        self.reactionMapping['reactants_positions_tracked']=reactants_positions_tracked_O
        self.reactionMapping['products_positions_tracked']=products_positions_tracked_O
        self.reactionMapping['reactants_mapping']=reactants_mapping_O
        self.reactionMapping['products_mapping']=products_mapping_O
        self.reactionMapping['rxn_equation']=None
        self.reactionMapping['used_']=True
        self.reactionMapping['comment_']=None
        self.reactionMapping['reactants_metaboliteMappings']=reactants_metaboliteMappings_O
        self.reactionMapping['products_metaboliteMappings']=products_metaboliteMappings_O
    def make_trackedCompoundReaction(self,mapping_id_I,model_id_I,rxn_id_I,reactant_ids_elements_I,base_reactant_positions_I,base_reactant_indices_I,compound_product_id_I,base_product_ids_elements_I,base_product_ids_O):
        '''Make a compound tracked reaction
        1. make compound product
        2. remove specified base products from compound product
        3. update the compound product
        4. rename the base products
        5. append base products to products list'''

        #Input
        # reactant_ids_elements_I = [{met_id:elements},...]
        # base_reactant_positions_I = [{met_id_reactant:position},...] #Note: must be listed in order (positions of the reactant to be partitioned)
        # base_reactant_indices_I = [{met_id_product:position in base_reactants_ids},...] #Note: must be listed in order (positions of the reactant to be partitioned)
        #                                                                                        index referes to the position of the base met_id in the reactant to be partitioned
        # compound_product_id_I = met_id
        # base_product_ids_elements_I = [{met_id:elements},...] #Note: must be listed in order
        # base_product_ids_O = [met_id_new,...] #Note: must be listed in order

        imm = stage02_isotopomer_metaboliteMapping();
        imm_product = stage02_isotopomer_metaboliteMapping();
        # initialize the structure to track the base_met_ids
        reactant_ids_all = [];
        for k in self.reactionMapping['reactants_ids_tracked']:
            reactant_ids_all.append(k);
        reactant_ids_unique = list(set(reactant_ids_all))
        reactant_ids_cnt = {};
        for reactant_id in reactant_ids_unique:
            reactant_ids_cnt[reactant_id] = 0;
        for reactant_id in reactant_ids_all:
            reactant_ids_cnt[reactant_id]+=1;
        # initialize the count for unique base_met_ids
        reactants_base_met_ids = [];
        reactants_base_indices = [];
        for cnt,mm in enumerate(self.reactionMapping['reactants_metaboliteMappings']):
            reactants_base_met_ids.extend(mm.metaboliteMapping['base_met_ids'])
            reactants_base_indices.extend(self.reactionMapping['reactants_metaboliteMappings'][cnt].metaboliteMapping['base_met_indices'])
        reactants_base_met_ids_I = [];
        # get unique reactants_base_met_ids
        reactants_base_met_ids_unique = list(set(reactants_base_met_ids));
        reactants_base_met_ids_cnt = {};
        for base_met_id in reactants_base_met_ids_unique:
            reactants_base_met_ids_cnt[base_met_id]=0;
        for cnt,base_met_id in enumerate(reactants_base_met_ids):
            reactants_base_met_ids_cnt[base_met_id]=reactants_base_indices[cnt]+1
        # make the reactants mapping
        imm_product.metaboliteMapping['mapping_id'] = mapping_id_I
        imm_product.metaboliteMapping['base_met_ids']=[];
        imm_product.metaboliteMapping['base_met_elements']=[];
        imm_product.metaboliteMapping['base_met_atompositions']=[];
        imm_product.metaboliteMapping['base_met_symmetry_elements']=[];
        imm_product.metaboliteMapping['base_met_symmetry_atompositions']=[];
        imm_product.metaboliteMapping['base_met_indices']=[];
        # initialize the counter the input
        matched_cnt = 0;      
        for row_cnt,row in enumerate(reactant_ids_elements_I):
            for k,v in row.iteritems():
                # initialize new metabolites
                if not k in reactant_ids_cnt.keys():
                    reactant_ids_cnt[k]=0
                # make the metabolite mapping
                imm.make_trackedMetabolite(mapping_id_I,model_id_I,{k:v},reactant_ids_cnt[k]);
                #update the counter for unique met_ids
                reactant_ids_cnt[k]+=1
                # update base_metabolites from the database for reactant that will be partitioned
                base_found = False;
                if matched_cnt < len(base_reactant_positions_I):
                    for k1,v1 in base_reactant_positions_I[matched_cnt].iteritems(): #there will be only 1 key-value pair
                        if k1 == k and row_cnt == v1:
                            imm.get_baseMetabolites();
                            imm.update_trackedMetabolite_fromBaseMetabolites(model_id_I);
                            base_found = True;
                            break;
                # assign new indices for each base metabolite based on the current indices in the reactants
                base_met_indices_tmp = copy(imm.metaboliteMapping['base_met_indices']);
                for cnt1,met_id1 in enumerate(imm.metaboliteMapping['base_met_ids']):
                    # initialize new base metabolites
                    if not met_id1 in reactants_base_met_ids_cnt.keys():
                        reactants_base_met_ids_cnt[met_id1]=0;
                    # assign the next current base_metabolite_index
                    imm.metaboliteMapping['base_met_indices'][cnt1]=reactants_base_met_ids_cnt[met_id1]
                    # update the base_reactant_indices_I if the corresponding base_met_index was changed
                    if matched_cnt < len(base_reactant_positions_I):
                        for k1,v1 in base_reactant_positions_I[matched_cnt].iteritems(): #there will be only 1 key-value pair
                            if k1 == k and row_cnt == v1: # does the met_id and position in the reactant list match?
                                for k2,v2 in base_reactant_indices_I[matched_cnt].iteritems():
                                    if k2==met_id1 and v2==base_met_indices_tmp[cnt1]: # does the base_met_id and previous index match?
                                        base_reactant_indices_I[matched_cnt][k2]=imm.metaboliteMapping['base_met_indices'][cnt1];
                    reactants_base_met_ids_cnt[met_id1]+=1;
                # update counter for matched input
                if base_found: matched_cnt+=1;
                # update met_mapping
                imm.update_trackedMetabolite_fromBaseMetabolites(model_id_I);
                # add in the new metaboliteMapping information
                self.reactionMapping['reactants_elements_tracked'].append(imm.metaboliteMapping['met_elements']);
                self.reactionMapping['reactants_positions_tracked'].append(imm.metaboliteMapping['met_atompositions']);
                self.reactionMapping['reactants_mapping'].append(imm.convert_arrayMapping2StringMapping());
                self.reactionMapping['reactants_stoichiometry_tracked'].append(-1.0);
                self.reactionMapping['reactants_ids_tracked'].append(k);
                self.reactionMapping['reactants_metaboliteMappings'].append(copy(imm.copy_metaboliteMapping())); 
                self.reactants_base_met_ids.extend(imm.metaboliteMapping['base_met_ids']);
                self.reactants_base_met_elements.extend(imm.metaboliteMapping['base_met_elements']);
                self.reactants_base_met_atompositions.extend(imm.metaboliteMapping['base_met_atompositions']);
                #self.reactants_base_met_symmetry_elements.extend(imm.metaboliteMapping['base_met_symmetry_elements']);
                #self.reactants_base_met_symmetry_atompositions.extend(imm.metaboliteMapping['base_met_symmetry_atompositions']);
                self.reactants_base_met_indices.extend(imm.metaboliteMapping['base_met_indices']);  
                # copy out all of the base information for the product
                imm_product.metaboliteMapping['base_met_ids'].extend(imm.metaboliteMapping['base_met_ids']);
                imm_product.metaboliteMapping['base_met_elements'].extend(imm.metaboliteMapping['base_met_elements']);
                imm_product.metaboliteMapping['base_met_atompositions'].extend(imm.metaboliteMapping['base_met_atompositions']);
                #imm_product.metaboliteMapping['base_met_symmetry_elements'].extend(imm.metaboliteMapping['base_met_symmetry_elements']);
                #imm_product.metaboliteMapping['base_met_symmetry_atompositions'].extend(imm.metaboliteMapping['base_met_symmetry_atompositions']);
                imm_product.metaboliteMapping['base_met_indices'].extend(imm.metaboliteMapping['base_met_indices']); 
                #
                imm.clear_metaboliteMapping()
        # make the initial compound product mapping
        imm_product.update_trackedMetabolite_fromBaseMetabolites(model_id_I)
        imm_product.metaboliteMapping['met_id']=compound_product_id_I;
        # extract out the products from the compound product
        base_products = [];
        for cnt,row in enumerate(base_product_ids_elements_I):
            for k,v in row.iteritems():
                base_products.append(imm_product.extract_baseMetabolite_fromMetabolite(model_id_I,{k:v},base_reactant_indices_I[cnt][k]));
        # remove the base_products from the compound product
        for cnt,row in enumerate(base_product_ids_elements_I):
            for k,v in row.iteritems():
                imm_product.remove_baseMetabolite_fromMetabolite(model_id_I,{k:v},met_id_O=compound_product_id_I,met_index_I=base_reactant_indices_I[cnt][k]);
        # make the final products
        if compound_product_id_I: imm_final_products = [imm_product];
        else: imm_final_products = [];
        for d in base_products:
            imm_final_products.append(d);
        if compound_product_id_I: imm_final_products_ids = [compound_product_id_I];
        else: imm_final_products_ids = [];
        for id in base_product_ids_O:
            imm_final_products_ids.append(id);
        for cnt,d in enumerate(imm_final_products):
            self.reactionMapping['products_elements_tracked'].append(d.metaboliteMapping['met_elements']);
            self.reactionMapping['products_positions_tracked'].append(d.metaboliteMapping['met_atompositions']);
            self.reactionMapping['products_mapping'].append(d.convert_arrayMapping2StringMapping());
            self.reactionMapping['products_stoichiometry_tracked'].append(1.0);
            self.reactionMapping['products_ids_tracked'].append(imm_final_products_ids[cnt]);
            self.reactionMapping['products_metaboliteMappings'].append(copy(d.copy_metaboliteMapping()));
        # save the reaction
        self.reactionMapping['mapping_id']=mapping_id_I
        self.reactionMapping['rxn_id']=rxn_id_I
        self.reactionMapping['rxn_description']=None
        self.reactionMapping['rxn_equation']=None
        self.reactionMapping['used_']=True
        self.reactionMapping['comment_']=None
    def make_trackedCompoundReaction_fromMetaboliteMappings(self,mapping_id_I,model_id_I,rxn_id_I,reactant_metaboliteMappings_I,base_reactant_positions_I,base_reactant_indices_I,compound_product_id_I,base_product_ids_elements_I,base_product_ids_O):
        '''Make a compound tracked reaction
        1. make compound product
        2. remove specified base products from compound product
        3. update the compound product
        4. rename the base products
        5. append base products to products list'''

        #Input
        # reactant_metaboliteMappings_I = [mm_1,mm_2,...]
        # base_reactant_positions_I = [{met_id_reactant:position},...] #Note: must be listed in order (positions of the reactant to be partitioned)
        # base_reactant_indices_I = [{met_id_product:position in base_reactants_ids},...] #Note: must be listed in order (positions of the reactant to be partitioned)
        #                                                                                        index referes to the position of the base met_id in the reactant to be partitioned
        # compound_product_id_I = met_id
        # base_product_ids_elements_I = [{met_id:elements},...] #Note: must be listed in order
        # base_product_ids_O = [met_id_new,...] #Note: must be listed in order

        imm_product = stage02_isotopomer_metaboliteMapping();
        # initialize the structure to track the base_met_ids
        reactant_ids_all = [];
        for k in self.reactionMapping['reactants_ids_tracked']:
            reactant_ids_all.append(k);
        reactant_ids_unique = list(set(reactant_ids_all))
        reactant_ids_cnt = {};
        for reactant_id in reactant_ids_unique:
            reactant_ids_cnt[reactant_id] = 0;
        for reactant_id in reactant_ids_all:
            reactant_ids_cnt[reactant_id]+=1;
        # initialize the count for unique base_met_ids
        reactants_base_met_ids = [];
        reactants_base_indices = [];
        for cnt,mm in enumerate(self.reactionMapping['reactants_metaboliteMappings']):
            reactants_base_met_ids.extend(mm.metaboliteMapping['base_met_ids'])
            reactants_base_indices.extend(self.reactionMapping['reactants_metaboliteMappings'][cnt].metaboliteMapping['base_met_indices'])
        reactants_base_met_ids_I = [];
        # get unique reactants_base_met_ids
        reactants_base_met_ids_unique = list(set(reactants_base_met_ids));
        reactants_base_met_ids_cnt = {};
        for base_met_id in reactants_base_met_ids_unique:
            reactants_base_met_ids_cnt[base_met_id]=0;
        for cnt,base_met_id in enumerate(reactants_base_met_ids):
            reactants_base_met_ids_cnt[base_met_id]=reactants_base_indices[cnt]+1
        # make the reactants mapping
        imm_product.metaboliteMapping['mapping_id'] = mapping_id_I
        imm_product.metaboliteMapping['base_met_ids']=[];
        imm_product.metaboliteMapping['base_met_elements']=[];
        imm_product.metaboliteMapping['base_met_atompositions']=[];
        imm_product.metaboliteMapping['base_met_symmetry_elements']=[];
        imm_product.metaboliteMapping['base_met_symmetry_atompositions']=[];
        imm_product.metaboliteMapping['base_met_indices']=[];
        # initialize the counter the input
        matched_cnt = 0;      
        for row_cnt,imm in enumerate(reactant_metaboliteMappings_I):
            # initialize new metabolites
            if not imm.metaboliteMapping['met_id'] in reactant_ids_cnt.keys():
                reactant_ids_cnt[imm.metaboliteMapping['met_id']]=0
            # make the metabolite mapping
            #update the counter for unique met_ids
            reactant_ids_cnt[imm.metaboliteMapping['met_id']]+=1
            # update base_metabolites from the database for reactant that will be partitioned
            base_found = False;
            if matched_cnt < len(base_reactant_positions_I):
                for k1,v1 in base_reactant_positions_I[matched_cnt].iteritems(): #there will be only 1 key-value pair
                    if k1 == imm.metaboliteMapping['met_id'] and row_cnt == v1:
                        base_found = True;
                        break;
            # assign new indices for each base metabolite based on the current indices in the reactants
            base_met_indices_tmp = copy(imm.metaboliteMapping['base_met_indices']);
            for cnt1,met_id1 in enumerate(imm.metaboliteMapping['base_met_ids']):
                # initialize new base metabolites
                if not met_id1 in reactants_base_met_ids_cnt.keys():
                    reactants_base_met_ids_cnt[met_id1]=0;
                # assign the next current base_metabolite_index
                imm.metaboliteMapping['base_met_indices'][cnt1]=reactants_base_met_ids_cnt[met_id1]
                # update the base_reactant_indices_I if the corresponding base_met_index was changed
                if matched_cnt < len(base_reactant_positions_I):
                    for k1,v1 in base_reactant_positions_I[matched_cnt].iteritems(): #there will be only 1 key-value pair
                        if k1 == imm.metaboliteMapping['met_id'] and row_cnt == v1: # does the met_id and position in the reactant list match?
                            for k2,v2 in base_reactant_indices_I[matched_cnt].iteritems():
                                if k2==met_id1 and v2==base_met_indices_tmp[cnt1]: # does the base_met_id and previous index match?
                                    base_reactant_indices_I[matched_cnt][k2]=imm.metaboliteMapping['base_met_indices'][cnt1];
                reactants_base_met_ids_cnt[met_id1]+=1;
            # update counter for matched input
            if base_found: matched_cnt+=1;
            # update met_mapping
            imm.update_trackedMetabolite_fromBaseMetabolites(model_id_I);
            # add in the new metaboliteMapping information
            self.reactionMapping['reactants_elements_tracked'].append(imm.metaboliteMapping['met_elements']);
            self.reactionMapping['reactants_positions_tracked'].append(imm.metaboliteMapping['met_atompositions']);
            self.reactionMapping['reactants_mapping'].append(imm.convert_arrayMapping2StringMapping());
            self.reactionMapping['reactants_stoichiometry_tracked'].append(-1.0);
            self.reactionMapping['reactants_ids_tracked'].append(imm.metaboliteMapping['met_id']);
            self.reactionMapping['reactants_metaboliteMappings'].append(copy(imm.copy_metaboliteMapping())); 
            self.reactants_base_met_ids.extend(imm.metaboliteMapping['base_met_ids']);
            self.reactants_base_met_elements.extend(imm.metaboliteMapping['base_met_elements']);
            self.reactants_base_met_atompositions.extend(imm.metaboliteMapping['base_met_atompositions']);
            #self.reactants_base_met_symmetry_elements.extend(imm.metaboliteMapping['base_met_symmetry_elements']);
            #self.reactants_base_met_symmetry_atompositions.extend(imm.metaboliteMapping['base_met_symmetry_atompositions']);
            self.reactants_base_met_indices.extend(imm.metaboliteMapping['base_met_indices']);  
            # copy out all of the base information for the product
            imm_product.metaboliteMapping['base_met_ids'].extend(imm.metaboliteMapping['base_met_ids']);
            imm_product.metaboliteMapping['base_met_elements'].extend(imm.metaboliteMapping['base_met_elements']);
            imm_product.metaboliteMapping['base_met_atompositions'].extend(imm.metaboliteMapping['base_met_atompositions']);
            #imm_product.metaboliteMapping['base_met_symmetry_elements'].extend(imm.metaboliteMapping['base_met_symmetry_elements']);
            #imm_product.metaboliteMapping['base_met_symmetry_atompositions'].extend(imm.metaboliteMapping['base_met_symmetry_atompositions']);
            imm_product.metaboliteMapping['base_met_indices'].extend(imm.metaboliteMapping['base_met_indices']); 
        # make the initial compound product mapping
        imm_product.update_trackedMetabolite_fromBaseMetabolites(model_id_I)
        imm_product.metaboliteMapping['met_id']=compound_product_id_I;
        # extract out the products from the compound product
        base_products = [];
        for cnt,row in enumerate(base_product_ids_elements_I):
            for k,v in row.iteritems():
                base_products.append(imm_product.extract_baseMetabolite_fromMetabolite(model_id_I,{k:v},base_reactant_indices_I[cnt][k]));
        # remove the base_products from the compound product
        for cnt,row in enumerate(base_product_ids_elements_I):
            for k,v in row.iteritems():
                imm_product.remove_baseMetabolite_fromMetabolite(model_id_I,{k:v},met_id_O=compound_product_id_I,met_index_I=base_reactant_indices_I[cnt][k]);
        # make the final products
        if compound_product_id_I: imm_final_products = [imm_product];
        else: imm_final_products = [];
        for d in base_products:
            imm_final_products.append(d);
        if compound_product_id_I: imm_final_products_ids = [compound_product_id_I];
        else: imm_final_products_ids = [];
        for id in base_product_ids_O:
            imm_final_products_ids.append(id);
        for cnt,d in enumerate(imm_final_products):
            self.reactionMapping['products_elements_tracked'].append(d.metaboliteMapping['met_elements']);
            self.reactionMapping['products_positions_tracked'].append(d.metaboliteMapping['met_atompositions']);
            self.reactionMapping['products_mapping'].append(d.convert_arrayMapping2StringMapping());
            self.reactionMapping['products_stoichiometry_tracked'].append(1.0);
            self.reactionMapping['products_ids_tracked'].append(imm_final_products_ids[cnt]);
            self.reactionMapping['products_metaboliteMappings'].append(copy(d.copy_metaboliteMapping()));
        # save the reaction
        self.reactionMapping['mapping_id']=mapping_id_I
        self.reactionMapping['rxn_id']=rxn_id_I
        self.reactionMapping['rxn_description']=None
        self.reactionMapping['rxn_equation']=None
        self.reactionMapping['used_']=True
        self.reactionMapping['comment_']=None
    def make_trackedUnitaryReactions(self,mapping_id_I,model_id_I,rxn_id_I,reactant_ids_elements_I,product_ids_I):
        '''Make a unitary reaction of the form aA = bB where the coefficient a = b'''
        #Input
        # reactant_ids_elements_I = [{met_id:elements},]
        # product_ids_elements_I = [met_id,...]

        # check input
        if len(reactant_ids_elements_I)!=len(product_ids_I):
            print "length of reactants_ids does not match the length of products_ids";
            return;
        imm = stage02_isotopomer_metaboliteMapping();
        # get unique met_ids
        reactant_ids_all = [];
        for row in reactant_ids_elements_I:
            for k,v in row.iteritems():
                reactant_ids_all.append(k);
        reactant_ids_unique = list(set(reactant_ids_all))
        reactant_ids_cnt = {};
        for reactant_id in reactant_ids_unique:
            reactant_ids_cnt[reactant_id] = 0;
        # make the reactants mapping
        reactants_stoichiometry_tracked_O = [];
        reactants_ids_tracked_O = [];
        reactants_elements_tracked_O = [];
        reactants_positions_tracked_O = [];
        reactants_mapping_O = [];
        reactants_metaboliteMappings_O = [];
        for row in reactant_ids_elements_I:
            for k,v in row.iteritems():
                imm.make_trackedMetabolite(mapping_id_I,model_id_I,{k:v},reactant_ids_cnt[k]);
                reactants_elements_tracked_O.append(imm.metaboliteMapping['met_elements']);
                reactants_positions_tracked_O.append(imm.metaboliteMapping['met_atompositions']);
                reactants_mapping_O.append(imm.convert_arrayMapping2StringMapping());
                reactants_stoichiometry_tracked_O.append(-abs(1));
                reactants_ids_tracked_O.append(k);
                reactants_metaboliteMappings_O.append(copy(imm.copy_metaboliteMapping()));
                imm.clear_metaboliteMapping()
                reactant_ids_cnt[k]+=1
        # make the products mapping
        products_stoichiometry_tracked_O = [];
        products_ids_tracked_O = [];
        products_elements_tracked_O = [];
        products_positions_tracked_O = [];
        products_mapping_O = [];
        products_metaboliteMappings_O = [];
        for product_cnt,product in enumerate(product_ids_I):
            products_elements_tracked_O.append(reactants_elements_tracked_O[product_cnt]);
            products_positions_tracked_O.append(reactants_positions_tracked_O[product_cnt]);
            products_mapping_O.append(reactants_mapping_O[product_cnt]);
            products_stoichiometry_tracked_O.append(abs(reactants_stoichiometry_tracked_O[product_cnt]));
            products_ids_tracked_O.append(product);
            imm_tmp = copy(reactants_metaboliteMappings_O[product_cnt].copy_metaboliteMapping());
            imm_tmp.metaboliteMapping['met_id']=product; # change the name
            products_metaboliteMappings_O.append(imm_tmp);
        # save the reaction
        self.reactionMapping['mapping_id']=mapping_id_I
        self.reactionMapping['rxn_id']=rxn_id_I
        self.reactionMapping['rxn_description']=None
        self.reactionMapping['reactants_stoichiometry_tracked']=reactants_stoichiometry_tracked_O
        self.reactionMapping['products_stoichiometry_tracked']=products_stoichiometry_tracked_O
        self.reactionMapping['reactants_ids_tracked']=reactants_ids_tracked_O
        self.reactionMapping['products_ids_tracked']=products_ids_tracked_O
        self.reactionMapping['reactants_elements_tracked']=reactants_elements_tracked_O
        self.reactionMapping['products_elements_tracked']=products_elements_tracked_O
        self.reactionMapping['reactants_positions_tracked']=reactants_positions_tracked_O
        self.reactionMapping['products_positions_tracked']=products_positions_tracked_O
        self.reactionMapping['reactants_mapping']=reactants_mapping_O
        self.reactionMapping['products_mapping']=products_mapping_O
        self.reactionMapping['rxn_equation']=None
        self.reactionMapping['used_']=True
        self.reactionMapping['comment_']=None
        self.reactionMapping['reactants_metaboliteMappings']=reactants_metaboliteMappings_O
        self.reactionMapping['products_metaboliteMappings']=products_metaboliteMappings_O
    def make_reverseReaction(self,rxn_id_I=None):
        '''Make the reverse of the current reaction'''
        forward_reactionMapping = {}
        forward_reactionMapping['mapping_id']=self.reactionMapping['mapping_id']
        forward_reactionMapping['rxn_id']=self.reactionMapping['rxn_id']
        forward_reactionMapping['rxn_description']=self.reactionMapping['rxn_description']
        forward_reactionMapping['reactants_stoichiometry_tracked']=self.reactionMapping['reactants_stoichiometry_tracked']
        forward_reactionMapping['products_stoichiometry_tracked']=self.reactionMapping['products_stoichiometry_tracked']
        forward_reactionMapping['reactants_ids_tracked']=self.reactionMapping['reactants_ids_tracked']
        forward_reactionMapping['products_ids_tracked']=self.reactionMapping['products_ids_tracked']
        forward_reactionMapping['reactants_elements_tracked']=self.reactionMapping['reactants_elements_tracked']
        forward_reactionMapping['products_elements_tracked']=self.reactionMapping['products_elements_tracked']
        forward_reactionMapping['reactants_positions_tracked']=self.reactionMapping['reactants_positions_tracked']
        forward_reactionMapping['products_positions_tracked']=self.reactionMapping['products_positions_tracked']
        forward_reactionMapping['reactants_mapping']=self.reactionMapping['reactants_mapping']
        forward_reactionMapping['products_mapping']=self.reactionMapping['products_mapping']
        forward_reactionMapping['rxn_equation']=self.reactionMapping['rxn_equation']
        forward_reactionMapping['used_']=self.reactionMapping['used_']
        forward_reactionMapping['comment_']=self.reactionMapping['comment_']
        forward_reactionMapping['reactants_metaboliteMappings']=self.reactionMapping['reactants_metaboliteMappings']
        forward_reactionMapping['products_metaboliteMappings']=self.reactionMapping['products_metaboliteMappings']
        reverse_reactionMapping = {}
        reverse_reactionMapping['mapping_id']=self.reactionMapping['mapping_id']
        if rxn_id_I: reverse_reactionMapping['rxn_id']=rxn_id_I
        else: reverse_reactionMapping['rxn_id']=self.reactionMapping['rxn_id']
        reverse_reactionMapping['rxn_description']=self.reactionMapping['rxn_description']
        reverse_reactionMapping['reactants_stoichiometry_tracked']=[-s for s in self.reactionMapping['products_stoichiometry_tracked']]
        reverse_reactionMapping['products_stoichiometry_tracked']=[-s for s in self.reactionMapping['reactants_stoichiometry_tracked']]
        reverse_reactionMapping['reactants_ids_tracked']=self.reactionMapping['products_ids_tracked']
        reverse_reactionMapping['products_ids_tracked']=self.reactionMapping['reactants_ids_tracked']
        reverse_reactionMapping['reactants_elements_tracked']=self.reactionMapping['products_elements_tracked']
        reverse_reactionMapping['products_elements_tracked']=self.reactionMapping['reactants_elements_tracked']
        reverse_reactionMapping['reactants_positions_tracked']=self.reactionMapping['products_positions_tracked']
        reverse_reactionMapping['products_positions_tracked']=self.reactionMapping['reactants_positions_tracked']
        reverse_reactionMapping['reactants_mapping']=self.reactionMapping['products_mapping']
        reverse_reactionMapping['products_mapping']=self.reactionMapping['reactants_mapping']
        reverse_reactionMapping['rxn_equation']=self.reactionMapping['rxn_equation']
        reverse_reactionMapping['used_']=self.reactionMapping['used_']
        reverse_reactionMapping['comment_']=self.reactionMapping['comment_']
        reverse_reactionMapping['reactants_metaboliteMappings']=self.reactionMapping['products_metaboliteMappings']
        reverse_reactionMapping['products_metaboliteMappings']=self.reactionMapping['reactants_metaboliteMappings']
        self.reactionMapping = reverse_reactionMapping;
    def add_reactionMapping(self,
            mapping_id_I=None,
            rxn_id_I=None,
            rxn_description_I=None,
            reactants_stoichiometry_tracked_I=[],
            products_stoichiometry_tracked_I=[],
            reactants_ids_tracked_I=[],
            products_ids_tracked_I=[],
            reactants_elements_tracked_I=[],
            products_elements_tracked_I=[],
            reactants_positions_tracked_I=[],
            products_positions_tracked_I=[],
            reactants_mapping_I=[],
            products_mapping_I=[],
            rxn_equation_I=None,
            used__I=None,
            comment__I=None):
        
        if mapping_id_I: self.reactionMapping['mapping_id']=mapping_id_I
        if rxn_id_I: self.reactionMapping['rxn_id']=rxn_id_I
        if rxn_description_I: self.reactionMapping['rxn_description']=rxn_description_I
        if reactants_stoichiometry_tracked_I: self.reactionMapping['reactants_stoichiometry_tracked']=reactants_stoichiometry_tracked_I
        if products_stoichiometry_tracked_I: self.reactionMapping['products_stoichiometry_tracked']=products_stoichiometry_tracked_I
        if reactants_ids_tracked_I: self.reactionMapping['reactants_ids_tracked']=reactants_ids_tracked_I
        if products_ids_tracked_I: self.reactionMapping['products_ids_tracked']=products_ids_tracked_I
        if reactants_elements_tracked_I: self.reactionMapping['reactants_elements_tracked']=reactants_elements_tracked_I
        if products_elements_tracked_I: self.reactionMapping['products_elements_tracked']=products_elements_tracked_I
        if reactants_positions_tracked_I: self.reactionMapping['reactants_positions_tracked']=reactants_positions_tracked_I
        if products_positions_tracked_I: self.reactionMapping['products_positions_tracked']=products_positions_tracked_I
        if reactants_mapping_I: self.reactionMapping['reactants_mapping']=reactants_mapping_I
        if products_mapping_I: self.reactionMapping['products_mapping']=products_mapping_I
        if rxn_equation_I: self.reactionMapping['rxn_equation']=rxn_equation_I
        if used__I: self.reactionMapping['used_']=used__I
        if comment__I: self.reactionMapping['comment_']=comment__I
        # add data to the database
        self.stage02_isotopomer_query.add_data_dataStage02IsotopomerAtomMappingReactions([self.reactionMapping])
    def add_productMapping(self,product_ids_I):
        '''Add newly made products to the atomMappingMetabolite table for future use'''
        for product in self.reactionMapping['products_metaboliteMappings']:
            if product.metaboliteMapping['met_id'] in product_ids_I:
                product.add_metaboliteMapping();
    def update_productMapping(self,product_ids_I):
        '''Update newly made products to the atomMappingMetabolite table for future use'''
        for product in self.reactionMapping['products_metaboliteMappings']:
            if product.metaboliteMapping['met_id'] in product_ids_I:
                product.update_metaboliteMapping();
    def update_reactionMapping(self,
            mapping_id_I=None,
            rxn_id_I=None,
            rxn_description_I=None,
            reactants_stoichiometry_tracked_I=[],
            products_stoichiometry_tracked_I=[],
            reactants_ids_tracked_I=[],
            products_ids_tracked_I=[],
            reactants_elements_tracked_I=[],
            products_elements_tracked_I=[],
            reactants_positions_tracked_I=[],
            products_positions_tracked_I=[],
            reactants_mapping_I=[],
            products_mapping_I=[],
            rxn_equation_I=None,
            used__I=None,
            comment__I=None):
        
        if mapping_id_I: self.reactionMapping['mapping_id']=mapping_id_I
        if rxn_id_I: self.reactionMapping['rxn_id']=rxn_id_I
        if rxn_description_I: self.reactionMapping['rxn_description']=rxn_description_I
        if reactants_stoichiometry_tracked_I: self.reactionMapping['reactants_stoichiometry_tracked']=reactants_stoichiometry_tracked_I
        if products_stoichiometry_tracked_I: self.reactionMapping['products_stoichiometry_tracked']=products_stoichiometry_tracked_I
        if reactants_ids_tracked_I: self.reactionMapping['reactants_ids_tracked']=reactants_ids_tracked_I
        if products_ids_tracked_I: self.reactionMapping['products_ids_tracked']=products_ids_tracked_I
        if reactants_elements_tracked_I: self.reactionMapping['reactants_elements_tracked']=reactants_elements_tracked_I
        if products_elements_tracked_I: self.reactionMapping['products_elements_tracked']=products_elements_tracked_I
        if reactants_positions_tracked_I: self.reactionMapping['reactants_positions_tracked']=reactants_positions_tracked_I
        if products_positions_tracked_I: self.reactionMapping['products_positions_tracked']=products_positions_tracked_I
        if reactants_mapping_I: self.reactionMapping['reactants_mapping']=reactants_mapping_I
        if products_mapping_I: self.reactionMapping['products_mapping']=products_mapping_I
        if rxn_equation_I: self.reactionMapping['rxn_equation']=rxn_equation_I
        if used__I: self.reactionMapping['used_']=used__I
        if comment__I: self.reactionMapping['comment_']=comment__I
        self.stage02_isotopomer_query.update_rows_dataStage02IsotopomerAtomMappingReactions([self.reactionMapping]);
    def get_reactionMapping(self,mapping_id_I,rxn_id_I):
        row = {};
        row = self.stage02_isotopomer_query.get_row_mappingIDAndRxnID_dataStage02IsotopomerAtomMappingReactions(mapping_id_I,rxn_id_I);
        self.reactionMapping = row;
        self.reactionMapping['reactants_metaboliteMappings']=[]
        self.reactionMapping['products_metaboliteMappings']=[]
        self.make_reactantsAndProductsMetaboliteMappings();
    def make_reactantsAndProductsMetaboliteMappings(self,reactionMapping_I=None):
        '''Make reactants and products metabolite mapping from atomMappingReaction information'''

        #Input:
        #   reactionMapping_I = row of atomMappingReactions
        #                       default: None, user current self

        if reactionMapping_I: reactionMapping_tmp = reactionMapping_I;
        else: reactionMapping_tmp = reactionMapping_tmp;
        for cnt,met in enumerate(reactionMapping_tmp['reactants_ids_tracked']):
            imm = stage02_isotopomer_metaboliteMapping(mapping_id_I=reactionMapping_tmp['mapping_id'],
                met_id_I=met,
                met_elements_I=reactionMapping_tmp['reactants_elements_tracked'][cnt],
                met_atompositions_I=reactionMapping_tmp['reactants_positions_tracked'][cnt],
                met_symmetry_elements_I=[],
                met_symmetry_atompositions_I=[],
                used__I=True,
                comment__I=None,
                met_mapping_I=reactionMapping_tmp['reactants_mapping'][cnt],
                base_met_ids_I=[],
                base_met_elements_I=[],
                base_met_atompositions_I=[],
                base_met_symmetry_elements_I=[],
                base_met_symmetry_atompositions_I=[],
                base_met_indices_I=[]);
            self.reactionMapping['reactants_metaboliteMappings'].append(copy(imm.copy_metaboliteMapping()));
        for cnt,met in enumerate(reactionMapping_tmp['products_ids_tracked']):
            imm = stage02_isotopomer_metaboliteMapping(mapping_id_I=reactionMapping_tmp['mapping_id'],
                met_id_I=met,
                met_elements_I=reactionMapping_tmp['products_elements_tracked'][cnt],
                met_atompositions_I=reactionMapping_tmp['products_positions_tracked'][cnt],
                met_symmetry_elements_I=[],
                met_symmetry_atompositions_I=[],
                used__I=True,
                comment__I=None,
                met_mapping_I=reactionMapping_tmp['products_mapping'][cnt],
                base_met_ids_I=[],
                base_met_elements_I=[],
                base_met_atompositions_I=[],
                base_met_symmetry_elements_I=[],
                base_met_symmetry_atompositions_I=[],
                base_met_indices_I=[]);
            self.reactionMapping['products_metaboliteMappings'].append(copy(imm.copy_metaboliteMapping()));
    def clear_reactionMapping(self):
        self.reactionMapping={}
        self.reactionMapping['mapping_id']=None
        self.reactionMapping['rxn_id']=None
        self.reactionMapping['rxn_description']=None
        self.reactionMapping['reactants_stoichiometry_tracked']=[]
        self.reactionMapping['products_stoichiometry_tracked']=[]
        self.reactionMapping['reactants_ids_tracked']=[]
        self.reactionMapping['products_ids_tracked']=[]
        self.reactionMapping['reactants_elements_tracked']=[]
        self.reactionMapping['products_elements_tracked']=[]
        self.reactionMapping['reactants_positions_tracked']=[]
        self.reactionMapping['products_positions_tracked']=[]
        self.reactionMapping['reactants_mapping']=[]
        self.reactionMapping['products_mapping']=[]
        self.reactionMapping['rxn_equation']=None
        self.reactionMapping['used_']=True
        self.reactionMapping['comment_']=None
        self.reactionMapping['reactants_metaboliteMappings']=[]
        self.reactionMapping['products_metaboliteMappings']=[]
        self.reactants_base_met_ids=[];
        self.reactants_base_met_elements=[];
        self.reactants_base_met_atompositions=[];
        self.reactants_base_met_symmetry_elements=[];
        self.reactants_base_met_symmetry_atompositions=[];
        self.reactants_base_met_indices=[];
        self.products_base_met_ids=[];
        self.products_base_met_elements=[];
        self.products_base_met_atompositions=[];
        self.products_base_met_symmetry_elements=[];
        self.products_base_met_symmetry_atompositions=[];
        self.products_base_met_indices=[];
    def checkAndCorrect_elementsAndPositions(self):
        '''Check that the reactant/product elements/positions are consistent with the
        reactants/products ids_tracked; if they are not, correct them'''
        # check that elements/positions are initialized
        if not self.reactionMapping['reactants_elements_tracked']:
            self.reactionMapping['reactants_elements_tracked']=[];
            for cnt,reactant_id in enumerate(self.reactionMapping['reactants_ids_tracked']):
                self.reactionMapping['reactants_elements_tracked'].append([]);
        if not self.reactionMapping['reactants_positions_tracked']:
            self.reactionMapping['reactants_positions_tracked']=[];
            for cnt,reactant_id in enumerate(self.reactionMapping['reactants_ids_tracked']):
                self.reactionMapping['reactants_positions_tracked'].append([]);
        # check that the length of the elements/positions match the length of the ids_tracked
        #TODO...
        # check each elements/positions
        for cnt,reactant_id in enumerate(self.reactionMapping['reactants_ids_tracked']):
            # get the metabolite data from the database
            met_data = {}
            met_data = self.stage02_isotopomer_query.get_rows_mappingIDAndMetID_dataStage02IsotopomerAtomMappingMetabolites(self.reactionMapping['mapping_id'],reactant_id);
            if len(met_data['met_elements'])!=len(self.reactionMapping['reactants_elements_tracked'][cnt]):
                self.reactionMapping['reactants_elements_tracked'][cnt]=met_data['met_elements'];
            if len(met_data['met_atompositions'])!=len(self.reactionMapping['reactants_positions_tracked'][cnt]):
                self.reactionMapping['reactants_positions_tracked'][cnt]=met_data['met_atompositions'];
        # check that elements/positions are initialized
        if not self.reactionMapping['products_elements_tracked']:
            self.reactionMapping['products_elements_tracked']=[];
            for cnt,product_id in enumerate(self.reactionMapping['products_ids_tracked']):
                self.reactionMapping['products_elements_tracked'].append([]);
        if not self.reactionMapping['products_positions_tracked']:
            self.reactionMapping['products_positions_tracked']=[];
            for cnt,product_id in enumerate(self.reactionMapping['products_ids_tracked']):
                self.reactionMapping['products_positions_tracked'].append([]);
        # check that the length of the elements/positions match the length of the ids_tracked
        #TODO...
        # check each elements/positions
        for cnt,product_id in enumerate(self.reactionMapping['products_ids_tracked']):
            # get the metabolite data from the database
            met_data = {}
            met_data = self.stage02_isotopomer_query.get_rows_mappingIDAndMetID_dataStage02IsotopomerAtomMappingMetabolites(self.reactionMapping['mapping_id'],product_id);
            if len(met_data['met_elements'])!=len(self.reactionMapping['products_elements_tracked'][cnt]):
                self.reactionMapping['products_elements_tracked'][cnt]=met_data['met_elements'];
            if len(met_data['met_atompositions'])!=len(self.reactionMapping['products_positions_tracked'][cnt]):
                self.reactionMapping['products_positions_tracked'][cnt]=met_data['met_atompositions'];
    def add_balanceProducts(self,unbalanced_met_I=None,unbalanced_met_position_I=None,unbalanced_met_positions_tracked_I=[],make_lumped_unbalanced_met_I=False,make_unique_unbalanced_mets_I=True):
        '''Add psuedo metabolites to the product in order to elementally balance the tracked reaction'''
        #Input:
        #   unbalanced_met_I = reactant_id that is not elementally balanced
        #   unbalanced_met_position_I = position of the reactant_id in the reactants_list
        #   unbalanced_met_positions_tracked_I = positions of the elements that are not elementally balanced
        #   make_lumped_unbalanced_met_I = boolean,
        #        automatically detect mappings that are not elementally balanced and make an unbalanced product metabolite to balance all elementally unbalanced reactants
        #        NOTE: does not work if the stoichiometry of all unbalanced reactants are not 1
        #   make_unique_unbalanced_mets_I = boolean,
        #        automatically detect mappings/metabolites that are not elementally balanced and makes unbalanced product mappings/metabolites to balance each elementally unbalanced reactant mapping/metabolite

        if make_lumped_unbalanced_met_I:
            #TODO: check that all unbalanced reactants have a stoichiometry of 1
            balance_met = self.reactionMapping['rxn_id'] + '_' + 'balance_c' + '.balance';
            reactants_mappings = []; #list of a list
            products_mappings = []; #list
            # extract out reactants and products mappings
            for imm in self.reactionMapping['reactants_metaboliteMappings']:
                reactant_mapping=[];
                reactant_mapping = imm.convert_stringMapping2ArrayMapping();
                reactants_mappings.append(reactant_mapping);
            for imm in self.reactionMapping['products_metaboliteMappings']:
                product_mapping=[];
                product_mapping = imm.convert_stringMapping2ArrayMapping();
                products_mappings.extend(product_mapping);
            # find unbalanced reactant_mappings and
            # make the product mapping, positions, and elements
            product_mapping = [];
            product_positions_tracked = [];
            product_elements_tracked = [];
            product_cnt = 0;
            for reactant_cnt,reactants_mapping in enumerate(reactants_mappings):
                for element_cnt,reactant_mapping in enumerate(reactants_mapping):
                    if not reactant_mapping in products_mappings:
                        product_mapping.append(reactant_mapping);
                        product_elements_tracked.append(self.reactionMapping['reactants_elements_tracked'][reactant_cnt][element_cnt]);
                        product_positions_tracked.append(product_cnt);
                        product_cnt += 1;
            imm = stage02_isotopomer_metaboliteMapping(mapping_id_I=self.reactionMapping['mapping_id'],
                met_id_I=balance_met,
                met_elements_I=product_elements_tracked,
                met_atompositions_I=product_positions_tracked,
                met_symmetry_elements_I=[],
                met_symmetry_atompositions_I=[],
                used__I=True,
                comment__I=None,
                met_mapping_I=product_mapping,
                base_met_ids_I=[],
                base_met_elements_I=[],
                base_met_atompositions_I=[],
                base_met_symmetry_elements_I=[],
                base_met_symmetry_atompositions_I=[],
                base_met_indices_I=[]);
            # add balance metabolite to the products
            self.reactionMapping['products_ids_tracked'].append(balance_met);
            self.reactionMapping['products_mapping'].append(imm.convert_arrayMapping2StringMapping());
            self.reactionMapping['products_positions_tracked'].append(product_positions_tracked);
            self.reactionMapping['products_stoichiometry_tracked'].append(1);
            self.reactionMapping['products_elements_tracked'].append(product_elements_tracked);
            self.reactionMapping['products_metaboliteMappings'].append(copy(imm.copy_metaboliteMapping()));
        elif make_unique_unbalanced_mets_I:
            products_mappings = []; #list
            # extract out products mappings
            for imm in self.reactionMapping['products_metaboliteMappings']:
                product_mapping=[];
                product_mapping = imm.convert_stringMapping2ArrayMapping();
                products_mappings.extend(product_mapping);
            # check each reactant mapping/metabolite
            for reactant_pos,imm in enumerate(self.reactionMapping['reactants_metaboliteMappings']):
                reactant_mapping=[];
                reactant_mapping = imm.convert_stringMapping2ArrayMapping();
                # find missing mappings
                product_mapping = [];
                product_positions_tracked = [];
                product_elements_tracked = [];
                balance_met = None;
                for mapping_pos,mapping in enumerate(reactant_mapping): 
                    if mapping not in products_mappings:
                        balance_met = self.reactionMapping['rxn_id'] + '_' + self.reactionMapping['reactants_ids_tracked'][reactant_pos] + '_' + str(reactant_pos) + '.balance';
                        product_mapping.append(mapping);
                        product_positions_tracked.append(self.reactionMapping['reactants_positions_tracked'][reactant_pos][mapping_pos]);
                        product_elements_tracked.append(self.reactionMapping['reactants_elements_tracked'][reactant_pos][mapping_pos]);
                if balance_met:        
                    imm = stage02_isotopomer_metaboliteMapping(mapping_id_I=self.reactionMapping['mapping_id'],
                        met_id_I=balance_met,
                        met_elements_I=product_elements_tracked,
                        met_atompositions_I=product_positions_tracked,
                        met_symmetry_elements_I=[],
                        met_symmetry_atompositions_I=[],
                        used__I=True,
                        comment__I=None,
                        met_mapping_I=product_mapping,
                        base_met_ids_I=[],
                        base_met_elements_I=[],
                        base_met_atompositions_I=[],
                        base_met_symmetry_elements_I=[],
                        base_met_symmetry_atompositions_I=[],
                        base_met_indices_I=[]);
                    # add balance metabolite to the products
                    self.reactionMapping['products_ids_tracked'].append(balance_met);
                    self.reactionMapping['products_mapping'].append(imm.convert_arrayMapping2StringMapping());
                    self.reactionMapping['products_positions_tracked'].append(product_positions_tracked);
                    self.reactionMapping['products_elements_tracked'].append(product_elements_tracked);
                    self.reactionMapping['products_metaboliteMappings'].append(copy(imm.copy_metaboliteMapping()));
                    self.reactionMapping['products_stoichiometry_tracked'].append(abs(self.reactionMapping['reactants_stoichiometry_tracked'][reactant_pos]));
        # use user specifications
        else:
            # find the position of the tracked metabolite
            if self.reactionMapping['reactants_ids_tracked'].index(unbalanced_met_I):
                if unbalanced_met_position_I: unbalanced_met_pos = unbalanced_met_position_I;
                else: unbalanced_met_pos = self.reactionMapping['reactants_ids_tracked'].index(unbalanced_met_I);
                balance_met = self.reactionMapping['rxn_id'] + '_' + unbalanced_met_I + '_' + str(unbalanced_met_pos) + '.balance';
                # extract out mapping, positions, and elements
                reactant_mapping = self.reactionMapping['reactants_metaboliteMappings'][unbalanced_met_pos].convert_stringMapping2ArrayMapping();
                reactant_positions_tracked = self.reactionMapping['reactants_positions_tracked'][unbalanced_met_pos];
                reactant_elements_tracked = self.reactionMapping['reactants_elements_tracked'][unbalanced_met_pos];
                # make the product mapping, positions, and elements
                product_mapping = [];
                product_positions_tracked = [];
                product_elements_tracked = [];
                if unbalanced_met_positions_tracked_I:
                    for pos_cnt,pos in enumerate(unbalanced_met_positions_tracked_I):
                        product_mapping.append(reactant_mapping[pos]);
                        product_positions_tracked.append(pos_cnt);
                        product_elements_tracked.append(reactant_elements_tracked[pos]);
                else:
                    product_mapping=reactant_mapping
                    product_positions_tracked=reactant_positions_tracked
                    product_elements_tracked=reactant_elements_tracked
                imm = stage02_isotopomer_metaboliteMapping(mapping_id_I=self.reactionMapping['mapping_id'],
                    met_id_I=balance_met,
                    met_elements_I=product_elements_tracked,
                    met_atompositions_I=product_positions_tracked,
                    met_symmetry_elements_I=[],
                    met_symmetry_atompositions_I=[],
                    used__I=True,
                    comment__I=None,
                    met_mapping_I=product_mapping,
                    base_met_ids_I=[],
                    base_met_elements_I=[],
                    base_met_atompositions_I=[],
                    base_met_symmetry_elements_I=[],
                    base_met_symmetry_atompositions_I=[],
                    base_met_indices_I=[]);
                # add balance metabolite to the products
                self.reactionMapping['products_ids_tracked'].append(balance_met);
                self.reactionMapping['products_mapping'].append(imm.convert_arrayMapping2StringMapping());
                self.reactionMapping['products_positions_tracked'].append(product_positions_tracked);
                self.reactionMapping['products_elements_tracked'].append(product_elements_tracked);
                self.reactionMapping['products_metaboliteMappings'].append(copy(imm.copy_metaboliteMapping()));
                self.reactionMapping['products_stoichiometry_tracked'].append(1);
            else:
                print 'unbalanced metabolite not found!'
    def check_elementalBalance(self):
        '''
        1. Check that the number of elements tracked in the reactant matches the number of elements tracked
        in the products
        2. Check that the reactant positions tracked match the reactant elements tracked'''

        #Output:
        #   reactants_positions_tracked_cnt
        #   products_positions_tracked_cnt

        element_balance = True;
        #check reactants
        reactants_positions_tracked_cnt = 0;
        for reactant_cnt,reactant in enumerate(self.reactionMapping['reactants_ids_tracked']):
            print 'checking reactant ' + reactant;
            # check that the reactant positions == reactant elements
            if len(self.reactionMapping['reactants_positions_tracked'][reactant_cnt])!=len(self.reactionMapping['reactants_elements_tracked'][reactant_cnt]):
                print 'inconsistent reactants_positions and reactants_elements';
                continue;
            reactants_positions_tracked_cnt += len(self.reactionMapping['reactants_positions_tracked'][reactant_cnt]);
        #check products
        products_positions_tracked_cnt = 0;
        for product_cnt,product in enumerate(self.reactionMapping['products_ids_tracked']):
            print 'checking product ' + product;
            # check that the product positions == product elements
            if len(self.reactionMapping['products_positions_tracked'][product_cnt])!=len(self.reactionMapping['products_elements_tracked'][product_cnt]):
                print 'inconsistent products_positions and products_elements';
                continue;
            products_positions_tracked_cnt += len(self.reactionMapping['products_positions_tracked'][product_cnt]);
        #record
        if reactants_positions_tracked_cnt!=products_positions_tracked_cnt:
            return reactants_positions_tracked_cnt,products_positions_tracked_cnt;
        else: 
            return reactants_positions_tracked_cnt,products_positions_tracked_cnt;
    def check_reactionMapping(self):
        '''
        1. Check that the number of elements tracked in the reactant matches the number of elements tracked
        in the products
        2. Check that the reactant positions tracked match the reactant elements tracked
        3. Check that the mappings are 1-to-1
        4. Check that the elements/positions/mappings are of the same length
        5. Check that the stoichiometry and ids tracked are of the same length'''

        #Output:
        #   reactants_positions_tracked_cnt
        #   products_positions_tracked_cnt

        #checks:
        reactants_ids_stoichiometry_check = True;
        reactants_elements_positions_check = True;
        reactants_elements_mapping_check = True;
        reactants_positions_mapping_check = True;
        products_ids_stoichiometry_check = True;
        products_elements_positions_check = True;
        products_elements_mapping_check = True;
        products_positions_mapping_check = True;
        element_balance_check = True;
        mapping_check = True;
        #check reactants
        reactants_positions_tracked_cnt = 0;
        reactants_elements_tracked_cnt = 0;
        reactants_mappings_cnt = 0;
        reactants_stoichiometry_cnt = 0;
        reactants_ids_cnt = 0;
        reactants_mappings = [];
        # check that the reactant stoichiometry == reactant ids
        if len(self.reactionMapping['reactants_ids_tracked'])!=len(self.reactionMapping['reactants_stoichiometry_tracked']):
            print 'inconsistent reactants_stoichiometry_tracked and reactants_ids_tracked';
            reactants_ids_stoichiometry_check = False;
        reactants_ids_cnt += len(self.reactionMapping['reactants_ids_tracked']);
        reactants_stoichiometry_cnt += len(self.reactionMapping['reactants_stoichiometry_tracked']);
        # check elemental balance
        for reactant_cnt,reactant in enumerate(self.reactionMapping['reactants_ids_tracked']):
            print 'checking reactant elemental balance ' + reactant;
            reactant_mapping=[];
            reactant_mapping = self.reactionMapping['reactants_metaboliteMappings'][reactant_cnt].convert_stringMapping2ArrayMapping();
            # check that the reactant positions == reactant elements
            if len(self.reactionMapping['reactants_positions_tracked'][reactant_cnt])!=len(self.reactionMapping['reactants_elements_tracked'][reactant_cnt]):
                print 'inconsistent reactants_positions and reactants_elements';
                reactants_elements_positions_check = False;
            # check that the reactant positions == reactant mapping
            if len(self.reactionMapping['reactants_positions_tracked'][reactant_cnt])!=len(reactant_mapping):
                print 'inconsistent reactants_positions and reactants_mapping';
                reactants_elements_mapping_check = False;
            # check that the reactant elements == reactant mapping
            if len(self.reactionMapping['reactants_elements_tracked'][reactant_cnt])!=len(reactant_mapping):
                print 'inconsistent reactants_elements and reactants_mapping';
                reactants_positions_mapping_check = False;
            reactants_positions_tracked_cnt += len(self.reactionMapping['reactants_positions_tracked'][reactant_cnt]);
            reactants_elements_tracked_cnt += len(self.reactionMapping['reactants_elements_tracked'][reactant_cnt]);
            reactants_mappings_cnt += len(reactant_mapping);
            reactants_mappings.append(reactant_mapping);
        #check products
        products_positions_tracked_cnt = 0;
        products_elements_tracked_cnt = 0;
        products_mappings_cnt = 0;
        products_stoichiometry_cnt = 0;
        products_ids_cnt = 0;
        products_mappings = [];
        # check that the product stoichiometry == product ids
        if len(self.reactionMapping['products_ids_tracked'])!=len(self.reactionMapping['products_stoichiometry_tracked']):
            print 'inconsistent products_stoichiometry_tracked and products_ids_tracked';
            products_ids_stoichiometry_check = False;
        products_ids_cnt += len(self.reactionMapping['products_ids_tracked']);
        products_stoichiometry_cnt += len(self.reactionMapping['products_stoichiometry_tracked']);
        # check elemental balance
        for product_cnt,product in enumerate(self.reactionMapping['products_ids_tracked']):
            print 'checking product elemental balance ' + product;
            product_mapping=[];
            product_mapping = self.reactionMapping['products_metaboliteMappings'][product_cnt].convert_stringMapping2ArrayMapping();
            # check that the product positions == product elements
            if len(self.reactionMapping['products_positions_tracked'][product_cnt])!=len(self.reactionMapping['products_elements_tracked'][product_cnt]):
                print 'inconsistent products_positions and products_elements';
                products_elements_positions_check = False;
            # check that the product positions == product mapping
            if len(self.reactionMapping['products_positions_tracked'][product_cnt])!=len(product_mapping):
                print 'inconsistent products_positions and products_mapping';
                products_elements_mapping_check = False;
            # check that the product elements == product mapping
            if len(self.reactionMapping['products_elements_tracked'][product_cnt])!=len(product_mapping):
                print 'inconsistent products_elements and products_mapping';
                products_positions_mapping_check = False;
            products_positions_tracked_cnt += len(self.reactionMapping['products_positions_tracked'][product_cnt]);
            products_elements_tracked_cnt += len(self.reactionMapping['products_elements_tracked'][product_cnt]);
            products_mappings_cnt += len(product_mapping);
            products_mappings.append(product_mapping);
        #check elemental balance
        if reactants_positions_tracked_cnt != products_positions_tracked_cnt:
            print 'the length of reactants_positions_tracked does not match the length of products_positions_tracked';
            element_balance_check = False;
        if reactants_elements_tracked_cnt != products_elements_tracked_cnt:
            print 'reactants_elements_tracked does not match the length of products_elements_tracked';
            element_balance_check = False;
        if reactants_mappings_cnt != products_mappings_cnt:
            print 'the length of reactants_mapping does not match the length of products_mapping';
            element_balance_check = False;
        #check 1-to-1 mapping
        reactants_mappings_list = [];
        for reactants_mapping in reactants_mappings:
            reactants_mappings_list.extend(reactants_mapping);
        # check for duplicate reactant mappings
        reactants_mappings_unique = list(set(reactants_mappings_list));
        if len(reactants_mappings_list)!=len(reactants_mappings_unique):
            print 'duplicate reactants_mappings found';
            mapping_check = False;
        products_mappings_list = [];
        for products_mapping in products_mappings:
            products_mappings_list.extend(products_mapping);
        # check for duplicate product mappings
        products_mappings_unique = list(set(products_mappings_list));
        if len(products_mappings_list)!=len(products_mappings_unique):
            print 'duplicate products_mappings found';
            mapping_check = False;
        # check that each product mapping has a matching reactant mapping, and vice versa
        for reactant_cnt,reactant in enumerate(reactants_mappings):
            print 'checking reactant mapping ' + self.reactionMapping['reactants_ids_tracked'][reactant_cnt];
            for mapping_cnt,mapping in enumerate(reactant):
                if not mapping in products_mappings_list:
                    print 'no mapping found for reactant mapping ' + mapping + ' and position ' + str(mapping_cnt);
                    mapping_check = False;
        for product_cnt,product in enumerate(products_mappings):
            print 'checking product mapping ' + self.reactionMapping['products_ids_tracked'][product_cnt];
            for mapping_cnt,mapping in enumerate(product):
                if not mapping in reactants_mappings_list:
                    print 'no mapping found for product mapping ' + mapping + ' and position ' + str(mapping_cnt);
                    mapping_check = False;
        if not element_balance_check or not mapping_check:
            print 'check reaction mapping';
        return reactants_ids_stoichiometry_check,reactants_elements_positions_check,reactants_elements_mapping_check,reactants_positions_mapping_check,\
                products_ids_stoichiometry_check,products_elements_positions_check,products_elements_mapping_check,products_positions_mapping_check,\
                element_balance_check,mapping_check;

class stage02_isotopomer_mappingUtilities():
    def __init__(self):
        self.stage02_isotopomer_query = stage02_isotopomer_query();
    def make_missingMetaboliteMappings(self,experiment_id_I,model_id_I=[],mapping_id_rxns_I=[],mapping_id_mets_I=[],mapping_id_new_I=None):
        '''Make atom mapping metabolites from atom mapping reactions, QC atom mapping reactions;
        and create a new set of metabolite mappings that correspond to the current reaction mappings that need to be QC/QA'd'''
        
        #Input:
        #   experiment_id_I = experiment_id
        #   model_id_I = model_id
        #   mapping_id_rxns_I = reaction mapping id (#default atomMappingMetabolite mapping id to add new metabolites to)
        #   mapping_id_mets_I = existing metabolite mappings to use when making the new metabolite mappings
        #   mapping_id_new_I = name of mapping id for the new metabolite mappings

        #Output:
        #   default: new metabolite mappings will be added for the mapping id of the reactions
        #            existing metabolite mappings will not be added
        #   mapping_id_new_I != None: new metabolite mappings will be added for the mapping id specified

        #get model ids:
        if model_id_I:
            model_ids = model_id_I;
        else:
            model_ids = [];
            model_ids = self.stage02_isotopomer_query.get_modelID_experimentID_dataStage02IsotopomerSimulation(experiment_id_I);
        for model_id in model_ids:
            #get mapping ids
            if mapping_id_rxns_I and mapping_id_mets_I:
                mapping_ids_rxns=mapping_id_rxns_I;
                mapping_ids_mets=mapping_id_mets_I;
            elif mapping_id_rxns_I:
                mapping_ids_rxns=mapping_id_rxns_I;
            else:
                mapping_ids_rxns=[];
                mapping_ids_rxns=self.stage02_isotopomer_query.get_mappingID_experimentIDAndModelID_dataStage02IsotopomerSimulation(experiment_id_I,model_id);
            for mapping_cnt,mapping_id_rxns in enumerate(mapping_ids_rxns):
                # get the metabolite mappings
                if mapping_id_rxns_I and mapping_id_mets_I:
                    mappings=self.stage02_isotopomer_query.get_atomMappingMetabolites_mappingID_dataStage02IsotopomerAtomMappingReactionsAndAtomMappingMetabolites(mapping_id_rxns,mapping_ids_mets[mapping_cnt]);
                else:
                    mappings = self.stage02_isotopomer_query.get_atomMappingMetabolites_mappingID_dataStage02IsotopomerAtomMappingReactions(mapping_id_rxns);
                # remove duplicates
                duplicate_ind = [];
                for d1_cnt,d1 in enumerate(mappings):
                    for d2_cnt in range(d1_cnt+1,len(mappings)):
                        if d1['mapping_id'] == mappings[d2_cnt]['mapping_id'] and \
                        d1['met_id'] == mappings[d2_cnt]['met_id'] and \
                        d1['met_elements'] == mappings[d2_cnt]['met_elements'] and \
                        d1['met_atompositions'] == mappings[d2_cnt]['met_atompositions'] and \
                        d1['met_symmetry_elements'] == mappings[d2_cnt]['met_symmetry_elements'] and \
                        d1['met_symmetry_atompositions'] == mappings[d2_cnt]['met_symmetry_atompositions']:
                            duplicate_ind.append(d2_cnt);
                duplicate_ind_unique=list(set(duplicate_ind));
                # copy out unique metabolites
                data_O = [];
                for d1_cnt,d1 in enumerate(mappings):
                    if d1_cnt in duplicate_ind_unique:
                        continue;
                    else:
                        if mapping_id_new_I: d1['mapping_id']=mapping_id_new_I; # change to the new mapping
                        data_O.append(d1);
                met_ids = [x['met_id'] for x in data_O];
                met_ids_unique = list(set(met_ids));
                data_mets_cnt = {};
                for met in met_ids_unique:
                    data_mets_cnt[met] = 0;
                for d in data_O:
                    data_mets_cnt[d['met_id']] += 1;
                # add data to the database
                if mapping_id_new_I:
                    self.stage02_isotopomer_query.add_data_dataStage02IsotopomerAtomMappingMetabolites(data_O);
                else:
                    data_add_O = [];
                    for d in data_O:
                        # check to see if the metabolite is already in the database
                        mapping_row = {};
                        mapping_row = self.stage02_isotopomer_query.get_rows_mappingIDAndMetID_dataStage02IsotopomerAtomMappingMetabolites(mapping_id_rxns,d['met_id']);
                        if not mapping_row: data_add_O.append(d);
                    self.stage02_isotopomer_query.add_data_dataStage02IsotopomerAtomMappingMetabolites(data_add_O);
    def make_missingReactionMappings(self,experiment_id_I,model_id_I=[],mapping_id_rxns_I=[],mapping_id_mets_I=[],mapping_id_new_I=None):
        '''Update missing reaction mappings for the current mapping from the matching metabolite mappings,
        and optionally, from the previous reaction mappings'''
        #Note: prior to running, remove all reaction mappings that are not used.
        data_O = [];
        #get model ids:
        if model_id_I:
            model_ids = model_id_I;
        else:
            model_ids = [];
            model_ids = self.stage02_isotopomer_query.get_modelID_experimentID_dataStage02IsotopomerSimulation(experiment_id_I);
        for model_id in model_ids:
            #get all reactions in the model:
            reactions = [];
            reactions = self.stage02_isotopomer_query.get_rows_modelID_dataStage02IsotopomerModelReactions(model_id);
            #get mapping ids
            if mapping_id_rxns_I and mapping_id_mets_I:
                mapping_ids_rxns=mapping_id_rxns_I;
                mapping_ids_mets=mapping_id_mets_I;
            elif mapping_id_rxns_I:
                mapping_ids_rxns=mapping_id_rxns_I;
            else:
                mapping_rxns=[];
                mapping_rxns=self.stage02_isotopomer_query.get_mappingID_experimentIDAndModelID_dataStage02IsotopomerSimulation(experiment_id_I,model_id);
            for mapping_cnt,mapping_id_rxns in enumerate(mapping_ids_rxns):
                missing_reactions_O = [];
                missing_metabolites_O = [];
                for reaction_cnt,reaction in enumerate(reactions):
                    #get the current reaction mappings
                    mapping_rxns = [];
                    mapping_rxns = self.stage02_isotopomer_query.get_row_mappingIDAndRxnID_dataStage02IsotopomerAtomMappingReactions(mapping_id_rxns,reaction['rxn_id']);
                    #if mapping_rxns:  # atom mapping for the reaction already exists and is used
                    #    continue; 
                    if mapping_id_new_I:
                        mapping_id_current = mapping_id_new_I;
                    else:
                        mapping_id_current = mapping_id_rxns;
                    data_tmp={'mapping_id':mapping_id_current,
                                'rxn_id':reaction['rxn_id'],
                                'rxn_description':None,
                                'reactants_stoichiometry_tracked':[],
                                'products_stoichiometry_tracked':[],
                                'reactants_ids_tracked':[],
                                'products_ids_tracked':[],
                                'reactants_mapping':[],
                                'products_mapping':[],
                                'rxn_equation':reaction['equation'],
                                'products_elements_tracked':[],
                                'products_positions_tracked':[],
                                'reactants_elements_tracked':[],
                                'reactants_positions_tracked':[],
                                'used_':True,
                                'comment_':''};
                    #check if the reactants or products are tracked
                    tracked_reactants = [];
                    for reactant in reaction['reactants_ids']:
                        tracked_reactant = {};
                        if mapping_id_mets_I:
                            tracked_reactant = self.stage02_isotopomer_query.get_rows_mappingIDAndMetID_dataStage02IsotopomerAtomMappingMetabolites(mapping_ids_mets[mapping_cnt],reactant);
                        else:
                            tracked_reactant = self.stage02_isotopomer_query.get_rows_mappingIDAndMetID_dataStage02IsotopomerAtomMappingMetabolites(mapping_id_rxns,reactant);
                        if tracked_reactant:
                            tracked_reactants.append(tracked_reactant);
                    tracked_products = [];
                    for product in reaction['products_ids']:
                        tracked_product = {};
                        if mapping_id_mets_I:
                            tracked_product = self.stage02_isotopomer_query.get_rows_mappingIDAndMetID_dataStage02IsotopomerAtomMappingMetabolites(mapping_ids_mets[mapping_cnt],product);
                        else:
                            tracked_product = self.stage02_isotopomer_query.get_rows_mappingIDAndMetID_dataStage02IsotopomerAtomMappingMetabolites(mapping_id_rxns,product);
                        if tracked_product:
                            tracked_products.append(tracked_product);
                    if tracked_reactants or tracked_products:
                        #check if the reaction is missing or is missing a tracked metabolite
                        tracked_reaction = {};
                        tracked_reaction = self.stage02_isotopomer_query.get_row_mappingIDAndRxnID_dataStage02IsotopomerAtomMappingReactions(mapping_id_rxns,reaction['rxn_id']);
                        if tracked_reaction:
                            missing_reactants = [];
                            # get the stoichiometry for each reactant
                            tracked_reaction_reactant_ids_stoich = {};
                            for tracked_reactant_id_cnt,tracked_reactant_id in enumerate(tracked_reaction['reactants_ids_tracked']):
                                tracked_reaction_reactant_ids_stoich[tracked_reactant_id] = 0;
                            for tracked_reactant_id_cnt,tracked_reactant_id in enumerate(tracked_reaction['reactants_ids_tracked']):
                                tracked_reaction_reactant_ids_stoich[tracked_reactant_id] += abs(tracked_reaction['reactants_stoichiometry_tracked'][tracked_reactant_id_cnt]);
                            #copy existing data
                            data_tmp['reactants_ids_tracked'].extend(tracked_reaction['reactants_ids_tracked']);
                            data_tmp['reactants_stoichiometry_tracked'].extend(tracked_reaction['reactants_stoichiometry_tracked']);
                            data_tmp['reactants_mapping'].extend(tracked_reaction['reactants_mapping']);
                            data_tmp['reactants_elements_tracked'].extend(tracked_reaction['reactants_elements_tracked']);
                            data_tmp['reactants_positions_tracked'].extend(tracked_reaction['reactants_positions_tracked']);
                            data_tmp['rxn_description']=tracked_reaction['rxn_description'];
                            for tracked_reactant in tracked_reactants:
                                if tracked_reactant['met_id'] in tracked_reaction['reactants_ids_tracked']:
                                    # check for matching stoichiometry
                                    reaction_stoich = 0;
                                    for met_id_cnt,met_id in enumerate(reaction['reactants_ids']):
                                        if met_id == tracked_reactant['met_id']:
                                            reaction_stoich = abs(reaction['reactants_stoichiometry'][met_id_cnt]);
                                            break;
                                    unbalanced_stoich = reaction_stoich - tracked_reaction_reactant_ids_stoich[tracked_reactant['met_id']];
                                    if tracked_reaction_reactant_ids_stoich[tracked_reactant['met_id']] != reaction_stoich:
                                        for stoich_cnt in range(int(unbalanced_stoich)):
                                            missing_reactants.append(tracked_reactant);
                                            #add missing data
                                            data_tmp['reactants_ids_tracked'].append(tracked_reactant['met_id']);
                                            data_tmp['reactants_stoichiometry_tracked'].append(0);
                                            data_tmp['reactants_mapping'].append('');
                                            data_tmp['reactants_elements_tracked'].append(tracked_reactant['met_elements']);
                                            data_tmp['reactants_positions_tracked'].append(tracked_reactant['met_atompositions']);
                                            data_tmp['rxn_description']=tracked_reaction['rxn_description'];
                                            data_tmp['used_']=False;
                                            data_tmp['comment_']+=tracked_reactant['met_id']+',';
                                else:
                                    missing_reactants.append(tracked_reactant);
                                    #add missing data
                                    data_tmp['reactants_ids_tracked'].append(tracked_reactant['met_id']);
                                    data_tmp['reactants_stoichiometry_tracked'].append(0);
                                    data_tmp['reactants_mapping'].append('');
                                    data_tmp['reactants_elements_tracked'].append(tracked_reactant['met_elements']);
                                    data_tmp['reactants_positions_tracked'].append(tracked_reactant['met_atompositions']);
                                    data_tmp['rxn_description']=tracked_reaction['rxn_description'];
                                    data_tmp['used_']=False;
                                    data_tmp['comment_']+=tracked_reactant['met_id']+',';
                            missing_products = [];
                            # get the stoichiometry for each product
                            tracked_reaction_product_ids_stoich = {};
                            for tracked_product_id_cnt,tracked_product_id in enumerate(tracked_reaction['products_ids_tracked']):
                                tracked_reaction_product_ids_stoich[tracked_product_id] = 0;
                            for tracked_product_id_cnt,tracked_product_id in enumerate(tracked_reaction['products_ids_tracked']):
                                tracked_reaction_product_ids_stoich[tracked_product_id] += abs(tracked_reaction['products_stoichiometry_tracked'][tracked_product_id_cnt]);
                            #copy existing data
                            data_tmp['products_ids_tracked'].extend(tracked_reaction['products_ids_tracked']);
                            data_tmp['products_stoichiometry_tracked'].extend(tracked_reaction['products_stoichiometry_tracked']);
                            data_tmp['products_mapping'].extend(tracked_reaction['products_mapping']);
                            data_tmp['products_elements_tracked'].extend(tracked_reaction['products_elements_tracked']);
                            data_tmp['products_positions_tracked'].extend(tracked_reaction['products_positions_tracked']);
                            data_tmp['rxn_description']=tracked_reaction['rxn_description'];
                            for tracked_product in tracked_products:
                                if tracked_product['met_id'] in tracked_reaction['products_ids_tracked']:
                                    # check for matching stoichiometry
                                    reaction_stoich = 0;
                                    for met_id_cnt,met_id in enumerate(reaction['products_ids']):
                                        if met_id == tracked_product['met_id']:
                                            reaction_stoich = abs(reaction['products_stoichiometry'][met_id_cnt]);
                                            break;
                                    unbalanced_stoich = reaction_stoich - tracked_reaction_product_ids_stoich[tracked_product['met_id']];
                                    if tracked_reaction_product_ids_stoich[tracked_product['met_id']] != reaction_stoich:
                                        for stoich_cnt in range(int(unbalanced_stoich)):
                                            missing_products.append(tracked_product);
                                            #add missing data
                                            data_tmp['products_ids_tracked'].append(tracked_product['met_id']);
                                            data_tmp['products_stoichiometry_tracked'].append(0);
                                            data_tmp['products_mapping'].append('');
                                            data_tmp['products_elements_tracked'].append(tracked_product['met_elements']);
                                            data_tmp['products_positions_tracked'].append(tracked_product['met_atompositions']);
                                            data_tmp['rxn_description']=tracked_reaction['rxn_description'];
                                            data_tmp['used_']=False;
                                            data_tmp['comment_']+=tracked_product['met_id']+',';
                                else:
                                    missing_products.append(tracked_product);
                                    #add missing data
                                    data_tmp['products_ids_tracked'].append(tracked_product['met_id']);
                                    data_tmp['products_stoichiometry_tracked'].append(0);
                                    data_tmp['products_mapping'].append('');
                                    data_tmp['products_elements_tracked'].append(tracked_product['met_elements']);
                                    data_tmp['products_positions_tracked'].append(tracked_product['met_atompositions']);
                                    data_tmp['rxn_description']=tracked_reaction['rxn_description'];
                                    data_tmp['used_']=False;
                                    data_tmp['comment_']+=tracked_product['met_id']+',';
                            if missing_reactants or missing_products:
                                tmp = {};
                                tmp = tracked_reaction;
                                tmp.update({'missing_reactants':missing_reactants});
                                tmp.update({'missing_products':missing_products});
                                tmp.update({'equation':reaction['equation']})
                                missing_metabolites_O.append(tmp);
                        else:
                            tmp = {};
                            tmp = reaction;
                            tmp.update({'tracked_reactants':tracked_reactants});
                            tmp.update({'tracked_products':tracked_products});
                            missing_reactions_O.append(reaction);
                            for tracked_reactant in tracked_reactants:
                                #add missing data
                                data_tmp['reactants_ids_tracked'].append(tracked_reactant['met_id']);
                                data_tmp['reactants_stoichiometry_tracked'].append(0);
                                data_tmp['reactants_mapping'].append('');
                                data_tmp['reactants_elements_tracked'].append(tracked_reactant['met_elements']);
                                data_tmp['reactants_positions_tracked'].append(tracked_reactant['met_atompositions']);
                                data_tmp['rxn_description']=None;
                                data_tmp['used_']=False;
                                data_tmp['comment_']=reaction['rxn_id'];
                            for tracked_product in tracked_products:
                                #add missing data
                                data_tmp['products_ids_tracked'].append(tracked_product['met_id']);
                                data_tmp['products_stoichiometry_tracked'].append(0);
                                data_tmp['products_mapping'].append('');
                                data_tmp['products_elements_tracked'].append(tracked_product['met_elements']);
                                data_tmp['products_positions_tracked'].append(tracked_product['met_atompositions']);
                                data_tmp['rxn_description']=None;
                                data_tmp['used_']=False;
                                data_tmp['comment_']=reaction['rxn_id'];
                    data_O.append(data_tmp);
                self.print_missingReactionMappings(missing_reactions_O,missing_metabolites_O);
        #add data to the database:
        #self.stage02_isotopomer_query.add_data_dataStage02IsotopomerAtomMappingReactions(data_O);
    def print_missingReactionMappings(self,missing_reactions_I,missing_metabolites_I):
        '''print missing reaction mappings to the screen'''
        #missing reactions
        script = '';
        for missing_reaction in missing_reactions_I:
            script+= missing_reaction['rxn_id']+'\t'+missing_reaction['equation']+'\t'+str(missing_reaction['reactants_ids'])+'\t'+str(missing_reaction['products_ids'])+'\t';
            for tracked_reactant in missing_reaction['tracked_reactants']:
                script+= tracked_reactant['met_id']+',';
            script+= '\t'
            for tracked_product in missing_reaction['tracked_products']:
                script+= tracked_product['met_id']+',';
            script+='\n'
        print script
        #missing metabolites
        script = '';
        for missing_metabolite in missing_metabolites_I:
            script+= missing_metabolite['rxn_id']+'\t'+missing_metabolite['equation']+'\t'+str(missing_metabolite['reactants_ids_tracked'])+'\t'+str(missing_metabolite['products_ids_tracked'])+'\t';
            for tracked_reactant in missing_metabolite['missing_reactants']:
                script+= tracked_reactant['met_id']+',';
            script+= '\t'
            for tracked_product in missing_metabolite['missing_products']:
                script+= tracked_product['met_id']+',';
            script+='\n'
        print script
    def find_inconsistentMetaboliteMappings(self,experiment_id_I,model_id_I=[],mapping_id_I=[]):
        '''Find inconsistencies in the atom mapping by comparing the metabolite information in
        atomMappingMetabolites table to the atom mapping in the atomMappingReactions table'''

        #Output:
        #   data_O = row of atomMappingReactions filled only with the inconsistent metabolite mapping information
        #   missing_mets_O = metabolites that are tracked in atomMappingReactions, but are not present in atomMappingMetabolites
        
        data_O = [];
        missing_mets_O = [];
        #get model ids:
        if model_id_I:
            model_ids = model_id_I;
        else:
            model_ids = [];
            model_ids = self.stage02_isotopomer_query.get_modelID_experimentID_dataStage02IsotopomerSimulation(experiment_id_I);
        for model_id in model_ids:
            print 'checking model_id ' + model_id;
            #get mapping ids
            if mapping_id_I:
                mapping_ids=mapping_id_I;
            else:
                mapping_ids=[];
                mapping_ids=self.stage02_isotopomer_query.get_mappingID_experimentIDAndModelID_dataStage02IsotopomerSimulation(experiment_id_I,model_id);
            for mapping_cnt,mapping_id in enumerate(mapping_ids):
                print 'checking mapping_id ' + mapping_id;
                # get the reaction mapping
                reaction_mappings = [];
                reaction_mappings = self.stage02_isotopomer_query.get_rows_mappingID_dataStage02IsotopomerAtomMappingReactions(mapping_id);
                for reaction_cnt,reaction_mapping in enumerate(reaction_mappings):
                    print 'checking reaction ' + reaction_mapping['rxn_id'];
                    #debug:
                    if reaction_mapping['rxn_id'] == 'COFACTOR_3':
                        print 'check';
                    #check reactants
                    rxn_tmp = {};
                    rxn_tmp['mapping_id']=mapping_id
                    rxn_tmp['rxn_id']=reaction_mapping['rxn_id']
                    rxn_tmp['rxn_description']=reaction_mapping['rxn_description']
                    rxn_tmp['reactants_stoichiometry_tracked']=[]
                    rxn_tmp['products_stoichiometry_tracked']=[]
                    rxn_tmp['reactants_ids_tracked']=[]
                    rxn_tmp['products_ids_tracked']=[]
                    rxn_tmp['reactants_elements_tracked']=[]
                    rxn_tmp['products_elements_tracked']=[]
                    rxn_tmp['reactants_positions_tracked']=[]
                    rxn_tmp['products_positions_tracked']=[]
                    rxn_tmp['reactants_mapping']=[]
                    rxn_tmp['products_mapping']=[]
                    rxn_tmp['rxn_equation']=None
                    rxn_tmp['used_']=True
                    rxn_tmp['comment_']='Inconsistent metabolites found';
                    rxn_tmp['reactants_metaboliteMappings']=[]
                    rxn_tmp['products_metaboliteMappings']=[]
                    bad_reactant = False;
                    for reactant_cnt,reactant in enumerate(reaction_mapping['reactants_ids_tracked']):
                        print 'checking reactant ' + reactant;
                        # get the metabolite mapping
                        metabolite_mapping = {};
                        metabolite_mapping = self.stage02_isotopomer_query.get_rows_mappingIDAndMetID_dataStage02IsotopomerAtomMappingMetabolites(mapping_id,reactant);
                        if not metabolite_mapping:
                            print 'metabolite mapping not found'
                            missing_mets_O.append(reactant);
                            continue;
                        # check the reaction mapping
                        reactants_mapping = reaction_mapping['reactants_mapping'][reactant_cnt];
                        if '[' in reaction_mapping['reactants_mapping'][reactant_cnt]:
                            reactants_mapping = reaction_mapping['reactants_mapping'][reactant_cnt].split('][');
                            reactants_mapping = [m.replace('[','') for m in reactants_mapping];
                            reactants_mapping = [m.replace(']','') for m in reactants_mapping];
                        if len(metabolite_mapping['met_atompositions']) != len(reactants_mapping):
                            rxn_tmp['reactants_metaboliteMappings'].append(reaction_mapping['reactants_mapping'][reactant_cnt]);
                            print 'bad reactants_metaboliteMappings';
                            bad_reactant = True;
                        # check the reaction elements tracked
                        if metabolite_mapping['met_atompositions'] != reaction_mapping['reactants_positions_tracked'][reactant_cnt]:
                            rxn_tmp['reactants_positions_tracked'].append(reaction_mapping['reactants_positions_tracked'][reactant_cnt]);
                            print 'bad reactants_positions_tracked';
                            bad_reactant = True;
                        # check the reaction positions tracked
                        if metabolite_mapping['met_elements'] != reaction_mapping['reactants_elements_tracked'][reactant_cnt]:
                            rxn_tmp['reactants_elements_tracked'].append(reaction_mapping['reactants_elements_tracked'][reactant_cnt]);
                            print 'bad reactants_elements_tracked';
                            bad_reactant = True;
                        if bad_reactant:
                            rxn_tmp['reactants_ids_tracked'].append(reactant);
                            rxn_tmp['reactants_stoichiometry_tracked'].append(reaction_mapping['reactants_stoichiometry_tracked'][reactant_cnt]);
                    #check products
                    bad_product = False;
                    for product_cnt,product in enumerate(reaction_mapping['products_ids_tracked']):
                        print 'checking product ' + product;
                        # get the metabolite mapping
                        metabolite_mapping = {};
                        metabolite_mapping = self.stage02_isotopomer_query.get_rows_mappingIDAndMetID_dataStage02IsotopomerAtomMappingMetabolites(mapping_id,product);
                        if not metabolite_mapping:
                            print 'metabolite mapping not found'
                            missing_mets_O.append(product);
                            continue;
                        # check the reaction mapping
                        products_mapping = reaction_mapping['products_mapping'][product_cnt];
                        if '[' in reaction_mapping['products_mapping'][product_cnt]:
                            products_mapping = reaction_mapping['products_mapping'][product_cnt].split('][');
                            products_mapping = [m.replace('[','') for m in products_mapping];
                            products_mapping = [m.replace(']','') for m in products_mapping];
                        if len(metabolite_mapping['met_atompositions']) != len(products_mapping):
                            rxn_tmp['products_metaboliteMappings'].append(reaction_mapping['products_mapping'][product_cnt]);
                            print 'bad products_metaboliteMappings';
                            bad_product = True;
                        # check the reaction elements tracked
                        if metabolite_mapping['met_atompositions'] != reaction_mapping['products_positions_tracked'][product_cnt]:
                            rxn_tmp['products_positions_tracked'].append(reaction_mapping['products_positions_tracked'][product_cnt]);
                            print 'bad products_positions_tracked';
                            bad_product = True;
                        # check the reaction positions tracked
                        if metabolite_mapping['met_elements'] != reaction_mapping['products_elements_tracked'][product_cnt]:
                            rxn_tmp['products_elements_tracked'].append(reaction_mapping['products_elements_tracked'][product_cnt]);
                            print 'bad products_elements_tracked';
                            bad_product = True;
                        if bad_product:
                            rxn_tmp['products_ids_tracked'].append(product);
                            rxn_tmp['products_stoichiometry_tracked'].append(reaction_mapping['products_stoichiometry_tracked'][product_cnt]);
                    #record
                    if bad_reactant or bad_product:
                        data_O.append(rxn_tmp);
        return data_O,missing_mets_O;
    def find_unbalancedReactionMappings(self,experiment_id_I,model_id_I=[],mapping_id_I=[]):
        '''Find reactions mappings that are not elementally balanced'''

        #Output:
        #   unbalanced_rxns_O = {rxn_id:{'n_products_elements_tracked':products_positions_tracked_cnt,
        #                                                'n_reactants_elements_tracked':reactants_positions_tracked_cnt},...}
        
        unbalanced_rxns_O = {};
        #get model ids:
        if model_id_I:
            model_ids = model_id_I;
        else:
            model_ids = [];
            model_ids = self.stage02_isotopomer_query.get_modelID_experimentID_dataStage02IsotopomerSimulation(experiment_id_I);
        for model_id in model_ids:
            print 'checking model_id ' + model_id;
            #get mapping ids
            if mapping_id_I:
                mapping_ids=mapping_id_I;
            else:
                mapping_ids=[];
                mapping_ids=self.stage02_isotopomer_query.get_mappingID_experimentIDAndModelID_dataStage02IsotopomerSimulation(experiment_id_I,model_id);
            for mapping_cnt,mapping_id in enumerate(mapping_ids):
                print 'checking mapping_id ' + mapping_id;
                # get the reaction mapping
                reaction_mappings = [];
                reaction_mappings = self.stage02_isotopomer_query.get_rows_mappingID_dataStage02IsotopomerAtomMappingReactions(mapping_id);
                for reaction_cnt,reaction_mapping in enumerate(reaction_mappings):
                    print 'checking reaction ' + reaction_mapping['rxn_id'];
                    #check reactants
                    reactants_positions_tracked_cnt = 0;
                    for reactant_cnt,reactant in enumerate(reaction_mapping['reactants_ids_tracked']):
                        print 'checking reactant ' + reactant;
                        # check that the reactant positions == reactant elements
                        if len(reaction_mapping['reactants_positions_tracked'][reactant_cnt])!=len(reaction_mapping['reactants_elements_tracked'][reactant_cnt]):
                            print 'inconsistent reactants_positions and reactants_elements';
                            continue;
                        reactants_positions_tracked_cnt += len(reaction_mapping['reactants_positions_tracked'][reactant_cnt]);
                    #check products
                    products_positions_tracked_cnt = 0;
                    for product_cnt,product in enumerate(reaction_mapping['products_ids_tracked']):
                        print 'checking product ' + product;
                        # check that the product positions == product elements
                        if len(reaction_mapping['products_positions_tracked'][product_cnt])!=len(reaction_mapping['products_elements_tracked'][product_cnt]):
                            print 'inconsistent products_positions and products_elements';
                            continue;
                        products_positions_tracked_cnt += len(reaction_mapping['products_positions_tracked'][product_cnt]);
                    #record
                    if reactants_positions_tracked_cnt!=products_positions_tracked_cnt:
                        unbalanced_rxns_O[reaction_mapping['rxn_id']] = {'n_products_elements_tracked':products_positions_tracked_cnt,
                                                           'n_reactants_elements_tracked':reactants_positions_tracked_cnt};
                        #unbalanced_rxns_O.append(reaction_mapping);

        return unbalanced_rxns_O;
    def find_inconsistentReactionMappings(self,experiment_id_I,model_id_I=[],mapping_id_I=[]):
        '''Find inconsistencies in the reaction mapping'''

        #Output:
        #   unbalanced_rxns_O = {rxn_id:{'n_products_elements_tracked':products_positions_tracked_cnt,
        #                                                'n_reactants_elements_tracked':reactants_positions_tracked_cnt},...}
        
        irm = stage02_isotopomer_reactionMapping();
        #get model ids:
        if model_id_I:
            model_ids = model_id_I;
        else:
            model_ids = [];
            model_ids = self.stage02_isotopomer_query.get_modelID_experimentID_dataStage02IsotopomerSimulation(experiment_id_I);
        for model_id in model_ids:
            print 'checking model_id ' + model_id;
            #get mapping ids
            if mapping_id_I:
                mapping_ids=mapping_id_I;
            else:
                mapping_ids=[];
                mapping_ids=self.stage02_isotopomer_query.get_mappingID_experimentIDAndModelID_dataStage02IsotopomerSimulation(experiment_id_I,model_id);
            for mapping_cnt,mapping_id in enumerate(mapping_ids):
                print 'checking mapping_id ' + mapping_id;
                # get the reaction ids
                reaction_ids = [];
                reaction_ids = self.stage02_isotopomer_query.get_rxnIDs_mappingID_dataStage02IsotopomerAtomMappingReactions(mapping_id);
                for reaction_cnt,reaction_id in enumerate(reaction_ids):
                    print 'checking reaction ' + reaction_id;
                    #check each reaction
                    irm.get_reactionMapping(mapping_id,reaction_id);
                    reactants_ids_stoichiometry_check,reactants_elements_positions_check,reactants_elements_mapping_check,reactants_positions_mapping_check,\
                        products_ids_stoichiometry_check,products_elements_positions_check,products_elements_mapping_check,products_positions_mapping_check,\
                        element_balance_check,mapping_check = irm.check_reactionMapping();
                    #clear reaction
                    irm.clear_reactionMapping();

'''Unit tests for stage02_isotopomer_metaboliteMapping:
from analysis.analysis_stage02_isotopomer.stage02_isotopomer_dependencies import stage02_isotopomer_metaboliteMapping
imm = stage02_isotopomer_metaboliteMapping()
imm.make_trackedMetabolite('full04','140407_iDM2014',{'f6p_c':'C'})
imm.clear_metaboliteMapping()
imm.make_compoundTrackedMetabolite('full04','140407_iDM2014',[{'f6p_c':'C'},{'f6p_c':'H'},{'f6p_c':'C'},{'f6p_c':'H'},{'ac_c':'C'},{'utp_c':'C'}],'uacgam_c')
imm.remove_baseMetabolite_fromMetabolite('140407_iDM2014',{'f6p_c':'C'})
imm.clear_metaboliteMapping()
imm.make_compoundTrackedMetabolite('full04','140407_iDM2014',[{'f6p_c':'C'},{'f6p_c':'H'},{'f6p_c':'C'},{'f6p_c':'H'},{'ac_c':'C'},{'utp_c':'C'}],'uacgam_c')
imm.remove_baseMetabolite_fromMetabolite('140407_iDM2014',{'f6p_c':'C'},met_index_I=2)
imm.clear_metaboliteMapping()
imm.make_compoundTrackedMetabolite('full04','140407_iDM2014',[{'f6p_c':'C'},{'f6p_c':'H'},{'f6p_c':'C'},{'f6p_c':'H'},{'ac_c':'C'},{'utp_c':'C'}],'uacgam_c')
imm.pop_baseMetabolite_fromMetabolite('140407_iDM2014',{'f6p_c':'C'})
imm.clear_metaboliteMapping()
imm.make_compoundTrackedMetabolite('full04','140407_iDM2014',[{'f6p_c':'C'},{'f6p_c':'H'},{'f6p_c':'C'},{'f6p_c':'H'},{'ac_c':'C'},{'utp_c':'C'}],'uacgam_c')
extracted_imm = imm.extract_baseMetabolite_fromMetabolite('140407_iDM2014',{'f6p_c':'C'},met_index_I=2)
imm.clear_metaboliteMapping()
'''

'''Unit tests for stage02_isotopomer_reactionMapping:
from analysis.analysis_stage02_isotopomer.stage02_isotopomer_dependencies import stage02_isotopomer_reactionMapping
irm = stage02_isotopomer_reactionMapping()
irm.make_trackedBinaryReaction('full04','140407_iDM2014','COFACTOR_7',[{'dxyl5p_c':'C'}],'h2mb4p_c')
irm.clear_reactionMapping()
irm.make_trackedBinaryReaction('full04','140407_iDM2014','COFACTOR_7',[{'dxyl5p_c':'C'},{'dxyl5p_c':'C'}],'h2mb4p_c')
irm.clear_reactionMapping()
irm.make_trackedUnitaryReactions('full04','140407_iDM2014','COFACTOR_7',[{'dxyl5p_c':'C'}],['h2mb4p_c'])
irm.clear_reactionMapping()
irm.make_trackedUnitaryReactions('full04','140407_iDM2014','COFACTOR_7',[{'dxyl5p_c':'C'},{'dxyl5p_c':'C'}],['h2mb4p_c','h2mb4p_c'])
irm.clear_reactionMapping()
'''