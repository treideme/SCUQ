## \file arithmetic.py
# \brief This file contains several functions and classes that are used
# for numeric computations in the other modules of this library.
#  \author <a href="http://thomas.reidemeister.org/" target="_blank">
#          Thomas Reidemeister</a>

## \namespace scuq::arithmetic
#  \brief This namespace contains several functions and classes that are used
#         for numeric computations within this class library.

## \defgroup arithmetic The Arithmetic Module
#
# This module contains several functions, classes, and constants 
# that are used for numeric computations in the other modules of 
# this library.
# \author <a href="http://thomas.reidemeister.org/" target="_blank">
#         Thomas Reidemeister</a>
# \addtogroup arithmetic 
# @{

# standard module
import operator
import numpy

def gcd( m, n ):
    """! @brief Calculate the greatest common divisor.
      @param n First integer value (greater or equal to zero).
      @param m Second value (greater or equal to zero).
      @return The greatest common divisor of the inputs.
    """
    assert( isinstance( m, int ) or isinstance( m, long ) )
    assert( isinstance( n, int ) or isinstance( n, long ) )
    assert( n >= 0L and m >= 0L )
    
    m = long( m )
    n = long( n )
    
    if( n == 0L ):
        return m
    else:
        return gcd( n, m % n )

def rational( n, d ):
    """! @brief       This function provides an interface for rational numbers
      creation, as suggested in PEP 239.
      @param d The denominator (must be an interger type).
      @param n The nominator (must be an integer type).
      @return An instance of RationalNumber
    """
    return RationalNumber( n, d )

def complex_to_matrix(c):
    """! @brief       This function converts a complex number to a column
       vector.
      @param c A complex number (a,b).
      @return An instance of numpy.matrix.
    """
    val = complex(c)
    
    return numpy.matrix([[val.real, -val.imag], [val.imag, val.real]])
    

