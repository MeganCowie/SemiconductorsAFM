# Vary the dopant concentration of n-type silicon
import Physics_Semiconductors
import Physics_BandDiagram
import Organization_IntermValues
import Organization_BuildArrays
import numpy as np
import pandas as pd

################################################################################
# Haughton Si values

toggle_type = False
slider_Vg = 8.5
slider_zins = 6
slider_Eg = 0.5
slider_epsilonsem = 11.7
slider_WFmet = 4.6
slider_EAsem = 4.05
slider_emass = 1
slider_hmass = 1
slider_donor = 33.2
slider_acceptor = 0
slider_T = 300
slider_alpha = 0.25
stylen = {'color': '#57c5f7', 'fontSize': 18, 'text-align': 'right'}
stylep = {'color': '#7f7f7f', 'fontSize': 18, 'text-align': 'right'}
disabledn = False
disabledp = True

slider_biassteps = 0
slider_zinssteps = 0
slider_timesteps = 128
slider_amplitude = 6
slider_resfreq = 300000
slider_lag = 0
slider_hop = 0
toggle_RTN = True
toggle_sampletype = False
slider_springconst = 42
slider_Qfactor = 18000
slider_tipradius = 12.6

################################################################################
# Input values and arrays
Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T,sampletype,biassteps,zinssteps,Vg_array,zins_array=Organization_IntermValues.Surface_inputvalues(slider_Vg,slider_zins,slider_alpha,slider_Eg,slider_epsilonsem,slider_WFmet,slider_EAsem,slider_donor,slider_acceptor,slider_emass,slider_hmass,slider_T,slider_biassteps,slider_zinssteps)
amplitude,frequency,lag,timesteps,time_AFMarray,zins_AFMarray,zinslag_AFMarray=Organization_IntermValues.AFM1_inputvalues(slider_amplitude,slider_resfreq,slider_lag,slider_timesteps,  zins)

# Calculations and results
NC,NV,Ec,Ev,Ei,Ef,no,po,ni,nb,pb,CPD,LD,Vs,Es,Qs,F,regime, zsem,Vsem,Esem,Qsem, P = Organization_IntermValues.Surface_calculations(Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T)
Vs_AFMarray, F_AFMarray, P_AFMarray = Organization_BuildArrays.AFM_timearrays(zinslag_AFMarray,Vg,zins,Na,Nd,epsilon_sem,T,CPD,LD,nb,pb,ni)
zsem_AFMarray,Vsem_AFMarray,zgap_AFMarray,Vgap_AFMarray,zvac_AFMarray,Vvac_AFMarray,zmet_AFMarray,Vmet_AFMarray = Organization_BuildArrays.AFM_banddiagrams(zins_AFMarray,Vg,T,Nd,Na,WFmet,EAsem,epsilon_sem, ni,nb,pb,Vs,Ec,Ev,Ef,CPD)

# Account for alpha
Vg = slider_Vg*Physics_Semiconductors.e #J
Vg_array = np.linspace(-10,10,biassteps)*Physics_Semiconductors.e #J


# Stack arrays to show two periods
zsem_AFMarray = np.vstack((zsem_AFMarray,zsem_AFMarray[1:]))
Vsem_AFMarray = np.vstack((Vsem_AFMarray,Vsem_AFMarray[1:]))
zgap_AFMarray = np.vstack((zgap_AFMarray,zgap_AFMarray[1:]))
Vgap_AFMarray = np.vstack((Vgap_AFMarray,Vgap_AFMarray[1:]))
zvac_AFMarray = np.vstack((zvac_AFMarray,zvac_AFMarray[1:]))
Vvac_AFMarray = np.vstack((Vvac_AFMarray,Vvac_AFMarray[1:]))
zmet_AFMarray = np.vstack((zmet_AFMarray,zmet_AFMarray[1:]))
Vmet_AFMarray = np.vstack((Vmet_AFMarray,Vmet_AFMarray[1:]))
time_AFMarray = np.hstack((time_AFMarray,time_AFMarray[1:]+2*np.pi))
zins_AFMarray = np.hstack((zins_AFMarray,zins_AFMarray[1:]))
Vs_AFMarray = np.hstack((Vs_AFMarray,Vs_AFMarray[1:]))
F_AFMarray = np.hstack((F_AFMarray,F_AFMarray[1:]))
P_AFMarray = np.hstack((P_AFMarray,P_AFMarray[1:]))

# Unit conversions and organize arrays for saving

