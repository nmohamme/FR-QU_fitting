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
def model(pDict, lamSqArr_m2):
    """Straight Burn depolarisation"""

    # Calculate the complex fractional q and u spectra
    pArr = pDict["fracPol"] * np.ones_like(lamSqArr_m2)
    quArr = (
        pArr
        * np.exp(-2.0 * pDict["sigmaRM_radm2"] ** 2.0 * lamSqArr_m2**2.0)
    )

    return quArr


# -----------------------------------------------------------------------------#
# Priors for the above model.                                                 #
# See https://lscsoft.docs.ligo.org/bilby/prior.html for details.             #
#                                                                             #
# -----------------------------------------------------------------------------#
priors = {
    "fracPol": bilby.prior.Uniform(
        minimum=0.001, maximum=1.0, name="fracPol", latex_label=r"$p$"
    ),
    "sigmaRM_radm2": bilby.prior.Uniform(
        minimum=0.0,
        maximum=20.0,
        name="sigmaRM_radm2",
        latex_label=r"$\sigma_{RM}$ (rad m$^{-2}$)",
    ),
}
