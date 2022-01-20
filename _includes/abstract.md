# Abstract
In order to investigate the forming of galaxies, astronomers look back in time using (sub)-mm astronomy. DESHIMA (the Deep Spectroscopic High-Redshift Mapper) is a 347 channel superconducting spectrometer with spectral resolution $R=\frac{\nu}{\Delta\nu}=500$ that operates in the range of $220 \mathrm{GHz}$ to $440 \mathrm{GHz}$ and can therefore accurately measure the frequency of spectral lines in order to calculate redshift $z$. 

This report investigates the sensitivity of DESHIMA-like spectrometers by investigating photon noise due to Poisson and bunching effects. It gives a broad overview of photon statistics and explains, through an analogous model, that photon bunching occurs due to an underlying change in the probabilistics, rather than the act of detecting itself. After that I investigate photon and recombination noise for a DESHIMA-like spectrometer with Lorentzian filters and find a closed form equation for Noise Equivalent Power per channel for a constant power spectral density

$$\begin{equation}
\mathrm{NEP}_{\tau}^2=\frac{1}{\tau}\left(h\nu\eta\mathrm{PSD}\Delta\nu+\frac{2}{\pi}\eta^2\mathrm{PSD}^2\Delta\nu+\frac{4\Delta_\mathrm{Al}}{\eta_\mathrm{pb}}\eta\mathrm{PSD}\Delta\nu\right)
\end{equation}$$

where $\eta$ is $\pi/4$ times the peak hight of the Lorentzian, the average transmission over the $\mathrm{FWHM}$ of the Lorentzian. The bunching is a factor of $\pi/2$ smaller than previously approximated.

Finally I propose and describe modifications to the sensitivity model DESHIMA uses. The following features will be improved and added:

## Integrate over the entire power spectrum when calculating photon noise
I use an integral expression for photon noise found in the literature and integrate over it using a Riemann sum to calculate the photon noise per channel. This improves accuracy, in particular in local extrema where the loading of the side bands smooths out the $\mathrm{PSD}$ at the center frequency.

## Use arbritatry filter designs loaded from a file
I design the modifications in such a way that an arbitrary filtershape can be loaded in and the sensitivity can be calculated from it. This is important when comparing filter designs, as it was previously challenging to calculate the noise equivalent power for these arbitrary filter shapes in order to calculate the signal to noise ratio.

## Improve estimations of the quantities that express sensitivity
Finally I will transform the calculated $\mathrm{NEP}$ to quantities like minimal detectable line flux ($\mathrm{MDLF}$) and noise equivalent flux density ($\mathrm{NEFD}$) to show the sensitivity of the system in an astronomical measurement. This was previously done by approximating the $\mathrm{PSD}$ as flat over the filter channel, but I will improve on this by taking the entire range of the filter into account for continuum sources.

I will compare the proposed modifications to the old model, which was compared with measurement results, and use it to validate the changes. Other than the previously mentioned factor of $\pi/2$ for the bunching term and the smoothing out in local extrema, the changes behave similarly to the old model.