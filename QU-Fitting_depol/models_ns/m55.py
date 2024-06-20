# =============================================================================#
#                          MODEL DEFINITION FILE                              #
# =============================================================================#
import bilby
import numpy as np
from bilby.core.prior import Constraint, PriorDict


# -----------------------------------------------------------------------------#
# Function defining the model.                                                #
#                                                                             #
#  pDict       = Dictionary of parameters, created by parsing inParms, below. #
#  lamSqArr_m2 = Array of lambda-squared values                               #
#  quArr       = Complex array containing the Re and Im spectra.              #
# -----------------------------------------------------------------------------#


def model(pDict, lamSqArr_m2, ref_p=1, ref_freq=22.8e9):
    """Two separate Faraday components, with Tribble depolarization and anchored p0"""
    # Calculate the complex fractional q and u spectra
    ref_lam_m = (3e8/ref_freq)
    freqArr_Hz = 3e8/np.sqrt(lamSqArr_m2)

    pArr1 = ref_p*np.ones_like(lamSqArr_m2)
    pArr2 = ref_p*np.ones_like(lamSqArr_m2)
    
    quArr1 = pArr1 * np.exp(
        2j * (np.radians(pDict["psi01_deg"]) + pDict["RM1_radm2"] * lamSqArr_m2)
    )
    quArr2 = pArr2 * np.exp(
        2j * (np.radians(pDict["psi02_deg"]) + pDict["RM2_radm2"] * lamSqArr_m2)
    )
    quArr = (quArr1 + quArr2) *
        (pDict["N"]**(-0.5)/(pDict["sigmaRM_radm2"]*lamSqArr_m2*np.sqrt(2)))

    return quArr


# -----------------------------------------------------------------------------#
# Priors for the above model.                                                 #
# See https://lscsoft.docs.ligo.org/bilby/prior.html for details.             #
#                                                                             #
# -----------------------------------------------------------------------------#
def converter(parameters):
    """
    Function to convert between sampled parameters and constraint parameter.

    Parameters
    ----------
    parameters: dict
        Dictionary containing sampled parameter values, 'RM1_radm2', 'RM1_radm2'.

    Returns
    -------
    dict: Dictionary with constraint parameter 'delta_RM1_RM2_radm2' added.
    """
    converted_parameters = parameters.copy()
    converted_parameters["delta_RM1_RM2_radm2"] = (
        parameters["RM1_radm2"] - parameters["RM2_radm2"]
    )
    return converted_parameters


priors = PriorDict(conversion_function=converter)

priors["N"] = bilby.prior.Uniform(
    minimum=0,
    maximum=5,
    name="N",
    latex_label=r"N",
)

priors["psi01_deg"] = bilby.prior.Uniform(
    minimum=0,
    maximum=180.0,
    name="psi01_deg",
    latex_label=r"$\psi_{0,1}$ (deg)",
    boundary="periodic",
)
priors["psi02_deg"] = bilby.prior.Uniform(
    minimum=0,
    maximum=180.0,
    name="psi02_deg",
    latex_label=r"$\psi_{0,2}$ (deg)",
    boundary="periodic",
)

priors["RM1_radm2"] = bilby.prior.Uniform(
    minimum=-100.0,
    maximum=100.0,
    name="RM1_radm2",
    latex_label=r"$\phi_1$ (rad m$^{-2}$)",
)
priors["RM2_radm2"] = bilby.prior.Uniform(
    minimum=-100.0,
    maximum=100.0,
    name="RM2_radm2",
    latex_label=r"$\phi_2$ (rad m$^{-2}$)",
)
priors["delta_RM1_RM2_radm2"] = Constraint(
    minimum=0,
    maximum=200.0,
    name="delta_RM1_RM2_radm2",
    latex_label=r"$\Delta\phi_{1,2}$ (rad m$^{-2}$)",
)

priors["sigmaRM_radm2"] = bilby.prior.Uniform(
    minimum=0,
    maximum=100.0,
    name="sigmaRM_radm2",
    latex_label=r"$\sigma_{RM}$ (rad m$^{-2}$)",
)
priors["sum_p1_p2"] = Constraint(
    minimum=0.001,
    maximum=1,
    name="sum_p1_p2",
    latex_label=r"$p_1+p_2$",
)
