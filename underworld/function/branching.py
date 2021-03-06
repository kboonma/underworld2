##~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~##
##                                                                                   ##
##  This file forms part of the Underworld geophysics modelling application.         ##
##                                                                                   ##
##  For full license and copyright information, please refer to the LICENSE.md file  ##
##  located at the project root, or contact the authors.                             ##
##                                                                                   ##
##~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~##
"""
The branching module provides functions which provide branching behaviour. 
Typically, these functions will select other user provided functions when 
certain conditions are met (with the condition also described by a function!).

"""
import underworld as uw
import libUnderworld.libUnderworldPy.Function as _cfn
from _function import Function as _Function


class map(_Function):
    """
    This function performs a map to other functions. The user provides a python 
    dictionary which maps unsigned integers keys to underworld functions. The 
    user must also provide a 'key function'. At evaluation time, the key function
    is evaluated first, with the outcome value determining which function should
    finally be evaluated to return a value.
    
    Parameters
    ----------
    fn_key:  underworld.function.Function (or convertible)
        Function which returns integer key values. This function will be evaluated 
        first to determine which function from the mapping is to be used. 
    mapping: dict(Function)
        Python dictionary providing a mapping from unsigned integer 'key' values to
        underworld 'value' functions. Note that the provided 'value' functions must
        return values of type 'double'.
    fn_default: underworld.function.Function (or convertible)
        Default function to be utilised when the key (returned by fn_key function)
        does not correspond to any key value in the mapping dictionary.
    
    
    The following example sets different function behaviour inside and outside
    of a unit sphere. The unit sphere is represented by particles which 
    record a swarm variable to determine if they are or not inside the sphere.


    Example
    -------
    Setup mesh, swarm, swarmvariable & populate
    
    >>> import underworld as uw
    >>> import underworld.function as fn
    >>> import numpy as np
    >>> mesh = uw.mesh.FeMesh_Cartesian(elementRes=(8,8),minCoord=(-1.0, -1.0), maxCoord=(1.0, 1.0))
    >>> swarm = uw.swarm.Swarm(mesh)
    >>> svar = swarm.add_variable("int",1)
    >>> swarm.populate_using_layout(uw.swarm.layouts.GlobalSpaceFillerLayout(swarm,20))

    For all particles in unit circle, set svar to 1

    >>> svar.data[:] = 0
    >>> for index, position in enumerate(swarm.particleCoordinates.data):
    ...     if position[0]**2 + position[1]**2 < 1.:
    ...         svar.data[index] = 1
    
    Create a function which reports the value '1.' inside the sphere, and
    '0.' otherwise. Note that while we have only used constant value functions 
    here, you can use any object of the class Function.
    
    >>> fn_map = fn.branching.map(fn_key=svar, mapping={0: 0., 1:1.})
    >>> np.isclose(np.pi, uw.utils.Integral(fn_map,mesh).evaluate(),rtol=2e-2)
    array([ True], dtype=bool)
    
    Alternatively, we could utilise the default function to achieve the same 
    result.
    
    >>> fn_map = fn.branching.map(fn_key=svar, mapping={1: 1.}, fn_default=0.)
    >>> np.isclose(np.pi, uw.utils.Integral(fn_map,mesh).evaluate(),rtol=2e-2)
    array([ True], dtype=bool)

    """
    

    def __init__(self, fn_key=None, mapping=None, fn_default=None, *args, **kwargs):
                    
        if not mapping:
            raise ValueError("You must specify a mapping via the 'mapping' parameter.")
        if not isinstance(mapping, dict):
            raise TypeError("'mapping' object passed in must be of python type 'dict'")

        if not fn_key:
            raise ValueError("You must specify a key function via the 'fn_key' parameter.")
        fn_key = _Function._CheckIsFnOrConvertOrThrow(fn_key)

        self.fn_default = _Function._CheckIsFnOrConvertOrThrow(fn_default)
        if self.fn_default == None:
            fn_defaultCself = None
        else:
            fn_defaultCself = self.fn_default._fncself
        # create instance
        self._fncself = _cfn.Map( fn_key._fncself, fn_defaultCself )

        self._fn_key  = fn_key
        self._mapping = mapping

        # build parent
        super(map,self).__init__(argument_fns=[fn_key,self.fn_default],**kwargs)
        
        self._map = {}

        for key, value in mapping.iteritems():
            if not isinstance(key, int) or key < 0:
                raise ValueError("Key '{}' not valid. Mapping keys must be unsigned integers.".format(key))
            funcVal = _Function._CheckIsFnOrConvertOrThrow(value)
            if funcVal == None:
                raise ValueError("'None' is not valid for mapped functions.")
            
            self._underlyingDataItems.update(funcVal._underlyingDataItems) # update dictionary
            # insert mapping and keep handles in py dict
            self._map[key] = funcVal
            self._fncself.insert( key, funcVal._fncself )

class conditional(_Function):
    """
    This function provides 'if/elif' type conditional behaviour.
    
    The user provides a list of tuples, with each tuple being of the 
    form (fn_condition, fn_action). Effectively, each tuple provides a clause 
    within the if/elif statement. 
    
    When evaluated, the function traverses the clauses, stopping at the first 
    fn_condition which returns 'true'. It then executes the corresponding 
    fn_action and returns the results.
    
    If none of the provided clauses return a 'True' result, an exception is 
    raised.
    
    Parameters
    ----------
    clauses: list
        list of tuples, with each tuple being of the form (fn_condition, fn_action).
    
    
    Example
    -------
    The following example uses functions to represent a unit circle. Here a 
    conditional function report back the value '1.' inside the sphere (as per
    the first condition), and '0.' otherwise.

    >>> import underworld as uw
    >>> import underworld.function as fn
    >>> import numpy as np
    >>> mesh = uw.mesh.FeMesh_Cartesian(elementRes=(16,16),minCoord=(-1.0, -1.0), maxCoord=(1.0, 1.0))
    >>> circleFn = fn.coord()[0]**2 + fn.coord()[1]**2
    >>> fn_conditional = fn.branching.conditional( [ (circleFn < 1., 1. ), \
                                                     (         True, 0. ) ] )
    >>> np.isclose(np.pi, uw.utils.Integral(fn_conditional,mesh).evaluate(),rtol=1e-2)
    array([ True], dtype=bool)
    """

    def __init__(self, clauses, *args, **kwargs):
        # error check mapping
        if not isinstance(clauses, (list,tuple)):
            raise TypeError("'clauses' object passed in must be of python type 'list' or 'tuple'")

        self._clauses = []
        funcSet = set()
        for clause in clauses:
            if not isinstance(clause, (list,tuple)):
                raise TypeError("Clauses within the clause list must be of python type 'list' or 'tuple'")
            if len(clause) != 2:
                raise ValueError("Clauses tuples must be of length 2.")
            conditionFn = _Function._CheckIsFnOrConvertOrThrow(clause[0])
            funcSet.add(conditionFn)
            actionFn    = _Function._CheckIsFnOrConvertOrThrow(clause[1])
            funcSet.add(actionFn)
            self._clauses.append( (conditionFn,actionFn) )
        
        # build parent
        self._fncself = _cfn.Conditional()

        super(conditional,self).__init__(argument_fns=funcSet,**kwargs)

        # insert clause into c object now
        for clause in self._clauses:
            self._fncself.insert( clause[0]._fncself, clause[1]._fncself )