time_AFMarray = time_AFMarray
zins_AFMarray = zins_AFMarray*1e9
Vs_AFMarray = Vs_AFMarray/Physics_Semiconductors.e
F_AFMarray = F_AFMarray*(1e-9)**2*1e12
P_AFMarray = P_AFMarray

save_AFMarray_time = pd.DataFrame({'time': [str(x) for x in time_AFMarray]})
save_AFMarray_zins = pd.DataFrame({'zins': [str(x) for x in zins_AFMarray]})
save_AFMarray_Vs = pd.DataFrame({'Vs': [str(x) for x in Vs_AFMarray]})
save_AFMarray_F = pd.DataFrame({'F': [str(x) for x in F_AFMarray]})
save_AFMarray_P = pd.DataFrame({'P': [str(x) for x in P_AFMarray]})
save_AFMarrays = pd.concat([save_AFMarray_time,save_AFMarray_zins,save_AFMarray_Vs,save_AFMarray_F,save_AFMarray_P], axis=1, join="outer")

zsem_AFMarray = pd.DataFrame(zsem_AFMarray*1e9)
Evsem_AFMarray = pd.DataFrame((Ev-Vsem_AFMarray)/Physics_Semiconductors.e)
Eisem_AFMarray = pd.DataFrame((Ei-Vsem_AFMarray)/Physics_Semiconductors.e)
Ecsem_AFMarray = pd.DataFrame((Ec-Vsem_AFMarray)/Physics_Semiconductors.e)
Efsem_AFMarray = pd.DataFrame(0*zsem_AFMarray+Ef/Physics_Semiconductors.e)
zgap_AFMarray = pd.DataFrame(zgap_AFMarray*1e9)
Vgap_AFMarray = pd.DataFrame(Vgap_AFMarray/Physics_Semiconductors.e)
zmet_AFMarray = pd.DataFrame(zmet_AFMarray*1e9)
Vmet_AFMarray = pd.DataFrame(Vmet_AFMarray/Physics_Semiconductors.e)
zvac_AFMarray = pd.DataFrame(zvac_AFMarray*1e9)
Vvac_AFMarray = pd.DataFrame(Vvac_AFMarray/Physics_Semiconductors.e)


################################################################################
# Save

name = "%.1f_%.2f_%.2f_%.2f_%.2f_%.2f_%.3f_%.3f_%.1f_%.1f_%.0f_%.0f_%.0f_%.0f_%.0f_%.0f_%.2f" % (slider_Vg, slider_zins, slider_Eg, slider_epsilonsem, slider_WFmet, slider_EAsem, slider_donor, slider_acceptor, slider_emass, slider_hmass, slider_T, slider_amplitude, slider_resfreq, slider_lag, slider_springconst, slider_Qfactor, slider_tipradius)

save_AFMarrays.to_csv('_'.join(['Xsave_AFMtime','Si',name,'timearrays.csv']),index=False)
zsem_AFMarray.to_csv('_'.join(['Xsave_AFMbanddiagram','Si',name,'zsem.csv']),index=False)
Evsem_AFMarray.to_csv('_'.join(['Xsave_AFMbanddiagram','Si',name,'Evsem.csv']),index=False)
Eisem_AFMarray.to_csv('_'.join(['Xsave_AFMbanddiagram','Si',name,'Eisem.csv']),index=False)
Ecsem_AFMarray.to_csv('_'.join(['Xsave_AFMbanddiagram','Si',name,'Ecsem.csv']),index=False)
Efsem_AFMarray.to_csv('_'.join(['Xsave_AFMbanddiagram','Si',name,'Efsem.csv']),index=False)
zgap_AFMarray.to_csv('_'.join(['Xsave_AFMbanddiagram','Si',name,'zgap.csv']),index=False)
Vgap_AFMarray.to_csv('_'.join(['Xsave_AFMbanddiagram','Si',name,'Vgap.csv']),index=False)
zmet_AFMarray.to_csv('_'.join(['Xsave_AFMbanddiagram','Si',name,'zmet.csv']),index=False)
Vmet_AFMarray.to_csv('_'.join(['Xsave_AFMbanddiagram','Si',name,'Vmet.csv']),index=False)
zvac_AFMarray.to_csv('_'.join(['Xsave_AFMbanddiagram','Si',name,'zvac.csv']),index=False)
Vvac_AFMarray.to_csv('_'.join(['Xsave_AFMbanddiagram','Si',name,'Vvac.csv']),index=False)