/*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
**                                                                                  **
** This file forms part of the Underworld geophysics modelling application.         **
**                                                                                  **
** For full license and copyright information, please refer to the LICENSE.md file  **
** located at the project root, or contact the authors.                             **
**                                                                                  **
**~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*/
/* -*- C -*-  (not really, but good for syntax highlighting) */

%module gLucifer

%include "exception.i"
%import "StGermain.i"
%import "StgDomain.i"
%import "StgFEM.i"
%import "PICellerator.i"

%include "carrays.i"
%include "cdata.i"
/* Create some functions for working with "float *" */
%array_functions(float, farray)

%{
/* Includes the header in the wrapper code */
#include <mpi.h>
#include <petsc.h>
#include <vector>

extern "C" {
#include <StGermain/StGermain.h>
#include <StgDomain/StgDomain.h>
#include <StgFEM/StgFEM.h>
#include <PICellerator/PICellerator.h>
#include <gLucifer/gLucifer.h>
}
%}


%include "Base/types.h"
%include "Base/ColourMap.h"
%include "Base/DrawingObject.h"
%include "Base/DrawingObject_Register.h"
%include "Base/Database.h"
%include "Base/Finalise.h"
%include "Base/Init.h"
%include "Base/ViewerTypes.h"
%include "DrawingObjects/CrossSection.h"
%include "DrawingObjects/SwarmViewer.h"
%include "DrawingObjects/VectorArrowCrossSection.h"
%include "DrawingObjects/MeshCrossSection.h"
%include "DrawingObjects/VectorArrowMeshCrossSection.h"
%include "DrawingObjects/VectorArrows.h"
%include "DrawingObjects/VectorArrowsOnMesh.h"
%include "DrawingObjects/MeshViewer.h"
%include "DrawingObjects/DrawingObjects.h"
%include "DrawingObjects/Isosurface.h"
%include "DrawingObjects/IsosurfaceCrossSection.h"
%include "DrawingObjects/ScalarFieldCrossSection.h"
%include "DrawingObjects/ScalarField.h"
%include "DrawingObjects/ScalarFieldOnMeshCrossSection.h"
%include "DrawingObjects/ScalarFieldOnMesh.h"
%include "DrawingObjects/FieldSampler.h"
%include "DrawingObjects/types.h"
%include "libgLucifer/Finalise.h"
%include "libgLucifer/gLucifer.h"
%include "libgLucifer/Init.h"




