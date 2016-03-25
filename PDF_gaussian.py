from __future__ import print_function, division
import numpy as np
import csv
import pandas
import matplotlib.pyplot as plt
from scipy.stats import norm
#import seaborn

def stack(in_catalog, out_img, out_csv, outdata_csv, dNdz_csv):
    annzfull = pandas.read_csv(in_catalog)

    zbins = np.array([np.arange(0.0, 0.4, 0.05), np.arange(0.05, 0.45, 0.05)]).T
    zbins = np.vstack([zbins, [0.4, 3.0]])


    #fig, axtup = plt.subplots(nrows=3, ncols=3, figsize=(10, 10))
    #fig.subplots_adjust(hspace=0, wspace=0)

    #axes = [elem for row in axtup for elem in row]

    bin_centres = np.arange(0.005, 0.805, 0.01)

    fl = open(out_csv, 'w')
    writer = csv.writer(fl)
    writer.writerow(['z_min', 'z_max', 'mean', 'st.dev', 'N_gal'])

    fl3 = open(dNdz_csv, 'w')
    writer3 = csv.writer(fl3)
    writer3.writerow(['z_mid', 'N_1', 'N_2', 'N_3', 'N_4', 'N_5', 'N_6', 'N_7'])
    inner_bins = np.arange(0.049, 0.401, 0.001) # <---- CHANGE STEP? 
    z_mids = inner_bins + 0.0005
    DNDZ = z_mids[:-1]

    # bin_centres2 = np.arange(0., 0.8, 0.01)
    # Gcsv = bin_centres2

    for i, (zinf, zsup) in enumerate(zbins):
    #     if i > 0:
    #       break
        # ax = axes[i]
        
        mask = (annzfull["ANNZ_best"] >= zinf) & (annzfull["ANNZ_best"] < zsup)
        annzbin = annzfull[mask]
        annzpdfs = annzbin.ix[:, 15:]
        zbinpdf_tot = annzpdfs.sum().as_matrix()
        zbinpdf = zbinpdf_tot/len(annzpdfs)
    #    print(zbinpdf_tot[0])
        # zbinpdf /= len(annzpdfs)
        zbinpdf2 = zbinpdf/zbinpdf.max()
        mean = np.sum(bin_centres*zbinpdf)
        variance = np.sum((bin_centres**2)*zbinpdf) - mean**2    
        # norm_dist = norm.pdf(np.arange(0.0, 0.8, 0.01), loc=mean, scale=np.sqrt(variance))
        # norm_dist /= norm_dist.max()
    #     ax.set_title("Normalised z-distributions = [%.2f, %.2f]" % (zinf, zsup), fontsize=7)
    #     ax.bar(np.arange(0.0, 0.8, 0.01), zbinpdf2, width=0.01, color="red", edgecolor="red", alpha=0.4,
    #            label=("ANNz2 PDF\nN = %d" % (len(annzpdfs))))
    #     ax.plot(np.arange(0.0, 0.8, 0.01), norm_dist, label=('$\mu$ = %.3f \n$\sigma$ = %.3f' % (mean, np.sqrt(variance))))
    #     ax.set_xlabel("$z$", fontsize=8)
    #     ax.set_ylabel("PDF", fontsize=7)
    # #     ax.set_ylim(0, 1.05)
    #     ax.legend(fontsize=10, loc='upper right') 

  #      if (zinf != 0.) & (zsup != 3.0):
  #          annzbest = annzbin['ANNZ_best']
  #          dndz = np.histogram(annzbest, bins=inner_bins)
            
 #           DNDZ = np.column_stack((DNDZ, dndz[0]))

       Gauss = ['%.2f' % zinf, '%.2f' % zsup, '%.4f' % mean, '%.4f' % np.sqrt(variance), len(annzpdfs)]
       writer.writerow(Gauss)

       csv_ext = str(i) + '.csv'
       outdata = outdata_csv + csv_ext

       fl2 = open(outdata, 'w')
       writer2 = csv.writer(fl2)
       writer2.writerow(['z_bin_centre', 'PDF_val', 'PDF_tot'])

       Stack = zip(bin_centres, zbinpdf2, zbinpdf_tot)
       for values in Stack:
           writer2.writerow(values)

        # if (zinf != 0.) & (zsup != 3.0):
        #     mask2 = (annzfull["zspec"] >= zinf) & (annzfull["zspec"] < zsup)
        #     gama_z = annzfull["zspec"]
        #     gama_z = gama_z[mask2]
        #     z_hist = np.histogram(gama_z, bins=80, range=(0., 0.8))
        #     Gcsv = np.column_stack((Gcsv, z_hist[0]))

    
    # print(DNDZ.shape)
#    np.savetxt(dNdz_csv, DNDZ, delimiter=",", fmt="%.4f, %.f, %.f, %.f, %.f, %.f, %.f, %.f")
    # for values in DNDZ:
    #     writer3.writerow(values)
    # np.savetxt('/share/splinter/ug_hj/M101/GAMA_hist.dat', Gcsv, delimiter=',',
                        fmt="%.4f, %.f, %.f, %.f, %.f, %.f, %.f, %.f")

    fl.close()
    fl2.close()
    fl3.close()
    fig.tight_layout()
    plt.savefig(out_img)


    return None

if __name__ == "__main__":
    in_catalog = "/share/splinter/moraes/2016-02-17_SDSS_annz2_photoz/ANNZ2_GAMA_full_matched.csv"
    out_img = "/share/splinter/ug_hj/M101/PDF_stack1.png"
    out_csv = "/share/splinter/ug_hj/M101/PDF_Gauss1.csv"
    outdata_csv = "/share/splinter/ug_hj/M101/PDF_stack_dat"
    dNdz_csv = "/share/splinter/ug_hj/M101/PDF_dNdz.csv"
    stack(in_catalog, out_img, out_csv, outdata_csv, dNdz_csv)
