// Distributed under MIT licence. See https://github.com/QuEST-Kit/QuEST/blob/master/LICENCE.txt for details

/** @file
 * Distributed version of some of the GPU functions for the KISTI RFP.
 *
 * @author Bruno Villasenor (AMD) bruno.villasenoralvarez@amd.com
 */

# ifndef QUEST_GPU_DISTRIBUTED_H
# define QUEST_GPU_DISTRIBUTED_H

# include "QuEST.h"

# ifdef __cplusplus
extern "C" {
# endif

QuESTEnv createQuESTEnvDistributed(void);

void synchronizeMPI(void);

void finalizeMPI(void);

void exchangeDeviceStateVectors(Qureg qureg, int pairRank);

qreal statevec_getRealAmpDistributed(Qureg qureg, long long int index);

qreal statevec_getImagAmpDistributed(Qureg qureg, long long int index);

qreal reduceStateProb( Qureg qureg, qreal stateProb );

# ifdef __cplusplus
}
# endif

# endif // QUEST_QASM_H
