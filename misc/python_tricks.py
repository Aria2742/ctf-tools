"""
	The 'del' keyword can be used to delete variables, removing them from the namespace
	References to a variable after deletion will result in an error unless the variable is declared/assigned again
"""
some_var = 'some_val'
# do stuff...
del some_var
# 'some_var' can't be used until it's declared again


"""
	The built-in function 'exec()' can be used to dynamically execute Python code
	https://docs.python.org/3/library/functions.html#exec
	The function parameters are as follows:
		exec(object [, globals [, locals]])
		Where 'object' is a string or code object and 'globals' and 'locals' are dictionaries
	If globals and locals aren't provided, the code is executed in the current scope
	Note: the built-in functions globals() and locals() can be useful for passing into exec()
"""
# prints 'Hello World'
exec("print('Hello World')")
# executes the code from another python file (or even itself)
exec(open('python_tricks.py').read())


"""
	The built-in functions 'globals()' and 'locals()' can be used to retrieve the global and local symbol tables, respectively
	https://docs.python.org/3/library/functions.html#globals
	https://docs.python.org/3/library/functions.html#locals
	globals() returns a dictionary representing the global symbol table for the module
	locals() returns a dictionary representing the current local symbol table
	A variable/function/etc is local only if it is assigned within a function (what about classes?)
"""
# return all globals
globals()
# return all locals
locals()


"""
	Using del, exec(), globals(), and locals(), we can simulate C preprocessor code
"""
# simulate the #ifdef directive (can easily be changed to #ifndef as well)
if 'some_var' in globals() or 'some_var' in locals(): 
# simulate the #define directive
some_var = 'some_val' # can use 'None' or other dummy value for #define w/o a value
# simulate the #undef directive
del some_var
# simulate the #include directive - may require special setup to work
exec(open('some_file').read())