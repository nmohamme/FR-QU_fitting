Code for interfacing with RM-Tool's QU-Fitting and modelling depolarization spectra.

Models are in the ‘[models_ns](https://github.com/CIRADA-Tools/RM-Tools/tree/master/RMtools_1D/models_ns)’ folder in RM-Tools. It is recommended to import this folder into the directory one is running their notebook in so that you can adjust it as needed. For example, you may want to constrain the range of allowed Rotation Measures for a faster and more reliable fitting. 

QU Fitting outputs three parameters. They are in the output file named `file_path = fn + '_m' + str(model_used) + '_' + str(sampler_used) + '.json'` 

Use the below to open the outputed results as a dictionary

```
with open(file_path, 'r') as json_file:
    data = json.load(json_file)
data['parNames'],data['values']
```
These parameters fit the equation:

$$
\tilde{p}(\lambda^2) = \Sigma_k p_{o,k} e^{2i(\chi_{0,k}+\phi_k\cdot\lambda^2)}
$$

If you use a model other than m1, there will be an additional term for the Burn beam depolarization model: $e^{-2\sigma_k^2\lambda^4}$. Many of the models I include use the Tribble depolarization term instead: $\frac{N^{-0.5}}{\sigma_\phi \lambda^2 2\sqrt2}$.

### Important
I use an edited verion of RM-Tools for the ```/RM-Tools_/RM-Tools/RMtools_1D/do_QUfit_1D_mnest.py``` file. I have included the edited version. You must clone the RM-Tools repository into your working directory ```git clone git@github.com:CIRADA-Tools/RM-Tools.git``` and replace their ```do_QUfit_1D_mnest.py``` with mine.

Then, you have to run ```pip install .``` within ```./QU-Fitting_depol/RM-Tools/``` for it to work.




PyMultinest is the recommended sampler. To use it, one must run the following command in the terminal *before* you create the Jupyter Notebook you will run the QU-fit on:
```
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
```
Details can be found [here](https://johannesbuchner.github.io/PyMultiNest/install.html).
