#dependencies
import csv
import re
from math import sqrt
import json

#classes
class convert_ids():
    """Class for converting ids from COBRA model to Isotopomer model"""

    def __init__(self,metmap_filename_I=None,ctrack_filename_I=None):

        if metmap_filename_I: self.metmap = self._get_metmap_csv(metmap_filename_I);
        else: print('no metmap mapping provided')
        
        if ctrack_filename_I: self.ctrack = self._get_ctrack_csv(ctrack_filename_I);
        else: print('no ctrack mapping provided')
        
        self.ctrack_converted = [];

    def _get_metmap_csv(self, metmap_filename_I):
        #Read in the metmap mapping
        
        metmap = {};
        with open(metmap_filename_I,mode='r') as infile:
            reader = csv.reader(infile);
            for i,r in enumerate(reader):
                if not(i==0):
                    id = 'x' + r[0];
                    metmap[id] = 'x' + r[1];
        return metmap

    def _get_ctrack_csv(self,ctrack_filename_I):
        #Read in ctrack file
        
        ctrack = [];
        with open(ctrack_filename_I,mode='r') as infile:
            reader = csv.reader(infile);
            for i,r in enumerate(reader):
                # will need to split white spaces if each entry is not in an individual cell
                row = [];
                for c in r:
                    row.append(c);
                ctrack.append(row);
        return ctrack

    def convert_ctrack(self):
        # convert ctrack to ctrack_converted using metmap

        for i,r in enumerate(self.ctrack):
            row = [];
            # will need to recombine cells by a white space if that format is desired
            for c in r:
                if c in self.metmap.keys():
                    row.append(self.metmap[c]);
                else:
                    row.append(c);
            self.ctrack_converted.append(row);

    def write_ctrack_converted(self,ctrack_converted_filename_I):
        #write _ctrack_converted to file

        with open(ctrack_converted_filename_I,mode='wb') as outfile:
            writer = csv.writer(outfile);
            writer.writerows(self.ctrack_converted);

#functions
def build_isotopomer_str(isotopomer_mapping_I):
    '''build isotopomer string'''
    # Input:
    #   isotopomer_mapping_I = {rxn_id:{'ctrack':'','mapping':['',''],'notes':''}}
    # Output:
    #   isotopomer_str_O = {rxn_id: 'rxn_id ctrack!mapping1!mapping2...'}

    isotopomer_str_O = {};
    for k,v in isotopomer_mapping_I.iteritems():
        str = '';
        if v['ctrack'].rstrip()!='':
            str = k + ' ' + v['ctrack'];
        for m in v['mapping']:
            if m!='': str = str + '!' + m;
        isotopomer_str_O[k] = str;

    return isotopomer_str_O;

def read_isotopomer_mapping_csv(filename_I):
    #Read in the isotopomer mappings
    # Output:
    # isotopomer_mapping = {
    #    'ptrc_to_4abut_1':{'ctrack':'1 xakg_c 1 xptrc_c > 1 x4abut_c 1 xglu_DASH_L_c',
    #                       'mapping':['#abcde #fghi > #fghi #abcde','#abcde #ihgf > #fghi #abcde'],
    #                       'notes':'combo'}};
        
    isotopomer_mapping = {};
    with open(filename_I,mode='r') as infile:
        reader = csv.DictReader(infile);
        for r in reader:
            mapping = r['mapping'].split(',');
            isotopomer_mapping[r['rxn_id']] = {'ctrack':r['ctrack'],'mapping':mapping,'notes':r['notes']};
    return isotopomer_mapping

#dictionary variables

