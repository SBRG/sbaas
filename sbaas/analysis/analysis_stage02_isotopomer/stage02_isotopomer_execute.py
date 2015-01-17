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
        self.biomass_INCA_v1 = '0.005707*pg160_c (C1:Y C2:1 C3:2) + \
                0.000168*coa_c (C1:A C2:B C3:C C4:D C5:E C6:F C7:G C8:H C9:I C10:J C11:K C12:L C13:M C14:N C15:O C16:P C17:Q C18:R C19:S C20:T C21:U) + \
                0.000003*lipopb_c + \
                0.000307*ni2_c + \
                0.000055*udcpdp_c + \
                0.004957*pe181_c + \
                0.000112*nadp_c + \
                0.140101*utp_c (C1:A C2:B C3:C C4:D C5:E C6:F C7:G C8:H C9:I) + \
                0.008253*mg2_c + \
                0.000024*cobalt2_c + \
                0.234232*asp_DASH_L_c (C1:r C2:s C3:t C4:u) + \
                0.002288*pg181_c (C1:U C2:V C3:W) + \
                0.154187*glycogen_c + \
                0.000098*succoa_c (C1:A C2:B C3:C C4:D C5:E C6:F C7:G C8:H C9:I C10:J C11:K C12:L C13:M C14:N C15:O C16:P C17:Q C18:R C19:S C20:T C21:U C22:4 C23:5 C24:6 C25:7) + \
                48.752916*h2o_c + \
                0.031798*pe160_p + \
                0.000223*gthrd_c + \
                0.000031*malcoa_c (C1:A C2:B C3:C C4:D C5:E C6:F C7:G C8:H C9:I C10:J C11:K C12:L C13:M C14:N C15:O C16:P C17:Q C18:R C19:S C20:T C21:U C22:6 C23:7 C24:8) + \
                0.209684*ser_DASH_L_c (C1:y C2:z C3:1) + \
                0.234232*asn_DASH_L_c (C1:2 C2:3 C3:4 C4:5) + \
                0.000223*amet_c (C1:1 C2:2 C3:3 C4:4 C5:5 C6:6 C7:7 C8:8 C9:9 C10:A C11:a C12:b C13:c C14:d C15:e) + \
                0.595297*gly_c (C1:b C2:c) + \
                0.000605*murein3px4p_p + \
                0.055234*trp_DASH_L_c (C1:i C2:j C3:k C4:l C5:m C6:n C7:o C8:p C9:q C10:r C11:s) + \
                0.03327*ptrc_c (C1:M C2:N C3:O C4:P) + \
                0.006388*fe2_c + \
                0.000223*thf_c + \
                0.000007*mocogdp_c + \
                0.000223*fad_c (C1:a C2:b C3:c C4:d C5:e C6:f C7:g C8:h C9:i C10:j C11:k C12:l C13:m C14:n C15:o C16:p C17:q C18:A C19:B C20:C C21:D C22:E C23:F C24:G C25:H C26:I C27:J) + \
                0.004126*so4_c + \
                0.411184*val_DASH_L_c (C1:d C2:e C3:f C4:g C5:h) + \
                0.18569*k_c + \
                0.005381*murein4p4p_p + \
                0.000223*adocbl_c + \
                0.005448*murein4px4p_p + \
                0.004952*ca2_c + \
                0.000025*2fe2s_c + \
                0.000335*nadph_c + \
                0.000045*nadh_c + \
                0.000674*cu2_c + \
                0.000007*mococdp_c + \
                0.000223*pheme_c + \
                0.004439*pg161_c (C1:A C2:B C3:C) + \
                0.012747*pe181_p + \
                0.282306*ile_DASH_L_c (C1:F C2:G C3:H C4:I C5:J C6:K) + \
                0.000223*chor_c (C1:v C2:w C3:x C4:y C5:z C6:1 C7:2 C8:3 C9:4 C10:5) + \
                0.000223*q8h2_c + \
                0.008151*colipa_e + \
                0.333448*lys_DASH_L_c (C1:9 C2:A C3:B C4:C C5:D C6:E) + \
                0.000223*enter_c + \
                0.000223*mlthf_c (C1:L) + \
                0.000223*thmpp_c + \
                0.28742*arg_DASH_L_c (C1:O C2:P C3:Q C4:R C5:S C6:T) + \
                0.000002*btn_c + \
                0.000223*hemeO_c + \
                0.499149*ala_DASH_L_c (C1:m C2:n C3:o) + \
                0.246506*thr_DASH_L_c (C1:e C2:f C3:g C4:h) + \
                0.088988*cys_DASH_L_c (C1:3 C2:4 C3:5) + \
                0.001787*nad_c + \
                0.180021*phe_DASH_L_c (C1:i C2:j C3:k C4:l C5:m C6:n C7:o C8:p C9:q) + \
                0.025612*dctp_c (C1:A C2:B C3:C C4:D C5:E C6:F C7:G C8:H C9:I) + \
                0.149336*met_DASH_L_c (C1:h C2:i C3:j C4:k C5:l) + \
                0.012366*pe160_c + \
                0.209121*gtp_c (C1:A C2:B C3:C C4:D C5:E C6:F C7:G C8:H C9:I C10:J) + \
                0.437778*leu_DASH_L_c (C1:X C2:Y C3:Z C4:1 C5:2 C6:3) + \
                0.007428*fe3_c + \
                0.092056*his_DASH_L_c (C1:8 C2:9 C3:a C4:b C5:c C6:d) + \
                0.009618*pe161_c + \
                0.000223*10fthf_c (C1:6) + \
                0.024805*datp_c (C1:A C2:B C3:C C4:D C5:E C6:F C7:G C8:H C9:I C10:J) + \
                0.000223*5mthf_c (C1:K) + \
                0.000673*murein4px4px4p_p + \
                0.024805*dttp_c (C1:A C2:B C3:C C4:D C5:E C6:F C7:G C8:H C9:I C10:J) + \
                0.000223*ribflv_c (C1:a C2:b C3:c C4:d C5:e C6:f C7:g C8:h C9:i C10:j C11:k C12:l C13:m C14:n C15:o C16:p C17:q) + \
                0.000223*pydx5p_c + \
                0.000324*zn2_c + \
                0.004952*cl_c + \
                0.000223*sheme_c + \
                0.001345*murein3p3p_p + \
                0.004892*pg160_p (C1:Q C2:R C3:S) + \
                0.129799*ctp_c (C1:A C2:B C3:C C4:D C5:E C6:F C7:G C8:H C9:I) + \
                0.255712*glu_DASH_L_c (C1:D C2:E C3:F C4:G C5:H) + \
                0.214798*pro_DASH_L_c (C1:6 C2:7 C3:8 C4:9 C5:a) + \
                0.025612*dgtp_c (C1:A C2:B C3:C C4:D C5:E C6:F C7:G C8:H C9:I C10:J) + \
                0.000007*mobd_c + \
                0.255712*gln_DASH_L_c (C1:T C2:U C3:V C4:W C5:X) + \
                0.001961*pg181_p (C1:L C2:M C3:N) + \
                0.000658*mn2_c + \
                0.000223*2dmmql8_c + \
                0.024732*pe161_p + \
                0.000248*4fe4s_c + \
                0.00118*clpn181_p + \
                0.012379*nh4_c + \
                0.000223*mql8_c + \
                0.003805*pg161_p (C1:7 C2:8 C3:9) + \
                0.000279*accoa_c (C1:A C2:B C3:C C4:D C5:E C6:F C7:G C8:H C9:I C10:J C11:K C12:L C13:M C14:N C15:O C16:P C17:Q C18:R C19:S C20:T C21:U C22:I C23:J) + \
                54.119975*atp_c (C1:A C2:B C3:C C4:D C5:E C6:F C7:G C8:H C9:I C10:J) + \
                0.133993*tyr_DASH_L_c (C1:p C2:q C3:r C4:s C5:t C6:u C7:v C8:w C9:x) + \
                0.006744*spmd_c (C1:a C2:b C3:c C4:d C5:e C6:f C7:g) + \
                0.002944*clpn160_p + \
                0.000116*bmocogdp_c + \
                0.00229*clpn161_p -> 0.749831*ppi_c + \
                53.95*adp_c + \
                53.945874*pi_c + \
                53.95*h_c';
        self.biomass_INCA = '0.005707*pg160_c + \
                0.000168*coa_c + \
                0.000003*lipopb_c + \
                0.000307*ni2_c + \
                0.000055*udcpdp_c + \
                0.004957*pe181_c + \
                0.000112*nadp_c + \
                0.140101*utp_c  + \
                0.008253*mg2_c + \
                0.000024*cobalt2_c + \
                0.234232*asp_DASH_L_c  + \
                0.002288*pg181_c  + \
                0.154187*glycogen_c + \
                0.000098*succoa_c + \
                48.752916*h2o_c + \
                0.031798*pe160_p + \
                0.000223*gthrd_c + \
                0.000031*malcoa_c  + \
                0.209684*ser_DASH_L_c  + \
                0.234232*asn_DASH_L_c + \
                0.000223*amet_c + \
                0.595297*gly_c + \
                0.000605*murein3px4p_p + \
                0.055234*trp_DASH_L_c + \
                0.03327*ptrc_c + \
                0.006388*fe2_c + \
                0.000223*thf_c + \
                0.000007*mocogdp_c + \
                0.000223*fad_c + \
                0.004126*so4_c + \
                0.411184*val_DASH_L_c + \
                0.18569*k_c + \
                0.005381*murein4p4p_p + \
                0.000223*adocbl_c + \
                0.005448*murein4px4p_p + \
                0.004952*ca2_c + \
                0.000025*2fe2s_c + \
                0.000335*nadph_c + \
                0.000045*nadh_c + \
                0.000674*cu2_c + \
                0.000007*mococdp_c + \
                0.000223*pheme_c + \
                0.004439*pg161_c + \
                0.012747*pe181_p + \
                0.282306*ile_DASH_L_c + \
                0.000223*chor_c + \
                0.000223*q8h2_c + \
                0.008151*colipa_e + \
                0.333448*lys_DASH_L_c + \
                0.000223*enter_c + \
                0.000223*mlthf_c + \
                0.000223*thmpp_c + \
                0.28742*arg_DASH_L_c + \
                0.000002*btn_c + \
                0.000223*hemeO_c + \
                0.499149*ala_DASH_L_c + \
                0.246506*thr_DASH_L_c + \
                0.088988*cys_DASH_L_c + \
                0.001787*nad_c + \
                0.180021*phe_DASH_L_c + \
                0.025612*dctp_c + \
                0.149336*met_DASH_L_c + \
                0.012366*pe160_c + \
                0.209121*gtp_c + \
                0.437778*leu_DASH_L_c + \
                0.007428*fe3_c + \
                0.092056*his_DASH_L_c + \
                0.009618*pe161_c + \
                0.000223*10fthf_c + \
                0.024805*datp_c + \
                0.000223*5mthf_c + \
                0.000673*murein4px4px4p_p + \
                0.024805*dttp_c + \
                0.000223*ribflv_c + \
                0.000223*pydx5p_c + \
                0.000324*zn2_c + \
                0.004952*cl_c + \
                0.000223*sheme_c + \
                0.001345*murein3p3p_p + \
                0.004892*pg160_p + \
                0.129799*ctp_c + \
                0.255712*glu_DASH_L_c + \
                0.214798*pro_DASH_L_c + \
                0.025612*dgtp_c + \
                0.000007*mobd_c + \
                0.255712*gln_DASH_L_c + \
                0.001961*pg181_p + \
                0.000658*mn2_c + \
                0.000223*2dmmql8_c + \
                0.024732*pe161_p + \
                0.000248*4fe4s_c + \
                0.00118*clpn181_p + \
                0.012379*nh4_c + \
                0.000223*mql8_c + \
                0.003805*pg161_p + \
                0.000279*accoa_c + \
                54.119975*atp_c + \
                0.133993*tyr_DASH_L_c + \
                0.006744*spmd_c + \
                0.002944*clpn160_p + \
                0.000116*bmocogdp_c + \
                0.00229*clpn161_p -> 0.749831*ppi_c + \
                53.95*adp_c + \
                53.945874*pi_c + \
                53.95*h_c';
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
        except SQLAlchemyError as e:
            print(e);
    def reset_datastage02(self,experiment_id_I = None,simulation_id_I = None):
        try:
            if experiment_id_I:
                reset = self.session.query(data_stage02_isotopomer_tracers).filter(data_stage02_isotopomer_tracers.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_isotopomer_measuredFluxes).filter(data_stage02_isotopomer_measuredFluxes.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_isotopomer_measuredPools).filter(data_stage02_isotopomer_measuredPools.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_isotopomer_measuredFragments).filter(data_stage02_isotopomer_measuredFragments.experiment_id.like(experiment_id_I)).delete(synchronize_session=False);
            elif simulation_id_I:
                reset = self.session.query(data_stage02_isotopomer_simulation).filter(data_stage02_isotopomer_simulation.experiment_id.like(simulation_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_isotopomer_fittedFluxes).filter(data_stage02_isotopomer_fittedFluxes.experiment_id.like(simulation_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_isotopomer_fittedFragments).filter(data_stage02_isotopomer_fittedFluxes.experiment_id.like(simulation_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_isotopomer_fittedData).filter(data_stage02_isotopomer_fittedData.experiment_id.like(simulation_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_isotopomer_fittedMeasuredFluxes).filter(data_stage02_isotopomer_fittedMeasuredFluxes.experiment_id.like(simulation_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_isotopomer_fittedMeasuredFragments).filter(data_stage02_isotopomer_fittedMeasuredFragments.experiment_id.like(simulation_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_isotopomer_fittedMeasuredFluxResiduals).filter(data_stage02_isotopomer_fittedMeasuredFluxResiduals.experiment_id.like(simulation_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_isotopomer_fittedMeasuredFragmentResiduals).filter(data_stage02_isotopomer_fittedMeasuredFragmentResiduals.experiment_id.like(simulation_id_I)).delete(synchronize_session=False);
                reset = self.session.query(data_stage02_isotopomer_simulationParameters).filter(data_stage02_isotopomer_simulationParameters.experiment_id.like(simulation_id_I)).delete(synchronize_session=False);
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
        except SQLAlchemyError as e:
            print(e);
    #analysis
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
                with open(settings.workspace_data + '\\cobra_model_tmp.xml','wb') as file:
                    file.write(cobra_model_sbml['model_file']);
                    file.close()
                cobra_model = None;
                cobra_model = create_cobra_model_from_sbml_file(settings.workspace_data + '\\cobra_model_tmp.xml', print_time=True);
            elif cobra_model_sbml['file_type'] == 'json':
                with open(settings.workspace_data + '\\cobra_model_tmp.json','wb') as file:
                    file.write(cobra_model_sbml['model_file']);
                    file.close()
                cobra_model = None;
                cobra_model = load_json_model(settings.workspace_data + '\\cobra_model_tmp.json');
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
                with open(settings.workspace_data + '\\cobra_model_tmp.xml','wb') as file:
                    file.write(cobra_model_sbml['model_file']);
                    file.close()
                cobra_model = None;
                cobra_model = create_cobra_model_from_sbml_file(settings.workspace_data + '\\cobra_model_tmp.xml', print_time=True);
            elif cobra_model_sbml['file_type'] == 'json':
                with open(settings.workspace_data + '\\cobra_model_tmp.json','wb') as file:
                    file.write(cobra_model_sbml['model_file']);
                    file.close()
                cobra_model = None;
                cobra_model = load_json_model(settings.workspace_data + '\\cobra_model_tmp.json');
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
                with open(settings.workspace_data + '\\cobra_model_tmp.xml','wb') as file:
                    file.write(cobra_model);
                # upload the model to the database
                qio02.import_dataStage02Model_sbml(model_id_I, date_I, settings.workspace_data + '\\cobra_model_tmp.xml');
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
                    filename = settings.workspace_data + '\\cobra_model_tmp.xml'
                    with open(filename,'wb') as file:
                        file.write(cobra_model);
                        file.close()
                elif '.json' in model_file_name_I:
                    filename = settings.workspace_data + '\\cobra_model_tmp.json';
                    with open(filename,'wb') as file:
                        file.write(cobra_model);
                        file.close()
                else: print 'file type not supported'
                # upload the model to the database
                qio02.import_dataStage02Model_sbml(model_id_I, date_I, filename);
        else:
            print 'need to specify either an existing model_id or model_file_name!'
        return
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
    def execute_makeIsotopomerSimulation_INCA(self,experiment_id_I, model_id_I = [], mapping_id_I = [], sample_name_abbreviations_I = [], time_points_I = [], met_ids_I = [], scan_types_I = [], stationary_I = True, parallel_I = False, ko_list_I=[],flux_dict_I={},description_I=None):
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
        #    sample_abbreviations = [];
        #    sample_abbreviations = self.stage02_isotopomer_query.get_sampleNameAbbreviations_experimentID_dataStage02IsotopomerSimulation(experiment_id_I);
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
                    ## get the tracer_ids:
                    #tracer_ids = self.stage02_isotopomer_query.get_tracerID__dataStage02IsotopomerSimulation(tracer_id_I,
                    #for tracer_id in tracer_ids:
                    #if parallel_I:
                    #else:
                    print 'Collecting and exporting tracer information for sample name abbreviation ' + sna;
                    ## get substrate labeling (i.e. tracer) information
                    tracers = [];
                    tracers = self.stage02_isotopomer_query.get_rows_experimentID_dataStage02IsotopomerTracers(experiment_id_I);

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
                            filename_mat = settings.workspace_data + '\\_output\\' + 'isotopomer_' + re.sub('[.\/]','',experiment_id_I) + '_' + re.sub(' ','',sna) + '_' + re.sub(' ','',str(tp)) + '.m';
                            filename_csv = settings.workspace_data + '\\_output\\' + 'isotopomer_' + re.sub('[.\/]','',experiment_id_I) + '_' + re.sub(' ','',sna) + '_' + re.sub(' ','',str(tp)) + '.csv';
                            filename_json = settings.workspace_data + '\\_output\\' + 'isotopomer_' + re.sub('[.\/]','',experiment_id_I) + '_' + re.sub(' ','',sna) + '_' + re.sub(' ','',str(tp)) + '.json';
                            #mat_script,rxn_ids_INCA = self.write_isotopomerExperiment_INCA(modelReaction_data,modelMetabolite_data,measuredFluxes_data,experimentalMS_data,tracers);
                            mat_script = self.write_isotopomerExperiment_INCA(modelReaction_data,modelMetabolite_data,measuredFluxes_data,experimentalMS_data,tracers);
                            with open(filename_mat,'w') as f:
                                f.write(mat_script);
                            #exportData = base_exportData(rxn_ids_INCA);
                            #exportData.write_dict2csv(filename_csv);
                    else:
                        # get the MS data
                        experimentalMS_data = self.stage02_isotopomer_query.get_row_experimentIDAndSampleNameAbbreviation_dataStage02IsotopomerMeasuredFragments(experiment_id_I,sna);
                        experiment_name = 'Isotopomer_' + re.sub('[.\/]','',experiment_id_I) + '_' + re.sub(' ','',sna);
                        filename_mat = settings.workspace_data + '\\_output\\' + 'isotopomer_' + re.sub('[.\/]','',experiment_id_I) + '_' + re.sub(' ','',sna) + '.m';
                        filename_csv = settings.workspace_data + '\\_output\\' + 'isotopomer_' + re.sub('[.\/]','',experiment_id_I) + '_' + re.sub(' ','',sna) + '.csv';
                        filename_json = settings.workspace_data + '\\_output\\' + 'isotopomer_' + re.sub('[.\/]','',experiment_id_I) + '_' + re.sub(' ','',sna) + '.json';
                        mat_script = self.write_isotopomerExperiment_INCA(modelReaction_data,modelMetabolite_data,measuredFluxes_data,experimentalMS_data,tracers);
                        with open(filename_mat,'w') as f:
                            f.write(mat_script);
                        #exportData = base_exportData(rxn_ids_INCA);
                        #exportData.write_dict2csv(filename_csv);
    #internal functions
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
    def write_isotopomerExperiment_INCA(self, modelReaction_data_I,modelMetabolite_data_I,measuredFluxes_data_I,experimentalMS_data_I,tracer_I):
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
            if not(rxn['upper_bound']==0.0 and rxn['lower_bound']==0.0):
                rxn_ids_INCA[rxn['rxn_id']] = ('R'+str(cnt+1));
                cnt+=1;
                if rxn['rxn_id'] == 'Ec_biomass_iJO1366_WT_53p95M':
                    #tmp_script = tmp_script + "'" + self.biomass_INCA + "';...\n"
                    tmp_script = tmp_script + "'" + self.biomass_INCA_iJS2012 + "';...\n"
                else:
                    tmp_script = tmp_script + "'" + rxn['rxn_equation'] + "';...\n"
                #tmp_script = tmp_script + "'" + rxn['rxn_equation'] + "';...\n"
            else:
                print 'rxn_id ' + rxn['rxn_id'] + ' will be excluded from INCA' 
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
        '''% Take care of symmetrical metabolites
        m.mets{'Suc'}.sym = list('rotate180',map('1:4 2:3 3:2 4:1'));
        m.mets{'Fum'}.sym = list('rotate180',map('1:4 2:3 3:2 4:1'));'''
        mat_script = mat_script + tmp_script;

        # Add in the metabolite states (balance), value, and lb/ub)

        # Add in initial fluxes (values lb/ub) and define the reaction ids
        tmp_script = ''
        tmp_script = tmp_script + 'm.rates.flx.lb = [...\n';
        for rxn_cnt,rxn in enumerate(modelReaction_data_I):
            if not(rxn['upper_bound']==0.0 and rxn['lower_bound']==0.0):
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
        for rxn_cnt,rxn in enumerate(modelReaction_data_I):
            if not(rxn['upper_bound']==0.0 and rxn['lower_bound']==0.0):
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
        for rxn_cnt,rxn in enumerate(modelReaction_data_I):
            if not(rxn['upper_bound']==0.0 and rxn['lower_bound']==0.0):
                tmp_script = tmp_script + str(rxn['flux_val']) + ',...\n'
        tmp_script = tmp_script + '];\n';
        #tmp_script = tmp_script + 'm.rates.flx.fix = [...\n';
        #for rxn_cnt,rxn in enumerate(modelReaction_data_I):
        #    if rxn['flux_val']==0.0 and rxn['upper_bound']==0.0 and rxn['lower_bound']==0.0:
        #        tmp_script = tmp_script + '1' + ',...\n'
        #    else:
        #        tmp_script = tmp_script + '0' + ',...\n'
        #tmp_script = tmp_script + '];\n';
        tmp_script = tmp_script + 'm.rates.id = {...\n';
        for rxn_cnt,rxn in enumerate(modelReaction_data_I):
            #TODO check on how the reactions are named
            if not(rxn['upper_bound']==0.0 and rxn['lower_bound']==0.0):
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
        
        ##2. Define the experiment

        # write out the measured fragment information
        # (actual MS measurements will be written to the script later)
        #snas_all = [x['sample_name_abbreviation'] for x in experimentalMS_data_I];
        #snas = list(set(snas_all));
        #snas.sort();
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

        ## Simulate measurements
        #mat_script = mat_script + 's = simulate(m);\n';
        #mat_script = mat_script + '% m = sim2mod(m,s);\n';
        ## Simulate fluxes

        ## Format rxn_ids_INCA
        #rxn_ids_INCA_O = [];
        #for k,v in rxn_ids_INCA.iteritems():
        #    rxn_ids_INCA_O.append({'rxn_id_INCA':v,'rxn_id':k})
        #return mat_script,rxn_ids_INCA_O;

        return mat_script;
    def make_missingReactionMappings_v1(self,experiment_id_I,mapping_id_new_I=None,model_id_I=[],mapping_id_I=[]):
        '''find reactions that contain a mapped metabolite that is present in the model, but not present in table atomMappingReactions;
        and create a new set of reaction mappings that need to be QC/QA'd'''

        #data structures:
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
            if mapping_id_I:
                mapping_ids=mapping_id_I;
            else:
                mapping_ids=[];
                mapping_ids=self.stage02_isotopomer_query.get_mappingID_experimentIDAndModelID_dataStage02IsotopomerSimulation(experiment_id_I,model_id);
            for mapping_id in mapping_ids:
                missing_reactions_O = [];
                missing_metabolites_O = [];
                for reaction in reactions:
                    data_tmp={'mapping_id':mapping_id_new_I,
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
                        tracked_reactant = self.stage02_isotopomer_query.get_rows_mappingIDAndMetID_dataStage02IsotopomerAtomMappingMetabolites(mapping_id,reactant);
                        if tracked_reactant:
                            tracked_reactants.append(tracked_reactant);
                    tracked_products = [];
                    for product in reaction['products_ids']:
                        tracked_product = {};
                        tracked_product = self.stage02_isotopomer_query.get_rows_mappingIDAndMetID_dataStage02IsotopomerAtomMappingMetabolites(mapping_id,product);
                        if tracked_product:
                            tracked_products.append(tracked_product);
                    if tracked_reactants or tracked_products:
                        #check if the reaction is missing or is missing a tracked metabolite
                        tracked_reaction = {};
                        tracked_reaction = self.stage02_isotopomer_query.get_row_mappingIDAndRxnID_dataStage02IsotopomerAtomMappingReactions(mapping_id,reaction['rxn_id']);
                        if tracked_reaction:
                            missing_reactants = [];
                            #copy existing data
                            data_tmp['reactants_ids_tracked'].extend(tracked_reaction['reactants_ids_tracked']);
                            data_tmp['reactants_stoichiometry_tracked'].extend(tracked_reaction['reactants_stoichiometry_tracked']);
                            data_tmp['reactants_mapping'].extend(tracked_reaction['reactants_mapping']);
                            data_tmp['reactants_elements_tracked'].extend(tracked_reaction['reactants_elements_tracked']);
                            data_tmp['reactants_positions_tracked'].extend(tracked_reaction['reactants_positions_tracked']);
                            data_tmp['rxn_description']=tracked_reaction['rxn_description'];
                            for tracked_reactant in tracked_reactants:
                                if tracked_reactant['met_id'] in tracked_reaction['reactants_ids_tracked']:
                                    continue;
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
                            #copy existing data
                            data_tmp['products_ids_tracked'].extend(tracked_reaction['products_ids_tracked']);
                            data_tmp['products_stoichiometry_tracked'].extend(tracked_reaction['products_stoichiometry_tracked']);
                            data_tmp['products_mapping'].extend(tracked_reaction['products_mapping']);
                            data_tmp['products_elements_tracked'].extend(tracked_reaction['products_elements_tracked']);
                            data_tmp['products_positions_tracked'].extend(tracked_reaction['products_positions_tracked']);
                            data_tmp['rxn_description']=tracked_reaction['rxn_description'];
                            for tracked_product in tracked_products:
                                if tracked_product['met_id'] in tracked_reaction['products_ids_tracked']:
                                    continue;
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
                #self.print_missingReactionMappings(missing_reactions_O,missing_metabolites_O);
        #add data to the database:
        for d in data_O:
            row = None;
            row = data_stage02_isotopomer_atomMappingReactions(d['mapping_id'],
                                d['rxn_id'],
                                d['rxn_description'],
                                d['reactants_stoichiometry_tracked'],
                                d['products_stoichiometry_tracked'],
                                d['reactants_ids_tracked'],
                                d['products_ids_tracked'],
                                d['reactants_elements_tracked'],
                                d['products_elements_tracked'],
                                d['reactants_positions_tracked'],
                                d['products_positions_tracked'],
                                d['reactants_mapping'],
                                d['products_mapping'],
                                d['rxn_equation'],
                                d['used_'],
                                d['comment_']);
            self.session.add(row);
        self.session.commit();
    def make_missingMetaboliteMappings_v1(self,experiment_id_I,model_id_I=[],mapping_id_rxns_I=[],mapping_id_mets_I=[]):
        '''Make atom mapping metabolites from atom mapping reactions, QC atom mapping reactions;
        and create a new set of metabolite mappings that correspond to the current reaction mappings that need to be QC/QA'd'''
        
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
                        data_O.append(d1);
                met_ids = [x['met_id'] for x in data_O];
                met_ids_unique = list(set(met_ids));
                data_mets_cnt = {};
                for met in met_ids_unique:
                    data_mets_cnt[met] = 0;
                for d in data_O:
                    data_mets_cnt[d['met_id']] += 1;
                # add data to the database
                self.stage02_isotopomer_query.add_data_dataStage02IsotopomerAtomMappingMetabolites(data_O);
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
                with open(settings.workspace_data + '\\cobra_model_tmp.xml','wb') as file:
                    file.write(cobra_model_sbml['model_file']);
                    file.close()
                cobra_model = None;
                cobra_model = create_cobra_model_from_sbml_file(settings.workspace_data + '\\cobra_model_tmp.xml', print_time=True);
            elif cobra_model_sbml['file_type'] == 'json':
                with open(settings.workspace_data + '\\cobra_model_tmp.json','wb') as file:
                    file.write(cobra_model_sbml['model_file']);
                    file.close()
                cobra_model = None;
                cobra_model = load_json_model(settings.workspace_data + '\\cobra_model_tmp.json');
            else:
                print 'file_type not supported'
            self.models[model_id]=cobra_model;
    #TODO:
    def make_isotopomerSimulation_Inca(self):
        '''Generate parameters for isotopomer simulation data for INCA1.1'''
        return
    def make_isotopomerParameterEstimation_Inca(self):
        '''Generate parameters for isotopomer parameter estimations (i.e. free fluxes) for INCA1.1'''
        return

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
                save_json_model(cobra_model,settings.workspace_data+'\\cobra_model_tmp.json')
                # add the model information to the database
                dataStage02IsotopomerModelRxns_data = [];
                dataStage02IsotopomerModelMets_data = [];
                dataStage02IsotopomerModels_data,\
                    dataStage02IsotopomerModelRxns_data,\
                    dataStage02IsotopomerModelMets_data = qio02._parse_model_json(model_id_O, date_I, settings.workspace_data+'\\cobra_model_tmp.json')
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
                save_json_model(cobra_model,settings.workspace_data+'\\cobra_model_tmp.json')
                # upload the model to the database
                # add the model information to the database
                dataStage02IsotopomerModelRxns_data = [];
                dataStage02IsotopomerModelMets_data = [];
                dataStage02IsotopomerModels_data,\
                    dataStage02IsotopomerModelRxns_data,\
                    dataStage02IsotopomerModelMets_data = qio02._parse_model_json(model_id_I, date_I, settings.workspace_data+'\\cobra_model_tmp.json')
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