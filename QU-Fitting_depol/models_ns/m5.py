# =============================================================================#
#                          MODEL DEFINITION FILE                              #
# =============================================================================#
import bilby
import numpy as np


# -----------------------------------------------------------------------------#
# Function defining the model.                                                #
#                                                                             #
#  pDict       = Dictionary of parameters, created by parsing inParms, below. #
#  lamSqArr_m2 = Array of lambda-squared values                               #
#  quArr       = Complex array containing the Re and Im spectra.              #
# -----------------------------------------------------------------------------#


def model(pDict, lamSqArr_m2, ref_p=1, ref_freq=22.8e9):
    """Single Faraday component with Tribble depolarisation and anchored p0"""
    # Calculate the complex fractional q and u spectra
    ref_lam_m = (3e8/ref_freq)
    freqArr_Hz = 3e8/np.sqrt(lamSqArr_m2)

    pArr = ref_p*np.ones_like(lamSqArr_m2)
    
    quArr = (
        pArr
        * np.exp(2j * (np.radians(pDict["psi0_deg"]) + pDict["RM_radm2"] * lamSqArr_m2))
        *(pDict["N"]**(-0.5)/(pDict["sigmaRM_radm2"]*lamSqArr_m2*np.sqrt(2)))
    )

    return quArr


# -----------------------------------------------------------------------------#
# Priors for the above model.                                                 #
# See https://lscsoft.docs.ligo.org/bilby/prior.html for details.             #
#                                                                             #
# -----------------------------------------------------------------------------#
priors = {
    "psi0_deg": bilby.prior.Uniform(
        minimum=0,
        maximum=180.0,
        name="psi0_deg",
        latex_label=r"$\psi_0$ (deg)",
        boundary="periodic",
    ),
    "RM_radm2": bilby.prior.Uniform(
        minimum=-100.0,
        maximum=100.0,
        name="RM_radm2",
        latex_label=r"RM (rad m$^{-2}$)",
    ),
    "sigmaRM_radm2": bilby.prior.Uniform(
        minimum=0.0,
        maximum=20.0,
        name="sigmaRM_radm2",
        latex_label=r"$\sigma_{RM}$ (rad m$^{-2}$)",
    ),
    "N": bilby.prior.Uniform(
        minimum=0,
        maximum=5,
        name="N",
        latex_label=r"N",
    ),
}