isotopomer_rxns_net = {
        'ptrc_to_4abut_1':{'reactions':['PTRCTA','ABUTD'],
                           'stoichiometry':[1,1]},
        'ptrc_to_4abut_2':{'reactions':['GGPTRCS','GGPTRCO','GGGABADr','GGGABAH'],
                           'stoichiometry':[1,1,1,1]},
        'glu_DASH_L_to_acg5p':{'reactions':['ACGS','ACGK'],
                           'stoichiometry':[1,1]},
        '2obut_and_pyr_to_3mop':{'reactions':['ACHBS','KARA2','DHAD2'],
                           'stoichiometry':[1,1,1]},
        'pyr_to_23dhmb':{'reactions':['ACLS','KARA1'],
                           'stoichiometry':[1,-1]},
        #'met_DASH_L_and_ptrc_to_spmd_and_5mta':{'reactions':['METAT','ADMDC','SPMS'],
        #                   'stoichiometry':[1,1,1]}, #cannot be lumped
        'chor_and_prpp_to_3ig3p':{'reactions':['ANS','ANPRT','PRAIi','IGPS'],
                           'stoichiometry':[1,1,1,1]},
        'hom_DASH_L_and_cyst_DASH_L_to_pyr_hcys_DASH_L':{'reactions':['HSST','SHSL1','CYSTL'],
                           'stoichiometry':[1,1,1]}, #cannot be lumpped
        'e4p_and_pep_to_3dhq':{'reactions':['DDPA','DHQS'],
                           'stoichiometry':[1,1]},
        'aspsa_to_sl2a6o':{'reactions':['DHDPS','DHDPRy','THDPS'],
                           'stoichiometry':[1,1,1]},
        'glu_DASH_L_to_glu5sa':{'reactions':['GLU5K','G5SD'],
                           'stoichiometry':[1,1]},
        'g1p_to_glycogen':{'reactions':['GLGC','GLCS1'],
                           'stoichiometry':[1,1]},
        'thr_DASH_L_to_gly':{'reactions':['THRD','GLYAT'],
                           'stoichiometry':[1,-1]},
        'dhap_to_lac_DASH_D':{'reactions':['MGSA','LGTHL','GLYOX'],
                           'stoichiometry':[1,1,1]},
        'hom_DASH_L_to_thr_DASH_L':{'reactions':['HSK','THRS'],
                           'stoichiometry':[1,1]},
        '3pg_to_ser_DASH_L':{'reactions':['PGCD','PSERT','PSP_L'],
                           'stoichiometry':[1,1,1]},
        'prpp_to_his_DASH_L':{'reactions':['ATPPRT','PRATPP','PRAMPC','PRMICI','IG3PS','IGPDH','HSTPT','HISTP','HISTD'],
                           'stoichiometry':[1,1,1,1,1,1,1,1,1]},
        'UMPSYN_aerobic':{'reactions':['ASPCT','DHORTS','DHORD2','ORPT','OMPDC'],
                           'stoichiometry':[1,-1,1,-1,1]},
        #'UMPSYN_anaerobic':{'reactions':['ASPCT','DHORTS','DHORD5','ORPT','OMPDC'],
        #                   'stoichiometry':[1,-1,1,-1,1]},
        #'IMPSYN1':{'reactions':['GLUPRT','PRAGSr','GARFT','PRFGS','PRAIS','AIRC2','AIRC3','PRASCSi','ADSL2r','AICART','IMPC'],
        #                   'stoichiometry':[1,1,1,1,1,1,-1,1,1,1,-1]}, #cannot be lumped
        #'IMPSYN2':{'reactions':['GLUPRT','PRAGSr','GART','PRFGS','PRAIS','AIRC2','AIRC3','PRASCSi','ADSL2r','AICART','IMPC'],
        #                   'stoichiometry':[1,1,1,1,1,1,-1,1,1,1,-1]}, #cannot be lumped
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
        'FADSYN_1':{'reactions':['GTPCII2','DHPPDA2','APRAUR','PMDPHT','DB4PS'],
                           'stoichiometry':[1,1,1,1,1]},
        'FADSYN_2':{'reactions':['RBFSa','RBFSb'],
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
        #'GTHSYN':{'reactions':['GLUCYS','GTHS'],
        #                   'stoichiometry':[1,1]},
        };

isotopomer_rxns_net_irreversible = {
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

# List variables:
isotopomer_alternateCarbon_noFlux = ['5DGLCNR','ACM6PH','ADNUC','AGDC','ALDD19xr','ALLPI','ALLULPE','AMANAPEr','ARAI','DDPGALA','DHACOAH',
                                     'DRPA','FCI','FCLPA','FORCT','FRULYSDG','FRULYSE','GLTPD','GUI1','GUI2','HADPCOADH3','IDOND','IDOND2',
                                     'PPM2','REPHACCOAI','RMI','RMPA','SBTPD','TAGURr','TGBPA','5DGLCNR_reverse','ALDD19xr_reverse','ALLPI_reverse',
                                     'ALLULPE_reverse','AMANAPEr_reverse','ARAI_reverse','DDPGALA_reverse','DHACOAH_reverse','FCI_reverse','FCLPA_reverse',
                                     'FORCT_reverse','FRULYSDG_reverse','FRULYSE_reverse','GLTPD_reverse','GUI1_reverse','GUI2_reverse','HADPCOADH3_reverse',
                                     'IDOND_reverse','PPM2_reverse','REPHACCOAI_reverse','RMI_reverse','RMPA_reverse','SBTPD_reverse','TAGURr_reverse','TGBPA_reverse'];

isotopomer_rxns_2_map = ['ptrc_to_4abut_1','ptrc_to_4abut_2','glu_DASH_L_to_acg5p','2obut_and_pyr_to_3mop','pyr_to_23dhmb','METAT','ADMDC','SPMS','MTAN','5MTRtpp',
                         '5MTRtex_reverse','EX_5mtr_LPAREN_e_RPAREN_','chor_and_prpp_to_3ig3p','hom_DASH_L_and_cyst_DASH_L_to_pyr_hcys_DASH_L','METS','e4p_and_pep_to_3dhq',
                         'aspsa_to_sl2a6o','glu_DASH_L_to_glu5sa','g1p_to_glycogen','thre_DASH_L_to_gly','dhap_to_lac_DASH_D','hom_DASH_L_to_thr_DASH_L','3pg_to_ser_DASH_L',
                         'prpp_to_his_DASH_L','UMPSYN_aerobic','IMPSYN_1','PRAGSr_reverse','GARFT','GART','IMPSYN_2','IMPSYN_3','imp_to_gmp','imp_to_amp','udp_to_dump_aerobic',
                         'TMDS','DTMPK','NDPK4','COASYN','FADSYN_1','FADSYN_2','FADSYN_3','NADSYN_aerobic','NADPPPS','NADN','NNAM','NAMNPP','NMNN','NMNDA','NMNAT',
                         'NADDP','ADPRDP','THFSYN','DHFR','DHFR_reverse','GCALDD','GTHSYN','EX_ac_LPAREN_e_RPAREN_','EX_co2_LPAREN_e_RPAREN_','EX_etoh_LPAREN_e_RPAREN_',
                         'EX_for_LPAREN_e_RPAREN_','EX_fum_LPAREN_e_RPAREN_','EX_glc_LPAREN_e_RPAREN_','EX_glyc_LPAREN_e_RPAREN_','EX_lac_DASH_D_LPAREN_e_RPAREN_',
                         'EX_lac_DASH_L_LPAREN_e_RPAREN_','EX_pyr_LPAREN_e_RPAREN_','EX_succ_LPAREN_e_RPAREN_','EX_co_LPAREN_e_RPAREN_','cotpp','cotex','cotpp_reverse',
                         'cotex_reverse','ABTA','ACKr','ACODA','ACONTa','ACONTb','ACOTA','ACS','ACt2rpp','ACtex','ALCD2x','ACALD_reverse','ALCD2x_reverse','ACALD',
                         'AGPR','ALAR','ALATA_L','ALDD2x','ARGSL','ARGSS','ASAD','ASNN','ASNS1','ASNS2','ASPK','ASPTA','CBPS','CHORM','CHORS','CO2tex','CO2tex_reverse',
                         'CO2tpp','CO2tpp_reverse','CS','CYSDS','CYSS','D_DASH_LACt2pp','D_DASH_LACtex','DAPDC','DAPE','DHAD1','DHQTi','EDA','EDD','ENO','ETOHtex',
                         'ETOHtrpp','F6PA','FBA','FBP','FDH2','FDH3','Htex','FHL','FORt2pp','FORtex','FRD2','FRD3','FTHFD','FUM','FUMt2_2pp','FUMt2_3pp','FUMtex','G1PPpp',
                         'G3PD2','G3PD5','G3PD6','G3PD7','G5SADs','G6PDH2r','GAPD','GHMT2r','GLCP','GLCptspp','GLNS','GLUDC','GLUDy','GLUN','GLUSy','GLXCL','GLYCK',
                         'GLYCL','GLYCLTDx','GLYCLTDy','GLYCTO2','GLYCTO3','GLYCTO4','GLYCtex','GLYCtpp','GLYK','GND','HCO3E','HEX1','HSDy','ICDHyr','ICL','ILETA','IPMD',
                         'IPPMIa','IPPMIb','IPPS','L_DASH_LACD2','L_DASH_LACD3','L_DASH_LACt2rpp','L_DASH_LACtex','LDH_D','LDH_D2','LEUTAi','MALS','MDH','MDH2','MDH3','ME1',
                         'ME2','MTHFC','MTHFD','MTHFR2','NACODA','OCBT','OMCDC','ORNDC','P5CD','P5CR','PDH','PFK','PFL','PGI','PGK','PGL','PGM','PGMT','PHETA1','POX','PPC',
                         'PPCK','PPND','PPNDH','PPS','PROD2','PRPPS','PSCVT','PTAr','PYK','PYRt2rpp','PYRt2rpp_reverse','PYRtex','PYRtex_reverse','RPE','RPI','SDPDS','SDPTA',
                         'SERAT','SERD_L','SHK3Dr','SHKK','SSALx','SSALy','SUCASPtpp','SUCCt2_2pp','SUCCt2_3pp','SUCCt3pp','SUCDi','SUCFUMtpp','SUCCtex','SUCOAS','TALA','AKGDH',
                         'THRAi','THRD_L','TKT1','TKT2','TPI','TRPAS2','TRPS1','TRPS2','TRPS3','TRSARr','TYRTA','VALTA','G3PT','ACKr_reverse','ACONTa_reverse','ACONTb_reverse',
                         'ACOTA_reverse','ACt2rpp_reverse','Actex_reverse','AGPR_reverse','ALAR_reverse','ALATA_L_reverse','ARGSL_reverse','ASAD_reverse','ASPK_reverse',
                         'ASPTA_reverse','D_DASH_LACt2pp_reverse','D_DASH_LACtex_reverse','DAPE_reverse','DHQTi_reverse','ENO_reverse','ETOHtex_reverse','ETOHtrpp_reverse',
                         'FBA_reverse','FORt2pp_reverse','FORtex_reverse','FUM_reverse','G3PD2_reverse','G6PDH2r_reverse','GAPD_reverse','GLUDy_reverse',
                         'GLYCtex_reverse','GLYCtpp_reverse','HCO3E_reverse','HSDy_reverse','ICDHyr_reverse','ILETA_reverse','IPPMIa_reverse','IPPMIb_reverse',
                         'L_DASH_LACt2rpp_reverse','L_DASH_LACtex_reverse','LDH_D_reverse','MDH_reverse','MTHFC_reverse','MTHFD_reverse','OCBT_reverse','PGI_reverse',
                         'PGK_reverse','PGM_reverse','PGMT_reverse','PHETA1_reverse','PRPPS_reverse','PSCVT_reverse','PTAr_reverse','RPE_reverse','RPI_reverse',
                         'SDPTA_reverse','SERAT_reverse','SHK3Dr_reverse','SUCFUMtpp_reverse','SUCCtex_reverse','SUCOAS_reverse','TALA_reverse','THRA2i','TKT1_reverse',
                         'TKT2_reverse','TPI_reverse','TRPAS2_reverse','TYRTA_reverse','VALTA_reverse','GHMT2r_reverse','CYTK1','NDPK2','NDPK3','UMPK','GK1','NDPK1',
                         'ADK1','ADK3','NTPP6','ATPS4rpp','CTPS2','GTHOr','GTHOr_reverse','GALUi','DXPS','ICHORSi','ICYSDS','CHRPL','ICHORT','ACCOAC','KAS15','MCOATA',
                         'CLPNS160pp','CLPNS161pp','CLPNS181pp','PG160abcpp','PG161abcpp','PG181abcpp','PE160abcpp','PE161abcpp','PE181abcpp','GLYCPHOSPHOLIPID_1',
                         'GLYCPHOSPHOLIPID_2','GLYCPHOSPHOLIPID_3','GLYCPHOSPHOLIPID_4','GLYCPHOSPHOLIPID_5','GLYCPHOSPHOLIPID_6','GLYCPHOSPHOLIPID_7',
                         'GLYCPHOSPHOLIPID_8','GLYCPHOSPHOLIPID_9','MOLYBDOPTERIN_1','MOLYBDOPTERIN_2','MOLYBDOPTERIN_3','COFACTOR_1','COFACTOR_2','COFACTOR_3',
                         'VITB6','THIAMIN','COFACTOR_4','COFACTOR_5','COFACTOR_6','COFACTOR_7','COFACTOR_8','COFACTOR_9','COFACTOR_10','COFACTOR_11','CELLENV_1',
                         'CELLENV_2','CELLENV_3','CELLENV_4','CELLENV_5','CELLENV_6','CELLENV_7','CELLENV_8','CELLENV_9','CELLENV_10','CELLENV_11','LIPOPOLYSACCHARIDE_1',
                         'LIPOPOLYSACCHARIDE_2','LIPOPOLYSACCHARIDE_3','LIPOPOLYSACCHARIDE_4','A5PISO','A5PISO_reverse','PPM','PPM_reverse','A5PISO','ACCOAL','ALCD19',
                         'ALDD2y','CYTDH','F6PP','G6PDA','GALKr','GLCATr','HEX4','HEX7','HPYRI','HPYRRx','HPYRRy','LCADi','LCARS','M1PD','MALTATr','MAN6PI','MANAO','MCITD',
                         'MCITL2','MCITS','MICITDr','MLTG3','MLTG4','MLTG5','MLTP1','MLTP2','MLTP3','MMCD','MMM','MN6PP','OBTFL','PMANM','PPAKr','PPCSCT','PPM','PTA2',
                         'R15BPK','R1PK','R5PP','RBK','RBP4E','TRE6PH','TRE6PP','TRE6PS','TREH','UDPG4E','UGLT','URIH','XYLI1','XYLI2','A5PISO_reverse','ALCD19_reverse',
                         'GALKr_reverse','GLCATr_reverse','HPYRI_reverse','LCARS_reverse','M1PD_reverse','MALTATr_reverse','MAN6PI_reverse','MANAO_reverse',
                         'MCITL2_reverse','MICITDr_reverse','MLTP1_reverse','MLTP2_reverse','MLTP3_reverse','PMANM_reverse','PPAKr_reverse','PPM_reverse',
                         'RBP4E_reverse','TRSARr_reverse','UDPG4E_reverse','UGLT_reverse','XYLI1_reverse','XYLI2_reverse','PUNP1','PUNP3','PUNP5','PUNP7',
                         'PYNP2r','UPPRT','XPPT','PUNP1_reverse','PUNP3_reverse','PUNP5_reverse','PUNP7_reverse','PYNP2r_reverse','ADPT','GUAPRT','HXPRT'];

CTracked = ['EX_ac', 'EX_co2', 'EX_etoh', 'EX_for', 'EX_fum', 'EX_glc',
            'EX_glyc', 'EX_lacD', 'EX_lacL', 'EX_pyr', 'EX_succ', 'ABTA',
            'ACALDi', 'ACKr', 'ACODA', 'rACONT', 'ACOTA', 'ACS', 'ACt2r',
            'ADHEr', 'AGPR', 'ALAR', 'ALATAL', 'ALDD2x', 'ARGSL', 'ARGSS',
            'ASAD', 'ASNN', 'ASNS1', 'ASNS2', 'ASPK', 'ASPTA', 'CBPS', 'CHORM',
            'CHORS', 'CO2t', 'CS', 'CYSDS', 'CYSS', 'DLACt2', 'DAPDC', 'DAPE',
            'DHAD1', 'DHAPT', 'DHQD', 'DKMPPD', 'DKMPPD2', 'EDA', 'EDD', 'ENO',
            'ETOHt2r', 'F6PA', 'FBA', 'FBP', 'FDH2', 'FDH3', 'FHL', 'FORt', 'FRD2',
            'FRD3', 'FTHFD', 'rFUM', 'FUMt22', 'FUMt23', 'G1PP', 'G3PD2', 'G3PD5',
            'G3PD6', 'G3PD7', 'G5SADs', 'G6PDH2r', 'GAPD', 'GHMT2', 'GLCP', 'GLCpts',
            'GLNS', 'GLUDC', 'GLUDy', 'GLUN', 'GLUSy', 'GLXCL', 'GLYCDx', 'GLYCK',
            'GLYCL', 'GLYCLTDx', 'GLYCLTDy', 'GLYCTO2', 'GLYCTO3', 'GLYCTO4', 'GLYCt',
            'GLYK', 'GMPS2', 'GND', 'HCO3E', 'HEX1', 'HSDy', 'ICDHyr', 'ICL', 'ILETA',
            'IPMD', 'IPPMIa', 'IPPMIb', 'IPPS', 'LLACD2', 'LLACD3', 'LLACt2r', 'LDHD',
            'LDHD2', 'LEUTAi', 'MALS', 'MDH', 'MDH2', 'MDH3', 'ME1', 'ME2', 'MTHFC',
            'MTHFD', 'MTHFR2', 'NACODA', 'OCBT', 'OMCDC', 'ORNDC', 'P5CD', 'P5CR',
            'PDH', 'PFK', 'PFL', 'PGI', 'PGK', 'PGL', 'PGM', 'PGMT', 'PHETA1', 'POX',
            'PPC', 'PPCK', 'PPND', 'PPNDH', 'PPS', 'PROD2', 'PRPPS', 'PSCVT', 'PTAr',
            'PYK', 'PYRt2r', 'RPE', 'RPI', 'SDPDS', 'SDPTA', 'SERAT', 'SERDL',
            'SHK3Dr', 'SHKK', 'SSALx', 'SSALy', 'SUCCabc', 'SUCCt22', 'SUCCt23',
            'SUCCt2b', 'SUCD1i', 'SUCFUMt', 'SUCOAS', 'TALA', 'TESTAKGDH',
            'THRAr', 'THRDL', 'TKT1', 'TKT2', 'TPI', 'TRPAS2', 'TRPS1', 'TRPS2',
            'TRPS3', 'TRSAR', 'TYRTA', 'UNK3', 'VALTA', 'G3PP', 'ACKr_r', 'rACONT_r',
            'ACOTA_r', 'ACt2r_r', 'ADHEr_r', 'AGPR_r', 'ALAR_r', 'ALATAL_r', 'ARGSL_r',
            'ASAD_r', 'ASPK_r', 'ASPTA_r', 'CO2t_r', 'DLACt2_r', 'DAPE_r', 'DHQD_r',
            'ENO_r', 'ETOHt2r_r', 'F6PA_r', 'FBA_r', 'FORt_r', 'rFUM_r', 'G3PD2_r',
            'G6PDH2r_r', 'GAPD_r', 'GLUDy_r', 'GLYCt_r', 'HCO3E_r', 'HSDy_r',
            'ICDHyr_r', 'ILETA_r', 'IPPMIa_r', 'IPPMIb_r', 'LLACt2r_r', 'LDHD_r',
            'MDH_r', 'MTHFC_r', 'MTHFD_r', 'OCBT_r', 'PGI_r', 'PGK_r', 'PGM_r',
            'PGMT_r', 'PHETA1_r', 'PRPPS_r', 'PSCVT_r', 'PTAr_r', 'PYRt2r_r',
            'RPE_r', 'RPI_r', 'SDPTA_r', 'SERAT_r', 'SHK3Dr_r', 'SUCFUMt_r',
            'SUCOAS_r', 'TALA_r', 'THRAr_r', 'TKT1_r', 'TKT2_r', 'TPI_r',
            'TRPAS2_r', 'TYRTA_r', 'VALTA_r', 'GHMT2_r'];
