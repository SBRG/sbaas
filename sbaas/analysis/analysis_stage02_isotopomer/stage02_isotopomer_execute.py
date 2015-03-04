'''isotopomer metabolomics analysis class'''

from analysis.analysis_base import *
from analysis.analysis_base.base_exportData import base_exportData
from stage02_isotopomer_query import *
from stage02_isotopomer_io import *
from stage02_isotopomer_dependencies import *
import re
from math import sqrt

class stage02_isotopomer_execute():
    '''class for isotopomer metabolomics analysis'''
    def __init__(self):
        self.session = Session();
        self.stage02_isotopomer_query = stage02_isotopomer_query();
        self.calculate = base_calculate();
        self.models = {};
        #modified biomass (INCA does not like exponential terms)
        self.biomass_INCA_iJS2012 = '0.488*ala_DASH_L_c + 0.0004*nadph_c + 0.176*phe_DASH_L_c + 0.582*gly_c + 0.00013*nadp_c + 0.276*ile_DASH_L_c + 0.21*pro_DASH_L_c + 0.25*glu_DASH_L_c + 0.154*glycogen_c + 45.73*atp_c + 0.139*utp_c + 0.00645*clpnEC_e + 0.131*tyr_DASH_L_c + 0.203*gtp_c + 0.00005*nadh_c + 0.0000006*coa_c + 0.00215*nad_c + 0.326*lys_DASH_L_c + 0.25*gln_DASH_L_c + 0.000003*succoa_c + 45.56*h2o_c + 0.205*ser_DASH_L_c + 0.126*ctp_c + 0.001*amp_c + 0.09675*peEC_e + 0.054*trp_DASH_L_c + 0.09*his_DASH_L_c + 0.0276*peptidoEC_e + 0.087*cys_DASH_L_c + 0.0084*lpsEC_e + 0.0247*datp_c + 0.0247*dttp_c + 0.241*thr_DASH_L_c + 0.281*arg_DASH_L_c + 0.00005*accoa_c + 0.402*val_DASH_L_c + 0.007*spmd_c + 0.0254*dgtp_c + 0.0232*pgEC_e + 0.146*met_DASH_L_c + 0.035*ptrc_c + 0.0254*dctp_c + 0.428*leu_DASH_L_c + 0.05*5mthf_c + 0.229*asp_DASH_L_c + 0.229*asn_DASH_L_c + 0.003*g1p_c + 0.0026*psEC_e + 0.00001*fad_c -> 45.56*pi_c + 45.56*h_c + 45.56*adp_c + 0.7332*ppi_c';
        self.biomass_INCA_iJS2012_v1 = '0.488*ala_DASH_L_c (C1:d C2:e C3:f) + 0.0004*nadph_c + 0.176*phe_DASH_L_c (C1:p C2:q C3:r C4:s C5:t C6:u C7:v C8:w C9:x) + 0.582*gly_c (C1:N C2:O) + 0.00013*nadp_c + 0.276*ile_DASH_L_c (C1:2 C2:3 C3:4 C4:5 C5:6 C6:7) + 0.21*pro_DASH_L_c (C1:y C2:z C3:A C4:B C5:C) + 0.25*glu_DASH_L_c (C1:I C2:J C3:K C4:L C5:M) + 0.154*glycogen_c (C1:P C2:Q C3:R C4:S C5:T C6:U) + 45.7318*atp_c + 0.139*utp_c + 0.00645*clpnEC_e + 0.131*tyr_DASH_L_c (C1:b C2:c C3:d C4:e C5:f C6:g C7:h C8:i C9:j) + 0.203*gtp_c + 0.00005*nadh_c + 0.000006*coa_c + 0.00215*nad_c + 0.326*lys_DASH_L_c (C1:e C2:f C3:g C4:h C5:i C6:j) + 0.25*gln_DASH_L_c (C1:D C2:E C3:F C4:G C5:H) + 0.000003*succoa_c (C1:R C2:S C3:T C4:U) + 45.5608*h2o_c + 0.205*ser_DASH_L_c (C1:H C2:I C3:J) + 0.126*ctp_c + 0.001*amp_c + 0.09675*peEC_e + 0.054*trp_DASH_L_c (C1:Z C2:1 C3:2 C4:3 C5:4 C6:5 C7:6 C8:7 C9:8 C10:9 C11:a) + 0.09*his_DASH_L_c (C1:V C2:W C3:X C4:Y C5:Z C6:1) + 0.0276*peptidoEC_e + 0.087*cys_DASH_L_c (C1:u C2:v C3:w) + 0.0084*lpsEC_e + 0.0247*datp_c + 0.0247*dttp_c + 0.241*thr_DASH_L_c (C1:V C2:W C3:X C4:Y) + 0.281*arg_DASH_L_c (C1:g C2:h C3:i C4:j C5:k C6:l) + 0.00005*accoa_c (C1:b C2:c) + 0.402*val_DASH_L_c (C1:k C2:l C3:m C4:n C5:o) + 0.007*spmd_c (C1:K C2:L C3:M C4:N C5:O C6:P C7:Q) + 0.0254*dgtp_c + 0.0232*pgEC_e + 0.146*met_DASH_L_c (C1:k C2:l C3:m C4:n C5:o) + 0.035*ptrc_c (C1:D C2:E C3:F C4:G) + 0.0254*dctp_c + 0.428*leu_DASH_L_c (C1:8 C2:9 C3:a C4:b C5:c C6:d) + 0.05*5mthf_c (C1:a) + 0.229*asp_DASH_L_c (C1:q C2:r C3:s C4:t) + 0.229*asn_DASH_L_c (C1:m C2:n C3:o C4:p) + 0.003*g1p_c (C1:x C2:y C3:z C4:A C5:B C6:C) + 0.0026*psEC_e + 0.00001*fad_c -> 45.5628*pi_c + 45.55735*h_c + 45.5608*adp_c + 0.7332*ppi_c ';
        self.biomass_INCA_iJS2012_v2 = '0.488*ala_DASH_L_c (C1:ala_DASH_L_cd C2:ala_DASH_L_ce C3:ala_DASH_L_cf) + 0.0004*nadph_c + 0.176*phe_DASH_L_c (C1:phe_DASH_L_cp C2:phe_DASH_L_cq C3:phe_DASH_L_cr C4:phe_DASH_L_cs C5:phe_DASH_L_ct C6:phe_DASH_L_cu C7:phe_DASH_L_cv C8:phe_DASH_L_cw C9:phe_DASH_L_cx) + 0.582*gly_c (C1:gly_cN C2:gly_cO) + 0.00013*nadp_c + 0.276*ile_DASH_L_c (C1:ile_DASH_L_c2 C2:ile_DASH_L_c3 C3:ile_DASH_L_c4 C4:ile_DASH_L_c5 C5:ile_DASH_L_c6 C6:ile_DASH_L_c7) + 0.21*pro_DASH_L_c (C1:pro_DASH_L_cy C2:pro_DASH_L_cz C3:pro_DASH_L_cA C4:pro_DASH_L_cB C5:pro_DASH_L_cC) + 0.25*glu_DASH_L_c (C1:glu_DASH_L_cI C2:glu_DASH_L_cJ C3:glu_DASH_L_cK C4:glu_DASH_L_cL C5:glu_DASH_L_cM) + 0.154*glycogen_c (C1:glycogen_cP C2:glycogen_cQ C3:glycogen_cR C4:glycogen_cS C5:glycogen_cT C6:glycogen_cU) + 45.73*atp_c + 0.139*utp_c + 0.00645*clpnEC_e + 0.131*tyr_DASH_L_c (C1:tyr_DASH_L_cb C2:tyr_DASH_L_cc C3:tyr_DASH_L_cd C4:tyr_DASH_L_ce C5:tyr_DASH_L_cf C6:tyr_DASH_L_cg C7:tyr_DASH_L_ch C8:tyr_DASH_L_ci C9:tyr_DASH_L_cj) + 0.203*gtp_c + 0.00005*nadh_c + 0.0000006*coa_c + 0.00215*nad_c + 0.326*lys_DASH_L_c (C1:lys_DASH_L_ce C2:lys_DASH_L_cf C3:lys_DASH_L_cg C4:lys_DASH_L_ch C5:lys_DASH_L_ci C6:lys_DASH_L_cj) + 0.25*gln_DASH_L_c (C1:gln_DASH_L_cD C2:gln_DASH_L_cE C3:gln_DASH_L_cF C4:gln_DASH_L_cG C5:gln_DASH_L_cH) + 0.000003*succoa_c (C1:succoa_cR C2:succoa_cS C3:succoa_cT C4:succoa_cU) + 45.56*h2o_c + 0.205*ser_DASH_L_c (C1:ser_DASH_L_cH C2:ser_DASH_L_cI C3:ser_DASH_L_cJ) + 0.126*ctp_c + 0.001*amp_c + 0.09675*peEC_e + 0.054*trp_DASH_L_c (C1:trp_DASH_L_cZ C2:trp_DASH_L_c1 C3:trp_DASH_L_c2 C4:trp_DASH_L_c3 C5:trp_DASH_L_c4 C6:trp_DASH_L_c5 C7:trp_DASH_L_c6 C8:trp_DASH_L_c7 C9:trp_DASH_L_c8 C10:trp_DASH_L_c9 C11:trp_DASH_L_ca) + 0.09*his_DASH_L_c (C1:his_DASH_L_cV C2:his_DASH_L_cW C3:his_DASH_L_cX C4:his_DASH_L_cY C5:his_DASH_L_cZ C6:his_DASH_L_c1) + 0.0276*peptidoEC_e + 0.087*cys_DASH_L_c (C1:cys_DASH_L_cu C2:cys_DASH_L_cv C3:cys_DASH_L_cw) + 0.0084*lpsEC_e + 0.0247*datp_c + 0.0247*dttp_c + 0.241*thr_DASH_L_c (C1:thr_DASH_L_cV C2:thr_DASH_L_cW C3:thr_DASH_L_cX C4:thr_DASH_L_cY) + 0.281*arg_DASH_L_c (C1:arg_DASH_L_cg C2:arg_DASH_L_ch C3:arg_DASH_L_ci C4:arg_DASH_L_cj C5:arg_DASH_L_ck C6:arg_DASH_L_cl) + 0.00005*accoa_c (C1:accoa_cb C2:accoa_cc) + 0.402*val_DASH_L_c (C1:val_DASH_L_ck C2:val_DASH_L_cl C3:val_DASH_L_cm C4:val_DASH_L_cn C5:val_DASH_L_co) + 0.007*spmd_c (C1:spmd_cK C2:spmd_cL C3:spmd_cM C4:spmd_cN C5:spmd_cO C6:spmd_cP C7:spmd_cQ) + 0.0254*dgtp_c + 0.0232*pgEC_e + 0.146*met_DASH_L_c (C1:met_DASH_L_ck C2:met_DASH_L_cl C3:met_DASH_L_cm C4:met_DASH_L_cn C5:met_DASH_L_co) + 0.035*ptrc_c (C1:ptrc_cD C2:ptrc_cE C3:ptrc_cF C4:ptrc_cG) + 0.0254*dctp_c + 0.428*leu_DASH_L_c (C1:leu_DASH_L_c8 C2:leu_DASH_L_c9 C3:leu_DASH_L_ca C4:leu_DASH_L_cb C5:leu_DASH_L_cc C6:leu_DASH_L_cd) + 0.05*5mthf_c (C1:5mthf_ca) + 0.229*asp_DASH_L_c (C1:asp_DASH_L_cq C2:asp_DASH_L_cr C3:asp_DASH_L_cs C4:asp_DASH_L_ct) + 0.229*asn_DASH_L_c (C1:asn_DASH_L_cm C2:asn_DASH_L_cn C3:asn_DASH_L_co C4:asn_DASH_L_cp) + 0.003*g1p_c (C1:g1p_cx C2:g1p_cy C3:g1p_cz C4:g1p_cA C5:g1p_cB C6:g1p_cC) + 0.0026*psEC_e + 0.00001*fad_c -> 45.56*pi_c + 45.56*h_c + 45.56*adp_c + 0.7332*ppi_c';
        self.biomass_INCA = '0.005707*pg160_c (C1:pg160_c0_C0 C2:pg160_c0_C1 C3:pg160_c0_C2 C4:pg160_c0_C3 C5:pg160_c0_C4 C6:pg160_c0_C5) + 0.000168*coa_c (C1:coa_c0_C0 C2:coa_c0_C1 C3:coa_c0_C2 C4:coa_c0_C3 C5:coa_c0_C4 C6:coa_c0_C5 C7:coa_c0_C6 C8:coa_c0_C7 C9:coa_c0_C8 C10:coa_c0_C9 C11:coa_c0_C10 C12:coa_c0_C11 C13:coa_c0_C12 C14:coa_c0_C13 C15:coa_c0_C14 C16:coa_c0_C15 C17:coa_c0_C16 C18:coa_c0_C17 C19:coa_c0_C18 C20:coa_c0_C19 C21:coa_c0_C20) + 0.000003*lipopb_c + 0.000307*ni2_c + 0.000055*udcpdp_c (C1:udcpdp_c0_C0 C2:udcpdp_c0_C1 C3:udcpdp_c0_C2 C4:udcpdp_c0_C3 C5:udcpdp_c0_C4 C6:udcpdp_c0_C5 C7:udcpdp_c0_C6 C8:udcpdp_c0_C7 C9:udcpdp_c0_C8 C10:udcpdp_c0_C9 C11:udcpdp_c0_C10 C12:udcpdp_c0_C11 C13:udcpdp_c0_C12 C14:udcpdp_c0_C13 C15:udcpdp_c0_C14 C16:udcpdp_c0_C15 C17:udcpdp_c0_C16 C18:udcpdp_c0_C17 C19:udcpdp_c0_C18 C20:udcpdp_c0_C19 C21:udcpdp_c0_C20 C22:udcpdp_c0_C21 C23:udcpdp_c0_C22 C24:udcpdp_c0_C23 C25:udcpdp_c0_C24 C26:udcpdp_c0_C25 C27:udcpdp_c0_C26 C28:udcpdp_c0_C27 C29:udcpdp_c0_C28 C30:udcpdp_c0_C29 C31:udcpdp_c0_C30 C32:udcpdp_c0_C31 C33:udcpdp_c0_C32 C34:udcpdp_c0_C33 C35:udcpdp_c0_C34 C36:udcpdp_c0_C35 C37:udcpdp_c0_C36 C38:udcpdp_c0_C37 C39:udcpdp_c0_C38 C40:udcpdp_c0_C39 C41:udcpdp_c0_C40 C42:udcpdp_c0_C41 C43:udcpdp_c0_C42 C44:udcpdp_c0_C43 C45:udcpdp_c0_C44 C46:udcpdp_c0_C45 C47:udcpdp_c0_C46 C48:udcpdp_c0_C47 C49:udcpdp_c0_C48 C50:udcpdp_c0_C49 C51:udcpdp_c0_C50 C52:udcpdp_c0_C51 C53:udcpdp_c0_C52 C54:udcpdp_c0_C53 C55:udcpdp_c0_C54) + 0.004957*pe181_c (C1:pe181_c0_C0 C2:pe181_c0_C1 C3:pe181_c0_C2 C4:pe181_c0_C3 C5:pe181_c0_C4) + 0.000112*nadp_c (C1:nadp_c0_C0 C2:nadp_c0_C1 C3:nadp_c0_C2 C4:nadp_c0_C3 C5:nadp_c0_C4 C6:nadp_c0_C5 C7:nadp_c0_C6 C8:nadp_c0_C7 C9:nadp_c0_C8 C10:nadp_c0_C9 C11:nadp_c0_C10 C12:nadp_c0_C11 C13:nadp_c0_C12 C14:nadp_c0_C13 C15:nadp_c0_C14 C16:nadp_c0_C15 C17:nadp_c0_C16 C18:nadp_c0_C17 C19:nadp_c0_C18 C20:nadp_c0_C19 C21:nadp_c0_C20) + 0.140101*utp_c (C1:utp_c0_C0 C2:utp_c0_C1 C3:utp_c0_C2 C4:utp_c0_C3 C5:utp_c0_C4 C6:utp_c0_C5 C7:utp_c0_C6 C8:utp_c0_C7 C9:utp_c0_C8) + 0.008253*mg2_c + 0.000024*cobalt2_c + 0.234232*asp_DASH_L_c (C1:asp_DASH_L_c0_C0 C2:asp_DASH_L_c0_C1 C3:asp_DASH_L_c0_C2 C4:asp_DASH_L_c0_C3) + 0.002288*pg181_c (C1:pg181_c0_C0 C2:pg181_c0_C1 C3:pg181_c0_C2 C4:pg181_c0_C3 C5:pg181_c0_C4 C6:pg181_c0_C5) + 0.154187*glycogen_c (C1:glycogen_c0_C0 C2:glycogen_c0_C1 C3:glycogen_c0_C2 C4:glycogen_c0_C3 C5:glycogen_c0_C4 C6:glycogen_c0_C5) + 0.000098*succoa_c (C1:succoa_c0_C0 C2:succoa_c0_C1 C3:succoa_c0_C2 C4:succoa_c0_C3 C5:succoa_c0_C4 C6:succoa_c0_C5 C7:succoa_c0_C6 C8:succoa_c0_C7 C9:succoa_c0_C8 C10:succoa_c0_C9 C11:succoa_c0_C10 C12:succoa_c0_C11 C13:succoa_c0_C12 C14:succoa_c0_C13 C15:succoa_c0_C14 C16:succoa_c0_C15 C17:succoa_c0_C16 C18:succoa_c0_C17 C19:succoa_c0_C18 C20:succoa_c0_C19 C21:succoa_c0_C20 C22:succoa_c0_C21 C23:succoa_c0_C22 C24:succoa_c0_C23 C25:succoa_c0_C24) + 48.752916*h2o_c + 0.031798*pe160_p (C1:pe160_p0_C0 C2:pe160_p0_C1 C3:pe160_p0_C2 C4:pe160_p0_C3 C5:pe160_p0_C4) + 0.000223*gthrd_c (C1:gthrd_c0_C0 C2:gthrd_c0_C1 C3:gthrd_c0_C2 C4:gthrd_c0_C3 C5:gthrd_c0_C4 C6:gthrd_c0_C5 C7:gthrd_c0_C6 C8:gthrd_c0_C7 C9:gthrd_c0_C8 C10:gthrd_c0_C9) + 0.000031*malcoa_c (C1:malcoa_c0_C0 C2:malcoa_c0_C1 C3:malcoa_c0_C2 C4:malcoa_c0_C3 C5:malcoa_c0_C4 C6:malcoa_c0_C5 C7:malcoa_c0_C6 C8:malcoa_c0_C7 C9:malcoa_c0_C8 C10:malcoa_c0_C9 C11:malcoa_c0_C10 C12:malcoa_c0_C11 C13:malcoa_c0_C12 C14:malcoa_c0_C13 C15:malcoa_c0_C14 C16:malcoa_c0_C15 C17:malcoa_c0_C16 C18:malcoa_c0_C17 C19:malcoa_c0_C18 C20:malcoa_c0_C19 C21:malcoa_c0_C20 C22:malcoa_c0_C21 C23:malcoa_c0_C22 C24:malcoa_c0_C23) + 0.209684*ser_DASH_L_c (C1:ser_DASH_L_c0_C0 C2:ser_DASH_L_c0_C1 C3:ser_DASH_L_c0_C2) + 0.234232*asn_DASH_L_c (C1:asn_DASH_L_c0_C0 C2:asn_DASH_L_c0_C1 C3:asn_DASH_L_c0_C2 C4:asn_DASH_L_c0_C3) + 0.000223*amet_c (C1:amet_c0_C0 C2:amet_c0_C1 C3:amet_c0_C2 C4:amet_c0_C3 C5:amet_c0_C4 C6:amet_c0_C5 C7:amet_c0_C6 C8:amet_c0_C7 C9:amet_c0_C8 C10:amet_c0_C9 C11:amet_c0_C10 C12:amet_c0_C11 C13:amet_c0_C12 C14:amet_c0_C13 C15:amet_c0_C14) + 0.595297*gly_c (C1:gly_c0_C0 C2:gly_c0_C1) + 0.000605*murein3px4p_p (C1:murein3px4p_p0_C0 C2:murein3px4p_p0_C1 C3:murein3px4p_p0_C2 C4:murein3px4p_p0_C3 C5:murein3px4p_p0_C4 C6:murein3px4p_p0_C5 C7:murein3px4p_p0_C6 C8:murein3px4p_p0_C7 C9:murein3px4p_p0_C8 C10:murein3px4p_p0_C9 C11:murein3px4p_p0_C10 C12:murein3px4p_p0_C11 C13:murein3px4p_p0_C12 C14:murein3px4p_p0_C13 C15:murein3px4p_p0_C14 C16:murein3px4p_p0_C15 C17:murein3px4p_p0_C16 C18:murein3px4p_p0_C17 C19:murein3px4p_p0_C18 C20:murein3px4p_p0_C19 C21:murein3px4p_p0_C20 C22:murein3px4p_p0_C21 C23:murein3px4p_p0_C22 C24:murein3px4p_p0_C23 C25:murein3px4p_p0_C24 C26:murein3px4p_p0_C25 C27:murein3px4p_p0_C26 C28:murein3px4p_p0_C27 C29:murein3px4p_p0_C28 C30:murein3px4p_p0_C29 C31:murein3px4p_p0_C30 C32:murein3px4p_p0_C31 C33:murein3px4p_p0_C32 C34:murein3px4p_p0_C33 C35:murein3px4p_p0_C34 C36:murein3px4p_p0_C35 C37:murein3px4p_p0_C36 C38:murein3px4p_p0_C37 C39:murein3px4p_p0_C38 C40:murein3px4p_p0_C39 C41:murein3px4p_p0_C40 C42:murein3px4p_p0_C41 C43:murein3px4p_p0_C42 C44:murein3px4p_p0_C43 C45:murein3px4p_p0_C44 C46:murein3px4p_p0_C45 C47:murein3px4p_p0_C46 C48:murein3px4p_p0_C47 C49:murein3px4p_p0_C48 C50:murein3px4p_p0_C49 C51:murein3px4p_p0_C50 C52:murein3px4p_p0_C51 C53:murein3px4p_p0_C52 C54:murein3px4p_p0_C53 C55:murein3px4p_p0_C54 C56:murein3px4p_p0_C55 C57:murein3px4p_p0_C56 C58:murein3px4p_p0_C57 C59:murein3px4p_p0_C58 C60:murein3px4p_p0_C59 C61:murein3px4p_p0_C60 C62:murein3px4p_p0_C61 C63:murein3px4p_p0_C62 C64:murein3px4p_p0_C63 C65:murein3px4p_p0_C64 C66:murein3px4p_p0_C65 C67:murein3px4p_p0_C66 C68:murein3px4p_p0_C67 C69:murein3px4p_p0_C68 C70:murein3px4p_p0_C69 C71:murein3px4p_p0_C70) + 0.055234*trp_DASH_L_c (C1:trp_DASH_L_c0_C0 C2:trp_DASH_L_c0_C1 C3:trp_DASH_L_c0_C2 C4:trp_DASH_L_c0_C3 C5:trp_DASH_L_c0_C4 C6:trp_DASH_L_c0_C5 C7:trp_DASH_L_c0_C6 C8:trp_DASH_L_c0_C7 C9:trp_DASH_L_c0_C8 C10:trp_DASH_L_c0_C9 C11:trp_DASH_L_c0_C10) + 0.03327*ptrc_c (C1:ptrc_c0_C0 C2:ptrc_c0_C1 C3:ptrc_c0_C2 C4:ptrc_c0_C3) + 0.006388*fe2_c + 0.000223*thf_c + 0.000007*mocogdp_c + 0.000223*fad_c (C1:fad_c0_C0 C2:fad_c0_C1 C3:fad_c0_C2 C4:fad_c0_C3 C5:fad_c0_C4 C6:fad_c0_C5 C7:fad_c0_C6 C8:fad_c0_C7 C9:fad_c0_C8 C10:fad_c0_C9 C11:fad_c0_C10 C12:fad_c0_C11 C13:fad_c0_C12 C14:fad_c0_C13 C15:fad_c0_C14 C16:fad_c0_C15 C17:fad_c0_C16 C18:fad_c0_C17 C19:fad_c0_C18 C20:fad_c0_C19 C21:fad_c0_C20 C22:fad_c0_C21 C23:fad_c0_C22 C24:fad_c0_C23 C25:fad_c0_C24 C26:fad_c0_C25 C27:fad_c0_C26) + 0.004126*so4_c + 0.411184*val_DASH_L_c (C1:val_DASH_L_c0_C0 C2:val_DASH_L_c0_C1 C3:val_DASH_L_c0_C2 C4:val_DASH_L_c0_C3 C5:val_DASH_L_c0_C4) + 0.18569*k_c + 0.005381*murein4p4p_p (C1:murein4p4p_p0_C0 C2:murein4p4p_p0_C1 C3:murein4p4p_p0_C2 C4:murein4p4p_p0_C3 C5:murein4p4p_p0_C4 C6:murein4p4p_p0_C5 C7:murein4p4p_p0_C6 C8:murein4p4p_p0_C7 C9:murein4p4p_p0_C8 C10:murein4p4p_p0_C9 C11:murein4p4p_p0_C10 C12:murein4p4p_p0_C11 C13:murein4p4p_p0_C12 C14:murein4p4p_p0_C13 C15:murein4p4p_p0_C14 C16:murein4p4p_p0_C15 C17:murein4p4p_p0_C16 C18:murein4p4p_p0_C17 C19:murein4p4p_p0_C18 C20:murein4p4p_p0_C19 C21:murein4p4p_p0_C20 C22:murein4p4p_p0_C21 C23:murein4p4p_p0_C22 C24:murein4p4p_p0_C23 C25:murein4p4p_p0_C24 C26:murein4p4p_p0_C25 C27:murein4p4p_p0_C26 C28:murein4p4p_p0_C27 C29:murein4p4p_p0_C28 C30:murein4p4p_p0_C29 C31:murein4p4p_p0_C30 C32:murein4p4p_p0_C31 C33:murein4p4p_p0_C32 C34:murein4p4p_p0_C33 C35:murein4p4p_p0_C34 C36:murein4p4p_p0_C35 C37:murein4p4p_p0_C36 C38:murein4p4p_p0_C37 C39:murein4p4p_p0_C38 C40:murein4p4p_p0_C39 C41:murein4p4p_p0_C40 C42:murein4p4p_p0_C41 C43:murein4p4p_p0_C42 C44:murein4p4p_p0_C43 C45:murein4p4p_p0_C44 C46:murein4p4p_p0_C45 C47:murein4p4p_p0_C46 C48:murein4p4p_p0_C47 C49:murein4p4p_p0_C48 C50:murein4p4p_p0_C49 C51:murein4p4p_p0_C50 C52:murein4p4p_p0_C51 C53:murein4p4p_p0_C52 C54:murein4p4p_p0_C53 C55:murein4p4p_p0_C54 C56:murein4p4p_p0_C55 C57:murein4p4p_p0_C56 C58:murein4p4p_p0_C57 C59:murein4p4p_p0_C58 C60:murein4p4p_p0_C59 C61:murein4p4p_p0_C60 C62:murein4p4p_p0_C61 C63:murein4p4p_p0_C62 C64:murein4p4p_p0_C63 C65:murein4p4p_p0_C64 C66:murein4p4p_p0_C65 C67:murein4p4p_p0_C66 C68:murein4p4p_p0_C67 C69:murein4p4p_p0_C68 C70:murein4p4p_p0_C69 C71:murein4p4p_p0_C70 C72:murein4p4p_p0_C71 C73:murein4p4p_p0_C72 C74:murein4p4p_p0_C73) + 0.000223*adocbl_c + 0.005448*murein4px4p_p (C1:murein4px4p_p0_C0 C2:murein4px4p_p0_C1 C3:murein4px4p_p0_C2 C4:murein4px4p_p0_C3 C5:murein4px4p_p0_C4 C6:murein4px4p_p0_C5 C7:murein4px4p_p0_C6 C8:murein4px4p_p0_C7 C9:murein4px4p_p0_C8 C10:murein4px4p_p0_C9 C11:murein4px4p_p0_C10 C12:murein4px4p_p0_C11 C13:murein4px4p_p0_C12 C14:murein4px4p_p0_C13 C15:murein4px4p_p0_C14 C16:murein4px4p_p0_C15 C17:murein4px4p_p0_C16 C18:murein4px4p_p0_C17 C19:murein4px4p_p0_C18 C20:murein4px4p_p0_C19 C21:murein4px4p_p0_C20 C22:murein4px4p_p0_C21 C23:murein4px4p_p0_C22 C24:murein4px4p_p0_C23 C25:murein4px4p_p0_C24 C26:murein4px4p_p0_C25 C27:murein4px4p_p0_C26 C28:murein4px4p_p0_C27 C29:murein4px4p_p0_C28 C30:murein4px4p_p0_C29 C31:murein4px4p_p0_C30 C32:murein4px4p_p0_C31 C33:murein4px4p_p0_C32 C34:murein4px4p_p0_C33 C35:murein4px4p_p0_C34 C36:murein4px4p_p0_C35 C37:murein4px4p_p0_C36 C38:murein4px4p_p0_C37 C39:murein4px4p_p0_C38 C40:murein4px4p_p0_C39 C41:murein4px4p_p0_C40 C42:murein4px4p_p0_C41 C43:murein4px4p_p0_C42 C44:murein4px4p_p0_C43 C45:murein4px4p_p0_C44 C46:murein4px4p_p0_C45 C47:murein4px4p_p0_C46 C48:murein4px4p_p0_C47 C49:murein4px4p_p0_C48 C50:murein4px4p_p0_C49 C51:murein4px4p_p0_C50 C52:murein4px4p_p0_C51 C53:murein4px4p_p0_C52 C54:murein4px4p_p0_C53 C55:murein4px4p_p0_C54 C56:murein4px4p_p0_C55 C57:murein4px4p_p0_C56 C58:murein4px4p_p0_C57 C59:murein4px4p_p0_C58 C60:murein4px4p_p0_C59 C61:murein4px4p_p0_C60 C62:murein4px4p_p0_C61 C63:murein4px4p_p0_C62 C64:murein4px4p_p0_C63 C65:murein4px4p_p0_C64 C66:murein4px4p_p0_C65 C67:murein4px4p_p0_C66 C68:murein4px4p_p0_C67 C69:murein4px4p_p0_C68 C70:murein4px4p_p0_C69 C71:murein4px4p_p0_C70 C72:murein4px4p_p0_C71 C73:murein4px4p_p0_C72 C74:murein4px4p_p0_C73) + 0.004952*ca2_c + 0.000025*2fe2s_c + 0.000335*nadph_c (C1:nadph_c0_C0 C2:nadph_c0_C1 C3:nadph_c0_C2 C4:nadph_c0_C3 C5:nadph_c0_C4 C6:nadph_c0_C5 C7:nadph_c0_C6 C8:nadph_c0_C7 C9:nadph_c0_C8 C10:nadph_c0_C9 C11:nadph_c0_C10 C12:nadph_c0_C11 C13:nadph_c0_C12 C14:nadph_c0_C13 C15:nadph_c0_C14 C16:nadph_c0_C15 C17:nadph_c0_C16 C18:nadph_c0_C17 C19:nadph_c0_C18 C20:nadph_c0_C19 C21:nadph_c0_C20) + 0.000045*nadh_c (C1:nadh_c0_C0 C2:nadh_c0_C1 C3:nadh_c0_C2 C4:nadh_c0_C3 C5:nadh_c0_C4 C6:nadh_c0_C5 C7:nadh_c0_C6 C8:nadh_c0_C7 C9:nadh_c0_C8 C10:nadh_c0_C9 C11:nadh_c0_C10 C12:nadh_c0_C11 C13:nadh_c0_C12 C14:nadh_c0_C13 C15:nadh_c0_C14 C16:nadh_c0_C15 C17:nadh_c0_C16 C18:nadh_c0_C17 C19:nadh_c0_C18 C20:nadh_c0_C19 C21:nadh_c0_C20) + 0.000674*cu2_c + 0.000007*mococdp_c + 0.000223*pheme_c + 0.004439*pg161_c (C1:pg161_c0_C0 C2:pg161_c0_C1 C3:pg161_c0_C2 C4:pg161_c0_C3 C5:pg161_c0_C4 C6:pg161_c0_C5) + 0.012747*pe181_p (C1:pe181_p0_C0 C2:pe181_p0_C1 C3:pe181_p0_C2 C4:pe181_p0_C3 C5:pe181_p0_C4) + 0.282306*ile_DASH_L_c (C1:ile_DASH_L_c0_C0 C2:ile_DASH_L_c0_C1 C3:ile_DASH_L_c0_C2 C4:ile_DASH_L_c0_C3 C5:ile_DASH_L_c0_C4 C6:ile_DASH_L_c0_C5) + 0.000223*chor_c (C1:chor_c0_C0 C2:chor_c0_C1 C3:chor_c0_C2 C4:chor_c0_C3 C5:chor_c0_C4 C6:chor_c0_C5 C7:chor_c0_C6 C8:chor_c0_C7 C9:chor_c0_C8 C10:chor_c0_C9) + 0.000223*q8h2_c + 0.008151*colipa_e + 0.333448*lys_DASH_L_c (C1:lys_DASH_L_c0_C0 C2:lys_DASH_L_c0_C1 C3:lys_DASH_L_c0_C2 C4:lys_DASH_L_c0_C3 C5:lys_DASH_L_c0_C4 C6:lys_DASH_L_c0_C5) + 0.000223*enter_c + 0.000223*mlthf_c (C1:mlthf_c0_C0) + 0.000223*thmpp_c + 0.28742*arg_DASH_L_c (C1:arg_DASH_L_c0_C0 C2:arg_DASH_L_c0_C1 C3:arg_DASH_L_c0_C2 C4:arg_DASH_L_c0_C3 C5:arg_DASH_L_c0_C4 C6:arg_DASH_L_c0_C5) + 0.000002*btn_c + 0.000223*hemeO_c + 0.499149*ala_DASH_L_c (C1:ala_DASH_L_c0_C0 C2:ala_DASH_L_c0_C1 C3:ala_DASH_L_c0_C2) + 0.246506*thr_DASH_L_c (C1:thr_DASH_L_c0_C0 C2:thr_DASH_L_c0_C1 C3:thr_DASH_L_c0_C2 C4:thr_DASH_L_c0_C3) + 0.088988*cys_DASH_L_c (C1:cys_DASH_L_c0_C0 C2:cys_DASH_L_c0_C1 C3:cys_DASH_L_c0_C2) + 0.001787*nad_c (C1:nad_c0_C0 C2:nad_c0_C1 C3:nad_c0_C2 C4:nad_c0_C3 C5:nad_c0_C4 C6:nad_c0_C5 C7:nad_c0_C6 C8:nad_c0_C7 C9:nad_c0_C8 C10:nad_c0_C9 C11:nad_c0_C10 C12:nad_c0_C11 C13:nad_c0_C12 C14:nad_c0_C13 C15:nad_c0_C14 C16:nad_c0_C15 C17:nad_c0_C16 C18:nad_c0_C17 C19:nad_c0_C18 C20:nad_c0_C19 C21:nad_c0_C20) + 0.180021*phe_DASH_L_c (C1:phe_DASH_L_c0_C0 C2:phe_DASH_L_c0_C1 C3:phe_DASH_L_c0_C2 C4:phe_DASH_L_c0_C3 C5:phe_DASH_L_c0_C4 C6:phe_DASH_L_c0_C5 C7:phe_DASH_L_c0_C6 C8:phe_DASH_L_c0_C7 C9:phe_DASH_L_c0_C8) + 0.025612*dctp_c (C1:dctp_c0_C0 C2:dctp_c0_C1 C3:dctp_c0_C2 C4:dctp_c0_C3 C5:dctp_c0_C4 C6:dctp_c0_C5 C7:dctp_c0_C6 C8:dctp_c0_C7 C9:dctp_c0_C8) + 0.149336*met_DASH_L_c (C1:met_DASH_L_c0_C0 C2:met_DASH_L_c0_C1 C3:met_DASH_L_c0_C2 C4:met_DASH_L_c0_C3 C5:met_DASH_L_c0_C4) + 0.012366*pe160_c (C1:pe160_c0_C0 C2:pe160_c0_C1 C3:pe160_c0_C2 C4:pe160_c0_C3 C5:pe160_c0_C4) + 0.209121*gtp_c (C1:gtp_c0_C0 C2:gtp_c0_C1 C3:gtp_c0_C2 C4:gtp_c0_C3 C5:gtp_c0_C4 C6:gtp_c0_C5 C7:gtp_c0_C6 C8:gtp_c0_C7 C9:gtp_c0_C8 C10:gtp_c0_C9) + 0.437778*leu_DASH_L_c (C1:leu_DASH_L_c0_C0 C2:leu_DASH_L_c0_C1 C3:leu_DASH_L_c0_C2 C4:leu_DASH_L_c0_C3 C5:leu_DASH_L_c0_C4 C6:leu_DASH_L_c0_C5) + 0.007428*fe3_c + 0.092056*his_DASH_L_c (C1:his_DASH_L_c0_C0 C2:his_DASH_L_c0_C1 C3:his_DASH_L_c0_C2 C4:his_DASH_L_c0_C3 C5:his_DASH_L_c0_C4 C6:his_DASH_L_c0_C5) + 0.009618*pe161_c (C1:pe161_c0_C0 C2:pe161_c0_C1 C3:pe161_c0_C2 C4:pe161_c0_C3 C5:pe161_c0_C4) + 0.000223*10fthf_c (C1:10fthf_c0_C0) + 0.024805*datp_c (C1:datp_c0_C0 C2:datp_c0_C1 C3:datp_c0_C2 C4:datp_c0_C3 C5:datp_c0_C4 C6:datp_c0_C5 C7:datp_c0_C6 C8:datp_c0_C7 C9:datp_c0_C8 C10:datp_c0_C9) + 0.000223*5mthf_c (C1:5mthf_c0_C0) + 0.000673*murein4px4px4p_p (C1:murein4px4px4p_p0_C0 C2:murein4px4px4p_p0_C1 C3:murein4px4px4p_p0_C2 C4:murein4px4px4p_p0_C3 C5:murein4px4px4p_p0_C4 C6:murein4px4px4p_p0_C5 C7:murein4px4px4p_p0_C6 C8:murein4px4px4p_p0_C7 C9:murein4px4px4p_p0_C8 C10:murein4px4px4p_p0_C9 C11:murein4px4px4p_p0_C10 C12:murein4px4px4p_p0_C11 C13:murein4px4px4p_p0_C12 C14:murein4px4px4p_p0_C13 C15:murein4px4px4p_p0_C14 C16:murein4px4px4p_p0_C15 C17:murein4px4px4p_p0_C16 C18:murein4px4px4p_p0_C17 C19:murein4px4px4p_p0_C18 C20:murein4px4px4p_p0_C19 C21:murein4px4px4p_p0_C20 C22:murein4px4px4p_p0_C21 C23:murein4px4px4p_p0_C22 C24:murein4px4px4p_p0_C23 C25:murein4px4px4p_p0_C24 C26:murein4px4px4p_p0_C25 C27:murein4px4px4p_p0_C26 C28:murein4px4px4p_p0_C27 C29:murein4px4px4p_p0_C28 C30:murein4px4px4p_p0_C29 C31:murein4px4px4p_p0_C30 C32:murein4px4px4p_p0_C31 C33:murein4px4px4p_p0_C32 C34:murein4px4px4p_p0_C33 C35:murein4px4px4p_p0_C34 C36:murein4px4px4p_p0_C35 C37:murein4px4px4p_p0_C36 C38:murein4px4px4p_p0_C37 C39:murein4px4px4p_p0_C38 C40:murein4px4px4p_p0_C39 C41:murein4px4px4p_p0_C40 C42:murein4px4px4p_p0_C41 C43:murein4px4px4p_p0_C42 C44:murein4px4px4p_p0_C43 C45:murein4px4px4p_p0_C44 C46:murein4px4px4p_p0_C45 C47:murein4px4px4p_p0_C46 C48:murein4px4px4p_p0_C47 C49:murein4px4px4p_p0_C48 C50:murein4px4px4p_p0_C49 C51:murein4px4px4p_p0_C50 C52:murein4px4px4p_p0_C51 C53:murein4px4px4p_p0_C52 C54:murein4px4px4p_p0_C53 C55:murein4px4px4p_p0_C54 C56:murein4px4px4p_p0_C55 C57:murein4px4px4p_p0_C56 C58:murein4px4px4p_p0_C57 C59:murein4px4px4p_p0_C58 C60:murein4px4px4p_p0_C59 C61:murein4px4px4p_p0_C60 C62:murein4px4px4p_p0_C61 C63:murein4px4px4p_p0_C62 C64:murein4px4px4p_p0_C63 C65:murein4px4px4p_p0_C64 C66:murein4px4px4p_p0_C65 C67:murein4px4px4p_p0_C66 C68:murein4px4px4p_p0_C67 C69:murein4px4px4p_p0_C68 C70:murein4px4px4p_p0_C69 C71:murein4px4px4p_p0_C70 C72:murein4px4px4p_p0_C71 C73:murein4px4px4p_p0_C72 C74:murein4px4px4p_p0_C73 C75:murein4px4px4p_p0_C74 C76:murein4px4px4p_p0_C75 C77:murein4px4px4p_p0_C76 C78:murein4px4px4p_p0_C77 C79:murein4px4px4p_p0_C78 C80:murein4px4px4p_p0_C79 C81:murein4px4px4p_p0_C80 C82:murein4px4px4p_p0_C81 C83:murein4px4px4p_p0_C82 C84:murein4px4px4p_p0_C83 C85:murein4px4px4p_p0_C84 C86:murein4px4px4p_p0_C85 C87:murein4px4px4p_p0_C86 C88:murein4px4px4p_p0_C87 C89:murein4px4px4p_p0_C88 C90:murein4px4px4p_p0_C89 C91:murein4px4px4p_p0_C90 C92:murein4px4px4p_p0_C91 C93:murein4px4px4p_p0_C92 C94:murein4px4px4p_p0_C93 C95:murein4px4px4p_p0_C94 C96:murein4px4px4p_p0_C95 C97:murein4px4px4p_p0_C96 C98:murein4px4px4p_p0_C97 C99:murein4px4px4p_p0_C98 C100:murein4px4px4p_p0_C99 C101:murein4px4px4p_p0_C100 C102:murein4px4px4p_p0_C101 C103:murein4px4px4p_p0_C102 C104:murein4px4px4p_p0_C103 C105:murein4px4px4p_p0_C104 C106:murein4px4px4p_p0_C105 C107:murein4px4px4p_p0_C106 C108:murein4px4px4p_p0_C107 C109:murein4px4px4p_p0_C108 C110:murein4px4px4p_p0_C109 C111:murein4px4px4p_p0_C110) + 0.024805*dttp_c (C1:dttp_c0_C0 C2:dttp_c0_C1 C3:dttp_c0_C2 C4:dttp_c0_C3 C5:dttp_c0_C4 C6:dttp_c0_C5 C7:dttp_c0_C6 C8:dttp_c0_C7 C9:dttp_c0_C8 C10:dttp_c0_C9) + 0.000223*ribflv_c (C1:ribflv_c0_C0 C2:ribflv_c0_C1 C3:ribflv_c0_C2 C4:ribflv_c0_C3 C5:ribflv_c0_C4 C6:ribflv_c0_C5 C7:ribflv_c0_C6 C8:ribflv_c0_C7 C9:ribflv_c0_C8 C10:ribflv_c0_C9 C11:ribflv_c0_C10 C12:ribflv_c0_C11 C13:ribflv_c0_C12 C14:ribflv_c0_C13 C15:ribflv_c0_C14 C16:ribflv_c0_C15 C17:ribflv_c0_C16) + 0.000223*pydx5p_c + 0.000324*zn2_c + 0.004952*cl_c + 0.000223*sheme_c + 0.001345*murein3p3p_p (C1:murein3p3p_p0_C0 C2:murein3p3p_p0_C1 C3:murein3p3p_p0_C2 C4:murein3p3p_p0_C3 C5:murein3p3p_p0_C4 C6:murein3p3p_p0_C5 C7:murein3p3p_p0_C6 C8:murein3p3p_p0_C7 C9:murein3p3p_p0_C8 C10:murein3p3p_p0_C9 C11:murein3p3p_p0_C10 C12:murein3p3p_p0_C11 C13:murein3p3p_p0_C12 C14:murein3p3p_p0_C13 C15:murein3p3p_p0_C14 C16:murein3p3p_p0_C15 C17:murein3p3p_p0_C16 C18:murein3p3p_p0_C17 C19:murein3p3p_p0_C18 C20:murein3p3p_p0_C19 C21:murein3p3p_p0_C20 C22:murein3p3p_p0_C21 C23:murein3p3p_p0_C22 C24:murein3p3p_p0_C23 C25:murein3p3p_p0_C24 C26:murein3p3p_p0_C25 C27:murein3p3p_p0_C26 C28:murein3p3p_p0_C27 C29:murein3p3p_p0_C28 C30:murein3p3p_p0_C29 C31:murein3p3p_p0_C30 C32:murein3p3p_p0_C31 C33:murein3p3p_p0_C32 C34:murein3p3p_p0_C33 C35:murein3p3p_p0_C34 C36:murein3p3p_p0_C35 C37:murein3p3p_p0_C36 C38:murein3p3p_p0_C37 C39:murein3p3p_p0_C38 C40:murein3p3p_p0_C39 C41:murein3p3p_p0_C40 C42:murein3p3p_p0_C41 C43:murein3p3p_p0_C42 C44:murein3p3p_p0_C43 C45:murein3p3p_p0_C44 C46:murein3p3p_p0_C45 C47:murein3p3p_p0_C46 C48:murein3p3p_p0_C47 C49:murein3p3p_p0_C48 C50:murein3p3p_p0_C49 C51:murein3p3p_p0_C50 C52:murein3p3p_p0_C51 C53:murein3p3p_p0_C52 C54:murein3p3p_p0_C53 C55:murein3p3p_p0_C54 C56:murein3p3p_p0_C55 C57:murein3p3p_p0_C56 C58:murein3p3p_p0_C57 C59:murein3p3p_p0_C58 C60:murein3p3p_p0_C59 C61:murein3p3p_p0_C60 C62:murein3p3p_p0_C61 C63:murein3p3p_p0_C62 C64:murein3p3p_p0_C63 C65:murein3p3p_p0_C64 C66:murein3p3p_p0_C65 C67:murein3p3p_p0_C66 C68:murein3p3p_p0_C67) + 0.004892*pg160_p (C1:pg160_p0_C0 C2:pg160_p0_C1 C3:pg160_p0_C2 C4:pg160_p0_C3 C5:pg160_p0_C4 C6:pg160_p0_C5) + 0.129799*ctp_c (C1:ctp_c0_C0 C2:ctp_c0_C1 C3:ctp_c0_C2 C4:ctp_c0_C3 C5:ctp_c0_C4 C6:ctp_c0_C5 C7:ctp_c0_C6 C8:ctp_c0_C7 C9:ctp_c0_C8) + 0.255712*glu_DASH_L_c (C1:glu_DASH_L_c0_C0 C2:glu_DASH_L_c0_C1 C3:glu_DASH_L_c0_C2 C4:glu_DASH_L_c0_C3 C5:glu_DASH_L_c0_C4) + 0.214798*pro_DASH_L_c (C1:pro_DASH_L_c0_C0 C2:pro_DASH_L_c0_C1 C3:pro_DASH_L_c0_C2 C4:pro_DASH_L_c0_C3 C5:pro_DASH_L_c0_C4) + 0.025612*dgtp_c (C1:dgtp_c0_C0 C2:dgtp_c0_C1 C3:dgtp_c0_C2 C4:dgtp_c0_C3 C5:dgtp_c0_C4 C6:dgtp_c0_C5 C7:dgtp_c0_C6 C8:dgtp_c0_C7 C9:dgtp_c0_C8 C10:dgtp_c0_C9) + 0.000007*mobd_c + 0.255712*gln_DASH_L_c (C1:gln_DASH_L_c0_C0 C2:gln_DASH_L_c0_C1 C3:gln_DASH_L_c0_C2 C4:gln_DASH_L_c0_C3 C5:gln_DASH_L_c0_C4) + 0.001961*pg181_p (C1:pg181_p0_C0 C2:pg181_p0_C1 C3:pg181_p0_C2 C4:pg181_p0_C3 C5:pg181_p0_C4 C6:pg181_p0_C5) + 0.000658*mn2_c + 0.000223*2dmmql8_c + 0.024732*pe161_p (C1:pe161_p0_C0 C2:pe161_p0_C1 C3:pe161_p0_C2 C4:pe161_p0_C3 C5:pe161_p0_C4) + 0.000248*4fe4s_c + 0.00118*clpn181_p (C1:clpn181_p0_C0 C2:clpn181_p0_C1 C3:clpn181_p0_C2 C4:clpn181_p0_C3 C5:clpn181_p0_C4 C6:clpn181_p0_C5 C7:clpn181_p0_C6 C8:clpn181_p0_C7 C9:clpn181_p0_C8) + 0.012379*nh4_c + 0.000223*mql8_c + 0.003805*pg161_p (C1:pg161_p0_C0 C2:pg161_p0_C1 C3:pg161_p0_C2 C4:pg161_p0_C3 C5:pg161_p0_C4 C6:pg161_p0_C5) + 0.000279*accoa_c (C1:accoa_c0_C0 C2:accoa_c0_C1 C3:accoa_c0_C2 C4:accoa_c0_C3 C5:accoa_c0_C4 C6:accoa_c0_C5 C7:accoa_c0_C6 C8:accoa_c0_C7 C9:accoa_c0_C8 C10:accoa_c0_C9 C11:accoa_c0_C10 C12:accoa_c0_C11 C13:accoa_c0_C12 C14:accoa_c0_C13 C15:accoa_c0_C14 C16:accoa_c0_C15 C17:accoa_c0_C16 C18:accoa_c0_C17 C19:accoa_c0_C18 C20:accoa_c0_C19 C21:accoa_c0_C20 C22:accoa_c0_C21 C23:accoa_c0_C22) + 54.119975*atp_c (C1:atp_c0_C0 C2:atp_c0_C1 C3:atp_c0_C2 C4:atp_c0_C3 C5:atp_c0_C4 C6:atp_c0_C5 C7:atp_c0_C6 C8:atp_c0_C7 C9:atp_c0_C8 C10:atp_c0_C9) + 0.133993*tyr_DASH_L_c (C1:tyr_DASH_L_c0_C0 C2:tyr_DASH_L_c0_C1 C3:tyr_DASH_L_c0_C2 C4:tyr_DASH_L_c0_C3 C5:tyr_DASH_L_c0_C4 C6:tyr_DASH_L_c0_C5 C7:tyr_DASH_L_c0_C6 C8:tyr_DASH_L_c0_C7 C9:tyr_DASH_L_c0_C8) + 0.006744*spmd_c (C1:spmd_c0_C0 C2:spmd_c0_C1 C3:spmd_c0_C2 C4:spmd_c0_C3 C5:spmd_c0_C4 C6:spmd_c0_C5 C7:spmd_c0_C6) + 0.002944*clpn160_p (C1:clpn160_p0_C0 C2:clpn160_p0_C1 C3:clpn160_p0_C2 C4:clpn160_p0_C3 C5:clpn160_p0_C4 C6:clpn160_p0_C5 C7:clpn160_p0_C6 C8:clpn160_p0_C7 C9:clpn160_p0_C8) + 0.000116*bmocogdp_c + 0.00229*clpn161_p (C1:clpn161_p0_C0 C2:clpn161_p0_C1 C3:clpn161_p0_C2 C4:clpn161_p0_C3 C5:clpn161_p0_C4 C6:clpn161_p0_C5 C7:clpn161_p0_C6 C8:clpn161_p0_C7 C9:clpn161_p0_C8) -> 0.749831*ppi_c + 53.95*adp_c (C1:atp_c0_C0 C2:atp_c0_C1 C3:atp_c0_C2 C4:atp_c0_C3 C5:atp_c0_C4 C6:atp_c0_C5 C7:atp_c0_C6 C8:atp_c0_C7 C9:atp_c0_C8 C10:atp_c0_C9) + 0.005707*Ec_biomass_iJO1366_WT_53p95M_pg160_c_0.balance (C1:pg160_c0_C0 C2:pg160_c0_C1 C3:pg160_c0_C2 C4:pg160_c0_C3 C5:pg160_c0_C4 C6:pg160_c0_C5) + 0.000168*Ec_biomass_iJO1366_WT_53p95M_coa_c_1.balance (C1:coa_c0_C0 C2:coa_c0_C1 C3:coa_c0_C2 C4:coa_c0_C3 C5:coa_c0_C4 C6:coa_c0_C5 C7:coa_c0_C6 C8:coa_c0_C7 C9:coa_c0_C8 C10:coa_c0_C9 C11:coa_c0_C10 C12:coa_c0_C11 C13:coa_c0_C12 C14:coa_c0_C13 C15:coa_c0_C14 C16:coa_c0_C15 C17:coa_c0_C16 C18:coa_c0_C17 C19:coa_c0_C18 C20:coa_c0_C19 C21:coa_c0_C20) + 0.000055*Ec_biomass_iJO1366_WT_53p95M_udcpdp_c_2.balance (C1:udcpdp_c0_C0 C2:udcpdp_c0_C1 C3:udcpdp_c0_C2 C4:udcpdp_c0_C3 C5:udcpdp_c0_C4 C6:udcpdp_c0_C5 C7:udcpdp_c0_C6 C8:udcpdp_c0_C7 C9:udcpdp_c0_C8 C10:udcpdp_c0_C9 C11:udcpdp_c0_C10 C12:udcpdp_c0_C11 C13:udcpdp_c0_C12 C14:udcpdp_c0_C13 C15:udcpdp_c0_C14 C16:udcpdp_c0_C15 C17:udcpdp_c0_C16 C18:udcpdp_c0_C17 C19:udcpdp_c0_C18 C20:udcpdp_c0_C19 C21:udcpdp_c0_C20 C22:udcpdp_c0_C21 C23:udcpdp_c0_C22 C24:udcpdp_c0_C23 C25:udcpdp_c0_C24 C26:udcpdp_c0_C25 C27:udcpdp_c0_C26 C28:udcpdp_c0_C27 C29:udcpdp_c0_C28 C30:udcpdp_c0_C29 C31:udcpdp_c0_C30 C32:udcpdp_c0_C31 C33:udcpdp_c0_C32 C34:udcpdp_c0_C33 C35:udcpdp_c0_C34 C36:udcpdp_c0_C35 C37:udcpdp_c0_C36 C38:udcpdp_c0_C37 C39:udcpdp_c0_C38 C40:udcpdp_c0_C39 C41:udcpdp_c0_C40 C42:udcpdp_c0_C41 C43:udcpdp_c0_C42 C44:udcpdp_c0_C43 C45:udcpdp_c0_C44 C46:udcpdp_c0_C45 C47:udcpdp_c0_C46 C48:udcpdp_c0_C47 C49:udcpdp_c0_C48 C50:udcpdp_c0_C49 C51:udcpdp_c0_C50 C52:udcpdp_c0_C51 C53:udcpdp_c0_C52 C54:udcpdp_c0_C53 C55:udcpdp_c0_C54) + 0.004957*Ec_biomass_iJO1366_WT_53p95M_pe181_c_3.balance (C1:pe181_c0_C0 C2:pe181_c0_C1 C3:pe181_c0_C2 C4:pe181_c0_C3 C5:pe181_c0_C4) + 0.000112*Ec_biomass_iJO1366_WT_53p95M_nadp_c_4.balance (C1:nadp_c0_C0 C2:nadp_c0_C1 C3:nadp_c0_C2 C4:nadp_c0_C3 C5:nadp_c0_C4 C6:nadp_c0_C5 C7:nadp_c0_C6 C8:nadp_c0_C7 C9:nadp_c0_C8 C10:nadp_c0_C9 C11:nadp_c0_C10 C12:nadp_c0_C11 C13:nadp_c0_C12 C14:nadp_c0_C13 C15:nadp_c0_C14 C16:nadp_c0_C15 C17:nadp_c0_C16 C18:nadp_c0_C17 C19:nadp_c0_C18 C20:nadp_c0_C19 C21:nadp_c0_C20) + 0.140101*Ec_biomass_iJO1366_WT_53p95M_utp_c_5.balance (C1:utp_c0_C0 C2:utp_c0_C1 C3:utp_c0_C2 C4:utp_c0_C3 C5:utp_c0_C4 C6:utp_c0_C5 C7:utp_c0_C6 C8:utp_c0_C7 C9:utp_c0_C8) + 0.234232*Ec_biomass_iJO1366_WT_53p95M_asp_DASH_L_c_6.balance (C1:asp_DASH_L_c0_C0 C2:asp_DASH_L_c0_C1 C3:asp_DASH_L_c0_C2 C4:asp_DASH_L_c0_C3) + 0.002288*Ec_biomass_iJO1366_WT_53p95M_pg181_c_7.balance (C1:pg181_c0_C0 C2:pg181_c0_C1 C3:pg181_c0_C2 C4:pg181_c0_C3 C5:pg181_c0_C4 C6:pg181_c0_C5) + 0.154187*Ec_biomass_iJO1366_WT_53p95M_glycogen_c_8.balance (C1:glycogen_c0_C0 C2:glycogen_c0_C1 C3:glycogen_c0_C2 C4:glycogen_c0_C3 C5:glycogen_c0_C4 C6:glycogen_c0_C5) + 0.000098*Ec_biomass_iJO1366_WT_53p95M_succoa_c_9.balance (C1:succoa_c0_C0 C2:succoa_c0_C1 C3:succoa_c0_C2 C4:succoa_c0_C3 C5:succoa_c0_C4 C6:succoa_c0_C5 C7:succoa_c0_C6 C8:succoa_c0_C7 C9:succoa_c0_C8 C10:succoa_c0_C9 C11:succoa_c0_C10 C12:succoa_c0_C11 C13:succoa_c0_C12 C14:succoa_c0_C13 C15:succoa_c0_C14 C16:succoa_c0_C15 C17:succoa_c0_C16 C18:succoa_c0_C17 C19:succoa_c0_C18 C20:succoa_c0_C19 C21:succoa_c0_C20 C22:succoa_c0_C21 C23:succoa_c0_C22 C24:succoa_c0_C23 C25:succoa_c0_C24) + 0.031798*Ec_biomass_iJO1366_WT_53p95M_pe160_p_10.balance (C1:pe160_p0_C0 C2:pe160_p0_C1 C3:pe160_p0_C2 C4:pe160_p0_C3 C5:pe160_p0_C4) + 0.000223*Ec_biomass_iJO1366_WT_53p95M_gthrd_c_11.balance (C1:gthrd_c0_C0 C2:gthrd_c0_C1 C3:gthrd_c0_C2 C4:gthrd_c0_C3 C5:gthrd_c0_C4 C6:gthrd_c0_C5 C7:gthrd_c0_C6 C8:gthrd_c0_C7 C9:gthrd_c0_C8 C10:gthrd_c0_C9) + 0.000031*Ec_biomass_iJO1366_WT_53p95M_malcoa_c_12.balance (C1:malcoa_c0_C0 C2:malcoa_c0_C1 C3:malcoa_c0_C2 C4:malcoa_c0_C3 C5:malcoa_c0_C4 C6:malcoa_c0_C5 C7:malcoa_c0_C6 C8:malcoa_c0_C7 C9:malcoa_c0_C8 C10:malcoa_c0_C9 C11:malcoa_c0_C10 C12:malcoa_c0_C11 C13:malcoa_c0_C12 C14:malcoa_c0_C13 C15:malcoa_c0_C14 C16:malcoa_c0_C15 C17:malcoa_c0_C16 C18:malcoa_c0_C17 C19:malcoa_c0_C18 C20:malcoa_c0_C19 C21:malcoa_c0_C20 C22:malcoa_c0_C21 C23:malcoa_c0_C22 C24:malcoa_c0_C23) + 0.209684*Ec_biomass_iJO1366_WT_53p95M_ser_DASH_L_c_13.balance (C1:ser_DASH_L_c0_C0 C2:ser_DASH_L_c0_C1 C3:ser_DASH_L_c0_C2) + 0.234232*Ec_biomass_iJO1366_WT_53p95M_asn_DASH_L_c_14.balance (C1:asn_DASH_L_c0_C0 C2:asn_DASH_L_c0_C1 C3:asn_DASH_L_c0_C2 C4:asn_DASH_L_c0_C3) + 0.000223*Ec_biomass_iJO1366_WT_53p95M_amet_c_15.balance (C1:amet_c0_C0 C2:amet_c0_C1 C3:amet_c0_C2 C4:amet_c0_C3 C5:amet_c0_C4 C6:amet_c0_C5 C7:amet_c0_C6 C8:amet_c0_C7 C9:amet_c0_C8 C10:amet_c0_C9 C11:amet_c0_C10 C12:amet_c0_C11 C13:amet_c0_C12 C14:amet_c0_C13 C15:amet_c0_C14) + 0.595297*Ec_biomass_iJO1366_WT_53p95M_gly_c_16.balance (C1:gly_c0_C0 C2:gly_c0_C1) + 0.000605*Ec_biomass_iJO1366_WT_53p95M_murein3px4p_p_17.balance (C1:murein3px4p_p0_C0 C2:murein3px4p_p0_C1 C3:murein3px4p_p0_C2 C4:murein3px4p_p0_C3 C5:murein3px4p_p0_C4 C6:murein3px4p_p0_C5 C7:murein3px4p_p0_C6 C8:murein3px4p_p0_C7 C9:murein3px4p_p0_C8 C10:murein3px4p_p0_C9 C11:murein3px4p_p0_C10 C12:murein3px4p_p0_C11 C13:murein3px4p_p0_C12 C14:murein3px4p_p0_C13 C15:murein3px4p_p0_C14 C16:murein3px4p_p0_C15 C17:murein3px4p_p0_C16 C18:murein3px4p_p0_C17 C19:murein3px4p_p0_C18 C20:murein3px4p_p0_C19 C21:murein3px4p_p0_C20 C22:murein3px4p_p0_C21 C23:murein3px4p_p0_C22 C24:murein3px4p_p0_C23 C25:murein3px4p_p0_C24 C26:murein3px4p_p0_C25 C27:murein3px4p_p0_C26 C28:murein3px4p_p0_C27 C29:murein3px4p_p0_C28 C30:murein3px4p_p0_C29 C31:murein3px4p_p0_C30 C32:murein3px4p_p0_C31 C33:murein3px4p_p0_C32 C34:murein3px4p_p0_C33 C35:murein3px4p_p0_C34 C36:murein3px4p_p0_C35 C37:murein3px4p_p0_C36 C38:murein3px4p_p0_C37 C39:murein3px4p_p0_C38 C40:murein3px4p_p0_C39 C41:murein3px4p_p0_C40 C42:murein3px4p_p0_C41 C43:murein3px4p_p0_C42 C44:murein3px4p_p0_C43 C45:murein3px4p_p0_C44 C46:murein3px4p_p0_C45 C47:murein3px4p_p0_C46 C48:murein3px4p_p0_C47 C49:murein3px4p_p0_C48 C50:murein3px4p_p0_C49 C51:murein3px4p_p0_C50 C52:murein3px4p_p0_C51 C53:murein3px4p_p0_C52 C54:murein3px4p_p0_C53 C55:murein3px4p_p0_C54 C56:murein3px4p_p0_C55 C57:murein3px4p_p0_C56 C58:murein3px4p_p0_C57 C59:murein3px4p_p0_C58 C60:murein3px4p_p0_C59 C61:murein3px4p_p0_C60 C62:murein3px4p_p0_C61 C63:murein3px4p_p0_C62 C64:murein3px4p_p0_C63 C65:murein3px4p_p0_C64 C66:murein3px4p_p0_C65 C67:murein3px4p_p0_C66 C68:murein3px4p_p0_C67 C69:murein3px4p_p0_C68 C70:murein3px4p_p0_C69 C71:murein3px4p_p0_C70) + 0.055234*Ec_biomass_iJO1366_WT_53p95M_trp_DASH_L_c_18.balance (C1:trp_DASH_L_c0_C0 C2:trp_DASH_L_c0_C1 C3:trp_DASH_L_c0_C2 C4:trp_DASH_L_c0_C3 C5:trp_DASH_L_c0_C4 C6:trp_DASH_L_c0_C5 C7:trp_DASH_L_c0_C6 C8:trp_DASH_L_c0_C7 C9:trp_DASH_L_c0_C8 C10:trp_DASH_L_c0_C9 C11:trp_DASH_L_c0_C10) + 0.03327*Ec_biomass_iJO1366_WT_53p95M_ptrc_c_19.balance (C1:ptrc_c0_C0 C2:ptrc_c0_C1 C3:ptrc_c0_C2 C4:ptrc_c0_C3) + 0.000223*Ec_biomass_iJO1366_WT_53p95M_fad_c_20.balance (C1:fad_c0_C0 C2:fad_c0_C1 C3:fad_c0_C2 C4:fad_c0_C3 C5:fad_c0_C4 C6:fad_c0_C5 C7:fad_c0_C6 C8:fad_c0_C7 C9:fad_c0_C8 C10:fad_c0_C9 C11:fad_c0_C10 C12:fad_c0_C11 C13:fad_c0_C12 C14:fad_c0_C13 C15:fad_c0_C14 C16:fad_c0_C15 C17:fad_c0_C16 C18:fad_c0_C17 C19:fad_c0_C18 C20:fad_c0_C19 C21:fad_c0_C20 C22:fad_c0_C21 C23:fad_c0_C22 C24:fad_c0_C23 C25:fad_c0_C24 C26:fad_c0_C25 C27:fad_c0_C26) + 0.411184*Ec_biomass_iJO1366_WT_53p95M_val_DASH_L_c_21.balance (C1:val_DASH_L_c0_C0 C2:val_DASH_L_c0_C1 C3:val_DASH_L_c0_C2 C4:val_DASH_L_c0_C3 C5:val_DASH_L_c0_C4) + 0.005381*Ec_biomass_iJO1366_WT_53p95M_murein4p4p_p_22.balance (C1:murein4p4p_p0_C0 C2:murein4p4p_p0_C1 C3:murein4p4p_p0_C2 C4:murein4p4p_p0_C3 C5:murein4p4p_p0_C4 C6:murein4p4p_p0_C5 C7:murein4p4p_p0_C6 C8:murein4p4p_p0_C7 C9:murein4p4p_p0_C8 C10:murein4p4p_p0_C9 C11:murein4p4p_p0_C10 C12:murein4p4p_p0_C11 C13:murein4p4p_p0_C12 C14:murein4p4p_p0_C13 C15:murein4p4p_p0_C14 C16:murein4p4p_p0_C15 C17:murein4p4p_p0_C16 C18:murein4p4p_p0_C17 C19:murein4p4p_p0_C18 C20:murein4p4p_p0_C19 C21:murein4p4p_p0_C20 C22:murein4p4p_p0_C21 C23:murein4p4p_p0_C22 C24:murein4p4p_p0_C23 C25:murein4p4p_p0_C24 C26:murein4p4p_p0_C25 C27:murein4p4p_p0_C26 C28:murein4p4p_p0_C27 C29:murein4p4p_p0_C28 C30:murein4p4p_p0_C29 C31:murein4p4p_p0_C30 C32:murein4p4p_p0_C31 C33:murein4p4p_p0_C32 C34:murein4p4p_p0_C33 C35:murein4p4p_p0_C34 C36:murein4p4p_p0_C35 C37:murein4p4p_p0_C36 C38:murein4p4p_p0_C37 C39:murein4p4p_p0_C38 C40:murein4p4p_p0_C39 C41:murein4p4p_p0_C40 C42:murein4p4p_p0_C41 C43:murein4p4p_p0_C42 C44:murein4p4p_p0_C43 C45:murein4p4p_p0_C44 C46:murein4p4p_p0_C45 C47:murein4p4p_p0_C46 C48:murein4p4p_p0_C47 C49:murein4p4p_p0_C48 C50:murein4p4p_p0_C49 C51:murein4p4p_p0_C50 C52:murein4p4p_p0_C51 C53:murein4p4p_p0_C52 C54:murein4p4p_p0_C53 C55:murein4p4p_p0_C54 C56:murein4p4p_p0_C55 C57:murein4p4p_p0_C56 C58:murein4p4p_p0_C57 C59:murein4p4p_p0_C58 C60:murein4p4p_p0_C59 C61:murein4p4p_p0_C60 C62:murein4p4p_p0_C61 C63:murein4p4p_p0_C62 C64:murein4p4p_p0_C63 C65:murein4p4p_p0_C64 C66:murein4p4p_p0_C65 C67:murein4p4p_p0_C66 C68:murein4p4p_p0_C67 C69:murein4p4p_p0_C68 C70:murein4p4p_p0_C69 C71:murein4p4p_p0_C70 C72:murein4p4p_p0_C71 C73:murein4p4p_p0_C72 C74:murein4p4p_p0_C73) + 0.005448*Ec_biomass_iJO1366_WT_53p95M_murein4px4p_p_23.balance (C1:murein4px4p_p0_C0 C2:murein4px4p_p0_C1 C3:murein4px4p_p0_C2 C4:murein4px4p_p0_C3 C5:murein4px4p_p0_C4 C6:murein4px4p_p0_C5 C7:murein4px4p_p0_C6 C8:murein4px4p_p0_C7 C9:murein4px4p_p0_C8 C10:murein4px4p_p0_C9 C11:murein4px4p_p0_C10 C12:murein4px4p_p0_C11 C13:murein4px4p_p0_C12 C14:murein4px4p_p0_C13 C15:murein4px4p_p0_C14 C16:murein4px4p_p0_C15 C17:murein4px4p_p0_C16 C18:murein4px4p_p0_C17 C19:murein4px4p_p0_C18 C20:murein4px4p_p0_C19 C21:murein4px4p_p0_C20 C22:murein4px4p_p0_C21 C23:murein4px4p_p0_C22 C24:murein4px4p_p0_C23 C25:murein4px4p_p0_C24 C26:murein4px4p_p0_C25 C27:murein4px4p_p0_C26 C28:murein4px4p_p0_C27 C29:murein4px4p_p0_C28 C30:murein4px4p_p0_C29 C31:murein4px4p_p0_C30 C32:murein4px4p_p0_C31 C33:murein4px4p_p0_C32 C34:murein4px4p_p0_C33 C35:murein4px4p_p0_C34 C36:murein4px4p_p0_C35 C37:murein4px4p_p0_C36 C38:murein4px4p_p0_C37 C39:murein4px4p_p0_C38 C40:murein4px4p_p0_C39 C41:murein4px4p_p0_C40 C42:murein4px4p_p0_C41 C43:murein4px4p_p0_C42 C44:murein4px4p_p0_C43 C45:murein4px4p_p0_C44 C46:murein4px4p_p0_C45 C47:murein4px4p_p0_C46 C48:murein4px4p_p0_C47 C49:murein4px4p_p0_C48 C50:murein4px4p_p0_C49 C51:murein4px4p_p0_C50 C52:murein4px4p_p0_C51 C53:murein4px4p_p0_C52 C54:murein4px4p_p0_C53 C55:murein4px4p_p0_C54 C56:murein4px4p_p0_C55 C57:murein4px4p_p0_C56 C58:murein4px4p_p0_C57 C59:murein4px4p_p0_C58 C60:murein4px4p_p0_C59 C61:murein4px4p_p0_C60 C62:murein4px4p_p0_C61 C63:murein4px4p_p0_C62 C64:murein4px4p_p0_C63 C65:murein4px4p_p0_C64 C66:murein4px4p_p0_C65 C67:murein4px4p_p0_C66 C68:murein4px4p_p0_C67 C69:murein4px4p_p0_C68 C70:murein4px4p_p0_C69 C71:murein4px4p_p0_C70 C72:murein4px4p_p0_C71 C73:murein4px4p_p0_C72 C74:murein4px4p_p0_C73) + 0.000335*Ec_biomass_iJO1366_WT_53p95M_nadph_c_24.balance (C1:nadph_c0_C0 C2:nadph_c0_C1 C3:nadph_c0_C2 C4:nadph_c0_C3 C5:nadph_c0_C4 C6:nadph_c0_C5 C7:nadph_c0_C6 C8:nadph_c0_C7 C9:nadph_c0_C8 C10:nadph_c0_C9 C11:nadph_c0_C10 C12:nadph_c0_C11 C13:nadph_c0_C12 C14:nadph_c0_C13 C15:nadph_c0_C14 C16:nadph_c0_C15 C17:nadph_c0_C16 C18:nadph_c0_C17 C19:nadph_c0_C18 C20:nadph_c0_C19 C21:nadph_c0_C20) + 0.000045*Ec_biomass_iJO1366_WT_53p95M_nadh_c_25.balance (C1:nadh_c0_C0 C2:nadh_c0_C1 C3:nadh_c0_C2 C4:nadh_c0_C3 C5:nadh_c0_C4 C6:nadh_c0_C5 C7:nadh_c0_C6 C8:nadh_c0_C7 C9:nadh_c0_C8 C10:nadh_c0_C9 C11:nadh_c0_C10 C12:nadh_c0_C11 C13:nadh_c0_C12 C14:nadh_c0_C13 C15:nadh_c0_C14 C16:nadh_c0_C15 C17:nadh_c0_C16 C18:nadh_c0_C17 C19:nadh_c0_C18 C20:nadh_c0_C19 C21:nadh_c0_C20) + 0.004439*Ec_biomass_iJO1366_WT_53p95M_pg161_c_26.balance (C1:pg161_c0_C0 C2:pg161_c0_C1 C3:pg161_c0_C2 C4:pg161_c0_C3 C5:pg161_c0_C4 C6:pg161_c0_C5) + 0.012747*Ec_biomass_iJO1366_WT_53p95M_pe181_p_27.balance (C1:pe181_p0_C0 C2:pe181_p0_C1 C3:pe181_p0_C2 C4:pe181_p0_C3 C5:pe181_p0_C4) + 0.282306*Ec_biomass_iJO1366_WT_53p95M_ile_DASH_L_c_28.balance (C1:ile_DASH_L_c0_C0 C2:ile_DASH_L_c0_C1 C3:ile_DASH_L_c0_C2 C4:ile_DASH_L_c0_C3 C5:ile_DASH_L_c0_C4 C6:ile_DASH_L_c0_C5) + 0.000223*Ec_biomass_iJO1366_WT_53p95M_chor_c_29.balance (C1:chor_c0_C0 C2:chor_c0_C1 C3:chor_c0_C2 C4:chor_c0_C3 C5:chor_c0_C4 C6:chor_c0_C5 C7:chor_c0_C6 C8:chor_c0_C7 C9:chor_c0_C8 C10:chor_c0_C9) + 0.333448*Ec_biomass_iJO1366_WT_53p95M_lys_DASH_L_c_30.balance (C1:lys_DASH_L_c0_C0 C2:lys_DASH_L_c0_C1 C3:lys_DASH_L_c0_C2 C4:lys_DASH_L_c0_C3 C5:lys_DASH_L_c0_C4 C6:lys_DASH_L_c0_C5) + 0.000223*Ec_biomass_iJO1366_WT_53p95M_mlthf_c_31.balance (C1:mlthf_c0_C0) + 0.28742*Ec_biomass_iJO1366_WT_53p95M_arg_DASH_L_c_32.balance (C1:arg_DASH_L_c0_C0 C2:arg_DASH_L_c0_C1 C3:arg_DASH_L_c0_C2 C4:arg_DASH_L_c0_C3 C5:arg_DASH_L_c0_C4 C6:arg_DASH_L_c0_C5) + 0.499149*Ec_biomass_iJO1366_WT_53p95M_ala_DASH_L_c_33.balance (C1:ala_DASH_L_c0_C0 C2:ala_DASH_L_c0_C1 C3:ala_DASH_L_c0_C2) + 0.246506*Ec_biomass_iJO1366_WT_53p95M_thr_DASH_L_c_34.balance (C1:thr_DASH_L_c0_C0 C2:thr_DASH_L_c0_C1 C3:thr_DASH_L_c0_C2 C4:thr_DASH_L_c0_C3) + 0.088988*Ec_biomass_iJO1366_WT_53p95M_cys_DASH_L_c_35.balance (C1:cys_DASH_L_c0_C0 C2:cys_DASH_L_c0_C1 C3:cys_DASH_L_c0_C2) + 0.001787*Ec_biomass_iJO1366_WT_53p95M_nad_c_36.balance (C1:nad_c0_C0 C2:nad_c0_C1 C3:nad_c0_C2 C4:nad_c0_C3 C5:nad_c0_C4 C6:nad_c0_C5 C7:nad_c0_C6 C8:nad_c0_C7 C9:nad_c0_C8 C10:nad_c0_C9 C11:nad_c0_C10 C12:nad_c0_C11 C13:nad_c0_C12 C14:nad_c0_C13 C15:nad_c0_C14 C16:nad_c0_C15 C17:nad_c0_C16 C18:nad_c0_C17 C19:nad_c0_C18 C20:nad_c0_C19 C21:nad_c0_C20) + 0.180021*Ec_biomass_iJO1366_WT_53p95M_phe_DASH_L_c_37.balance (C1:phe_DASH_L_c0_C0 C2:phe_DASH_L_c0_C1 C3:phe_DASH_L_c0_C2 C4:phe_DASH_L_c0_C3 C5:phe_DASH_L_c0_C4 C6:phe_DASH_L_c0_C5 C7:phe_DASH_L_c0_C6 C8:phe_DASH_L_c0_C7 C9:phe_DASH_L_c0_C8) + 0.025612*Ec_biomass_iJO1366_WT_53p95M_dctp_c_38.balance (C1:dctp_c0_C0 C2:dctp_c0_C1 C3:dctp_c0_C2 C4:dctp_c0_C3 C5:dctp_c0_C4 C6:dctp_c0_C5 C7:dctp_c0_C6 C8:dctp_c0_C7 C9:dctp_c0_C8) + 0.149336*Ec_biomass_iJO1366_WT_53p95M_met_DASH_L_c_39.balance (C1:met_DASH_L_c0_C0 C2:met_DASH_L_c0_C1 C3:met_DASH_L_c0_C2 C4:met_DASH_L_c0_C3 C5:met_DASH_L_c0_C4) + 0.012366*Ec_biomass_iJO1366_WT_53p95M_pe160_c_40.balance (C1:pe160_c0_C0 C2:pe160_c0_C1 C3:pe160_c0_C2 C4:pe160_c0_C3 C5:pe160_c0_C4) + 0.209121*Ec_biomass_iJO1366_WT_53p95M_gtp_c_41.balance (C1:gtp_c0_C0 C2:gtp_c0_C1 C3:gtp_c0_C2 C4:gtp_c0_C3 C5:gtp_c0_C4 C6:gtp_c0_C5 C7:gtp_c0_C6 C8:gtp_c0_C7 C9:gtp_c0_C8 C10:gtp_c0_C9) + 0.437778*Ec_biomass_iJO1366_WT_53p95M_leu_DASH_L_c_42.balance (C1:leu_DASH_L_c0_C0 C2:leu_DASH_L_c0_C1 C3:leu_DASH_L_c0_C2 C4:leu_DASH_L_c0_C3 C5:leu_DASH_L_c0_C4 C6:leu_DASH_L_c0_C5) + 0.092056*Ec_biomass_iJO1366_WT_53p95M_his_DASH_L_c_43.balance (C1:his_DASH_L_c0_C0 C2:his_DASH_L_c0_C1 C3:his_DASH_L_c0_C2 C4:his_DASH_L_c0_C3 C5:his_DASH_L_c0_C4 C6:his_DASH_L_c0_C5) + 0.009618*Ec_biomass_iJO1366_WT_53p95M_pe161_c_44.balance (C1:pe161_c0_C0 C2:pe161_c0_C1 C3:pe161_c0_C2 C4:pe161_c0_C3 C5:pe161_c0_C4) + 0.000223*Ec_biomass_iJO1366_WT_53p95M_10fthf_c_45.balance (C1:10fthf_c0_C0) + 0.024805*Ec_biomass_iJO1366_WT_53p95M_datp_c_46.balance (C1:datp_c0_C0 C2:datp_c0_C1 C3:datp_c0_C2 C4:datp_c0_C3 C5:datp_c0_C4 C6:datp_c0_C5 C7:datp_c0_C6 C8:datp_c0_C7 C9:datp_c0_C8 C10:datp_c0_C9) + 0.000223*Ec_biomass_iJO1366_WT_53p95M_5mthf_c_47.balance (C1:5mthf_c0_C0) + 0.000673*Ec_biomass_iJO1366_WT_53p95M_murein4px4px4p_p_48.balance (C1:murein4px4px4p_p0_C0 C2:murein4px4px4p_p0_C1 C3:murein4px4px4p_p0_C2 C4:murein4px4px4p_p0_C3 C5:murein4px4px4p_p0_C4 C6:murein4px4px4p_p0_C5 C7:murein4px4px4p_p0_C6 C8:murein4px4px4p_p0_C7 C9:murein4px4px4p_p0_C8 C10:murein4px4px4p_p0_C9 C11:murein4px4px4p_p0_C10 C12:murein4px4px4p_p0_C11 C13:murein4px4px4p_p0_C12 C14:murein4px4px4p_p0_C13 C15:murein4px4px4p_p0_C14 C16:murein4px4px4p_p0_C15 C17:murein4px4px4p_p0_C16 C18:murein4px4px4p_p0_C17 C19:murein4px4px4p_p0_C18 C20:murein4px4px4p_p0_C19 C21:murein4px4px4p_p0_C20 C22:murein4px4px4p_p0_C21 C23:murein4px4px4p_p0_C22 C24:murein4px4px4p_p0_C23 C25:murein4px4px4p_p0_C24 C26:murein4px4px4p_p0_C25 C27:murein4px4px4p_p0_C26 C28:murein4px4px4p_p0_C27 C29:murein4px4px4p_p0_C28 C30:murein4px4px4p_p0_C29 C31:murein4px4px4p_p0_C30 C32:murein4px4px4p_p0_C31 C33:murein4px4px4p_p0_C32 C34:murein4px4px4p_p0_C33 C35:murein4px4px4p_p0_C34 C36:murein4px4px4p_p0_C35 C37:murein4px4px4p_p0_C36 C38:murein4px4px4p_p0_C37 C39:murein4px4px4p_p0_C38 C40:murein4px4px4p_p0_C39 C41:murein4px4px4p_p0_C40 C42:murein4px4px4p_p0_C41 C43:murein4px4px4p_p0_C42 C44:murein4px4px4p_p0_C43 C45:murein4px4px4p_p0_C44 C46:murein4px4px4p_p0_C45 C47:murein4px4px4p_p0_C46 C48:murein4px4px4p_p0_C47 C49:murein4px4px4p_p0_C48 C50:murein4px4px4p_p0_C49 C51:murein4px4px4p_p0_C50 C52:murein4px4px4p_p0_C51 C53:murein4px4px4p_p0_C52 C54:murein4px4px4p_p0_C53 C55:murein4px4px4p_p0_C54 C56:murein4px4px4p_p0_C55 C57:murein4px4px4p_p0_C56 C58:murein4px4px4p_p0_C57 C59:murein4px4px4p_p0_C58 C60:murein4px4px4p_p0_C59 C61:murein4px4px4p_p0_C60 C62:murein4px4px4p_p0_C61 C63:murein4px4px4p_p0_C62 C64:murein4px4px4p_p0_C63 C65:murein4px4px4p_p0_C64 C66:murein4px4px4p_p0_C65 C67:murein4px4px4p_p0_C66 C68:murein4px4px4p_p0_C67 C69:murein4px4px4p_p0_C68 C70:murein4px4px4p_p0_C69 C71:murein4px4px4p_p0_C70 C72:murein4px4px4p_p0_C71 C73:murein4px4px4p_p0_C72 C74:murein4px4px4p_p0_C73 C75:murein4px4px4p_p0_C74 C76:murein4px4px4p_p0_C75 C77:murein4px4px4p_p0_C76 C78:murein4px4px4p_p0_C77 C79:murein4px4px4p_p0_C78 C80:murein4px4px4p_p0_C79 C81:murein4px4px4p_p0_C80 C82:murein4px4px4p_p0_C81 C83:murein4px4px4p_p0_C82 C84:murein4px4px4p_p0_C83 C85:murein4px4px4p_p0_C84 C86:murein4px4px4p_p0_C85 C87:murein4px4px4p_p0_C86 C88:murein4px4px4p_p0_C87 C89:murein4px4px4p_p0_C88 C90:murein4px4px4p_p0_C89 C91:murein4px4px4p_p0_C90 C92:murein4px4px4p_p0_C91 C93:murein4px4px4p_p0_C92 C94:murein4px4px4p_p0_C93 C95:murein4px4px4p_p0_C94 C96:murein4px4px4p_p0_C95 C97:murein4px4px4p_p0_C96 C98:murein4px4px4p_p0_C97 C99:murein4px4px4p_p0_C98 C100:murein4px4px4p_p0_C99 C101:murein4px4px4p_p0_C100 C102:murein4px4px4p_p0_C101 C103:murein4px4px4p_p0_C102 C104:murein4px4px4p_p0_C103 C105:murein4px4px4p_p0_C104 C106:murein4px4px4p_p0_C105 C107:murein4px4px4p_p0_C106 C108:murein4px4px4p_p0_C107 C109:murein4px4px4p_p0_C108 C110:murein4px4px4p_p0_C109 C111:murein4px4px4p_p0_C110) + 0.024805*Ec_biomass_iJO1366_WT_53p95M_dttp_c_49.balance (C1:dttp_c0_C0 C2:dttp_c0_C1 C3:dttp_c0_C2 C4:dttp_c0_C3 C5:dttp_c0_C4 C6:dttp_c0_C5 C7:dttp_c0_C6 C8:dttp_c0_C7 C9:dttp_c0_C8 C10:dttp_c0_C9) + 0.000223*Ec_biomass_iJO1366_WT_53p95M_ribflv_c_50.balance (C1:ribflv_c0_C0 C2:ribflv_c0_C1 C3:ribflv_c0_C2 C4:ribflv_c0_C3 C5:ribflv_c0_C4 C6:ribflv_c0_C5 C7:ribflv_c0_C6 C8:ribflv_c0_C7 C9:ribflv_c0_C8 C10:ribflv_c0_C9 C11:ribflv_c0_C10 C12:ribflv_c0_C11 C13:ribflv_c0_C12 C14:ribflv_c0_C13 C15:ribflv_c0_C14 C16:ribflv_c0_C15 C17:ribflv_c0_C16) + 0.001345*Ec_biomass_iJO1366_WT_53p95M_murein3p3p_p_51.balance (C1:murein3p3p_p0_C0 C2:murein3p3p_p0_C1 C3:murein3p3p_p0_C2 C4:murein3p3p_p0_C3 C5:murein3p3p_p0_C4 C6:murein3p3p_p0_C5 C7:murein3p3p_p0_C6 C8:murein3p3p_p0_C7 C9:murein3p3p_p0_C8 C10:murein3p3p_p0_C9 C11:murein3p3p_p0_C10 C12:murein3p3p_p0_C11 C13:murein3p3p_p0_C12 C14:murein3p3p_p0_C13 C15:murein3p3p_p0_C14 C16:murein3p3p_p0_C15 C17:murein3p3p_p0_C16 C18:murein3p3p_p0_C17 C19:murein3p3p_p0_C18 C20:murein3p3p_p0_C19 C21:murein3p3p_p0_C20 C22:murein3p3p_p0_C21 C23:murein3p3p_p0_C22 C24:murein3p3p_p0_C23 C25:murein3p3p_p0_C24 C26:murein3p3p_p0_C25 C27:murein3p3p_p0_C26 C28:murein3p3p_p0_C27 C29:murein3p3p_p0_C28 C30:murein3p3p_p0_C29 C31:murein3p3p_p0_C30 C32:murein3p3p_p0_C31 C33:murein3p3p_p0_C32 C34:murein3p3p_p0_C33 C35:murein3p3p_p0_C34 C36:murein3p3p_p0_C35 C37:murein3p3p_p0_C36 C38:murein3p3p_p0_C37 C39:murein3p3p_p0_C38 C40:murein3p3p_p0_C39 C41:murein3p3p_p0_C40 C42:murein3p3p_p0_C41 C43:murein3p3p_p0_C42 C44:murein3p3p_p0_C43 C45:murein3p3p_p0_C44 C46:murein3p3p_p0_C45 C47:murein3p3p_p0_C46 C48:murein3p3p_p0_C47 C49:murein3p3p_p0_C48 C50:murein3p3p_p0_C49 C51:murein3p3p_p0_C50 C52:murein3p3p_p0_C51 C53:murein3p3p_p0_C52 C54:murein3p3p_p0_C53 C55:murein3p3p_p0_C54 C56:murein3p3p_p0_C55 C57:murein3p3p_p0_C56 C58:murein3p3p_p0_C57 C59:murein3p3p_p0_C58 C60:murein3p3p_p0_C59 C61:murein3p3p_p0_C60 C62:murein3p3p_p0_C61 C63:murein3p3p_p0_C62 C64:murein3p3p_p0_C63 C65:murein3p3p_p0_C64 C66:murein3p3p_p0_C65 C67:murein3p3p_p0_C66 C68:murein3p3p_p0_C67) + 0.004892*Ec_biomass_iJO1366_WT_53p95M_pg160_p_52.balance (C1:pg160_p0_C0 C2:pg160_p0_C1 C3:pg160_p0_C2 C4:pg160_p0_C3 C5:pg160_p0_C4 C6:pg160_p0_C5) + 0.129799*Ec_biomass_iJO1366_WT_53p95M_ctp_c_53.balance (C1:ctp_c0_C0 C2:ctp_c0_C1 C3:ctp_c0_C2 C4:ctp_c0_C3 C5:ctp_c0_C4 C6:ctp_c0_C5 C7:ctp_c0_C6 C8:ctp_c0_C7 C9:ctp_c0_C8) + 0.255712*Ec_biomass_iJO1366_WT_53p95M_glu_DASH_L_c_54.balance (C1:glu_DASH_L_c0_C0 C2:glu_DASH_L_c0_C1 C3:glu_DASH_L_c0_C2 C4:glu_DASH_L_c0_C3 C5:glu_DASH_L_c0_C4) + 0.214798*Ec_biomass_iJO1366_WT_53p95M_pro_DASH_L_c_55.balance (C1:pro_DASH_L_c0_C0 C2:pro_DASH_L_c0_C1 C3:pro_DASH_L_c0_C2 C4:pro_DASH_L_c0_C3 C5:pro_DASH_L_c0_C4) + 0.025612*Ec_biomass_iJO1366_WT_53p95M_dgtp_c_56.balance (C1:dgtp_c0_C0 C2:dgtp_c0_C1 C3:dgtp_c0_C2 C4:dgtp_c0_C3 C5:dgtp_c0_C4 C6:dgtp_c0_C5 C7:dgtp_c0_C6 C8:dgtp_c0_C7 C9:dgtp_c0_C8 C10:dgtp_c0_C9) + 0.255712*Ec_biomass_iJO1366_WT_53p95M_gln_DASH_L_c_57.balance (C1:gln_DASH_L_c0_C0 C2:gln_DASH_L_c0_C1 C3:gln_DASH_L_c0_C2 C4:gln_DASH_L_c0_C3 C5:gln_DASH_L_c0_C4) + 0.001961*Ec_biomass_iJO1366_WT_53p95M_pg181_p_58.balance (C1:pg181_p0_C0 C2:pg181_p0_C1 C3:pg181_p0_C2 C4:pg181_p0_C3 C5:pg181_p0_C4 C6:pg181_p0_C5) + 0.024732*Ec_biomass_iJO1366_WT_53p95M_pe161_p_59.balance (C1:pe161_p0_C0 C2:pe161_p0_C1 C3:pe161_p0_C2 C4:pe161_p0_C3 C5:pe161_p0_C4) + 0.00118*Ec_biomass_iJO1366_WT_53p95M_clpn181_p_60.balance (C1:clpn181_p0_C0 C2:clpn181_p0_C1 C3:clpn181_p0_C2 C4:clpn181_p0_C3 C5:clpn181_p0_C4 C6:clpn181_p0_C5 C7:clpn181_p0_C6 C8:clpn181_p0_C7 C9:clpn181_p0_C8) + 0.003805*Ec_biomass_iJO1366_WT_53p95M_pg161_p_61.balance (C1:pg161_p0_C0 C2:pg161_p0_C1 C3:pg161_p0_C2 C4:pg161_p0_C3 C5:pg161_p0_C4 C6:pg161_p0_C5) + 0.000279*Ec_biomass_iJO1366_WT_53p95M_accoa_c_62.balance (C1:accoa_c0_C0 C2:accoa_c0_C1 C3:accoa_c0_C2 C4:accoa_c0_C3 C5:accoa_c0_C4 C6:accoa_c0_C5 C7:accoa_c0_C6 C8:accoa_c0_C7 C9:accoa_c0_C8 C10:accoa_c0_C9 C11:accoa_c0_C10 C12:accoa_c0_C11 C13:accoa_c0_C12 C14:accoa_c0_C13 C15:accoa_c0_C14 C16:accoa_c0_C15 C17:accoa_c0_C16 C18:accoa_c0_C17 C19:accoa_c0_C18 C20:accoa_c0_C19 C21:accoa_c0_C20 C22:accoa_c0_C21 C23:accoa_c0_C22) + 54.119975*Ec_biomass_iJO1366_WT_53p95M_atp_c_63.balance (C1:atp_c0_C0 C2:atp_c0_C1 C3:atp_c0_C2 C4:atp_c0_C3 C5:atp_c0_C4 C6:atp_c0_C5 C7:atp_c0_C6 C8:atp_c0_C7 C9:atp_c0_C8 C10:atp_c0_C9) + 0.133993*Ec_biomass_iJO1366_WT_53p95M_tyr_DASH_L_c_64.balance (C1:tyr_DASH_L_c0_C0 C2:tyr_DASH_L_c0_C1 C3:tyr_DASH_L_c0_C2 C4:tyr_DASH_L_c0_C3 C5:tyr_DASH_L_c0_C4 C6:tyr_DASH_L_c0_C5 C7:tyr_DASH_L_c0_C6 C8:tyr_DASH_L_c0_C7 C9:tyr_DASH_L_c0_C8) + 0.006744*Ec_biomass_iJO1366_WT_53p95M_spmd_c_65.balance (C1:spmd_c0_C0 C2:spmd_c0_C1 C3:spmd_c0_C2 C4:spmd_c0_C3 C5:spmd_c0_C4 C6:spmd_c0_C5 C7:spmd_c0_C6) + 0.002944*Ec_biomass_iJO1366_WT_53p95M_clpn160_p_66.balance (C1:clpn160_p0_C0 C2:clpn160_p0_C1 C3:clpn160_p0_C2 C4:clpn160_p0_C3 C5:clpn160_p0_C4 C6:clpn160_p0_C5 C7:clpn160_p0_C6 C8:clpn160_p0_C7 C9:clpn160_p0_C8) + 0.00229*Ec_biomass_iJO1366_WT_53p95M_clpn161_p_67.balance (C1:clpn161_p0_C0 C2:clpn161_p0_C1 C3:clpn161_p0_C2 C4:clpn161_p0_C3 C5:clpn161_p0_C4 C6:clpn161_p0_C5 C7:clpn161_p0_C6 C8:clpn161_p0_C7 C9:clpn161_p0_C8) + 53.945874*pi_c + 53.95*h_c ';
    #table initializations:
    def drop_datastage02(self):
        try:
            data_stage02_isotopomer_tracers.__table__.drop(engine,True);
            data_stage02_isotopomer_models.__table__.drop(engine,True);
            data_stage02_isotopomer_modelReactions.__table__.drop(engine,True);
            data_stage02_isotopomer_modelMetabolites.__table__.drop(engine,True);
            data_stage02_isotopomer_measuredFluxes.__table__.drop(engine,True);
            data_stage02_isotopomer_measuredPools.__table__.drop(engine,True);
            data_stage02_isotopomer_measuredFragments.__table__.drop(engine,True);
            data_stage02_isotopomer_atomMappingReactions.__table__.drop(engine,True);
            data_stage02_isotopomer_atomMappingMetabolites.__table__.drop(engine,True);
            data_stage02_isotopomer_fittedFluxes.__table__.drop(engine,True);
            data_stage02_isotopomer_fittedFragments.__table__.drop(engine,True);
            data_stage02_isotopomer_fittedData.__table__.drop(engine,True);
            data_stage02_isotopomer_fittedMeasuredFluxes.__table__.drop(engine,True);
            data_stage02_isotopomer_fittedMeasuredFragments.__table__.drop(engine,True);
            data_stage02_isotopomer_fittedMeasuredFluxResiduals.__table__.drop(engine,True);
            data_stage02_isotopomer_fittedMeasuredFragmentResiduals.__table__.drop(engine,True);
            data_stage02_isotopomer_simulationParameters.__table__.drop(engine,True);
            data_stage02_isotopomer_fittedNetFluxes.__table__.drop(engine,True);
        except SQLAlchemyError as e:
            print(e);
    def reset_datastage02(self,experiment_id_I = None,simulation_id_I = None):
        try:
            if experiment_id_I:
                reset = self.session.query(data_stage02_isotopomer_simulation).filter(data_stage02_isotopomer_simulation.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_isotopomer_tracers).filter(data_stage02_isotopomer_tracers.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_isotopomer_measuredFluxes).filter(data_stage02_isotopomer_measuredFluxes.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_isotopomer_measuredPools).filter(data_stage02_isotopomer_measuredPools.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_isotopomer_measuredFragments).filter(data_stage02_isotopomer_measuredFragments.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
            elif simulation_id_I:
                reset = self.session.query(data_stage02_isotopomer_fittedFluxes).filter(data_stage02_isotopomer_fittedFluxes.simulation_id.like(simulation_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_isotopomer_fittedFragments).filter(data_stage02_isotopomer_fittedFluxes.simulation_id.like(simulation_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_isotopomer_fittedData).filter(data_stage02_isotopomer_fittedData.simulation_id.like(simulation_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_isotopomer_fittedMeasuredFluxes).filter(data_stage02_isotopomer_fittedMeasuredFluxes.simulation_id.like(simulation_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_isotopomer_fittedMeasuredFragments).filter(data_stage02_isotopomer_fittedMeasuredFragments.simulation_id.like(simulation_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_isotopomer_fittedMeasuredFluxResiduals).filter(data_stage02_isotopomer_fittedMeasuredFluxResiduals.simulation_id.like(simulation_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_isotopomer_fittedMeasuredFragmentResiduals).filter(data_stage02_isotopomer_fittedMeasuredFragmentResiduals.simulation_id.like(simulation_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_isotopomer_simulationParameters).filter(data_stage02_isotopomer_simulationParameters.simulation_id.like(simulation_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_isotopomer_fittedNetFluxes).filter(data_stage02_isotopomer_fittedNetFluxes.simulation_id.like(simulation_id_I)).delete(synchronize_session=False);
            else:
                reset = self.session.query(data_stage02_isotopomer_simulation).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_isotopomer_tracers).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_isotopomer_models).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_isotopomer_measuredFluxes).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_isotopomer_modelMetabolites).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_isotopomer_modelReactions).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_isotopomer_measuredPools).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_isotopomer_measuredFragments).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_isotopomer_atomMappingReactions).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_isotopomer_atomMappingMetabolites).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_isotopomer_fittedFluxes).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_isotopomer_fittedFragments).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_isotopomer_fittedData).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_isotopomer_fittedMeasuredFluxes).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_isotopomer_fittedMeasuredFragments).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_isotopomer_fittedMeasuredFluxResiduals).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_isotopomer_fittedMeasuredFragmentResiduals).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_isotopomer_simulationParameters).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_isotopomer_fittedNetFluxes).delete(synchronize_session=False);
            self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def reset_datastage02_isotopomer_fittedNetFluxes(self,simulation_id_I = None):
        try:
            reset = self.session.query(data_stage02_isotopomer_fittedNetFluxes).filter(data_stage02_isotopomer_fittedNetFluxes.simulation_id.like(simulation_id_I)).delete(synchronize_session=False);
            self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def reset_datastage02_isotopomer_measuredPools(self,experiment_id_I = None):
        try:
            reset = self.session.query(data_stage02_isotopomer_measuredPools).filter(data_stage02_isotopomer_measuredPools.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
            self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def reset_datastage02_isotopomer_measuredFluxes(self,experiment_id_I = None):
        try:
            reset = self.session.query(data_stage02_isotopomer_measuredFluxes).filter(data_stage02_isotopomer_measuredFluxes.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
            self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def reset_datastage02_isotopomer_measuredFragments(self,experiment_id_I = None):
        try:
            reset = self.session.query(data_stage02_isotopomer_measuredFragments).filter(data_stage02_isotopomer_measuredFragments.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
            self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def initialize_datastage02(self):
        try:
            data_stage02_isotopomer_simulation.__table__.create(engine,True);
            data_stage02_isotopomer_tracers.__table__.create(engine,True);
            data_stage02_isotopomer_models.__table__.create(engine,True);
            data_stage02_isotopomer_measuredFluxes.__table__.create(engine,True);
            data_stage02_isotopomer_modelMetabolites.__table__.create(engine,True);
            data_stage02_isotopomer_modelReactions.__table__.create(engine,True);
            data_stage02_isotopomer_measuredPools.__table__.create(engine,True);
            data_stage02_isotopomer_measuredFragments.__table__.create(engine,True);
            data_stage02_isotopomer_atomMappingReactions.__table__.create(engine,True);
            data_stage02_isotopomer_atomMappingMetabolites.__table__.create(engine,True);
            data_stage02_isotopomer_fittedFluxes.__table__.create(engine,True);
            data_stage02_isotopomer_fittedFragments.__table__.create(engine,True);
            data_stage02_isotopomer_fittedData.__table__.create(engine,True);
            data_stage02_isotopomer_fittedMeasuredFluxes.__table__.create(engine,True);
            data_stage02_isotopomer_fittedMeasuredFragments.__table__.create(engine,True);
            data_stage02_isotopomer_fittedMeasuredFluxResiduals.__table__.create(engine,True);
            data_stage02_isotopomer_fittedMeasuredFragmentResiduals.__table__.create(engine,True);
            data_stage02_isotopomer_simulationParameters.__table__.create(engine,True);
            data_stage02_isotopomer_fittedNetFluxes.__table__.create(engine,True);
        except SQLAlchemyError as e:
            print(e);
    #analysis
    def execute_makeMeasuredFragments(self,experiment_id_I, sample_name_abbreviations_I = [], time_points_I = [], scan_types_I = [], met_ids_I = []):
        '''Collect and format MS data from data_stage01_isotopomer_averagesNormSum for fluxomics simulation'''
        # get experiment information:
        met_id_conv_dict = {'Hexose_Pool_fru_glc-D':'glc-D',
                            'Pool_2pg_3pg':'3pg',
                            '23dpg':'13dpg'};
        data_O = [];
        experiment_stdev = [];
        # get sample names and sample name abbreviations
        if sample_name_abbreviations_I:
            sample_abbreviations = sample_name_abbreviations_I;
            st = 'Unknown';
            sample_types_lst = [];
            sample_types_lst.extend([st for i in range(len(sample_abbreviations))]);
        else:
            sample_abbreviations = [];
            sample_types = ['Unknown'];
            sample_types_lst = [];
            for st in sample_types:
                sample_abbreviations_tmp = [];
                sample_abbreviations_tmp = self.stage02_isotopomer_query.get_sampleNameAbbreviations_experimentIDAndSampleType_dataStage01AveragesNormSum(experiment_id_I,st);
                sample_abbreviations.extend(sample_abbreviations_tmp);
                sample_types_lst.extend([st for i in range(len(sample_abbreviations_tmp))]);
        for sna_cnt,sna in enumerate(sample_abbreviations):
            print 'Collecting experimental MS data for sample name abbreviation ' + sna;
            # get time points
            if time_points_I:
                time_points = time_points_I;
            else:
                time_points = [];
                time_points = self.stage02_isotopomer_query.get_timePoint_experimentIDAndSampleNameAbbreviation_dataStage01AveragesNormSum(experiment_id_I,sna);
            for tp in time_points:
                print 'Collecting experimental MS data for time-point ' + str(tp);
                # get the scan_types
                if scan_types_I:
                    scan_types = [];
                    scan_types_tmp = [];
                    scan_types_tmp = self.stage02_isotopomer_query.get_scanTypes_experimentIDAndTimePointAndSampleAbbreviationsAndSampleType_dataStage01AveragesNormSum(experiment_id_I,tp,sna,sample_types_lst[sna_cnt]);
                    scan_types = [st for st in scan_types_tmp if st in scan_types_I];
                else:
                    scan_types = [];
                    scan_types = self.stage02_isotopomer_query.get_scanTypes_experimentIDAndTimePointAndSampleAbbreviationsAndSampleType_dataStage01AveragesNormSum(experiment_id_I,tp,sna,sample_types_lst[sna_cnt]);
                for scan_type in scan_types:
                    print 'Collecting experimental MS data for scan type ' + scan_type
                    # met_ids
                    if not met_ids_I:
                        met_ids = [];
                        met_ids = self.stage02_isotopomer_query.get_metIDs_experimentIDAndSampleAbbreviationAndTimePointAndSampleTypeAndScanType_dataStage01AveragesNormSum( \
                                experiment_id_I,sna,tp,sample_types_lst[sna_cnt],scan_type);
                    else:
                        met_ids = met_ids_I;
                    if not(met_ids): continue #no component information was found
                    for met in met_ids:
                        print 'Collecting experimental MS data for metabolite ' + met;
                        # format the metabolite
                        if met in met_id_conv_dict.keys():
                            met_formatted = met_id_conv_dict[met];
                        else: met_formatted = met;
                        met_formatted = re.sub('-','_DASH_',met_formatted)
                        met_formatted = re.sub('[(]','_LPARANTHES_',met_formatted)
                        met_formatted = re.sub('[)]','_RPARANTHES_',met_formatted)
                        # fragments
                        fragment_formulas = [];
                        fragment_formulas = self.stage02_isotopomer_query.get_fragmentFormula_experimentIDAndSampleAbbreviationAndTimePointAndSampleTypeAndScanTypeAndMetID_dataStage01AveragesNormSum( \
                                experiment_id_I,sna,tp,sample_types_lst[sna_cnt],scan_type,met);
                        # frag c map
                        frag_cmap = {};
                        frag_cmap = self.stage02_isotopomer_query.get_precursorFormulaAndProductFormulaAndCMapsAndPositions_metID(met,'-','tuning');
                        for frag in fragment_formulas:
                            # data
                            data_mat = [];
                            data_mat_cv = [];
                            data_mat_n = [];
                            data_mat, data_mat_cv, data_mat_n = self.stage02_isotopomer_query.get_spectrum_experimentIDAndSampleAbbreviationAndTimePointAndSampleTypeAndScanTypeAndMetIDAndFragmentFormula_dataStage01AveragesNormSum( \
                                experiment_id_I,sna,tp,sample_types_lst[sna_cnt],scan_type,met,frag);
                            # combine into a structure
                            positions,elements = [],[];
                            positions,elements = self.convert_fragmentAndElements2PositionAndElements(frag_cmap[frag]['fragment'],frag_cmap[frag]['fragment_elements']);
                            fragname = met_formatted+'_c'+'_'+ re.sub('[-+]','',frag);
                            data_names = [];
                            data_stdev = [];
                            data_stderr = [];
                            for i,d in enumerate(data_mat):
                                stdev = 0.0;
                                stderr = 0.0;
                                if data_mat_cv[i]: 
                                    stdev = data_mat[i]*data_mat_cv[i]/100;
                                    stderr = stdev/sqrt(data_mat_n[i]);
                                data_names.append(fragname+str(i));
                                data_stdev.append(stdev);
                                data_stderr.append(stderr);
                                experiment_stdev.append(stdev);
                            data_tmp = {'experiment_id':experiment_id_I,
                                           'sample_name_abbreviation':sna,
                                           'sample_type':sample_types_lst[sna_cnt],
                                           'time_point':tp,
                                            'met_id':met_formatted+'_c',
                                            'fragment_id':fragname,
                                            'fragment_formula':frag,
                                            'intensity_normalized_average':data_mat,
                                            'intensity_normalized_cv':data_mat_cv,
                                            'intensity_normalized_stdev':data_stdev,
                                            'intensity_normalized_n':data_mat_n,
                                            'intensity_normalized_units':'normSum',
                                            'met_elements':elements,
                                            'met_atompositions':positions};
                            data_O.append(data_tmp);
                            #add data to the database
                            row = [];
                            row = data_stage02_isotopomer_measuredFragments(
                                    experiment_id_I,
                                    sna,
                                    tp,
                                    met_formatted+'_c',
                                    fragname,
                                    frag,
                                    data_mat,
                                    data_mat_cv,
                                    data_stdev,
                                    'normSum',
                                    scan_type,
                                    elements,
                                    positions,
                                    True,
                                    None);
                            self.session.add(row);
        self.session.commit();
    def execute_addMeasuredFluxes(self,experiment_id_I, ko_list={}, flux_dict={}, model_ids_I=[], sample_name_abbreviations_I=[]):
        '''Add flux data for physiological simulation'''
        #Input:
            #flux_dict = {};
            #flux_dict['iJO1366'] = {};
            #flux_dict['iJO1366'] = {};
            #flux_dict['iJO1366']['sna'] = {};
            #flux_dict['iJO1366']['sna']['Ec_biomass_iJO1366_WT_53p95M'] = {'ave':None,'stdev':None,'units':'mmol*gDCW-1*hr-1','lb':0.704*0.9,'ub':0.704*1.1};
            #flux_dict['iJO1366']['sna']['EX_ac_LPAREN_e_RPAREN_'] = {'ave':None,'stdev':None,'units':'mmol*gDCW-1*hr-1','lb':2.13*0.9,'ub':2.13*1.1};
            #flux_dict['iJO1366']['sna']['EX_o2_LPAREN_e_RPAREN__reverse'] = {'ave':None,'units':'mmol*gDCW-1*hr-1','stdev':None,'lb':0,'ub':16};
            #flux_dict['iJO1366']['sna']['EX_glc_LPAREN_e_RPAREN_'] = {'ave':None,'stdev':None,'units':'mmol*gDCW-1*hr-1','lb':-7.4*1.1,'ub':-7.4*0.9};

        data_O = [];
        # get the model ids:
        if model_ids_I:
            model_ids = model_ids_I;
        else:
            model_ids = [];
            model_ids = self.stage02_isotopomer_query.get_modelID_experimentID_dataStage02IstopomerSimulation(experiment_id_I);
        for model_id in model_ids:
            # get sample names and sample name abbreviations
            if sample_name_abbreviations_I:
                sample_name_abbreviations = sample_name_abbreviations_I;
            else:
                sample_name_abbreviations = [];
                sample_name_abbreviations = self.stage02_isotopomer_query.get_sampleNameAbbreviations_experimentIDAndModelID_dataStage02IstopomerSimulation(experiment_id_I,model_id);
            for sna_cnt,sna in enumerate(sample_name_abbreviations):
                print 'Adding experimental fluxes for sample name abbreviation ' + sna;
                if flux_dict:
                    for k,v in flux_dict[model_id][sna].iteritems():
                        # record the data
                        data_tmp = {'experiment_id':experiment_id_I,
                                'model_id':model_id,
                                'sample_name_abbreviation':sna,
                                'rxn_id':k,
                                'flux_average':v['ave'],
                                'flux_stdev':v['stdev'],
                                'flux_lb':v['lb'], 
                                'flux_ub':v['ub'],
                                'flux_units':v['units'],
                                'used_':True,
                                'comment_':None}
                        data_O.append(data_tmp);
                        #add data to the database
                        row = [];
                        row = data_stage02_isotopomer_measuredFluxes(
                            experiment_id_I,
                            model_id,
                            sna,
                            k,
                            v['ave'],
                            v['stdev'],
                            v['lb'], 
                            v['ub'],
                            v['units'],
                            True,
                            None);
                        self.session.add(row);
                if ko_list:
                    for k in ko_list[model_id][sna]:
                        # record the data
                        data_tmp = {'experiment_id':experiment_id_I,
                                'model_id':model_id,
                                'sample_name_abbreviation':sna,
                                'rxn_id':k,
                                'flux_average':0.0,
                                'flux_stdev':0.0,
                                'flux_lb':0.0, 
                                'flux_ub':0.0,
                                'flux_units':'mmol*gDCW-1*hr-1',
                                'used_':True,
                                'comment_':None}
                        data_O.append(data_tmp);
                        #add data to the database
                        row = [];
                        row = data_stage02_isotopomer_measuredFluxes(
                            experiment_id_I,
                            model_id,
                            sna,
                            k,
                            0.0,
                            0.0,
                            0.0, 
                            0.0,
                            'mmol*gDCW-1*hr-1',
                            True,
                            None);
                        self.session.add(row);
        self.session.commit();
    def execute_makeMeasuredFluxes(self,experiment_id_I, metID2RxnID_I = {}, sample_name_abbreviations_I = [], met_ids_I = [],snaIsotopomer2snaPhysiology_I={}):
        '''Collect and flux data from data_stage01_physiology_ratesAverages for fluxomics simulation'''
        #Input:
        #   metID2RxnID_I = e.g. {'glc-D':{'model_id':'140407_iDM2014','rxn_id':'EX_glc_LPAREN_e_RPAREN_'},
                                #'ac':{'model_id':'140407_iDM2014','rxn_id':'EX_ac_LPAREN_e_RPAREN_'},
                                #'succ':{'model_id':'140407_iDM2014','rxn_id':'EX_succ_LPAREN_e_RPAREN_'},
                                #'lac-L':{'model_id':'140407_iDM2014','rxn_id':'EX_lac_DASH_L_LPAREN_e_RPAREN_'},
                                #'biomass':{'model_id':'140407_iDM2014','rxn_id':'Ec_biomass_iJO1366_WT_53p95M'}};
        #   snaIsotopomer2snaPhysiology_I = {'OxicEvo04Ecoli13CGlc':'OxicEvo04EcoliGlc',
                                #'OxicEvo04gndEcoli13CGlc':'OxicEvo04gndEcoliGlc',
                                #'OxicEvo04pgiEcoli13CGlc':'OxicEvo04pgiEcoliGlc',
                                #'OxicEvo04sdhCBEcoli13CGlc':'OxicEvo04sdhCBEcoliGlc',
                                #'OxicEvo04tpiAEcoli13CGlc':'OxicEvo04tpiAEcoliGlc'}

        '''TODO:'''
        #   Need to implement a way to detect the direction of the reaction,
        #   and change direction of the rate accordingly

        data_O = [];
        # get sample names and sample name abbreviations
        if sample_name_abbreviations_I:
            sample_name_abbreviations = sample_name_abbreviations_I;
        else:
            sample_name_abbreviations = [];
            sample_name_abbreviations = self.stage02_isotopomer_query.get_sampleNameAbbreviations_experimentID_dataStage02IsotopomerSimulation(experiment_id_I);
        for sna in sample_name_abbreviations:
            print 'Collecting experimental fluxes for sample name abbreviation ' + sna;
            query_sna = sna;
            if snaIsotopomer2snaPhysiology_I: query_sna = snaIsotopomer2snaPhysiology_I[sna];
            # get met_ids
            if not met_ids_I:
                met_ids = [];
                met_ids = self.stage02_isotopomer_query.get_metID_experimentIDAndSampleNameAbbreviation_dataStage01PhysiologyRatesAverages(experiment_id_I,query_sna);
            else:
                met_ids = met_ids_I;
            if not(met_ids): continue #no component information was found
            for met in met_ids:
                print 'Collecting experimental fluxes for metabolite ' + met;
                # get rateData
                slope_average, intercept_average, rate_average, rate_lb, rate_ub, rate_units, rate_var = None,None,None,None,None,None,None;
                slope_average, intercept_average, rate_average, rate_lb, rate_ub, rate_units, rate_var = self.stage02_isotopomer_query.get_rateData_experimentIDAndSampleNameAbbreviationAndMetID_dataStage01PhysiologyRatesAverages(experiment_id_I,query_sna,met);
                rate_stdev = sqrt(rate_var);
                model_id = metID2RxnID_I[met]['model_id'];
                rxn_id = metID2RxnID_I[met]['rxn_id'];
                # record the data
                data_tmp = {'experiment_id':experiment_id_I,
                        'model_id':model_id,
                        'sample_name_abbreviation':sna,
                        'rxn_id':rxn_id,
                        'flux_average':rate_average,
                        'flux_stdev':rate_stdev,
                        'flux_lb':rate_lb, 
                        'flux_ub':rate_ub,
                        'flux_units':rate_units,
                        'used_':True,
                        'comment_':None}
                data_O.append(data_tmp);
                #add data to the database
                row = [];
                row = data_stage02_isotopomer_measuredFluxes(
                    experiment_id_I,
                    model_id,
                    sna,
                    rxn_id,
                    rate_average,
                    rate_stdev,
                    rate_lb, 
                    rate_ub,
                    rate_units,
                    True,
                    None);
                self.session.add(row);
        self.session.commit();
    def execute_makeIsotopomerSimulation_INCA(self,simulation_id_I, stationary_I = True, parallel_I = False, ko_list_I=[],flux_dict_I={},description_I=None):
        '''export a fluxomics experimental data for simulation using INCA'''
        #Input:
        #   stationary_I = boolean
        #                  indicates whether each time-point is written to a separate file, or part of a time-course
        #   parallel_I = boolean
        #                  indicates whether multiple tracers were used

        inca = inca_api();

        # get simulation information
        simulation_info = {};
        simulation_info = self.stage02_isotopomer_query.get_simulation_simulationID_dataStage02IsotopomerSimulation(simulation_id_I);

        # extract model/mapping info
        if len(simulation_info['model_id'])>1 or len(simulation_info['mapping_id'])>1:
            print 'multiple model and mapping ids found for the simulation!';
            print 'only the first model/mapping id will be used';
        # determine if the simulation is a parallel labeling experiment, non-stationary, or both
        multiple_experiment_ids = False;
        multiple_snas = False;
        multiple_time_points = False;
        if len(simulation_info['experiment_id'])>1 and len(simulation_info['sample_name_abbreviation'])>1:
            print 'multiple experiment_ids and sample_name_abbreviations found for the simulation!'
            print 'only 1 experiment_ids and with multiple sample_name_abbreviations or 1 sample_name_abbreviation with multiple experiments can be specified'
        elif len(simulation_info['experiment_id'])>1:
            multiple_experiment_ids = True;
        elif len(simulation_info['sample_name_abbreviation'])>1:
            multiple_snas = True;
        if len(simulation_info['time_point'])>1:
            multiple_time_points = True;

        if parallel_I and multiple_experiment_ids:
            inca.make_isotopomerSimulation_parallel_experimentID_INCA(simulation_info,stationary_I,ko_list_I,flux_dict_I,description_I)
        elif parallel_I and multiple_snas:
            inca.make_isotopomerSimulation_parallel_sna_INCA(simulation_info,stationary_I,ko_list_I,flux_dict_I,description_I)
        else:
            inca.make_isotopomerSimulation_individual_INCA(simulation_info,stationary_I,ko_list_I,flux_dict_I,description_I)
    def execute_makeNetFluxes(self, simulation_id_I):
        '''Determine the net flux through a reaction'''
        
        data_O = [];
        # simulation_dateAndTime
        simulation_dateAndTimes = [];
        simulation_dateAndTimes = self.stage02_isotopomer_query.get_simulationDateAndTimes_simulationID_dataStage02IsotopomerfittedFluxes(simulation_id_I);
        for simulation_dateAndTime in simulation_dateAndTimes:
            # get all reactions included in the simulation (in alphabetical order)
            rxns = [];
            rxns = self.stage02_isotopomer_query.get_rxnIDs_simulationIDAndSimulationDateAndTime_dataStage02IsotopomerfittedFluxes(simulation_id_I,simulation_dateAndTime)
            # group into forward and reverse reactions
            rxns_pairs = {};
            rxn_pair = [];
            for rxn_cnt,rxn in enumerate(rxns):
                if not rxn_pair:
                    rxn_pair.append(rxn);
                else:
                    if '_reverse' in rxn and rxn_pair[0] in rxn:
                        rxn_pair.append(rxn);
                        rxns_pairs[rxn_pair[0]]=rxn_pair;
                        rxn_pair = [];
                    elif '_reverse' in rxn_pair[0]:
                        rxn_pair.insert(0,None);
                        rxn_name = rxn_pair[1].replace('_reverse','');
                        rxns_pairs[rxn_name]=rxn_pair;
                        rxn_pair = [];
                        rxn_pair.append(rxn);
                    else:
                        rxn_pair.append(None);
                        rxns_pairs[rxn_pair[0]]=rxn_pair;
                        rxn_pair = [];
                        rxn_pair.append(rxn);
            # calculate the net reaction flux average, stdev, lb and ub
            for k,v in rxns_pairs.iteritems():
                flux_average_1 = 0.0
                flux_average_2 = 0.0
                flux_stdev_1 = 0.0
                flux_stdev_2 = 0.0
                flux_lb_1 = 0.0
                flux_lb_2 = 0.0
                flux_ub_1 = 0.0
                flux_ub_2 = 0.0
                flux_units_1 = None
                flux_units_2 = None
                # get the flux data
                if v[0]:
                    flux_average_1,flux_stdev_1,flux_lb_1,flux_ub_1,flux_units_1 = self.stage02_isotopomer_query.get_flux_simulationIDAndSimulationDateAndTimeAndRxnID_dataStage02IsotopomerfittedFluxes(simulation_id_I,simulation_dateAndTime,v[0]);
                if v[1]:
                    flux_average_2,flux_stdev_2,flux_lb_2,flux_ub_2,flux_units_2 = self.stage02_isotopomer_query.get_flux_simulationIDAndSimulationDateAndTimeAndRxnID_dataStage02IsotopomerfittedFluxes(simulation_id_I,simulation_dateAndTime,v[1]);
                # determine if the fluxes are observable
                observable_1 = self.check_observableFlux(flux_average_1,flux_lb_1,flux_ub_1)
                observable_2 = self.check_observableFlux(flux_average_2,flux_lb_2,flux_ub_2)
                ## calculate the net flux
                #if k=='SUCOAS':
                #    print 'check';
                flux_average,flux_stdev,flux_lb,flux_ub,flux_units = self.calculate_netFlux(flux_average_1,flux_stdev_1,flux_lb_1,flux_ub_1,flux_units_1,
                          flux_average_2,flux_stdev_2,flux_lb_2,flux_ub_2,flux_units_2)
                # correct the flux stdev
                flux_stdev = self.correct_fluxStdev(flux_lb,flux_ub)
                # record net reaction flux
                data_O.append({'simulation_id':simulation_id_I,
                            'simulation_dateAndTime':simulation_dateAndTime,
                            'rxn_id':k,
                            'flux':flux_average,
                            'flux_stdev':flux_stdev,
                            'flux_lb':flux_lb,
                            'flux_ub':flux_ub,
                            'flux_units':flux_units,
                            'used_':True,
                            'comment_':None})
        # add data to the database:
        for d in data_O:
            try:
                data_add = data_stage02_isotopomer_fittedNetFluxes(d['simulation_id'],
                d['simulation_dateAndTime'],
                d['rxn_id'],
                d['flux'],
                d['flux_stdev'],
                d['flux_lb'],
                d['flux_ub'],
                d['flux_units'],
                d['used_'],
                d['comment_']);
                self.session.add(data_add);
            except SQLAlchemyError as e:
                print(e);
        self.session.commit();
    #internal functions
    def simulate_model(self,model_id_I,ko_list=[],flux_dict={},measured_flux_list=[],description=None):
        '''simulate a cobra model'''
        
        # Dependencies from cobra
        from cobra.io.sbml import create_cobra_model_from_sbml_file
        from cobra.io import save_json_model, load_json_model
        from cobra.flux_analysis.variability import flux_variability_analysis
        from cobra.flux_analysis.parsimonious import optimize_minimal_flux
        from cobra.flux_analysis import flux_variability_analysis

        # get the xml model
        cobra_model_sbml = ''
        cobra_model_sbml = self.stage02_isotopomer_query.get_row_modelID_dataStage02IsotopomerModels(model_id_I);
        # load the model
        if cobra_model_sbml:
            if cobra_model_sbml['file_type'] == 'sbml':
                with open(settings.workspace_data + '/cobra_model_tmp.xml','wb') as file:
                    file.write(cobra_model_sbml['model_file']);
                    file.close()
                cobra_model = None;
                cobra_model = create_cobra_model_from_sbml_file(settings.workspace_data + '/cobra_model_tmp.xml', print_time=True);
            elif cobra_model_sbml['file_type'] == 'json':
                with open(settings.workspace_data + '/cobra_model_tmp.json','wb') as file:
                    file.write(cobra_model_sbml['model_file']);
                    file.close()
                cobra_model = None;
                cobra_model = load_json_model(settings.workspace_data + '/cobra_model_tmp.json');
            else:
                print 'file_type not supported'
        # implement optimal KOs and flux constraints:
        for ko in ko_list:
            cobra_model.reactions.get_by_id(ko).lower_bound = 0.0;
            cobra_model.reactions.get_by_id(ko).upper_bound = 0.0;
        for rxn,flux in flux_dict.iteritems():
            cobra_model.reactions.get_by_id(rxn).lower_bound = flux['lb'];
            cobra_model.reactions.get_by_id(rxn).upper_bound = flux['ub'];
        for flux in measured_flux_list:
            cobra_model.reactions.get_by_id(flux['rxn_id']).lower_bound = flux['flux_lb'];
            cobra_model.reactions.get_by_id(flux['rxn_id']).upper_bound = flux['flux_ub'];
        # change description, if any:
        if description:
            cobra_model.description = description;
        # test for a solution:
        cobra_model.optimize(solver='gurobi');
        if not cobra_model.solution.f:
            print "model does not converge to a solution";
        ##find minimal flux solution:
        #pfba = optimize_minimal_flux(cobra_model,True,solver='gurobi');

        return cobra_model;
    def make_Model(self,model_id_I=None,model_id_O=None,date_I=None,model_file_name_I=None,ko_list=[],flux_dict={},description=None):
        '''make a new model'''

        qio02 = stage02_isotopomer_io();

        if model_id_I and model_id_O: #make a new model based off of a modification of an existing model in the database
            cobra_model_sbml = None;
            cobra_model_sbml = self.stage02_isotopomer_query.get_row_modelID_dataStage02IsotopomerModels(model_id_I);
            # write the model to a temporary file
            if cobra_model_sbml['file_type'] == 'sbml':
                with open(settings.workspace_data + '/cobra_model_tmp.xml','wb') as file:
                    file.write(cobra_model_sbml['model_file']);
                    file.close()
                cobra_model = None;
                cobra_model = create_cobra_model_from_sbml_file(settings.workspace_data + '/cobra_model_tmp.xml', print_time=True);
            elif cobra_model_sbml['file_type'] == 'json':
                with open(settings.workspace_data + '/cobra_model_tmp.json','wb') as file:
                    file.write(cobra_model_sbml['model_file']);
                    file.close()
                cobra_model = None;
                cobra_model = load_json_model(settings.workspace_data + '/cobra_model_tmp.json');
            else:
                print 'file_type not supported'
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
            # test the model
            if self.test_model(cobra_model):
                # write the model to a temporary file
                with open(settings.workspace_data + '/cobra_model_tmp.xml','wb') as file:
                    file.write(cobra_model);
                # upload the model to the database
                qio02.import_dataStage02Model_sbml(model_id_I, date_I, settings.workspace_data + '/cobra_model_tmp.xml');
        elif model_file_name_I and model_id_O: #modify an existing model in not in the database
            # check for the file type
            if '.json' in model_file_name_I:
                # Read in the sbml file and define the model conditions
                cobra_model = load_json_model(model_file_name_I, print_time=True);
            elif '.xml' in model_file_name_I:
                # Read in the sbml file and define the model conditions
                cobra_model = create_cobra_model_from_sbml_file(model_file_name_I, print_time=True);
            else: print 'file type not supported'
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
            # test the model
            if self.test_model(cobra_model):
                # write the model to a temporary file
                filename = '';
                if '.xml' in model_file_name_I:
                    filename = settings.workspace_data + '/cobra_model_tmp.xml'
                    with open(filename,'wb') as file:
                        file.write(cobra_model);
                        file.close()
                elif '.json' in model_file_name_I:
                    filename = settings.workspace_data + '/cobra_model_tmp.json';
                    with open(filename,'wb') as file:
                        file.write(cobra_model);
                        file.close()
                else: print 'file type not supported'
                # upload the model to the database
                qio02.import_dataStage02Model_sbml(model_id_I, date_I, filename);
        else:
            print 'need to specify either an existing model_id or model_file_name!'
        return
    def load_models(self,experiment_id_I,model_ids_I=[]):
        '''pre-load all models for the experiment_id'''
        # get the model ids:
        if model_ids_I:
            model_ids = model_ids_I;
        else:
            model_ids = [];
            model_ids = self.stage02_isotopomer_query.get_modelID_experimentID_dataStage02PhysiologySimulation(experiment_id_I);
        for model_id in model_ids:
            # get the cobra model
            cobra_model_sbml = None;
            cobra_model_sbml = self.stage02_isotopomer_query.get_row_modelID_dataStage02IsotopomerModels(model_id);
            # write the model to a temporary file
            if cobra_model_sbml['file_type'] == 'sbml':
                with open(settings.workspace_data + '/cobra_model_tmp.xml','wb') as file:
                    file.write(cobra_model_sbml['model_file']);
                    file.close()
                cobra_model = None;
                cobra_model = create_cobra_model_from_sbml_file(settings.workspace_data + '/cobra_model_tmp.xml', print_time=True);
            elif cobra_model_sbml['file_type'] == 'json':
                with open(settings.workspace_data + '/cobra_model_tmp.json','wb') as file:
                    file.write(cobra_model_sbml['model_file']);
                    file.close()
                cobra_model = None;
                cobra_model = load_json_model(settings.workspace_data + '/cobra_model_tmp.json');
            else:
                print 'file_type not supported'
            self.models[model_id]=cobra_model;
    def make_modelFromRxnsAndMetsTables(self,model_id_I=None,model_id_O=None,date_I=None,ko_list=[],flux_dict={},description=None):
        '''make/update the model using the modelReactions and modelMetabolites table'''

        qio02 = stage02_isotopomer_io();

        if model_id_I and model_id_O: #make a new model based off of a modification of an existing model in the database
            # get the model reactions and metabolites from the database
            reactions = [];
            metabolites = [];
            reactions = self.stage02_isotopomer_query.get_rows_modelID_dataStage02IsotopomerModelReactions(model_id_I);
            metabolites = self.stage02_isotopomer_query.get_rows_modelID_dataStage02IsotopomerModelMetabolites(model_id_I);
            # creat the model
            cobra_model = qio02.create_modelFromReactionsAndMetabolitesTables(reactions,metabolites)
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
            # test the model
            if self.test_model(cobra_model):
                # write the model to a temporary file
                save_json_model(cobra_model,settings.workspace_data+'/cobra_model_tmp.json')
                # add the model information to the database
                dataStage02IsotopomerModelRxns_data = [];
                dataStage02IsotopomerModelMets_data = [];
                dataStage02IsotopomerModels_data,\
                    dataStage02IsotopomerModelRxns_data,\
                    dataStage02IsotopomerModelMets_data = qio02._parse_model_json(model_id_O, date_I, settings.workspace_data+'/cobra_model_tmp.json')
                qio02.add_data_stage02_isotopomer_models(dataStage02IsotopomerModels_data);
        elif model_id_I and not model_id_O:  #update an existing model in the database
            # get the model reactions and metabolites from the database
            reactions = [];
            metabolites = [];
            reactions = self.stage02_isotopomer_query.get_rows_modelID_dataStage02IsotopomerModelReactions(model_id_I);
            metabolites = self.stage02_isotopomer_query.get_rows_modelID_dataStage02IsotopomerModelMetabolites(model_id_I);
            # creat the model
            cobra_model = qio02.create_modelFromReactionsAndMetabolitesTables(reactions,metabolites)
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
            # test the model
            if self.test_model(cobra_model):
                # write the model to a temporary file
                save_json_model(cobra_model,settings.workspace_data+'/cobra_model_tmp.json')
                # upload the model to the database
                # add the model information to the database
                dataStage02IsotopomerModelRxns_data = [];
                dataStage02IsotopomerModelMets_data = [];
                dataStage02IsotopomerModels_data,\
                    dataStage02IsotopomerModelRxns_data,\
                    dataStage02IsotopomerModelMets_data = qio02._parse_model_json(model_id_I, date_I, settings.workspace_data+'/cobra_model_tmp.json')
                qio02.update_data_stage02_isotopomer_models(dataStage02IsotopomerModels_data);

        else:
            print 'need to specify either an existing model_id!'
        return
    def test_model(self,cobra_model):
        '''simulate a cobra model'''
        
        # Dependencies from cobra
        from cobra.flux_analysis.parsimonious import optimize_minimal_flux

        # test for a solution:
        cobra_model.optimize(solver='gurobi');
        if not cobra_model.solution.f:
            print "model does not converge to a solution";
            return False,
        else:
            print 'solution = ' + str(cobra_model.solution.f)
            return True;
    def check_observableFlux(self,flux_I,flux_lb_I,flux_ub_I):
        '''Determine if a flux is observable
        based on the criteria in doi:10.1016/j.ymben.2010.11.006'''
        flux_span = flux_ub_I-flux_lb_I;
        if flux_I==0.0 and flux_lb_I==0.0 and flux_ub_I==0.0:
            observable = False;
        elif flux_span > 4*flux_I and flux_lb_I == 0:
            observable = False;
        else:
            observable = True;
        return observable;
    def correct_fluxStdev(self,flux_lb_I,flux_ub_I):
        '''Calculate the standard deviation based off of the 95% confidence intervals
        described in doi:0.1016/j.ymben.2013.08.006'''
        flux_stdev = 0.0;
        flux_stdev = (flux_ub_I - flux_lb_I)/4
        return flux_stdev;
    def calculate_netFlux(self,flux_1,flux_stdev_1,flux_lb_1,flux_ub_1,flux_units_1,
                          flux_2,flux_stdev_2,flux_lb_2,flux_ub_2,flux_units_2):
        '''Calculate the net flux through a reaction,
        where "1" denotes the forward flux, and "2" denotes the reverse flux'''

        # determine if the fluxes are observable
        observable_1 = self.check_observableFlux(flux_1,flux_lb_1,flux_ub_1)
        observable_2 = self.check_observableFlux(flux_2,flux_lb_2,flux_ub_2)
        # calculate the net flux
        flux_average = flux_1-flux_2
        flux_stdev = sqrt(abs(flux_stdev_1*flux_stdev_1-flux_stdev_2*flux_stdev_2))
        # flux 1 and 2 are observable
        if observable_1 and observable_2:
            # note that both fluxes cannot be unbounded
            if flux_1 > 999.9 and flux_2 > 999.9:
                print 'both fluxes are unbounded'
                flux_average = None;
                flux_lb = -1000.0;
                flux_ub = 1000.0;
            elif flux_1 > 999.9: # flux 1 is unbounded
                flux_lb = flux_lb_1-flux_2
                flux_ub = flux_ub_1-0.0
            elif flux_2 > 999.9: # flux 2 is unbounded
                flux_lb = flux_1-flux_lb_2
                flux_ub = 0.0-flux_ub_2
            else:
                flux_lb = flux_lb_1-flux_lb_2
                flux_ub = flux_ub_1-flux_ub_2
            flux_units = flux_units_1;
        # flux 1 is observable, flux 2 is not observable, and flux 2 exists
        elif observable_1 and not observable_2 and flux_units_2:
            flux_lb = flux_lb_1-flux_2
            flux_ub = flux_ub_1-0.0
            flux_units = flux_units_1;
        # flux 2 is observable, flux 1 is not observable, and flux 1 exists
        elif observable_2 and not observable_1 and flux_units_1:
            flux_lb = flux_1-flux_lb_2
            flux_ub = 0.0-flux_ub_2
            flux_units = flux_units_2;
        # flux 1 is observable, flux 2 is not observable, and there is no flux 2
        elif observable_1 and not observable_2 and not flux_units_2:
            flux_lb = flux_lb_1
            flux_ub = flux_ub_1
            flux_units = flux_units_1;
        # flux 2 is observable, flux 1 is not observable,, and there is no flux 1
        elif observable_2 and not observable_1 and not flux_units_1:
            flux_lb = -flux_lb_2
            flux_ub = -flux_ub_2
            flux_units = flux_units_2;
        # flux 1 is not observable, and there is no flux 2
        elif not observable_1 and not flux_units_2:
            flux_lb = flux_lb_1
            flux_ub = flux_ub_1
            flux_units = flux_units_1;
        # flux 2 is not observable,  and there is no flux 1
        elif not observable_2 and not flux_units_1:
            flux_lb = -flux_ub_2
            flux_ub = -flux_lb_2
            flux_units = flux_units_2;
        # flux 1 is observable, flux 2 is not observable, and flux 2 exists
        elif not observable_1 and not observable_2 and flux_units_2:
            flux_lb = -1000.0
            flux_ub = 1000.0
            flux_units = flux_units_1;
        # flux 2 is observable, flux 1 is not observable, and flux 1 exists
        elif not observable_2 and not observable_1 and flux_units_1:
            flux_lb = -1000.0
            flux_ub = 1000.0
            flux_units = flux_units_2;
        # flux 1 is not observable and there is no flux 2
        elif not observable_1 and not flux_units_2:
            flux_lb = flux_lb_1
            flux_ub = flux_ub_1
            #flux_lb = 0.0
            #flux_ub = 1000.0
            flux_units = flux_units_1;
        # flux 2 is not observable and there is no flux 1
        elif not observable_2 and not flux_units_1:
            flux_lb = -flux_ub_2
            flux_ub = -flux_lb_2
            #flux_lb = -1000.0
            #flux_ub = 0.0
            flux_units = flux_units_2;
        #elif not observable_1 and not flux_units_1 and not flux_units_2:
        #    flux_average = None;
        #    flux_lb = 0.0
        #    flux_ub = 1000.0
        #    flux_units = flux_units_1;
        #elif not observable_2 and not flux_units_2:
        #    flux_average = None;
        #    flux_lb = -1000.0
        #    flux_ub = 0.0
        #    flux_units = flux_units_2;
        else:
            flux_average = None;
            flux_lb = -1000.0
            flux_ub = 1000.0
            flux_units = 'mmol*gDCW-1*hr-1';
        # check the direction of the lower/upper bounds
        if flux_lb>flux_ub:
            flux_lb_tmp,flux_ub_tmp = flux_lb,flux_ub;
            flux_lb = flux_ub_tmp;
            flux_ub = flux_lb_tmp;
        elif flux_lb==0.0 and flux_ub==0.0:
            flux_lb = -1000.0;
            flux_ub = 1000.0;
        # check the flux
        # substitute 0.0 for None
        if flux_average == 0.0:
            flux_average = None;
        elif flux_average < flux_lb or flux_average > flux_ub:
            flux_average = numpy.mean([flux_lb,flux_ub]);
        return flux_average,flux_stdev,flux_lb,flux_ub,flux_units
    def convert_fragmentAndElements2PositionAndElements(self,fragment_I,element_I):
        '''convert boolean fragment array representation of tracked atom positions to a numerical array representation'''
        positions_O = [];
        elements_O = [];
        cmap_cnt = 0;
        for i,f in enumerate(fragment_I):
            if f: 
                positions_O.append(cmap_cnt);
                elements_O.append(element_I[i]);
            cmap_cnt += 1;
        return positions_O,elements_O;
    #Visualization
    def plot_fluxPrecision(self,simulation_ids_I = [], rxn_ids_I = [],plot_by_rxn_id_I=True,exclude_I = {}):
        '''Plot the flux precision for a given set of simulations and a given set of reactions
        Default: plot the flux precision for each simulation on a single plot for a single reaction'''

        from resources.matplot import matplot
        plot = matplot();

        data_O ={}; # keys = simulation_id, values = {rxn_id:{flux_info}};
        for simulation_id in simulation_ids_I:
            # get the simulation dataAndTime
            simulation_dateAndTimes = [];
            simulation_dateAndTimes = self.stage02_isotopomer_query.get_simulationDateAndTimes_simulationID_dataStage02IsotopomerfittedNetFluxes(simulation_id);
            data_O[simulation_id] = {};
            if len(simulation_dateAndTimes) > 1:
                print 'more than 1 simulation date and time found!'
                continue;
            else:
                simulation_dataAndTime = simulation_dateAndTimes[0];
            # get the rxn_ids
            if rxn_ids_I:
                rxn_ids = rxn_ids_I;
            else:
                rxn_ids = [];
                rxn_ids = self.stage02_isotopomer_query.get_rxnIDs_simulationIDAndSimulationDateAndTime_dataStage02IsotopomerfittedNetFluxes(simulation_id,simulation_dataAndTime)
            # get the flux information for each simulation
            for rxn_id in rxn_ids:
                data_O[simulation_id][rxn_id] = {}
                if exclude_I and exclude_I.has_key(rxn_id) and exclude_I[rxn_id] == simulation_id:
                    data_O[simulation_id][rxn_id] = {};
                else:
                    flux_O,flux_stdev_O,flux_lb_O,flux_ub_O,flux_units_O=0.0,0.0,0.0,0.0,'';
                    flux_O,flux_stdev_O,flux_lb_O,flux_ub_O,flux_units_O = self.stage02_isotopomer_query.get_flux_simulationIDAndRxnID_dataStage02IsotopomerfittedNetFluxes(simulation_id,rxn_id);
                    # check for None flux
                    if not flux_O: flux_O = 0.0;
                    # save the flux information
                    tmp_O = {};
                    tmp_O = {'flux':flux_O,'flux_stdev':flux_stdev_O,'flux_lb':flux_lb_O,
                             'flux_ub':flux_ub_O,'flux_units':flux_units_O}
                    data_O[simulation_id][rxn_id] = tmp_O;
        # reorder the data for plotting
        if plot_by_rxn_id_I:
            rxn_ids_all = [];
            for k1,v1 in data_O.iteritems():
                for k in v1.keys():
                    rxn_ids_all.append(k);
            rxn_ids = list(set(rxn_ids_all));
            for rxn_id in rxn_ids:
                title_I,xticklabels_I,ylabel_I,xlabel_I,data_I,mean_I,ci_I = '',[],'','',[],[],[];
                for simulation_id in simulation_ids_I:
                    if data_O[simulation_id][rxn_id]:
                        xticklabels_I.append(simulation_id);
                        data_I.append([data_O[simulation_id][rxn_id]['flux_lb'],data_O[simulation_id][rxn_id]['flux_ub'],data_O[simulation_id][rxn_id]['flux']])
                        mean_I.append(data_O[simulation_id][rxn_id]['flux'])
                        ci_I.append([data_O[simulation_id][rxn_id]['flux_lb'],data_O[simulation_id][rxn_id]['flux_ub']])
                        ylabel_I = 'Flux [' + data_O[simulation_id][rxn_id]['flux_units'] + ']';
                title_I = rxn_id;
                xlabel_I = 'Simulation_id'
                plot.boxAndWhiskersPlot(title_I,xticklabels_I,ylabel_I,xlabel_I,data_I=data_I,mean_I=mean_I,ci_I=ci_I)
        else: 
            return;
    
    # Deprecated
    def execute_makeIsotopomerSimulation_INCA_v1(self,experiment_id_I, model_id_I = [], mapping_id_I = [], sample_name_abbreviations_I = [], time_points_I = [], met_ids_I = [], scan_types_I = [], stationary_I = True, parallel_I = False, ko_list_I=[],flux_dict_I={},description_I=None):
        '''export a fluxomics experimental data for simulation using INCA1.1'''
        #Input:
        #   stationary_I = boolean
        #                  indicates whether each time-point is written to a separate file, or part of a time-course
        #   parallel_I = boolean
        #                  indicates whether multiple tracers were used

        # get the different simulations:
        # get the sample name abbreviations
        #if simulations_I:
        #    simulations = simulations_I;
        #else:
        #    simulations = [];
        #    simulations = self.stage02_isotopomer_query.get_sampleNameAbbreviations_experimentID_dataStage02IsotopomerSimulation(experiment_id_I);
        # get the sample name abbreviations
        if sample_name_abbreviations_I:
            sample_abbreviations = sample_name_abbreviations_I;
        else:
            sample_abbreviations = [];
            sample_abbreviations = self.stage02_isotopomer_query.get_sampleNameAbbreviations_experimentID_dataStage02IsotopomerSimulation(experiment_id_I);
            #sample_abbreviations = self.stage02_isotopomer_query.get_sampleNameAbbreviations_experimentID_dataStage02IsotopomerMeasuredFragments(experiment_id_I);
        for sna_cnt,sna in enumerate(sample_abbreviations):
            print 'Collecting and writing experimental and model data for sample name abbreviation ' + sna;
            # get the model_ids
            if model_id_I:
                model_ids = model_id_I;
            else:
                model_ids = [];
                model_ids = self.stage02_isotopomer_query.get_modelID_experimentIDAndSampleNameAbbreviations_dataStage02IsotopomerSimulation(experiment_id_I,sna);
            for model_id in model_ids:
                # get the mapping_ids
                if mapping_id_I:
                    mapping_ids =  mapping_id_I;
                else:
                    mapping_ids = [];
                    mapping_ids = self.stage02_isotopomer_query.get_mappingID_experimentIDAndSampleNameAbbreviationsAndModelID_dataStage02IsotopomerSimulation(experiment_id_I,sna,model_id);
                for mapping_id in mapping_ids:
                    print 'Collecting and exporting tracer information for sample name abbreviation ' + sna;
                    ## get substrate labeling (i.e. tracer) information
                    if parallel_I:
                        tracers = [];
                        tracers = self.stage02_isotopomer_query.get_rows_experimentID_dataStage02IsotopomerTracers(experiment_id_I);
                    else:
                        tracers = [];
                        tracers = self.stage02_isotopomer_query.get_rows_experimentIDAndSampleNameAbbreviation_dataStage02IsotopomerTracers(experiment_id_I,sna);

                    # data containers
                    modelReaction_data,modelMetabolite_data,measuredFluxes_data,experimentalMS_data = [],[],[],[];
                    
                    # get flux measurements
                    measuredFluxes_data = [];
                    measuredFluxes_data = self.stage02_isotopomer_query.get_rows_experimentIDAndModelIDAndSampleNameAbbreviation_dataStage02IsotopomerMeasuredFluxes(experiment_id_I,model_id,sna);
                    #get model reactions
                    modelReaction_data = [];
                    modelReaction_data = self.stage02_isotopomer_query.get_rows_modelID_dataStage02IsotopomerModelReactions(model_id);
                    #simulate the model
                    cobra_model = self.simulate_model(model_id,ko_list_I,flux_dict_I,measuredFluxes_data,description_I);
                    for i,row in enumerate(modelReaction_data):
                        #get atom mapping data
                        atomMapping = {};
                        atomMapping = self.stage02_isotopomer_query.get_row_mappingIDAndRxnID_dataStage02IsotopomerAtomMappingReactions(mapping_id,row['rxn_id']);
                        #generate reaction equations
                        rxn_equation = '';
                        print row['rxn_id']
                        #if row['rxn_id'] == 'EX_glc_LPAREN_e_RPAREN_':
                        #    print 'check'
                        if atomMapping:
                            rxn_equation = self.make_isotopomerRxnEquations_INCA(
                                        row['reactants_ids'],
                                        row['products_ids'],
                                        row['reactants_stoichiometry'],
                                        row['products_stoichiometry'],
                                        row['reversibility'],
                                        atomMapping['reactants_stoichiometry_tracked'],
                                        atomMapping['products_stoichiometry_tracked'],
                                        atomMapping['reactants_ids_tracked'],
                                        atomMapping['products_ids_tracked'],
                                        atomMapping['reactants_elements_tracked'],
                                        atomMapping['products_elements_tracked'],
                                        atomMapping['reactants_positions_tracked'],
                                        atomMapping['products_positions_tracked'],
                                        atomMapping['reactants_mapping'],
										atomMapping['products_mapping']);
                        else:
                            rxn_equation = self.make_isotopomerRxnEquations_INCA(
                                        row['reactants_ids'],
                                        row['products_ids'],
                                        row['reactants_stoichiometry'],
                                        row['products_stoichiometry'],
                                        row['reversibility'],
                                        [],
                                        [],
                                        [],
                                        [],
                                        [],
                                        [],
                                        [],
                                        [],
                                        [],
										[]);
                        atomMapping['rxn_equation']=rxn_equation;
                        modelReaction_data[i].update(atomMapping);
                        # update the lower bounds and upper bounds of the model to represent the experimental data
                        if measuredFluxes_data:
                            for flux in measuredFluxes_data:
                                if row['rxn_id'] == flux['rxn_id']:
                                    modelReaction_data[i]['lower_bound'] = flux['flux_lb']
                                    modelReaction_data[i]['upper_bound'] = flux['flux_ub']
                        # update the lower bounds and upper bounds of the model to represent the input data (if the model has not already been updated)
                        for ko in ko_list_I: # implement optimal KOs
                            if row['rxn_id'] == ko:
                                modelReaction_data[i]['lower_bound'] = 0.0;
                                modelReaction_data[i]['upper_bound'] = 0.0;
                        for rxn,flux in flux_dict_I.iteritems():  # implement flux constraints:
                            if row['rxn_id'] == rxn:
                                modelReaction_data[i]['lower_bound'] = flux['lb'];
                                modelReaction_data[i]['upper_bound'] = flux['ub'];
                        # add in a flux_val field to supply an initial starting guess for the MFA solver
                        if cobra_model.solution.f:
                            modelReaction_data[i]['flux_val'] = cobra_model.solution.x_dict[row['rxn_id']];
                        else:
                            modelReaction_data[i]['flux_val'] = 0;
                    # get model metabolites
                    modelMetabolite_data = [];
                    modelMetabolite_data = self.stage02_isotopomer_query.get_rows_modelID_dataStage02IsotopomerModelMetabolites(model_id);
                    for i,row in enumerate(modelMetabolite_data):
                        #get atom mapping data
                        atomMapping = {};
                        atomMapping = self.stage02_isotopomer_query.get_rows_mappingIDAndMetID_dataStage02IsotopomerAtomMappingMetabolites(mapping_id,row['met_id']);
                        #update
                        if atomMapping:
                            modelMetabolite_data[i].update(atomMapping);
                        else:
                            modelMetabolite_data[i].update({
                                'met_elements':None,
                                'met_atompositions':None,
                                'met_symmetry_elements':None,
                                'met_symmetry_atompositions':None});

                    ## dump the experiment to a matlab script to generate the matlab files in matlab
                    # Matlab script file to make the structures
                    if stationary_I:
                        if time_points_I:
                            time_points = time_points_I;
                        else:
                            time_points = [];
                            time_points = self.stage02_isotopomer_query.get_timePoint_experimentIDAndSampleNameAbbreviation_dataStage02IsotopomerMeasuredFragments(experiment_id_I,sna);
                        for tp in time_points:
                            # get the MS data
                            experimentalMS_data =self.stage02_isotopomer_query.get_row_experimentIDAndSampleNameAbbreviationAndTimePoint_dataStage02IsotopomerMeasuredFragments(experiment_id_I,sna,tp);
                            experiment_name = 'Isotopomer_' + re.sub('[.\/]','',experiment_id_I) + '_' + re.sub(' ','',sna) + '_' + re.sub(' ','',str(tp));
                            filename_mat = settings.workspace_data + '/_output/' + 'isotopomer_' + re.sub('[.\/]','',experiment_id_I) + '_' + re.sub(' ','',sna) + '_' + re.sub(' ','',str(tp)) + '.m';
                            filename_mat_model = filename_mat + "_model" + '.m';
                            filename_mat_simulationOptions = filename_mat + "_options" + '.m';
                            filename_mat_experiment = filename_mat + "_experiment" + '.m';
                            filename_mat_data = filename_mat + "_data" + '.m';
                            filename_mat_run = filename_mat + "_run" + '.m';
                            mat_script = self.write_isotopomerExperiment_INCA(modelReaction_data,modelMetabolite_data,measuredFluxes_data,experimentalMS_data,tracers);
                            with open(filename_mat_model,'w') as f:
                                f.write(mat_script);
                    else:
                        # get the MS data
                        experimentalMS_data = self.stage02_isotopomer_query.get_row_experimentIDAndSampleNameAbbreviation_dataStage02IsotopomerMeasuredFragments(experiment_id_I,sna);
                        experiment_name = 'Isotopomer_' + re.sub('[.\/]','',experiment_id_I) + '_' + re.sub(' ','',sna);
                        filename_mat = settings.workspace_data + '/_output/' + 'isotopomer_' + re.sub('[.\/]','',experiment_id_I) + '_' + re.sub(' ','',sna) + '.m';
                        mat_script = self.write_isotopomerExperiment_INCA(modelReaction_data,modelMetabolite_data,measuredFluxes_data,experimentalMS_data,tracers);
                        with open(filename_mat,'w') as f:
                            f.write(mat_script);

    # TODO
    def make_modelAndMappingFromRxnsAndMetsTables(self,model_id_I=None,model_id_O=None,mapping_id_I=None,mapping_id_O=None,date_I=None,ko_list=[],flux_dict={},description=None):
        '''make/update the model AND model mappings using the modelReactions and modelMetabolites table'''

        qio02 = stage02_isotopomer_io();

        if model_id_I and model_id_O and mapping_id_I and mapping_id_O: #make a new model based off of a modification of an existing model in the database
            # get the model reactions and metabolites from the database
            reactions = [];
            metabolites = [];
            reactions = self.stage02_isotopomer_query.get_rows_modelID_dataStage02IsotopomerModelReactions(model_id_I);
            metabolites = self.stage02_isotopomer_query.get_rows_modelID_dataStage02IsotopomerModelMetabolites(model_id_I);
            reactions_mappings = [];
            metabolites_mappings = [];
            reactions_mappings = self.stage02_isotopomer_query.get_rows_mappingID_dataStage02IsotopomerAtomMappingReactions(mapping_id_I);
            metabolites_mappings = self.stage02_isotopomer_query.get_rows_mappingID_dataStage02IsotopomerAtomMappingMetabolites(mapping_id_I);
            # rename the reactions and metabolite model_ids
            for rxn_cnt,rxn in enumerate(reactions):
                reactions[rxn_cnt]['model_id'] = model_id_O;
            for met_cnt,met in enumerate(metabolites):
                metabolites[met_cnt]['model_id'] = model_id_O;
            # rename the reactions and metabolite mapping_ids
            for rxn_cnt,rxn in enumerate(reactions_mappings):
                reactions_mappings[rxn_cnt]['mapping_id'] = mapping_id_O;
            for met_cnt,met in enumerate(metabolites_mappings):
                metabolites_mappings[met_cnt]['mapping_id'] = mapping_id_O;
            # create the model
            cobra_model = qio02.create_modelFromReactionsAndMetabolitesTables(reactions,metabolites)
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
            # test the model
            if self.test_model(cobra_model):
                # write the model to a temporary file
                save_json_model(cobra_model,settings.workspace_data+'/cobra_model_tmp.json')
                # add the model information to the database
                dataStage02IsotopomerModelRxns_data = [];
                dataStage02IsotopomerModelMets_data = [];
                dataStage02IsotopomerModels_data,\
                    dataStage02IsotopomerModelRxns_data,\
                    dataStage02IsotopomerModelMets_data = qio02._parse_model_json(model_id_O, date_I, settings.workspace_data+'/cobra_model_tmp.json')
                qio02.add_data_stage02_isotopomer_models(dataStage02IsotopomerModels_data);
                # add the metabolite and reaction information to the database
                qio02.add_data_stage02_isotopomer_modelReactions(reactions);
                qio02.add_data_stage02_isotopomer_modelMetabolites(metabolites);
                # add the metabolites and reactions mappings to the database
                self.stage02_isotopomer_query.add_data_dataStage02IsotopomerAtomMappingReactions(reactions_mappings);
                self.stage02_isotopomer_query.add_data_dataStage02IsotopomerAtomMappingMetabolites(metabolites_mappings);
        elif model_id_I and not model_id_O and mapping_id_I and not mapping_id_O:  #update an existing model in the database
            # get the model reactions and metabolites from the database
            reactions = [];
            metabolites = [];
            reactions = self.stage02_isotopomer_query.get_rows_modelID_dataStage02IsotopomerModelReactions(model_id_I);
            metabolites = self.stage02_isotopomer_query.get_rows_modelID_dataStage02IsotopomerModelMetabolites(model_id_I);
            # creat the model
            cobra_model = qio02.create_modelFromReactionsAndMetabolitesTables(reactions,metabolites)
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
            # test the model
            if self.test_model(cobra_model):
                # write the model to a temporary file
                save_json_model(cobra_model,settings.workspace_data+'/cobra_model_tmp.json')
                # upload the model to the database
                # add the model information to the database
                dataStage02IsotopomerModelRxns_data = [];
                dataStage02IsotopomerModelMets_data = [];
                dataStage02IsotopomerModels_data,\
                    dataStage02IsotopomerModelRxns_data,\
                    dataStage02IsotopomerModelMets_data = qio02._parse_model_json(model_id_I, date_I, settings.workspace_data+'/cobra_model_tmp.json')
                qio02.update_data_stage02_isotopomer_models(dataStage02IsotopomerModels_data);

        else:
            print 'need to specify an existing model_id/mapping_id!'
        return

class inca_api(stage02_isotopomer_execute):

    def write_isotopomerExperiment_INCA(self, modelReaction_data_I,modelMetabolite_data_I,
                                        measuredFluxes_data_I,experimentalMS_data_I,tracer_I,
                                        parallel_I = 'experiment_id'):
        '''Write matlab script file that describes the fluxomics experiment for INCA1.1'''

        mat_script = 'clear functions\n';

        ##1. Define the model:

        ## debug reaction equations
        #tmp_script = ''
        #for rxn in modelReaction_data_I:
        #    #TODO check on how the reactions are named  
        #    tmp_script = tmp_script + 'r = reaction({...\n';
        #    tmp_script = tmp_script + "'" + rxn['rxn_equation'] + "';...\n"
        #    tmp_script = tmp_script + '});\n';
        #mat_script = mat_script + tmp_script;

        # write out reaction equations
        tmp_script = ''
        tmp_script = tmp_script + 'r = reaction({...\n';
        rxn_ids_INCA = {};
        cnt = 0
        for rxn_cnt,rxn in enumerate(modelReaction_data_I):
            #if not(rxn['upper_bound']==0.0 and rxn['lower_bound']==0.0):
                rxn_ids_INCA[rxn['rxn_id']] = ('R'+str(cnt+1));
                cnt+=1;
                if rxn['rxn_id'] == 'Ec_biomass_iJO1366_WT_53p95M':
                    #tmp_script = tmp_script + "'" + self.biomass_INCA + "';...\n"
                    tmp_script = tmp_script + "'" + self.biomass_INCA_iJS2012 + "';...\n"
                else:
                    tmp_script = tmp_script + "'" + rxn['rxn_equation'] + "';...\n"
                #tmp_script = tmp_script + "'" + rxn['rxn_equation'] + "';...\n"
            #else:
            #    print 'rxn_id ' + rxn['rxn_id'] + ' will be excluded from INCA' 
        tmp_script = tmp_script + '});\n';
        mat_script = mat_script + tmp_script;

        # setup the model
        mat_script = mat_script + 'm = model(r);\n'

        # Take care of symmetrical metabolites if not done so in the reaction equations
        tmp_script = ''
        for met in modelMetabolite_data_I:
            if met['met_symmetry_atompositions']:
                tmp_script = tmp_script + "m.mets{'" + met['met_id'] + "'}.sym = list('rotate180',map('";
                for cnt,atompositions in enumerate(met['met_atompositions']):
                    tmp_script = tmp_script + met['met_elements'][cnt] + str(atompositions+1) + ':' + met['met_symmetry_elements'][cnt] + str(met['met_symmetry_atompositions'][cnt]+1) + ' ';
                tmp_script = tmp_script[:-1];
                tmp_script = tmp_script + "'));\n";
        mat_script = mat_script + tmp_script;

        # Add in the metabolite states (balance), value, and lb/ub)
        tmp_script = ''
        # specify reactions that should be forcible unbalanced
        #NOTE: hard-coded for now until a better workaround can be done
        metabolites_all = [x['met_id'] for x in modelMetabolite_data_I];
        for met in ['co2_e','h2o_e','h_e','na1_e']:
            if met in metabolites_all:
                tmp_script = tmp_script + "m.states{'" + met + ".EX" + "'}.bal = false";
                tmp_script = tmp_script + "'));\n";
        mat_script = mat_script + tmp_script;

        # Add in initial fluxes (values lb/ub) and define the reaction ids
        tmp_script = ''
        tmp_script = tmp_script + 'm.rates.flx.lb = [...\n';
        # lower bounds
        for rxn_cnt,rxn in enumerate(modelReaction_data_I):
            #if not(rxn['upper_bound']==0.0 and rxn['lower_bound']==0.0):
                if measuredFluxes_data_I:
                    for flux in measuredFluxes_data_I:
                        if rxn['rxn_id'] == flux['rxn_id']:
                            tmp_script = tmp_script + str(flux['flux_lb']) + ',...\n'
                            break;
                        else:
                            tmp_script = tmp_script + str(rxn['lower_bound']) + ',...\n'
                            break;
                else: tmp_script = tmp_script + str(rxn['lower_bound']) + ',...\n'
        tmp_script = tmp_script + '];\n';
        tmp_script = tmp_script + 'm.rates.flx.ub = [...\n';
        # upper bounds
        for rxn_cnt,rxn in enumerate(modelReaction_data_I):
            #if not(rxn['upper_bound']==0.0 and rxn['lower_bound']==0.0):
                if measuredFluxes_data_I:
                    for flux in measuredFluxes_data_I:
                        if rxn['rxn_id'] == flux['rxn_id']:
                            tmp_script = tmp_script + str(flux['flux_ub']) + ',...\n'
                            break;
                        else:
                            tmp_script = tmp_script + str(rxn['upper_bound']) + ',...\n'
                            break;
                else: tmp_script = tmp_script + str(rxn['upper_bound']) + ',...\n'
        tmp_script = tmp_script + '];\n';
        tmp_script = tmp_script + 'm.rates.flx.val = [...\n';
        # intial flux values
        for rxn_cnt,rxn in enumerate(modelReaction_data_I):
            #if not(rxn['upper_bound']==0.0 and rxn['lower_bound']==0.0):
                tmp_script = tmp_script + str(rxn['flux_val']) + ',...\n'
        tmp_script = tmp_script + '];\n';
        tmp_script = tmp_script + 'm.rates.on = [...\n';
        # include/exclude a reaction from the simulation
        for rxn_cnt,rxn in enumerate(modelReaction_data_I):
            if rxn['flux_val']==0.0 and rxn['upper_bound']==0.0 and rxn['lower_bound']==0.0:
                #tmp_script = tmp_script + 'm.rates.on(' + str(rxn_cnt) + ') = 0;\n'
                tmp_script = tmp_script + 'false' + ',...\n'
            else:
                #tmp_script = tmp_script + 'm.rates.on(' + str(rxn_cnt) + ') = 1;\n'
                tmp_script = tmp_script + 'true' + ',...\n'
        tmp_script = tmp_script + '];\n';
        tmp_script = tmp_script + 'm.rates.id = {...\n';
        # rxn_ids
        for rxn_cnt,rxn in enumerate(modelReaction_data_I):
            #if not(rxn['upper_bound']==0.0 and rxn['lower_bound']==0.0):
                tmp_script = tmp_script + "'" + rxn['rxn_id'] + "',...\n"
        tmp_script = tmp_script + '};\n';
        tmp_script = tmp_script + 'm.rates.id = {...\n';

        for rxn_cnt,rxn in enumerate(modelReaction_data_I):
            tmp_script = tmp_script + "'" + rxn['rxn_id'] + "',...\n"
        tmp_script = tmp_script + '};\n';
        mat_script = mat_script + tmp_script;

        ## Check that fluxes are feasible
        #mat_script = mat_script + "m.rates.flx.val = mod2stoich(m)';\n"

        ## Add in the metabolite states (value and lb/ub)
        ##TODO: decide on met_equations structure
        ##NOTE: lb, ub, val = 0 for steady-state
        #mat_script = mat_script + 'm.states.flx.lb = [...';
        #for met in modelMetabolite_data_I:
        #    #TODO check on how the metabolites are named
        #    mat_script = mat_script + met['lower_bound'] + ',...\n'
        #mat_script = mat_script + '];\n';
        #mat_script = mat_script + 'm.states.flx.ub = [...';
        #for met in modelMetabolite_data_I:
        #    #TODO check on how the metabolites are named
        #    mat_script = mat_script + met['upper_bound'] + ',...\n'
        #mat_script = mat_script + '];\n';
        #mat_script = mat_script + 'm.states.flx.ub = [...';
        #for met in modelMetabolite_data_I:
        #    #TODO check on how the metabolites are named
        #    mat_script = mat_script + met['flux'] + ',...\n'
        #mat_script = mat_script + '];\n';

        ##2. Set simulation options

        # Specify simulation parameters (non-stationary only!)
        '''% simulate MS measurements
        nmts = 8;                               % number of total measurements
        samp = 8/60/60;                         % spacing between measurements in hours
        m.options.int_tspan = 0:samp:(samp*nmts);   % time points in hours
        m.options.sim_tunit = 'h';              % hours are unit of time
        m.options.fit_reinit = true;
        m.options.sim_ss = false;
        m.options.sim_sens = true;'''

        tmp_script = ''
        tmp_script = tmp_script + 'm.options.fit_starts = 10;\n' #10 restarts during the estimation procedure
        mat_script = mat_script + tmp_script;
        
        ##3. Define the experiment

        # write out the measured fragment information
        # (actual MS measurements will be written to the script later)

        if parallel_I == 'experiment_id':
            experiments_all = [x['experiment_id'] for x in experimentalMS_data_I];
            experiments = list(set(experiments_all));
            experiments.sort();
        
            fragments_all = [x['fragment_id'] for x in experimentalMS_data_I];
            fragments = list(set(fragments_all));
            fragments.sort();
            mets_all = [x['met_id'] for x in experimentalMS_data_I];
            mets = list(set(mets_all));
            mets.sort();
            times_all = [x['time_point'] for x in experimentalMS_data_I];
            times = list(set(times_all));
            times.sort();

            for experiment_cnt,experiment in enumerate(experiments):
                tmp_script = ''
                tmp_script = tmp_script + 'd = msdata({...\n';
                for fragment in fragments:
                    for ms_data in experimentalMS_data_I:
                        if ms_data['fragment_id'] == fragment and ms_data['experiment_id'] == experiment:
                            tmp_script = tmp_script + "'" + ms_data['fragment_id'] + ': ' + ms_data['met_id'] + ' @ ';
                            for pos_cnt,pos in enumerate(ms_data['met_atompositions']):
                                    tmp_script = tmp_script + ms_data['met_elements'][pos_cnt] + str(pos+1) + ' ';
                            tmp_script = tmp_script[:-1];
                            tmp_script = tmp_script + "';\n"
                            break;
                tmp_script = tmp_script + '});\n';
                tmp_script = tmp_script + 'd.mdvs = mdv;\n';
                mat_script = mat_script + tmp_script;

                ## write substrate labeling (i.e. tracer) information
                tmp_script = ''
                tmp_script = tmp_script + 't = tracer({...\n';
                for tracer in tracer_I:
                    if tracer['experiment_id'] == experiment:
                        tmp_script = tmp_script + "'" + tracer['met_name'] + ': ' + tracer['met_id'] + '.EX' + ' @ '
                        for cnt,met_atompositions in enumerate(tracer['met_atompositions']):
                                tmp_script = tmp_script + tracer['met_elements'][cnt]+str(met_atompositions) + ' '
                        tmp_script = tmp_script[:-1]; #remove extra white space
                        tmp_script = tmp_script + "';...\n";
                tmp_script = tmp_script + '});\n';
                tmp_script = tmp_script + 't.frac = [';
                for tracer in tracer_I:
                    if tracer['experiment_id'] == experiment:
                        tmp_script = tmp_script + str(tracer['ratio']) + ',';
                tmp_script = tmp_script[:-1]; #remove extra ,
                tmp_script = tmp_script + '];\n'; #remove extra ,
                mat_script = mat_script + tmp_script;
                    
                ## write flux measurements
                tmp_script = ''
                tmp_script = tmp_script + "f = data('";
                for flux in measuredFluxes_data_I:
                    if flux['experiment_id'] == experiment:
                        ## Temporary fix until reactions can be properly named
                        #tmp_script = tmp_script + rxn_ids_INCA[flux['rxn_id']] + " ";
                        tmp_script = tmp_script + flux['rxn_id'] + " ";
                tmp_script = tmp_script[:-1]; #remove extra ,
                tmp_script = tmp_script + "');\n";
                tmp_script = tmp_script + 'f.val = [...\n';
                for flux in measuredFluxes_data_I:
                    if flux['experiment_id'] == experiment: tmp_script = tmp_script + str(flux['flux_average']) + ',...\n';
                tmp_script = tmp_script + '];\n';
                tmp_script = tmp_script + 'f.std = [...\n';
                for flux in measuredFluxes_data_I:
                    if flux['experiment_id'] == experiment: tmp_script = tmp_script + str(flux['flux_stdev']) + ',...\n';
                tmp_script = tmp_script + '];\n';

                tmp_script = tmp_script + 'x = experiment(t);\n'
                tmp_script = tmp_script + 'x.data_flx = f;\n'
                tmp_script = tmp_script + 'x.data_ms = d;\n'
                tmp_script = tmp_script + ('m.expts(%d) = x;\n' %(experiment_cnt+1));
                tmp_script = tmp_script + ("m.expts(%d).id = {'%s'};\n" %(experiment_cnt+1,experiment));
                mat_script = mat_script + tmp_script;

            # Add in ms data or Write ms data to separate file
            for experiment_cnt,experiment in enumerate(experiments):
                tmp_script = ''
                for i,fragment in enumerate(fragments):
                    for j,time in enumerate(times):
                        # Pad the data file:
                        tmp_script = tmp_script + ('m.expts(%d).data_ms(%d).mdvs.val(%d,%d) = %s;\n' %(experiment_cnt+1,i+1,1,j+1,'NaN'));
                        tmp_script = tmp_script + ('m.expts(%d).data_ms(%d).mdvs.std(%d,%d) = %s;\n' %(experiment_cnt+1,i+1,1,j+1,'NaN'));
                        for ms_data in experimentalMS_data_I:
                            if ms_data['fragment_id']==fragments[i] and \
                                ms_data['time_point']==times[j] and \
                                ms_data['experiment_id'] == experiment:
                                for cnt,intensity in enumerate(ms_data['intensity_normalized_average']):
                                    # each column is a seperate time point
                                    # each row is a seperate mdv
                                    # Assign names and times
                                    name = fragment + '_' + str(cnt) + '_' + str(j) + '_' + str(experiment);
                                    tmp_script = tmp_script + ("m.expts(%d).data_ms(%d).mdvs.id(%d,%d) = {'%s'};\n" %(experiment_cnt+1,i+1,1,j+1,name));
                                    tmp_script = tmp_script + ("m.expts(%d).data_ms(%d).mdvs.time(%d,%d) = %s;\n" %(experiment_cnt+1,i+1,1,j+1,time));
                                    # Assign values
                                    ave = ms_data['intensity_normalized_average'][cnt]
                                    stdev = ms_data['intensity_normalized_stdev'][cnt]
                                    # remove 0.0000 values and replace with NaN
                                    if ave < 1e-9: 
                                        ave = 'NaN';
                                        tmp_script = tmp_script + ('m.expts(%d).data_ms(%d).mdvs.val(%d,%d) = %s;\n' %(experiment_cnt+1,i+1,cnt+1,j+1,ave));
                                    else:
                                        tmp_script = tmp_script + ('m.expts(%d).data_ms(%d).mdvs.val(%d,%d) = %f;\n' %(experiment_cnt+1,i+1,cnt+1,j+1,ave));
                                    if stdev < 1e-9:
                                        # check if the ave is NaN
                                        if ave=='NaN': stdev = 'NaN';
                                        else: stdev = 0.0001;
                                        tmp_script = tmp_script + ('m.expts(%d).data_ms(%d).mdvs.std(%d,%d) = %s;\n' %(experiment_cnt+1,i+1,cnt+1,j+1,stdev));
                                    else:
                                        tmp_script = tmp_script + ('m.expts(%d).data_ms(%d).mdvs.std(%d,%d) = %f;\n' %(experiment_cnt+1,i+1,cnt+1,j+1,stdev));
                mat_script = mat_script + tmp_script;
        elif parallel_I == 'sample_name_abbreviation':
            snas_all = [x['sample_name_abbreviation'] for x in experimentalMS_data_I];
            snas = list(set(snas_all));
            snas.sort();
        
            fragments_all = [x['fragment_id'] for x in experimentalMS_data_I];
            fragments = list(set(fragments_all));
            fragments.sort();
            mets_all = [x['met_id'] for x in experimentalMS_data_I];
            mets = list(set(mets_all));
            mets.sort();
            times_all = [x['time_point'] for x in experimentalMS_data_I];
            times = list(set(times_all));
            times.sort();
        
            for sna_cnt,sna in enumerate(snas):
                tmp_script = ''
                tmp_script = tmp_script + 'd = msdata({...\n';
                for fragment in fragments:
                    for ms_data in snaalMS_data_I:
                        if ms_data['fragment_id'] == fragment and ms_data['sample_name_abbreviation'] == sna:
                            tmp_script = tmp_script + "'" + ms_data['fragment_id'] + ': ' + ms_data['met_id'] + ' @ ';
                            for pos_cnt,pos in enumerate(ms_data['met_atompositions']):
                                    tmp_script = tmp_script + ms_data['met_elements'][pos_cnt] + str(pos+1) + ' ';
                            tmp_script = tmp_script[:-1];
                            tmp_script = tmp_script + "';\n"
                            break;
                tmp_script = tmp_script + '});\n';
                tmp_script = tmp_script + 'd.mdvs = mdv;\n';
                mat_script = mat_script + tmp_script;

                ## write substrate labeling (i.e. tracer) information
                tmp_script = ''
                tmp_script = tmp_script + 't = tracer({...\n';
                for tracer in tracer_I:
                    if tracer['sample_name_abbreviation'] == sna:
                        tmp_script = tmp_script + "'" + tracer['met_name'] + ': ' + tracer['met_id'] + '.EX' + ' @ '
                        for cnt,met_atompositions in enumerate(tracer['met_atompositions']):
                                tmp_script = tmp_script + tracer['met_elements'][cnt]+str(met_atompositions) + ' '
                        tmp_script = tmp_script[:-1]; #remove extra white space
                        tmp_script = tmp_script + "';...\n";
                tmp_script = tmp_script + '});\n';
                tmp_script = tmp_script + 't.frac = [';
                for tracer in tracer_I:
                    if tracer['sample_name_abbreviation'] == sna:
                        tmp_script = tmp_script + str(tracer['ratio']) + ',';
                tmp_script = tmp_script[:-1]; #remove extra ,
                tmp_script = tmp_script + '];\n'; #remove extra ,
                mat_script = mat_script + tmp_script;
                    
                ## write flux measurements
                tmp_script = ''
                tmp_script = tmp_script + "f = data('";
                for flux in measuredFluxes_data_I:
                    if flux['sample_name_abbreviation'] == sna:
                        ## Temporary fix until reactions can be properly named
                        #tmp_script = tmp_script + rxn_ids_INCA[flux['rxn_id']] + " ";
                        tmp_script = tmp_script + flux['rxn_id'] + " ";
                tmp_script = tmp_script[:-1]; #remove extra ,
                tmp_script = tmp_script + "');\n";
                tmp_script = tmp_script + 'f.val = [...\n';
                for flux in measuredFluxes_data_I:
                    if flux['sample_name_abbreviation'] == sna: tmp_script = tmp_script + str(flux['flux_average']) + ',...\n';
                tmp_script = tmp_script + '];\n';
                tmp_script = tmp_script + 'f.std = [...\n';
                for flux in measuredFluxes_data_I:
                    if flux['sample_name_abbreviation'] == sna: tmp_script = tmp_script + str(flux['flux_stdev']) + ',...\n';
                tmp_script = tmp_script + '];\n';

                tmp_script = tmp_script + 'x = sna(t);\n'
                tmp_script = tmp_script + 'x.data_flx = f;\n'
                tmp_script = tmp_script + 'x.data_ms = d;\n'
                tmp_script = tmp_script + ('m.expts(%d) = x;\n' %(sna_cnt+1));
                tmp_script = tmp_script + ("m.expts(%d).id = {'%s'};\n" %(sna_cnt+1,sna));
                mat_script = mat_script + tmp_script;

            # Add in ms data or Write ms data to separate file
            for sna_cnt,sna in enumerate(snas):
                tmp_script = ''
                for i,fragment in enumerate(fragments):
                    for j,time in enumerate(times):
                        # Pad the data file:
                        tmp_script = tmp_script + ('m.expts(%d).data_ms(%d).mdvs.val(%d,%d) = %s;\n' %(sna_cnt+1,i+1,1,j+1,'NaN'));
                        tmp_script = tmp_script + ('m.expts(%d).data_ms(%d).mdvs.std(%d,%d) = %s;\n' %(sna_cnt+1,i+1,1,j+1,'NaN'));
                        for ms_data in snaalMS_data_I:
                            if ms_data['fragment_id']==fragments[i] and \
                                ms_data['time_point']==times[j] and \
                                ms_data['sample_name_abbreviation'] == sna:
                                for cnt,intensity in enumerate(ms_data['intensity_normalized_average']):
                                    # each column is a seperate time point
                                    # each row is a seperate mdv
                                    # Assign names and times
                                    name = fragment + '_' + str(cnt) + '_' + str(j) + '_' + str(sna);
                                    tmp_script = tmp_script + ("m.expts(%d).data_ms(%d).mdvs.id(%d,%d) = {'%s'};\n" %(sna_cnt+1,i+1,1,j+1,name));
                                    tmp_script = tmp_script + ("m.expts(%d).data_ms(%d).mdvs.time(%d,%d) = %s;\n" %(sna_cnt+1,i+1,1,j+1,time));
                                    # Assign values
                                    ave = ms_data['intensity_normalized_average'][cnt]
                                    stdev = ms_data['intensity_normalized_stdev'][cnt]
                                    # remove 0.0000 values and replace with NaN
                                    if ave < 1e-9: 
                                        ave = 'NaN';
                                        tmp_script = tmp_script + ('m.expts(%d).data_ms(%d).mdvs.val(%d,%d) = %s;\n' %(sna_cnt+1,i+1,cnt+1,j+1,ave));
                                    else:
                                        tmp_script = tmp_script + ('m.expts(%d).data_ms(%d).mdvs.val(%d,%d) = %f;\n' %(sna_cnt+1,i+1,cnt+1,j+1,ave));
                                    if stdev < 1e-9:
                                        # check if the ave is NaN
                                        if ave=='NaN': stdev = 'NaN';
                                        else: stdev = 0.0001;
                                        tmp_script = tmp_script + ('m.expts(%d).data_ms(%d).mdvs.std(%d,%d) = %s;\n' %(sna_cnt+1,i+1,cnt+1,j+1,stdev));
                                    else:
                                        tmp_script = tmp_script + ('m.expts(%d).data_ms(%d).mdvs.std(%d,%d) = %f;\n' %(sna_cnt+1,i+1,cnt+1,j+1,stdev));
                mat_script = mat_script + tmp_script;

        return mat_script;
    #Matlab Scripts for INCA
    def writeScript_model_INCA(self, modelReaction_data_I,modelMetabolite_data_I,
                                        measuredFluxes_data_I,experimentalMS_data_I,tracer_I):
        '''Generate the model information for INCA'''

        mat_script = 'clear functions\n';

        ##1. Define the model:

        ## debug reaction equations
        #tmp_script = ''
        #for rxn in modelReaction_data_I:
        #    #TODO check on how the reactions are named  
        #    tmp_script = tmp_script + 'r = reaction({...\n';
        #    tmp_script = tmp_script + "'" + rxn['rxn_equation'] + "';...\n"
        #    tmp_script = tmp_script + '});\n';
        #mat_script = mat_script + tmp_script;

        # write out reaction equations
        tmp_script = ''
        tmp_script = tmp_script + 'r = reaction({...\n';
        rxn_ids_INCA = {};
        cnt = 0
        for rxn_cnt,rxn in enumerate(modelReaction_data_I):
            #if not(rxn['upper_bound']==0.0 and rxn['lower_bound']==0.0):
                rxn_ids_INCA[rxn['rxn_id']] = ('R'+str(cnt+1));
                cnt+=1;
                #if rxn['rxn_id'] == 'Ec_biomass_iJO1366_WT_53p95M':
                #    tmp_script = tmp_script + "'" + self.biomass_INCA + "';...\n"
                #    #tmp_script = tmp_script + "'" + self.biomass_INCA_iJS2012 + "';...\n"
                #else:
                #    tmp_script = tmp_script + "'" + rxn['rxn_equation'] + "';...\n"
                tmp_script = tmp_script + "'" + rxn['rxn_equation'] + "';...\n"
            #else:
            #    print 'rxn_id ' + rxn['rxn_id'] + ' will be excluded from INCA' 
        tmp_script = tmp_script + '});\n';
        mat_script = mat_script + tmp_script;

        # setup the model
        mat_script = mat_script + 'm = model(r);\n'

        # Take care of symmetrical metabolites if not done so in the reaction equations
        tmp_script = ''
        for met in modelMetabolite_data_I:
            if met['met_symmetry_atompositions']:
                tmp_script = tmp_script + "m.mets{'" + met['met_id'] + "'}.sym = list('rotate180',map('";
                for cnt,atompositions in enumerate(met['met_atompositions']):
                    tmp_script = tmp_script + met['met_elements'][cnt] + str(atompositions+1) + ':' + met['met_symmetry_elements'][cnt] + str(met['met_symmetry_atompositions'][cnt]+1) + ' ';
                tmp_script = tmp_script[:-1];
                tmp_script = tmp_script + "'));\n";
        mat_script = mat_script + tmp_script;

        # Add in the metabolite states (balance), value, and lb/ub)
        tmp_script = ''
        # specify metabolites that should be forcible unbalanced
        #NOTE: hard-coded for now until a better workaround can be done
        metabolites_all = [x['met_id'] for x in modelMetabolite_data_I];
        for met in ['co2_e','h2o_e','h_e','na1_e']:
            if met in metabolites_all:
                tmp_script = tmp_script + "m.states{'" + met + ".EX" + "'}.bal = false";
                tmp_script = tmp_script + ";\n";
        for met in modelMetabolite_data_I:
            if '.balance' in met['met_id']:
                tmp_script = tmp_script + "m.states{'" + met['met_id']  + "'}.bal = false";
        mat_script = mat_script + tmp_script;

        # Add in initial fluxes (values lb/ub) and define the reaction ids
        tmp_script = ''
        tmp_script = tmp_script + 'm.rates.flx.lb = [...\n';
        # lower bounds
        for rxn_cnt,rxn in enumerate(modelReaction_data_I):
            #if not(rxn['upper_bound']==0.0 and rxn['lower_bound']==0.0):
                if measuredFluxes_data_I:
                    for flux in measuredFluxes_data_I:
                        if rxn['rxn_id'] == flux['rxn_id']:
                            tmp_script = tmp_script + str(flux['flux_lb']) + ',...\n'
                            break;
                        else:
                            tmp_script = tmp_script + str(rxn['lower_bound']) + ',...\n'
                            break;
                else: tmp_script = tmp_script + str(rxn['lower_bound']) + ',...\n'
        tmp_script = tmp_script + '];\n';
        tmp_script = tmp_script + 'm.rates.flx.ub = [...\n';
        # upper bounds
        for rxn_cnt,rxn in enumerate(modelReaction_data_I):
            #if not(rxn['upper_bound']==0.0 and rxn['lower_bound']==0.0):
                if measuredFluxes_data_I:
                    for flux in measuredFluxes_data_I:
                        if rxn['rxn_id'] == flux['rxn_id']:
                            tmp_script = tmp_script + str(flux['flux_ub']) + ',...\n'
                            break;
                        else:
                            tmp_script = tmp_script + str(rxn['upper_bound']) + ',...\n'
                            break;
                else: tmp_script = tmp_script + str(rxn['upper_bound']) + ',...\n'
        tmp_script = tmp_script + '];\n';
        tmp_script = tmp_script + 'm.rates.flx.val = [...\n';
        # intial flux values
        for rxn_cnt,rxn in enumerate(modelReaction_data_I):
            #if not(rxn['upper_bound']==0.0 and rxn['lower_bound']==0.0):
                tmp_script = tmp_script + str(rxn['flux_val']) + ',...\n'
        tmp_script = tmp_script + '];\n';
        tmp_script = tmp_script + 'm.rates.on = [...\n';
        # include/exclude a reaction from the simulation
        for rxn_cnt,rxn in enumerate(modelReaction_data_I):
            if rxn['flux_val']==0.0 and rxn['upper_bound']==0.0 and rxn['lower_bound']==0.0:
                #tmp_script = tmp_script + 'm.rates.on(' + str(rxn_cnt) + ') = 0;\n'
                tmp_script = tmp_script + 'false' + ',...\n'
            else:
                #tmp_script = tmp_script + 'm.rates.on(' + str(rxn_cnt) + ') = 1;\n'
                tmp_script = tmp_script + 'true' + ',...\n'
        tmp_script = tmp_script + '];\n';
        tmp_script = tmp_script + 'm.rates.id = {...\n';
        # rxn_ids
        for rxn_cnt,rxn in enumerate(modelReaction_data_I):
            #if not(rxn['upper_bound']==0.0 and rxn['lower_bound']==0.0):
                tmp_script = tmp_script + "'" + rxn['rxn_id'] + "',...\n"
        tmp_script = tmp_script + '};\n';
        tmp_script = tmp_script + 'm.rates.id = {...\n';

        for rxn_cnt,rxn in enumerate(modelReaction_data_I):
            tmp_script = tmp_script + "'" + rxn['rxn_id'] + "',...\n"
        tmp_script = tmp_script + '};\n';
        mat_script = mat_script + tmp_script;

        ## Check that fluxes are feasible
        #mat_script = mat_script + "m.rates.flx.val = mod2stoich(m)';\n"

        ## Add in the metabolite states (value and lb/ub)
        ##TODO: decide on met_equations structure
        ##NOTE: lb, ub, val = 0 for steady-state
        #mat_script = mat_script + 'm.states.flx.lb = [...';
        #for met in modelMetabolite_data_I:
        #    #TODO check on how the metabolites are named
        #    mat_script = mat_script + met['lower_bound'] + ',...\n'
        #mat_script = mat_script + '];\n';
        #mat_script = mat_script + 'm.states.flx.ub = [...';
        #for met in modelMetabolite_data_I:
        #    #TODO check on how the metabolites are named
        #    mat_script = mat_script + met['upper_bound'] + ',...\n'
        #mat_script = mat_script + '];\n';
        #mat_script = mat_script + 'm.states.flx.ub = [...';
        #for met in modelMetabolite_data_I:
        #    #TODO check on how the metabolites are named
        #    mat_script = mat_script + met['flux'] + ',...\n'
        #mat_script = mat_script + '];\n';

        return mat_script;
    def writeScript_experiment_INCA(self, modelReaction_data_I,modelMetabolite_data_I,
                                        measuredFluxes_data_I,experimentalMS_data_I,tracer_I,
                                        parallel_I = 'experiment_id'):
        '''Generate the experimental information for INCA'''##3. Define the experiment

        # write out the measured fragment information
        # (actual MS measurements will be written to the script later)
        mat_script = '';

        if parallel_I == 'experiment_id':
            experiments_all = [x['experiment_id'] for x in experimentalMS_data_I];
            experiments = list(set(experiments_all));
            experiments.sort();
        
            fragments_all = [x['fragment_id'] for x in experimentalMS_data_I];
            fragments = list(set(fragments_all));
            fragments.sort();
            mets_all = [x['met_id'] for x in experimentalMS_data_I];
            mets = list(set(mets_all));
            mets.sort();
            times_all = [x['time_point'] for x in experimentalMS_data_I];
            times = list(set(times_all));
            times.sort();

            for experiment_cnt,experiment in enumerate(experiments):
                tmp_script = ''
                tmp_script = tmp_script + 'd = msdata({...\n';
                for fragment in fragments:
                    for ms_data in experimentalMS_data_I:
                        if ms_data['fragment_id'] == fragment and ms_data['experiment_id'] == experiment:
                            tmp_script = tmp_script + "'" + ms_data['fragment_id'] + ': ' + ms_data['met_id'] + ' @ ';
                            for pos_cnt,pos in enumerate(ms_data['met_atompositions']):
                                    tmp_script = tmp_script + ms_data['met_elements'][pos_cnt] + str(pos+1) + ' ';
                            tmp_script = tmp_script[:-1];
                            tmp_script = tmp_script + "';\n"
                            break;
                tmp_script = tmp_script + '});\n';
                tmp_script = tmp_script + 'd.mdvs = mdv;\n';
                mat_script = mat_script + tmp_script;

                ## write substrate labeling (i.e. tracer) information
                tmp_script = ''
                tmp_script = tmp_script + 't = tracer({...\n';
                for tracer in tracer_I:
                    if tracer['experiment_id'] == experiment:
                        tmp_script = tmp_script + "'" + tracer['met_name'] + ': ' + tracer['met_id'] + '.EX' + ' @ '
                        for cnt,met_atompositions in enumerate(tracer['met_atompositions']):
                                tmp_script = tmp_script + tracer['met_elements'][cnt]+str(met_atompositions) + ' '
                        tmp_script = tmp_script[:-1]; #remove extra white space
                        tmp_script = tmp_script + "';...\n";
                tmp_script = tmp_script + '});\n';
                tmp_script = tmp_script + 't.frac = [';
                for tracer in tracer_I:
                    if tracer['experiment_id'] == experiment:
                        tmp_script = tmp_script + str(tracer['ratio']) + ',';
                tmp_script = tmp_script[:-1]; #remove extra ,
                tmp_script = tmp_script + '];\n'; #remove extra ,
                mat_script = mat_script + tmp_script;
                    
                ## write flux measurements
                tmp_script = ''
                tmp_script = tmp_script + "f = data('";
                for flux in measuredFluxes_data_I:
                    if flux['experiment_id'] == experiment:
                        ## Temporary fix until reactions can be properly named
                        #tmp_script = tmp_script + rxn_ids_INCA[flux['rxn_id']] + " ";
                        tmp_script = tmp_script + flux['rxn_id'] + " ";
                tmp_script = tmp_script[:-1]; #remove extra ,
                tmp_script = tmp_script + "');\n";
                tmp_script = tmp_script + 'f.val = [...\n';
                for flux in measuredFluxes_data_I:
                    if flux['experiment_id'] == experiment: tmp_script = tmp_script + str(flux['flux_average']) + ',...\n';
                tmp_script = tmp_script + '];\n';
                tmp_script = tmp_script + 'f.std = [...\n';
                for flux in measuredFluxes_data_I:
                    if flux['experiment_id'] == experiment: tmp_script = tmp_script + str(flux['flux_stdev']) + ',...\n';
                tmp_script = tmp_script + '];\n';

                tmp_script = tmp_script + 'x = experiment(t);\n'
                tmp_script = tmp_script + 'x.data_flx = f;\n'
                tmp_script = tmp_script + 'x.data_ms = d;\n'
                tmp_script = tmp_script + ('m.expts(%d) = x;\n' %(experiment_cnt+1));
                tmp_script = tmp_script + ("m.expts(%d).id = {'%s'};\n" %(experiment_cnt+1,experiment));
                mat_script = mat_script + tmp_script;

            # Add in ms data or Write ms data to separate file
            for experiment_cnt,experiment in enumerate(experiments):
                tmp_script = ''
                for i,fragment in enumerate(fragments):
                    for j,time in enumerate(times):
                        # Pad the data file:
                        tmp_script = tmp_script + ('m.expts(%d).data_ms(%d).mdvs.val(%d,%d) = %s;\n' %(experiment_cnt+1,i+1,1,j+1,'NaN'));
                        tmp_script = tmp_script + ('m.expts(%d).data_ms(%d).mdvs.std(%d,%d) = %s;\n' %(experiment_cnt+1,i+1,1,j+1,'NaN'));
                        for ms_data in experimentalMS_data_I:
                            if ms_data['fragment_id']==fragments[i] and \
                                ms_data['time_point']==times[j] and \
                                ms_data['experiment_id'] == experiment:
                                if not ms_data['intensity_normalized_average']: continue; #measurements will need to be added/simulated later
                                for cnt,intensity in enumerate(ms_data['intensity_normalized_average']):
                                    # each column is a seperate time point
                                    # each row is a seperate mdv
                                    # Assign names and times
                                    name = fragment + '_' + str(cnt) + '_' + str(j) + '_' + str(experiment);
                                    tmp_script = tmp_script + ("m.expts(%d).data_ms(%d).mdvs.id(%d,%d) = {'%s'};\n" %(experiment_cnt+1,i+1,1,j+1,name));
                                    tmp_script = tmp_script + ("m.expts(%d).data_ms(%d).mdvs.time(%d,%d) = %s;\n" %(experiment_cnt+1,i+1,1,j+1,time));
                                    # Assign values
                                    ave = ms_data['intensity_normalized_average'][cnt]
                                    stdev = ms_data['intensity_normalized_stdev'][cnt]
                                    # remove 0.0000 values and replace with NaN
                                    if ave < 1e-9: 
                                        ave = 'NaN';
                                        tmp_script = tmp_script + ('m.expts(%d).data_ms(%d).mdvs.val(%d,%d) = %s;\n' %(experiment_cnt+1,i+1,cnt+1,j+1,ave));
                                    else:
                                        tmp_script = tmp_script + ('m.expts(%d).data_ms(%d).mdvs.val(%d,%d) = %f;\n' %(experiment_cnt+1,i+1,cnt+1,j+1,ave));
                                    if stdev < 1e-9:
                                        # check if the ave is NaN
                                        if ave=='NaN': stdev = 'NaN';
                                        else: stdev = 0.0001;
                                        tmp_script = tmp_script + ('m.expts(%d).data_ms(%d).mdvs.std(%d,%d) = %s;\n' %(experiment_cnt+1,i+1,cnt+1,j+1,stdev));
                                    else:
                                        tmp_script = tmp_script + ('m.expts(%d).data_ms(%d).mdvs.std(%d,%d) = %f;\n' %(experiment_cnt+1,i+1,cnt+1,j+1,stdev));
                mat_script = mat_script + tmp_script;
        elif parallel_I == 'sample_name_abbreviation':
            snas_all = [x['sample_name_abbreviation'] for x in experimentalMS_data_I];
            snas = list(set(snas_all));
            snas.sort();
        
            fragments_all = [x['fragment_id'] for x in experimentalMS_data_I];
            fragments = list(set(fragments_all));
            fragments.sort();
            mets_all = [x['met_id'] for x in experimentalMS_data_I];
            mets = list(set(mets_all));
            mets.sort();
            times_all = [x['time_point'] for x in experimentalMS_data_I];
            times = list(set(times_all));
            times.sort();
        
            for sna_cnt,sna in enumerate(snas):
                tmp_script = ''
                tmp_script = tmp_script + 'd = msdata({...\n';
                for fragment in fragments:
                    for ms_data in experimentalMS_data_I:
                        if ms_data['fragment_id'] == fragment and ms_data['sample_name_abbreviation'] == sna:
                            tmp_script = tmp_script + "'" + ms_data['fragment_id'] + ': ' + ms_data['met_id'] + ' @ ';
                            for pos_cnt,pos in enumerate(ms_data['met_atompositions']):
                                    tmp_script = tmp_script + ms_data['met_elements'][pos_cnt] + str(pos+1) + ' ';
                            tmp_script = tmp_script[:-1];
                            tmp_script = tmp_script + "';\n"
                            break;
                tmp_script = tmp_script + '});\n';
                tmp_script = tmp_script + 'd.mdvs = mdv;\n';
                mat_script = mat_script + tmp_script;

                ## write substrate labeling (i.e. tracer) information
                tmp_script = ''
                tmp_script = tmp_script + 't = tracer({...\n';
                for tracer in tracer_I:
                    if tracer['sample_name_abbreviation'] == sna:
                        tmp_script = tmp_script + "'" + tracer['met_name'] + ': ' + tracer['met_id'] + '.EX' + ' @ '
                        for cnt,met_atompositions in enumerate(tracer['met_atompositions']):
                                tmp_script = tmp_script + tracer['met_elements'][cnt]+str(met_atompositions) + ' '
                        tmp_script = tmp_script[:-1]; #remove extra white space
                        tmp_script = tmp_script + "';...\n";
                tmp_script = tmp_script + '});\n';
                tmp_script = tmp_script + 't.frac = [';
                for tracer in tracer_I:
                    if tracer['sample_name_abbreviation'] == sna:
                        tmp_script = tmp_script + str(tracer['ratio']) + ',';
                tmp_script = tmp_script[:-1]; #remove extra ,
                tmp_script = tmp_script + '];\n'; #remove extra ,
                mat_script = mat_script + tmp_script;
                    
                ## write flux measurements
                tmp_script = ''
                tmp_script = tmp_script + "f = data('";
                for flux in measuredFluxes_data_I:
                    if flux['sample_name_abbreviation'] == sna:
                        ## Temporary fix until reactions can be properly named
                        #tmp_script = tmp_script + rxn_ids_INCA[flux['rxn_id']] + " ";
                        tmp_script = tmp_script + flux['rxn_id'] + " ";
                tmp_script = tmp_script[:-1]; #remove extra ,
                tmp_script = tmp_script + "');\n";
                tmp_script = tmp_script + 'f.val = [...\n';
                for flux in measuredFluxes_data_I:
                    if flux['sample_name_abbreviation'] == sna: tmp_script = tmp_script + str(flux['flux_average']) + ',...\n';
                tmp_script = tmp_script + '];\n';
                tmp_script = tmp_script + 'f.std = [...\n';
                for flux in measuredFluxes_data_I:
                    if flux['sample_name_abbreviation'] == sna: tmp_script = tmp_script + str(flux['flux_stdev']) + ',...\n';
                tmp_script = tmp_script + '];\n';
                
                tmp_script = tmp_script + 'x = experiment(t);\n'
                tmp_script = tmp_script + 'x.data_flx = f;\n'
                tmp_script = tmp_script + 'x.data_ms = d;\n'
                tmp_script = tmp_script + ('m.expts(%d) = x;\n' %(sna_cnt+1));
                tmp_script = tmp_script + ("m.expts(%d).id = {'%s'};\n" %(sna_cnt+1,sna));
                mat_script = mat_script + tmp_script;

            # Add in ms data or Write ms data to separate file
            for sna_cnt,sna in enumerate(snas):
                tmp_script = ''
                for i,fragment in enumerate(fragments):
                    for j,time in enumerate(times):
                        # Pad the data file:
                        tmp_script = tmp_script + ('m.expts(%d).data_ms(%d).mdvs.val(%d,%d) = %s;\n' %(sna_cnt+1,i+1,1,j+1,'NaN'));
                        tmp_script = tmp_script + ('m.expts(%d).data_ms(%d).mdvs.std(%d,%d) = %s;\n' %(sna_cnt+1,i+1,1,j+1,'NaN'));
                        for ms_data in experimentalMS_data_I:
                            if ms_data['fragment_id']==fragments[i] and \
                                ms_data['time_point']==times[j] and \
                                ms_data['sample_name_abbreviation'] == sna:
                                if not ms_data['intensity_normalized_average']: continue; #measurements will need to be added/simulated later
                                for cnt,intensity in enumerate(ms_data['intensity_normalized_average']):
                                    # each column is a seperate time point
                                    # each row is a seperate mdv
                                    # Assign names and times
                                    name = fragment + '_' + str(cnt) + '_' + str(j) + '_' + str(sna);
                                    tmp_script = tmp_script + ("m.expts(%d).data_ms(%d).mdvs.id(%d,%d) = {'%s'};\n" %(sna_cnt+1,i+1,1,j+1,name));
                                    tmp_script = tmp_script + ("m.expts(%d).data_ms(%d).mdvs.time(%d,%d) = %s;\n" %(sna_cnt+1,i+1,1,j+1,time));
                                    # Assign values
                                    ave = ms_data['intensity_normalized_average'][cnt]
                                    stdev = ms_data['intensity_normalized_stdev'][cnt]
                                    # remove 0.0000 values and replace with NaN
                                    if ave < 1e-9: 
                                        ave = 'NaN';
                                        tmp_script = tmp_script + ('m.expts(%d).data_ms(%d).mdvs.val(%d,%d) = %s;\n' %(sna_cnt+1,i+1,cnt+1,j+1,ave));
                                    else:
                                        tmp_script = tmp_script + ('m.expts(%d).data_ms(%d).mdvs.val(%d,%d) = %f;\n' %(sna_cnt+1,i+1,cnt+1,j+1,ave));
                                    if stdev < 1e-9:
                                        # check if the ave is NaN
                                        if ave=='NaN': stdev = 'NaN';
                                        else: stdev = 0.0001;
                                        tmp_script = tmp_script + ('m.expts(%d).data_ms(%d).mdvs.std(%d,%d) = %s;\n' %(sna_cnt+1,i+1,cnt+1,j+1,stdev));
                                    else:
                                        tmp_script = tmp_script + ('m.expts(%d).data_ms(%d).mdvs.std(%d,%d) = %f;\n' %(sna_cnt+1,i+1,cnt+1,j+1,stdev));
                mat_script = mat_script + tmp_script;
        return mat_script
    def writeScript_experimentFromMSData_INCA(self, modelReaction_data_I,modelMetabolite_data_I,
                                        measuredFluxes_data_I,experimentalMS_data_I,tracer_I,
                                        experiment_index_I=1,experiment_name_I=None):
        '''Generate the experimental MS data for INCA'''
        return
    def writeScript_experimentFromSimulation_INCA(self, modelReaction_data_I,modelMetabolite_data_I,
                                        measuredFluxes_data_I,experimentalMS_data_I,tracer_I,
                                        experiment_index_I=1,experiment_name_I=None):
        '''Generate simulated MS data for INCA'''

        mat_script = ''

        # check that the fluxes are feasible
        mat_script += "m.rates.flx.val = mod2stoich(m)';\n";

        # simulate measurements
        mat_script += "s = simulate(m);\n"
        mat_script += "m = sim2mod(m,s);\n" # copy simulated measurements into model

        # GC/MS standard error ranges linearly
        mat_script += "x0 = 0.005; e0 = 0.003; x1 = 0.25; e1 = 0.01;\n"
        mat_script += ("for i = 1:length(m.expts(%d).data_ms)\n" %(experiment_index_I))
        mat_script += ("\tm.expts(%d).data_ms(i).mdvs.std = max(min((e1-e0)/(x1-x0)*(m.expts(%d)data_ms(i).mdvs.val-x1)+e1,e1),e0);\n" %(experiment_index_I,experiment_index_I))
        mat_script += "end\n"

        # Introduce randomly distributed error into measurements
        mat_script += ("for i = 1:length(m.expts(%d).data_ms)\n" %(experiment_index_I))
        mat_script += ("m.expts(%d).data_ms(i).mdvs.val = normrnd(m.expts(%d).data_ms(i).mdvs.val,m.expts(%d).data_ms(i).mdvs.std" %(experiment_index_I,experiment_index_I,experiment_index_I))
        mat_script += "end\n"

        return mat_script
    def writeScript_simulationOptions_Inca(self,stationary_I=True):
        '''Generate parameters for isotopomer simulation for INCA1.1'''

        # Specify simulation parameters (non-stationary only!)
        '''% simulate MS measurements
        nmts = 8;                               % number of total measurements
        samp = 8/60/60;                         % spacing between measurements in hours
        m.options.int_tspan = 0:samp:(samp*nmts);   % time points in hours
        m.options.sim_tunit = 'h';              % hours are unit of time
        m.options.fit_reinit = true;
        m.options.sim_ss = false;
        m.options.sim_sens = true;'''

        mat_script = ''
        mat_script += 'm.options.fit_starts = 10;\n' #10 restarts during the estimation procedure

        return mat_script
    def writeScript_parameterEstimation_Inca(self):
        '''Run parameter estimations INCA1.1'''

        mat_script = ''
        mat_script += "f=estimate(m,10);\n" #10 restarts

        return mat_script
    def writeScript_parameterContinuation_Inca(self):
        '''Run parameter continuation INCA1.1'''

        mat_script = ''
        mat_script += "f=continuate(f,m);\n"

        return mat_script
    def make_isotopomerSimulation_parallel_experimentID_INCA(self,simulation_info, stationary_I = True, ko_list_I=[],flux_dict_I={},description_I=None):
        '''Make parallel labeling simulation by experiment_id for INCA'''
        
        model_id = simulation_info['model_id'][0]
        mapping_id = simulation_info['mapping_id'][0]
        time_points = simulation_info['time_point'][0]
        experiment_ids = simulation_info['experiment_id']
        sna = simulation_info['sample_name_abbreviation'][0]
        # collect the simulation data
        modelReaction_data,modelMetabolite_data,measuredFluxes_data,experimentalMS_data,tracers = [],[],[],[],[];
        for experiment_cnt,experiment_id in enumerate(experiment_ids):
            # get the tracers
            tracers_tmp = [];
            tracers_tmp = self.stage02_isotopomer_query.get_rows_experimentIDAndSampleNameAbbreviation_dataStage02IsotopomerTracers(experiment_id,sna);  
            tracers.extend(tracers_tmp); 
            # get flux measurements
            measuredFluxes_data_tmp = [];
            measuredFluxes_data_tmp = self.stage02_isotopomer_query.get_rows_experimentIDAndModelIDAndSampleNameAbbreviation_dataStage02IsotopomerMeasuredFluxes(experiment_id,model_id,sna);
            measuredFluxes_data.extend(measuredFluxes_data_tmp)
            # get the ms_data
            if stationary_I:
                experimentalMS_data_tmp = [];
                experimentalMS_data_tmp = self.stage02_isotopomer_query.get_row_experimentIDAndSampleNameAbbreviationAndTimePoint_dataStage02IsotopomerMeasuredFragments(experiment_id,sna,time_points[0]);
                experimentalMS_data.extend(experimentalMS_data_tmp);
            else:
                experimentalMS_data_tmp = [];
                experimentalMS_data = self.stage02_isotopomer_query.get_row_experimentIDAndSampleNameAbbreviation_dataStage02IsotopomerMeasuredFragments(experiment_id,sna);
                experimentalMS_data.extend(experimentalMS_data_tmp);
            #get model reactions
            if not modelReaction_data: #only once
                modelReaction_data = [];
                modelReaction_data = self.stage02_isotopomer_query.get_rows_modelID_dataStage02IsotopomerModelReactions(model_id);
                #simulate the model
                cobra_model = self.simulate_model(model_id,ko_list_I,flux_dict_I,measuredFluxes_data,description_I);
                for i,row in enumerate(modelReaction_data):
                    #get atom mapping data
                    atomMapping = {};
                    atomMapping = self.stage02_isotopomer_query.get_row_mappingIDAndRxnID_dataStage02IsotopomerAtomMappingReactions(mapping_id,row['rxn_id']);
                    #generate reaction equations
                    rxn_equation = '';
                    print row['rxn_id']
                    #if row['rxn_id'] == 'EX_glc_LPAREN_e_RPAREN_':
                    #    print 'check'
                    if atomMapping:
                        rxn_equation = self.make_isotopomerRxnEquations_INCA(
                                    row['reactants_ids'],
                                    row['products_ids'],
                                    row['reactants_stoichiometry'],
                                    row['products_stoichiometry'],
                                    row['reversibility'],
                                    atomMapping['reactants_stoichiometry_tracked'],
                                    atomMapping['products_stoichiometry_tracked'],
                                    atomMapping['reactants_ids_tracked'],
                                    atomMapping['products_ids_tracked'],
                                    atomMapping['reactants_elements_tracked'],
                                    atomMapping['products_elements_tracked'],
                                    atomMapping['reactants_positions_tracked'],
                                    atomMapping['products_positions_tracked'],
                                    atomMapping['reactants_mapping'],
								    atomMapping['products_mapping']);
                    else:
                        rxn_equation = self.make_isotopomerRxnEquations_INCA(
                                    row['reactants_ids'],
                                    row['products_ids'],
                                    row['reactants_stoichiometry'],
                                    row['products_stoichiometry'],
                                    row['reversibility'],
                                    [],
                                    [],
                                    [],
                                    [],
                                    [],
                                    [],
                                    [],
                                    [],
                                    [],
								    []);
                    atomMapping['rxn_equation']=rxn_equation;
                    modelReaction_data[i].update(atomMapping);
                    # update the lower bounds and upper bounds of the model to represent the experimental data
                    if measuredFluxes_data:
                        for flux in measuredFluxes_data:
                            if row['rxn_id'] == flux['rxn_id']:
                                modelReaction_data[i]['lower_bound'] = flux['flux_lb']
                                modelReaction_data[i]['upper_bound'] = flux['flux_ub']
                    # update the lower bounds and upper bounds of the model to represent the input data (if the model has not already been updated)
                    for ko in ko_list_I: # implement optimal KOs
                        if row['rxn_id'] == ko:
                            modelReaction_data[i]['lower_bound'] = 0.0;
                            modelReaction_data[i]['upper_bound'] = 0.0;
                    for rxn,flux in flux_dict_I.iteritems():  # implement flux constraints:
                        if row['rxn_id'] == rxn:
                            modelReaction_data[i]['lower_bound'] = flux['lb'];
                            modelReaction_data[i]['upper_bound'] = flux['ub'];
                    # add in a flux_val field to supply an initial starting guess for the MFA solver
                    if cobra_model.solution.f:
                        modelReaction_data[i]['flux_val'] = cobra_model.solution.x_dict[row['rxn_id']];
                    else:
                        modelReaction_data[i]['flux_val'] = 0;
            # get model metabolites
            if not modelMetabolite_data: #only once
                modelMetabolite_data = [];
                modelMetabolite_data = self.stage02_isotopomer_query.get_rows_modelID_dataStage02IsotopomerModelMetabolites(model_id);
                for i,row in enumerate(modelMetabolite_data):
                    #get atom mapping data
                    atomMapping = {};
                    atomMapping = self.stage02_isotopomer_query.get_rows_mappingIDAndMetID_dataStage02IsotopomerAtomMappingMetabolites(mapping_id,row['met_id']);
                    #update
                    if atomMapping:
                        modelMetabolite_data[i].update(atomMapping);
                    else:
                        modelMetabolite_data[i].update({
                            'met_elements':None,
                            'met_atompositions':None,
                            'met_symmetry_elements':None,
                            'met_symmetry_atompositions':None});
        # Write out to matlab script
        filename_mat = settings.workspace_data + '/_output/' + re.sub('[.\/]','',simulation_info['simulation_id'][0]);
        filename_mat_model = filename_mat + "_model" + '.m';
        mat_script = '';
        mat_script += self.writeScript_model_INCA(modelReaction_data,modelMetabolite_data,
                                        measuredFluxes_data,experimentalMS_data,tracers)
        mat_script += self.writeScript_simulationOptions_Inca(stationary_I)
        mat_script += self.writeScript_experiment_INCA(modelReaction_data,modelMetabolite_data,
                                                measuredFluxes_data,experimentalMS_data,tracers,
                                                'sample_name_abbreviation')
        with open(filename_mat_model,'w') as f:
            f.write(mat_script);
    def make_isotopomerSimulation_parallel_sna_INCA(self,simulation_info, stationary_I = True, ko_list_I=[],flux_dict_I={},description_I=None):
        '''Make parallel labeling simulation by sample name abbreviation for INCA'''
        
        model_id = simulation_info['model_id'][0]
        mapping_id = simulation_info['mapping_id'][0]
        time_points = simulation_info['time_point']
        experiment_id = simulation_info['experiment_id'][0]
        sample_name_abbreviations = simulation_info['sample_name_abbreviation']
        # collect the simulation data
        modelReaction_data,modelMetabolite_data,measuredFluxes_data,experimentalMS_data,tracers = [],[],[],[],[];
        for sna_cnt,sna in enumerate(sample_name_abbreviations):
            # get the tracers
            tracers_tmp = [];
            tracers_tmp = self.stage02_isotopomer_query.get_rows_experimentIDAndSampleNameAbbreviation_dataStage02IsotopomerTracers(experiment_id,sna);  
            tracers.extend(tracers_tmp); 
            # get flux measurements
            measuredFluxes_data_tmp = [];
            measuredFluxes_data_tmp = self.stage02_isotopomer_query.get_rows_experimentIDAndModelIDAndSampleNameAbbreviation_dataStage02IsotopomerMeasuredFluxes(experiment_id,model_id,sna);
            measuredFluxes_data.extend(measuredFluxes_data_tmp)
            # get the ms_data
            if stationary_I:
                experimentalMS_data_tmp = [];
                experimentalMS_data_tmp = self.stage02_isotopomer_query.get_row_experimentIDAndSampleNameAbbreviationAndTimePoint_dataStage02IsotopomerMeasuredFragments(experiment_id,sna,time_points[0]);
                experimentalMS_data.extend(experimentalMS_data_tmp);
            else:
                experimentalMS_data_tmp = [];
                experimentalMS_data = self.stage02_isotopomer_query.get_row_experimentIDAndSampleNameAbbreviation_dataStage02IsotopomerMeasuredFragments(experiment_id,sna);
                experimentalMS_data.extend(experimentalMS_data_tmp);
            #get model reactions
            if not modelReaction_data: #only once
                modelReaction_data = [];
                modelReaction_data = self.stage02_isotopomer_query.get_rows_modelID_dataStage02IsotopomerModelReactions(model_id);
                #simulate the model
                cobra_model = self.simulate_model(model_id,ko_list_I,flux_dict_I,measuredFluxes_data,description_I);
                for i,row in enumerate(modelReaction_data):
                    #get atom mapping data
                    atomMapping = {};
                    atomMapping = self.stage02_isotopomer_query.get_row_mappingIDAndRxnID_dataStage02IsotopomerAtomMappingReactions(mapping_id,row['rxn_id']);
                    #generate reaction equations
                    rxn_equation = '';
                    print row['rxn_id']
                    #if row['rxn_id'] == 'EX_glc_LPAREN_e_RPAREN_':
                    #    print 'check'
                    if atomMapping:
                        rxn_equation = self.make_isotopomerRxnEquations_INCA(
                                    row['reactants_ids'],
                                    row['products_ids'],
                                    row['reactants_stoichiometry'],
                                    row['products_stoichiometry'],
                                    row['reversibility'],
                                    atomMapping['reactants_stoichiometry_tracked'],
                                    atomMapping['products_stoichiometry_tracked'],
                                    atomMapping['reactants_ids_tracked'],
                                    atomMapping['products_ids_tracked'],
                                    atomMapping['reactants_elements_tracked'],
                                    atomMapping['products_elements_tracked'],
                                    atomMapping['reactants_positions_tracked'],
                                    atomMapping['products_positions_tracked'],
                                    atomMapping['reactants_mapping'],
								    atomMapping['products_mapping']);
                    else:
                        rxn_equation = self.make_isotopomerRxnEquations_INCA(
                                    row['reactants_ids'],
                                    row['products_ids'],
                                    row['reactants_stoichiometry'],
                                    row['products_stoichiometry'],
                                    row['reversibility'],
                                    [],
                                    [],
                                    [],
                                    [],
                                    [],
                                    [],
                                    [],
                                    [],
                                    [],
								    []);
                    atomMapping['rxn_equation']=rxn_equation;
                    modelReaction_data[i].update(atomMapping);
                    # update the lower bounds and upper bounds of the model to represent the experimental data
                    if measuredFluxes_data:
                        for flux in measuredFluxes_data:
                            if row['rxn_id'] == flux['rxn_id']:
                                modelReaction_data[i]['lower_bound'] = flux['flux_lb']
                                modelReaction_data[i]['upper_bound'] = flux['flux_ub']
                    # update the lower bounds and upper bounds of the model to represent the input data (if the model has not already been updated)
                    for ko in ko_list_I: # implement optimal KOs
                        if row['rxn_id'] == ko:
                            modelReaction_data[i]['lower_bound'] = 0.0;
                            modelReaction_data[i]['upper_bound'] = 0.0;
                    for rxn,flux in flux_dict_I.iteritems():  # implement flux constraints:
                        if row['rxn_id'] == rxn:
                            modelReaction_data[i]['lower_bound'] = flux['lb'];
                            modelReaction_data[i]['upper_bound'] = flux['ub'];
                    # add in a flux_val field to supply an initial starting guess for the MFA solver
                    if cobra_model.solution.f:
                        modelReaction_data[i]['flux_val'] = cobra_model.solution.x_dict[row['rxn_id']];
                    else:
                        modelReaction_data[i]['flux_val'] = 0;
            # get model metabolites
            if not modelMetabolite_data: #only once
                modelMetabolite_data = [];
                modelMetabolite_data = self.stage02_isotopomer_query.get_rows_modelID_dataStage02IsotopomerModelMetabolites(model_id);
                for i,row in enumerate(modelMetabolite_data):
                    #get atom mapping data
                    atomMapping = {};
                    atomMapping = self.stage02_isotopomer_query.get_rows_mappingIDAndMetID_dataStage02IsotopomerAtomMappingMetabolites(mapping_id,row['met_id']);
                    #update
                    if atomMapping:
                        modelMetabolite_data[i].update(atomMapping);
                    else:
                        modelMetabolite_data[i].update({
                            'met_elements':None,
                            'met_atompositions':None,
                            'met_symmetry_elements':None,
                            'met_symmetry_atompositions':None});
        # Write out to matlab script
        filename_mat = settings.workspace_data + '/_output/' + re.sub('[.\/]','',simulation_info['simulation_id'][0]);
        filename_mat_model = filename_mat + "_model" + '.m';
        mat_script = '';
        mat_script += self.writeScript_model_INCA(modelReaction_data,modelMetabolite_data,
                                        measuredFluxes_data,experimentalMS_data,tracers)
        mat_script += self.writeScript_simulationOptions_Inca(stationary_I)
        mat_script += self.writeScript_experiment_INCA(modelReaction_data,modelMetabolite_data,
                                                measuredFluxes_data,experimentalMS_data,tracers,
                                                'sample_name_abbreviation')
        with open(filename_mat_model,'w') as f:
            f.write(mat_script);
    def make_isotopomerSimulation_individual_INCA(self,simulation_info, stationary_I = True, ko_list_I=[],flux_dict_I={},description_I=None):
        '''Make individual labeling simulations for INCA'''
        
        model_id = simulation_info['model_id'][0]
        mapping_id = simulation_info['mapping_id'][0]
        time_points = simulation_info['time_point']
        experiment_ids = simulation_info['experiment_id']
        sample_name_abbreviations = simulation_info['sample_name_abbreviation']
        for experiment_id in experiment_ids:
            for sna_cnt,sna in enumerate(sample_name_abbreviations):
                print 'Collecting and writing experimental and model data for sample name abbreviation ' + sna;
                # get the tracers
                tracers = [];
                tracers = self.stage02_isotopomer_query.get_rows_experimentIDAndSampleNameAbbreviation_dataStage02IsotopomerTracers(experiment_id,sna);

                # data containers
                modelReaction_data,modelMetabolite_data,measuredFluxes_data,experimentalMS_data = [],[],[],[];  
                # get flux measurements
                measuredFluxes_data = [];
                measuredFluxes_data = self.stage02_isotopomer_query.get_rows_experimentIDAndModelIDAndSampleNameAbbreviation_dataStage02IsotopomerMeasuredFluxes(experiment_id,model_id,sna);
                # get the ms_data
                if stationary_I:
                    experimentalMS_data = [];
                    experimentalMS_data = self.stage02_isotopomer_query.get_row_experimentIDAndSampleNameAbbreviationAndTimePoint_dataStage02IsotopomerMeasuredFragments(experiment_id,sna,time_points[0]);
                else:
                    experimentalMS_data = [];
                    experimentalMS_data = self.stage02_isotopomer_query.get_row_experimentIDAndSampleNameAbbreviation_dataStage02IsotopomerMeasuredFragments(experiment_id,sna);
                #get model reactions
                modelReaction_data = [];
                modelReaction_data = self.stage02_isotopomer_query.get_rows_modelID_dataStage02IsotopomerModelReactions(model_id);
                #simulate the model
                cobra_model = self.simulate_model(model_id,ko_list_I,flux_dict_I,measuredFluxes_data,description_I);
                for i,row in enumerate(modelReaction_data):
                    #get atom mapping data
                    atomMapping = {};
                    atomMapping = self.stage02_isotopomer_query.get_row_mappingIDAndRxnID_dataStage02IsotopomerAtomMappingReactions(mapping_id,row['rxn_id']);
                    #generate reaction equations
                    rxn_equation = '';
                    print row['rxn_id']
                    #if row['rxn_id'] == 'EX_glc_LPAREN_e_RPAREN_':
                    #    print 'check'
                    if atomMapping:
                        rxn_equation = self.make_isotopomerRxnEquations_INCA(
                                    row['reactants_ids'],
                                    row['products_ids'],
                                    row['reactants_stoichiometry'],
                                    row['products_stoichiometry'],
                                    row['reversibility'],
                                    atomMapping['reactants_stoichiometry_tracked'],
                                    atomMapping['products_stoichiometry_tracked'],
                                    atomMapping['reactants_ids_tracked'],
                                    atomMapping['products_ids_tracked'],
                                    atomMapping['reactants_elements_tracked'],
                                    atomMapping['products_elements_tracked'],
                                    atomMapping['reactants_positions_tracked'],
                                    atomMapping['products_positions_tracked'],
                                    atomMapping['reactants_mapping'],
								    atomMapping['products_mapping']);
                    else:
                        rxn_equation = self.make_isotopomerRxnEquations_INCA(
                                    row['reactants_ids'],
                                    row['products_ids'],
                                    row['reactants_stoichiometry'],
                                    row['products_stoichiometry'],
                                    row['reversibility'],
                                    [],
                                    [],
                                    [],
                                    [],
                                    [],
                                    [],
                                    [],
                                    [],
                                    [],
								    []);
                    atomMapping['rxn_equation']=rxn_equation;
                    modelReaction_data[i].update(atomMapping);
                    # update the lower bounds and upper bounds of the model to represent the experimental data
                    if measuredFluxes_data:
                        for flux in measuredFluxes_data:
                            if row['rxn_id'] == flux['rxn_id']:
                                modelReaction_data[i]['lower_bound'] = flux['flux_lb']
                                modelReaction_data[i]['upper_bound'] = flux['flux_ub']
                    # update the lower bounds and upper bounds of the model to represent the input data (if the model has not already been updated)
                    for ko in ko_list_I: # implement optimal KOs
                        if row['rxn_id'] == ko:
                            modelReaction_data[i]['lower_bound'] = 0.0;
                            modelReaction_data[i]['upper_bound'] = 0.0;
                    for rxn,flux in flux_dict_I.iteritems():  # implement flux constraints:
                        if row['rxn_id'] == rxn:
                            modelReaction_data[i]['lower_bound'] = flux['lb'];
                            modelReaction_data[i]['upper_bound'] = flux['ub'];
                    # add in a flux_val field to supply an initial starting guess for the MFA solver
                    if cobra_model.solution.f and cobra_model.solution.x_dict.has_key(row['rxn_id']):
                        modelReaction_data[i]['flux_val'] = cobra_model.solution.x_dict[row['rxn_id']];
                    else:
                        modelReaction_data[i]['flux_val'] = 0;
                # get model metabolites
                modelMetabolite_data = [];
                modelMetabolite_data = self.stage02_isotopomer_query.get_rows_modelID_dataStage02IsotopomerModelMetabolites(model_id);
                for i,row in enumerate(modelMetabolite_data):
                    #get atom mapping data
                    atomMapping = {};
                    atomMapping = self.stage02_isotopomer_query.get_rows_mappingIDAndMetID_dataStage02IsotopomerAtomMappingMetabolites(mapping_id,row['met_id']);
                    #update
                    if atomMapping:
                        modelMetabolite_data[i].update(atomMapping);
                    else:
                        modelMetabolite_data[i].update({
                            'met_elements':None,
                            'met_atompositions':None,
                            'met_symmetry_elements':None,
                            'met_symmetry_atompositions':None});

                ## dump the experiment to a matlab script to generate the matlab files in matlab
                # Matlab script file to make the structures
                filename_mat = settings.workspace_data + '/_output/' + re.sub('[.\/]','',simulation_info['simulation_id'][0]);
                filename_mat_model = filename_mat + "_model" + '.m';
                mat_script = '';
                mat_script += self.writeScript_model_INCA(modelReaction_data,modelMetabolite_data,
                                                measuredFluxes_data,experimentalMS_data,tracers)
                mat_script += self.writeScript_simulationOptions_Inca(stationary_I)
                mat_script += self.writeScript_experiment_INCA(modelReaction_data,modelMetabolite_data,
                                                        measuredFluxes_data,experimentalMS_data,tracers,
                                                        'sample_name_abbreviation')
        with open(filename_mat_model,'w') as f:
            f.write(mat_script);
    def make_isotopomerRxnEquations_INCA(self,reactants_ids_I = [],
                                        products_ids_I = [],
                                        reactants_stoichiometry_I = [],
                                        products_stoichiometry_I = [],
                                        reversibility_I = True,
                                        reactants_stoichiometry_tracked_I = [],
                                        products_stoichiometry_tracked_I = [],
                                        reactants_ids_tracked_I = [],
                                        products_ids_tracked_I = [],
                                        reactants_elements_tracked_I = [[]],
                                        products_elements_tracked_I = [[]],
                                        reactants_positions_tracked_I = [[]],
                                        products_positions_tracked_I = [[]],
                                        reactants_mapping_I = [],
                                        products_mapping_I = []):
        '''Generate string represention of reactions equations for INCA1.1'''

        #e.g. A (AabB) + H (c) -> B (AbBc) + H (a)
        #e.g. A (C1:A C2:B H1R:a H1S:b) + H (H1:c) -> B (C1:A C2:B H1:a H2:c) + H (H1:a)

        rxn_equations_INCA = '';

        #add balance dummy metabolite for an exchange reaction
        if len(reactants_ids_I)==0 and len(products_ids_I)==1:
            reactants_ids_I=[products_ids_I[0] + '.EX'];
            reactants_stoichiometry_I=[products_stoichiometry_I[0]]
            if products_ids_tracked_I and products_ids_tracked_I[0]:
                reactants_stoichiometry_tracked_I=[products_stoichiometry_tracked_I[0]]
                reactants_ids_tracked_I=[products_ids_tracked_I[0] + '.EX']
                reactants_elements_tracked_I=[products_elements_tracked_I[0]]
                reactants_positions_tracked_I=[products_positions_tracked_I[0]]
                reactants_mapping_I=[products_mapping_I[0]]
        elif len(products_ids_I)==0 and len(reactants_ids_I)==1:
            products_ids_I=[reactants_ids_I[0] + '.EX'];
            products_stoichiometry_I=[reactants_stoichiometry_I[0]]
            if reactants_ids_tracked_I and reactants_ids_tracked_I[0]:
                products_stoichiometry_tracked_I=[reactants_stoichiometry_tracked_I[0]]
                products_ids_tracked_I=[reactants_ids_tracked_I[0] + '.EX']
                products_elements_tracked_I=[reactants_elements_tracked_I[0]]
                products_positions_tracked_I=[reactants_positions_tracked_I[0]]
                products_mapping_I=[reactants_mapping_I[0]]

        # pseudo metabolites
        pseudo_mets = [];

        #build the string for the reactants
        for reactant_cnt,reactant in enumerate(reactants_ids_I):
            reactants_stoichiometry = abs(reactants_stoichiometry_I[reactant_cnt]);
            if reactant in reactants_ids_tracked_I:
                for reactant_tracked_cnt, reactant_tracked in enumerate(reactants_ids_tracked_I):
                    if reactant_tracked == reactant and \
                        reactants_stoichiometry == abs(reactants_stoichiometry_tracked_I[reactant_tracked_cnt]):
                        # if the tracked reactant matches and the stoichiometry aggrees, 
                        # combine the information for the tracked_reactant and the reactant
                        #rxn_equations_INCA += ('%f' % reactants_stoichiometry) + '*' + reactant + ' ';
                        rxn_equations_INCA += str(reactants_stoichiometry) + '*' + reactant + ' ';
                        rxn_equations_INCA += '(';
                        if reactants_mapping_I[reactant_tracked_cnt]:
                            reactants_mapping = reactants_mapping_I[reactant_tracked_cnt];
                            if '[' in reactants_mapping_I[reactant_tracked_cnt]:
                                reactants_mapping = reactants_mapping_I[reactant_tracked_cnt].split('][');
                                reactants_mapping = [m.replace('[','') for m in reactants_mapping];
                                reactants_mapping = [m.replace(']','') for m in reactants_mapping];
                            for mapping_cnt, mapping in enumerate(reactants_mapping):
                                rxn_equations_INCA += reactants_elements_tracked_I[reactant_tracked_cnt][mapping_cnt] + \
                                    str(reactants_positions_tracked_I[reactant_tracked_cnt][mapping_cnt]+1) + \
                                    ':' + mapping + ' ';
                            rxn_equations_INCA = rxn_equations_INCA[:-1];
                            rxn_equations_INCA += ') ';
                            rxn_equations_INCA += '+ ';
                            reactants_stoichiometry -= abs(reactants_stoichiometry_tracked_I[reactant_tracked_cnt]); # subtract out the stoichiometry of the tracked reactant from the reactant
                    elif reactant_tracked == reactant and \
                        reactants_stoichiometry > abs(reactants_stoichiometry_tracked_I[reactant_tracked_cnt]):
                        # if the tracked reactant matches and the stoichiometry of the reactant is greater than the tracked_reactant, 
                        # combine the information for the tracked_reactant and the reactant after substracking out the stoichiometry of the tracked_reactant
                        rxn_equations_INCA += str(abs(reactants_stoichiometry_tracked_I[reactant_tracked_cnt])) + '*' + reactant + ' ';
                        rxn_equations_INCA += '(';
                        if reactants_mapping_I[reactant_tracked_cnt]:
                            reactants_mapping = reactants_mapping_I[reactant_tracked_cnt];
                            if '[' in reactants_mapping_I[reactant_tracked_cnt]:
                                reactants_mapping = reactants_mapping_I[reactant_tracked_cnt].split('][');
                                reactants_mapping = [m.replace('[','') for m in reactants_mapping];
                                reactants_mapping = [m.replace(']','') for m in reactants_mapping];
                            for mapping_cnt, mapping in enumerate(reactants_mapping):
                                rxn_equations_INCA += reactants_elements_tracked_I[reactant_tracked_cnt][mapping_cnt] + \
                                    str(reactants_positions_tracked_I[reactant_tracked_cnt][mapping_cnt]+1) + \
                                    ':' + mapping + ' ';
                            rxn_equations_INCA = rxn_equations_INCA[:-1];
                            rxn_equations_INCA += ') ';
                            rxn_equations_INCA += '+ ';
                            reactants_stoichiometry -= abs(reactants_stoichiometry_tracked_I[reactant_tracked_cnt]) # subtract out the stoichiometry of the tracked reactant from the reactant and continue
                    elif not reactant_tracked in reactants_ids_I:
                        print 'unaccounted for reactant_tracked: ' + reactant_tracked;
                        if reactants_stoichiometry_tracked_I[reactant_tracked_cnt]==-1e-13 and not reactant_tracked in pseudo_mets:
                            #add in the pseudo-metabolite used to complete the atom mapping
                            rxn_equations_INCA += '0.0000000000001' + '*' + reactant_tracked + ' ';
                            rxn_equations_INCA += '(';
                            if reactants_mapping_I[reactant_tracked_cnt]:
                                reactants_mapping = reactants_mapping_I[reactant_tracked_cnt];
                                if '[' in reactants_mapping_I[reactant_tracked_cnt]:
                                    reactants_mapping = reactants_mapping_I[reactant_tracked_cnt].split('][');
                                    reactants_mapping = [m.replace('[','') for m in reactants_mapping];
                                    reactants_mapping = [m.replace(']','') for m in reactants_mapping];
                                for mapping_cnt, mapping in enumerate(reactants_mapping):
                                    rxn_equations_INCA += reactants_elements_tracked_I[reactant_tracked_cnt][mapping_cnt] + \
                                        str(reactants_positions_tracked_I[reactant_tracked_cnt][mapping_cnt]+1) + \
                                        ':' + mapping + ' ';
                                rxn_equations_INCA = rxn_equations_INCA[:-1];
                                rxn_equations_INCA += ') ';
                                rxn_equations_INCA += '+ ';
                                pseudo_mets.append(reactant_tracked); # only 1 unique pseudo_met per reaction
                if reactants_stoichiometry>0.0: # check if there is a remainder of the reactant stoichiometry that has not yet been accounted for
                                                # after iterating through all reactants
                                                # if so, the molecule is not tracked
                    rxn_equations_INCA += str(reactants_stoichiometry) + '*' + reactant + ' ';
                    rxn_equations_INCA += '+ ';
            else:
                rxn_equations_INCA += str(reactants_stoichiometry) + '*' + reactant + ' ';
                rxn_equations_INCA += '+ ';
        rxn_equations_INCA = rxn_equations_INCA[:-2];
        if reversibility_I:
            rxn_equations_INCA += '<->  ';
        else:
            rxn_equations_INCA += '->  ';
        #build the string for the products
        for product_cnt,product in enumerate(products_ids_I):
            if product_cnt == 0: rxn_equations_INCA = rxn_equations_INCA[:-1];
            #rxn_equations_INCA += str(abs(reactants_stoichiometry_I[product_cnt])) + '*' + product + ' ';
            products_stoichiometry = abs(products_stoichiometry_I[product_cnt]);
            if product in products_ids_tracked_I:
                for product_tracked_cnt, product_tracked in enumerate(products_ids_tracked_I):
                    if product_tracked == product and \
                        products_stoichiometry == abs(products_stoichiometry_tracked_I[product_tracked_cnt]):
                        # if the tracked product matches and the stoichiometry aggrees, 
                        # combine the information for the tracked_product and the product
                        rxn_equations_INCA += str(products_stoichiometry) + '*' + product + ' ';
                        rxn_equations_INCA += '(';
                        if products_mapping_I[product_tracked_cnt]:
                            products_mapping = products_mapping_I[product_tracked_cnt];
                            if '[' in products_mapping_I[product_tracked_cnt]:
                                products_mapping = products_mapping_I[product_tracked_cnt].split('][');
                                products_mapping = [m.replace('[','') for m in products_mapping];
                                products_mapping = [m.replace(']','') for m in products_mapping];
                            for mapping_cnt, mapping in enumerate(products_mapping):
                                rxn_equations_INCA += products_elements_tracked_I[product_tracked_cnt][mapping_cnt] + \
                                    str(products_positions_tracked_I[product_tracked_cnt][mapping_cnt]+1) + \
                                    ':' + mapping + ' ';
                            rxn_equations_INCA = rxn_equations_INCA[:-1];
                            rxn_equations_INCA += ') ';
                            rxn_equations_INCA += '+ ';
                            products_stoichiometry -= abs(products_stoichiometry_tracked_I[product_tracked_cnt]);
                    elif product_tracked == product and \
                        products_stoichiometry > abs(products_stoichiometry_tracked_I[product_tracked_cnt]):
                        # if the tracked product matches and the stoichiometry of the product is greater than the tracked_product, 
                        # combine the information for the tracked_product and the product after substracking out the stoichiometry of the tracked_product
                        rxn_equations_INCA += str(products_stoichiometry_tracked_I[product_tracked_cnt]) + '*' + product + ' ';
                        rxn_equations_INCA += '(';
                        if products_mapping_I[product_tracked_cnt]:
                            products_mapping = products_mapping_I[product_tracked_cnt];
                            if '[' in products_mapping_I[product_tracked_cnt]:
                                products_mapping = products_mapping_I[product_tracked_cnt].split('][');
                                products_mapping = [m.replace('[','') for m in products_mapping];
                                products_mapping = [m.replace(']','') for m in products_mapping];
                            for mapping_cnt, mapping in enumerate(products_mapping):
                                rxn_equations_INCA += products_elements_tracked_I[product_tracked_cnt][mapping_cnt] + \
                                    str(products_positions_tracked_I[product_tracked_cnt][mapping_cnt]+1) + \
                                    ':' + mapping + ' ';
                            rxn_equations_INCA = rxn_equations_INCA[:-1];
                            rxn_equations_INCA += ') ';
                            rxn_equations_INCA += '+ ';
                            products_stoichiometry -= abs(products_stoichiometry_tracked_I[product_tracked_cnt])
                    elif not product_tracked in products_ids_I:
                        print 'unaccounted for product_tracked: ' + product_tracked;
                        if '.balance' in product_tracked and not product_tracked in pseudo_mets:
                            #add in the pseudo-metabolite used to complete the atom mapping
                            rxn_equations_INCA += str(products_stoichiometry_tracked_I[product_tracked_cnt]) + '*' + product_tracked + ' ';
                            rxn_equations_INCA += '(';
                            if products_mapping_I[product_tracked_cnt]:
                                products_mapping = products_mapping_I[product_tracked_cnt];
                                if '[' in products_mapping_I[product_tracked_cnt]:
                                    products_mapping = products_mapping_I[product_tracked_cnt].split('][');
                                    products_mapping = [m.replace('[','') for m in products_mapping];
                                    products_mapping = [m.replace(']','') for m in products_mapping];
                                for mapping_cnt, mapping in enumerate(products_mapping):
                                    rxn_equations_INCA += products_elements_tracked_I[product_tracked_cnt][mapping_cnt] + \
                                        str(products_positions_tracked_I[product_tracked_cnt][mapping_cnt]+1) + \
                                        ':' + mapping + ' ';
                                rxn_equations_INCA = rxn_equations_INCA[:-1];
                                rxn_equations_INCA += ') ';
                                rxn_equations_INCA += '+ ';
                                pseudo_mets.append(product_tracked); # only 1 unique pseudo_met per reaction
                if products_stoichiometry>0.0:
                    rxn_equations_INCA += str(products_stoichiometry) + '*' + product + ' ';
                    rxn_equations_INCA += '+ ';
            else:
                rxn_equations_INCA += str(products_stoichiometry) + '*' + product + ' ';
                rxn_equations_INCA += '+ ';
        rxn_equations_INCA = rxn_equations_INCA[:-2];

        #add in unbalanced metabolites to the products

        return rxn_equations_INCA;
