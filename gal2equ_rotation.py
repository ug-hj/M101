from __future__ import print_function, division
import numpy as np
import healpy as hp
import matplotlib

def gal2equ(in_file, out_file, smooth, eulers=None):
    
    e2g = np.array([[-0.054882486, -0.993821033, -0.096476249],
                   [ 0.494116468, -0.110993846,  0.862281440],
                   [-0.867661702, -0.000346354,  0.497154957]]) # intrinsic rotation
    g2e = np.linalg.inv(e2g)
    eps = 23.452294 - 0.0130125 - 1.63889E-6 + 5.02778E-7
    eps = eps * np.pi / 180.
    e2q = np.array([[1.,     0.    ,      0.         ],
                   [0., np.cos( eps ), -1. * np.sin( eps )],
                   [0., np.sin( eps ),    np.cos( eps )   ]])
    g2q = np.dot(e2q , g2e)

    psi = np.arctan2(g2q[1,2],g2q[0,2])
    theta = np.arccos(g2q[2,2])
    phi = np.arctan2(g2q[2,1],-g2q[2,0]) # deduced from zyz rotation matrix
    
    fwhm = smooth*((2*np.pi)/360)

    alms = hp.read_alm(in_file)
    hp.smoothalm(alms, fwhm=fwhm)

    if eulers == None:
        hp.rotate_alm(alms, phi, theta, psi) # reverse rotation order ->                                            extrinsic rotation
        print('Euler angles (zyz) = ', str(np.rad2deg(phi)), str(np.rad2deg(theta)), str(np.rad2deg(psi)))
    else:
        eulers = np.deg2rad(eulers)
        hp.rotate_alm(alms, eulers[0], eulers[1], eulers[2])
        print('Euler angles (zyz) = ', str(np.rad2deg(eulers[0])), str(np.rad2deg(eulers[1])), str(np.rad2deg(eulers[2])))

    print(e2q)
    hp.write_alm(out_file, alms)

if __name__ == "__main__":
    in_file = '/share/splinter/ug_hj/M101/lambda256ebv_alms.fits'
    out_file = '/share/splinter/ug_hj/M101/lambda256ebv_almsRotated.fits'
    smooth = 0.7
    gal2ecl(in_file, out_file, smooth, eulers)
