## this file contains supplement functions for Healpix maps analysis

import numpy as np
import healpy as hp
import fitsio as fs
import gc
import pyfits as pf

def fast_read_map(path,field = 0,defaultHDU = 1, RING = True):
    field += 1
    hdu = pf.open(path)[defaultHDU].header
    field_name = hdu['TTYPE'+str(field)]
    ringnest = hdu['ORDERING']
    nside = hdu['NSIDE']
    print 'NSIDE = '+str(nside)
    print 'ORDERING = '+ ringnest
    outmap = fs.read(path)[field_name].ravel()        
    del hdu
    gc.collect()
    if (ringnest=='RING')*RING == True:
        return outmap

    elif ringnest == 'NESTED':
        rawind = np.arange(outmap.size)
        newind = hp.ring2nest(nside,rawind)
        print 'Ordering converted to RING'
        del rawind
        outmap_1 = outmap[newind]
        del newind
        gc.collect()
        return outmap_1

    elif ringnest == 'RING':
        rawind = np.arange(outmap.size)
        newind = hp.nest2ring(nside,rawind)
        print 'Ordering converted to NEST'
        del rawind
        outmap_1 = outmap[newind]
        del newind
        gc.collect()
        return outmap_1
        