class RationalNumber:
    """! @brief This class provides support for rational numbers.    
      @attention This class emulates the behaviour of rational numbers. 
                 If the overloaded emulation methods have an unknown
                 number type, they fall back to floating point
                 operations.
      @note Instances of this class can be serialized using pickle.
      @see RationalNumber.__float__
    """
    
    def __init__( self, dividend, divisor=1L ):
        """! @brief Default constructor.
        
              This initializes the rational number.
              @param self
              @param dividend An integer representing the dividend of this 
                     rational number.
              @param divisor An integer representing the divisor of this 
                     rational number. If this parameter is obmitted it is 
                     initialized to 1.
        """
        assert( isinstance( dividend, int ) or isinstance( dividend, long ) )
        assert( isinstance( divisor, int ) or isinstance( divisor, long ) 
                or divisor == None )
        
        if( divisor == 0L ):
            raise ArithmeticError( "Divide by zero" )
        
        self.__divisor__ = long( divisor )    
        self.__dividend__ = long( dividend )
        self.normalize()
        
    def __str__( self ):
        """! @brief This method returns a string representing this rational number.
              @param self
              @return A string representing this rational number.
        """
        if( self.__divisor__ == 1L ):
            return str( self.__dividend__ )
        else:
            return "("+str( self.__dividend__ )+"/"+str( self.__divisor__ )+")"
        
    def normalize( self ):
        """! @brief  This method maintains the canonical form of this rational 
               number and avoids negative divisors.
               @param self
        """
        if( self.__divisor__ < 0 ):
            self.__dividend__ = - self.__dividend__
            self.__divisor__  = - self.__divisor__
        mygcd = gcd( abs( self.__dividend__ ), self.__divisor__ )
        self.__dividend__ = self.__dividend__ / mygcd
        self.__divisor__  = self.__divisor__ / mygcd
        
    ### The following methods are used to emulate the
    ### numeric behaviour.
    
    def __complex__( self ):
        """! @brief Cast this rational number to a complex number.
              @param self
              @return A complex number, having a zero imaginary part.
        """
        return complex( self.__float__() )

    def __int__( self ):
        """! @brief Cast this rational number to an integer.
              @exception OverflowError If the conversion raises an
                         integer overflow.
              @param self
              @return An integer.    
        """
        return int( self.__dividend__ )/int( self.__divisor__ )
    
    def __long__( self ):
        """! @brief Cast this rational number to a long integer.
              @param self
              @return An integer. 
        """
        return self.__dividend__ / self.__divisor__
    
    def __float__( self ):
        """! @brief Cast this rational number to a floating point number.
              @param self
              @return An integer. 
        """
        return float( operator.truediv( self.__dividend__, 
                                       self.__divisor__ ) )
    
    def __add__( self, value ):
        """! @brief Add a number and return the result.
              @param self
              @param value The number to add.
              @return The sum of this instance and the argument.
        """
        assert( isinstance( value, RationalNumber ) )
        
        selfDividend  = self.__dividend__ * value.__divisor__
        otherDividend = value.__dividend__ * self.__divisor__
        newDivisor    = self.__divisor__ * value.__divisor__
        return RationalNumber( selfDividend + otherDividend, \
                               newDivisor )
    
    def __sub__( self, value ):
        """! @brief Substract a number and return the result.
              @param self
              @param value The number to substract.
              @return The difference of this instance and the argument.
        """
        assert( isinstance( value, RationalNumber ) )
        
        selfDividend  = self.__dividend__ * value.__divisor__
        otherDividend = value.__dividend__ * self.__divisor__
        newDivisor    = self.__divisor__ * value.__divisor__
        return RationalNumber( selfDividend - otherDividend, \
                                  newDivisor )
    
    def __mul__( self, value ):
        """! @brief Multiply a number and return the result.
              @param self
              @param value The number to multiply.
              @return The product of this instance and the argument.
        """
        assert( isinstance( value, RationalNumber ) )
        
        newDividend   = self.__dividend__ * value.__dividend__
        newDivisor    = self.__divisor__ * value.__divisor__
        return RationalNumber( newDividend, newDivisor )
    
    def __pow__( self, value ):
        """! @brief Raise this rational number to the given power and return
              the result.
              @attention If the argument is a floating point number then
                         a floating point number will be returned. Note that
                         this may result in a loss of accuracy.
              @param self
              @param value A numeric value representing the power.
              @return A new rational number representing power of this instance.
        """
        assert( isinstance( value, RationalNumber ) )
        if( value.is_integer() ):
            if( value < 0L ):
                return pow( ~self, -value )
            else:
                value = long(value)
                return RationalNumber( self.__dividend__**value, self.__divisor__
                                       **value )
                
        ## something else (maybe float)
        return float( self )**value

    def __rpow__( self, value ):
        """! @brief Raise another value to the power of this rational number.
              the result.
              @param self The exponent.
              @param value A value to be raised to the power.
              @return A new rational number representing power of this instance.
        """
        assert(isinstance(value, RationalNumber))
        if( self.is_integer() ):
            return value ** long( self )
        else:
            return value ** float( self )
    
    def __div__( self, value ):
        """! @brief Divide by another number and return the result.
              @param self
              @param value A number.
              @return The fraction of this instance and the number.
        """
        assert( isinstance( value, RationalNumber ) )

        if( value.__dividend__ == 0L ):
            raise ArithmeticError( "Divide by zero" )

        newDividend   = self.__dividend__ * value.__divisor__
        newDivisor    = self.__divisor__ * value.__dividend__
        return RationalNumber( newDividend, newDivisor )
    
    def __neg__( self ):
        """! @brief This method returns the negative of this instance.
              @param self
              @return A new rational number.
        """
        return RationalNumber( -self.__dividend__, self.__divisor__ )
    
    def __pos__( self ):
        """! @brief This method returns a copy of this instance.
              @param self
              @return A new rational number.
        """
        return RationalNumber( self.__dividend__, self.__divisor__ )
    
    def __abs__( self ):
        """! @brief This method returns the absolute value of this instance.
              @param self
              @return A new rational number.
        """
        if( self.__dividend__ < 0 ):
            return self.__neg__()
        return self.__pos__()
    
    def __invert__( self ):
        """! @brief This method returns a new rational number that
              swapped dividend and divsor of this instance.
              @param self
              @return A new rational number.
        """
        return RationalNumber( self.__divisor__, self.__dividend__ )
    
    def get_dividend( self ):
        """! @brief Returns the dividend of this instance.
              @param self
              @return The dividend of this instance.
        """
        return self.__dividend__
    
    def get_divisor( self ):
        """! @brief Returns the divisor of this instance.
              @param self
              @return The divisor of this instance.
        """
        return self.__divisor__
    
    def __eq__( self, value ):
        """! @brief Checks if this instance is equal to a number.
              @param self
              @param value The value to compare to.
              @return If this rational number is equal to the argument.
        """
        if(not isinstance(value, RationalNumber)):
            try:
                s,v = coerce(self, value)
                return s == v
            except NotImplementedError:
                return False
        
        return self.__divisor__ == value.__divisor__ \
           and self.__dividend__ == value.__dividend__

    def __lt__( self, value ):
        """! @brief Checks if this instance is less than another number.
              @param self
              @param value The value to compare to.
              @return True, if this rational number is less than the argument.
        """
        assert( operator.isNumberType( value ) )
        
        if( isinstance( value, long ) or isinstance( value, int ) ):
            return self.__dividend__ < self.__divisor__ * long( value )
        if( isinstance( value, RationalNumber ) ):
            return self.__dividend__ * value.__divisor__ < \
                   value.__dividend__ * self.__divisor__
        # something else
        return float( self ) < value
    
    def __ne__( self, value ):
        """! @brief Checks if this instance unequal to another number.
              @param self
              @param value The value to compare to.
              @return True, if this rational number unequal to the argument.
        """
        assert( operator.isNumberType( value ) )
        
        if( isinstance( value, long ) or isinstance( value, int ) ):
           return self.__divisor__ != 1L or self.__dividend__ != value
        if( isinstance( value, RationalNumber ) ):
           return self.__divisor__ != value.__divisor__ or \
                  self.__dividend__ != value.__dividend__
        # something else
        return value != float( self )

    def __gt__( self, value ):
        """! @brief Checks if this instance is greater than another number.
              @param self
              @param value The value to compare to.
              @return True, if this rational number is greater than the argument.
        """
        assert( operator.isNumberType( value ) )
        
        if( isinstance( value, long ) or isinstance( value, int ) ):
            return self.__dividend__ > self.__divisor__ * long( value )
        if( isinstance( value, RationalNumber ) ):
            return self.__dividend__ * value.__divisor__ > \
                   value.__dividend__ * self.__divisor__
        # something else
        return float( self ) > value

    def __ge__( self, value ):
        """! @brief Checks if this instance is greater or equal to another number.
              @param self
              @param value The value to compare to.
              @return True, if this rational number is greater or equal to the 
                      argument.    
        """
        return self.__gt__( value ) or self.__eq__( value )
    
    def __le__( self, value ):
        """! @brief Checks if this instance is less or equal to another number.
              @param self
              @param value The value to compare to.
              @return True, if this rational number is less or equal to the 
                      argument.
        """
        return self.__lt__( value ) or self.__eq__( value )
    
    def __cmp__( self, value ):
        """! @brief Compares this instance to another number.
              @param self
              @param value The value to compare to.
              @return -1: if this instance is less...; +1: if this is greater 
                      than the argument; 0 otherwise
        """
        assert( operator.isNumberType( value ) )
        
        if( self.__lt__( value ) ):
            return -1
        if( self.__gt__( value ) ):
            return +1
        return 0
    
    def __nonzero__( self ):
        """! @brief Check if this instance is nonzero.
              @param self
              @return True, if the dividend is nonzero.
        """
        return self.__dividend__ != 0L
    
    ### The same arithmetic Operations again, now for
    ### left arguments.
    ### Attention: only +,-,*,/ are defined in this case.
    
    def __radd__( self, value ):
        """! @brief Left addition of a numeric value.
              @param self
              @param value A value to left from this instance. 
        """
        # since this operation is symmetric
        return self.__add__( value )
    
    def __rsub__( self, value ):
        """! @brief Right substraction of a numeric value.
              @param self
              @param value A value to left from this instance. 
        """
        return ( -self ).__add__( value )
    
    def __rmul__( self, value ):
        """! @brief Right multiplication of a numeric value.
              @param self
              @param value A value to left from this instance. 
        """
        return self.__mul__( value )
    
    def __rdiv__( self, value ):
        """! @brief Right division of a numeric value.
              @param self
              @param value A value to left from this instance. 
        """
        return ( ~self ).__mul__( value )
    
    def __getstate__( self ):
        """! @brief Serialization using pickle.
              @param self
              @return A string that represents the serialized form
                      of this instance.
        """
        return ( self.__dividend__, self.__divisor__ )
    
    def __setstate__( self, state ):
        """! @brief Deserialization using pickle.
              @param self
              @param state The state of the object.
        """
        self.__dividend__, self.__divisor__ = state
        
    def value_of( number ):
        """! @brief Factory for generating Rationalnumbers.
              @param number a numeric value (not float nor complex)
              @exception TypeError If the argument is not int, long, or
                         a RationalNumber.
        """
        # no conversion needed
        if( isinstance( number, RationalNumber ) ):
            return number
        if( isinstance( number, int ) ):
            return RationalNumber( number )
        if( isinstance( number, long ) ):
            return RationalNumber( number )
        raise TypeError( "Illegal Argument" )
    value_of = staticmethod( value_of )
    
    def is_integer( self ):
        """! @brief Check wether this instance could be  
              be casted to long accurately.
              @return True, if the divisor is equal to one.
        """
        return self.__divisor__ == 1L
    
    ### The definition of numpy ufuncts
    ### All of these methods cast the rational numbers
    ### to float
    
    def arccos( self ):
        """! @brief This method provides the broadcast interface for
              numpy.arccos.
              @param self
              @return The inverse Cosine of this number.
              @note This number will be converted to float.  
        """
        return numpy.arccos( float( self ) )
    
    def arccosh( self ):
        """! @brief This method provides the broadcast interface for
              numpy.arccosh.
              @param self
              @return The inverse hyperbolic Cosine of this number.
              @note This number will be converted to float.  
        """
        return numpy.arccosh( float( self ) )
    
    def arcsin( self ):
        """! @brief This method provides the broadcast interface for
              numpy.arcsin.
              @param self
              @return The inverse Sine of this number.
              @note This number will be converted to float. 
        """
        return numpy.arcsin( float( self ) )
    
    def arcsinh( self ):
        """! @brief This method provides the broadcast interface for
              numpy.arcsinh.
              @param self
              @return The inverse hyperbolic Sine of this number.
              @note This number will be converted to float. 
        """
        return numpy.arcsinh( float( self ) )
    
    def arctan( self ):
        """! @brief This method provides the broadcast interface for
              numpy.arctan.
              @param self
              @return The inverse Tangent of this number.
              @note This number will be converted to float. 
        """
        return numpy.arctan( float( self ) )
    
    def arctanh( self ):
        """! @brief This method provides the broadcast interface for
              numpy.arctanh.
              @param self
              @return The inverse hyperbolic Tangent of this number.
              @note This number will be converted to float. 
        """
        return numpy.arctanh( float( self ) )
    
    def cos( self ):
        """! @brief This method provides the broadcast interface for
              numpy.cos.
              @param self
              @return The Cosine of this number.
              @note This number will be converted to float. 
        """
        return numpy.cos( float( self ) )
    
    def cosh( self ):
        """! @brief This method provides the broadcast interface for
              numpy.cosh.
              @param self
              @return The hyperbolic Cosine of this number.
              @note This number will be converted to float. 
        """
        return numpy.cosh( float( self ) )
    
    def tan( self ):
        """! @brief This method provides the broadcast interface for
              numpy.tan.
              @param self
              @return The Tangent of this number.
              @note This number will be converted to float. 
        """
        return numpy.tan( float( self ) )
    
    def tanh( self ):
        """! @brief This method provides the broadcast interface for
              numpy.tanh.
              @param self
              @return The hyperbolic Tangent of this number.
              @note This number will be converted to float. 
        """
        return numpy.tanh( float( self ) )
    
    def log10( self ):
        """! @brief This method provides the broadcast interface for
              numpy.log10.
              @param self
              @return The decadic Logarithm of this number.
              @note This number will be converted to float. 
        """
        return numpy.log10( float( self ) )
    
    def sin( self ):
        """! @brief This method provides the broadcast interface for
              numpy.sin.
              @param self
              @return The Sine of this number.
              @note This number will be converted to float. 
        """
        return numpy.sin( float( self ) )
    
    def sinh( self ):
        """! @brief This method provides the broadcast interface for
              numpy.sinh.
              @param self
              @return The hyperbolic Sine of this number.
              @note This number will be converted to float. 
        """
        return numpy.sinh( float( self ) )
    
    def sqrt( self ):
        """! @brief This method provides the broadcast interface for
              numpy.sqrt.
              @param self
              @return The Square Root of this number.
              @note This number will be converted to float. 
        """
        return numpy.sqrt( float( self ) )
    
    def fabs( self ):
        """! @brief This method provides the broadcast interface for
              numpy.fabs.
              @param self
              @return The absolute value of this number.
              @note This number will be converted to float. 
        """
        return numpy.fabs( float( self ) )
    
    def floor( self ):
        """! @brief This method provides the broadcast interface for
              numpy.floor.
              @param self
              @return The largest integer less than or equal to this number.
              @note This number will be converted to float. 
        """
        return numpy.floor( float( self ) )
    
    def ceil( self ):
        """! @brief This method provides the broadcast interface for
              numpy.ceil.
              @param self
              @return The largest integer greater than or equal to this number.
              @note This number will be converted to float. 
        """
        return numpy.ceil( float( self ) )
    
    def exp( self ):
        """! @brief This method provides the broadcast interface for
              numpy.exp.
              @param self
              @return The Exponential of this number.
              @note This number will be converted to float. 
        """
        return numpy.exp( float( self ) )
    
    def log( self ):
        """! @brief This method provides the broadcast interface for
              numpy.log.
              @param self
              @return The Natural Logarithm of this number.
              @note This number will be converted to float. 
        """
        return numpy.log( float( self ) )
    
    def log2( self ):
        """! @brief This method provides the broadcast interface for
              numpy.log2.
              @param self
              @return The binary logarithm of this number.
              @note This number will be converted to float. 
        """
        return numpy.log2( float( self ) )
    
    def square( self ):
        """! @brief This method provides the broadcast interface for
              numpy.square.
              @param self
              @return The binary logarithm of this number.
              @note This number will be converted to float. 
        """
        return self * self
    
    def arctan2( self, other ):
        """! @brief This method provides the broadcast interface for
              numpy.arctan2.
              @param self
              @param other Another rational number.
              @return The binary logarithm of this number.
              @note This number will be converted to float. 
        """
        if(not isinstance(other, RationalNumber)):
            tmp,other = coerce(self,other)
            return numpy.arctan2(tmp, other)
        
        assert(isinstance(other, RationalNumber))
        numpy.arctan2(float(self),float(other))
        
    def hypot( self, other ):
        """! @brief This method provides the broadcast interface for
              numpy.hypot.
              @param self
              @param other Another rational number.
              @return The binary logarithm of this number.
              @note This number will be converted to float. 
        """
        if(not isinstance(other, RationalNumber)):
            tmp,other = coerce(self,other)
            return numpy.hypot(tmp, other)
        return numpy.sqrt(self*self + other*other)
    
    def fmod( self, other ):
        """! @brief This method provides the broadcast interface for
              numpy.fmod.
              @param self
              @param other Another value.
              @return This number modulo other.
              @note This number will be converted to float.
              @attention This method only works one-way. If another
                         type is called i.e. fmod(other, rational(1,1))
                         then it will fail.
        """
        return numpy.fmod( float( self ), other )
    
    def conjugate( self ):
        """! @brief This method provides the broadcast interface for
              numpy.conjugate.
              @param self
              @return This number.
              @note This number will be converted to float.
        """
        return float( self )
    
    def __coerce__(self, other):
        """! @brief Implementation of coercion rules.
        \see Coercion - The page describing the coercion rules."""
        # A x A
        if(isinstance(other, RationalNumber)):
            return (self,other)
        elif(isinstance(other, int)):
            return (self,RationalNumber.value_of(other))
        # A x long -> A x A
        elif(isinstance(other, long)):
            return (self, RationalNumber.value_of(other))
        # fall back to float
        else:
            ret = float(self)
            return coerce(ret, other)
    
## \brief Global constant for infinity that is used in combination with the 
# degrees of freedom evaluation.
INFINITY = "inf"
    
## @}
