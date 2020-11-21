import inspect
import threading
import time


class GenericCard:
    """
    A function calls a set of functions with latest args at a set time interval
    """
    #  functions to call is a dictionary hz:[functions]
    # list of methods registered with their functions to call at the relevant intervals
    # method gc_f_name: {args:most recent,functions_to_call: { hz: [functions]}
    __methods_registered = {}

    def __init__(self, class_type):
        # get all class methods
        print(class_type)
        print(dir(class_type))

        self.__register_hooks(self.__get_child_methods(class_type))

    @staticmethod
    def __bind(instance, func, as_name=None):
        """
        Bind the function *func* to *instance*, with either provided gc_f_name *as_name*
        or the existing gc_f_name of *func*. The provided *func* should accept the
        instance as the first argument, i.e. "self".
        """
        if as_name is None:
            as_name = func.__name__
        bound_method = func.__get__(instance, instance.__class__)
        setattr(instance, as_name, bound_method)
        return bound_method

    @staticmethod
    def __get_child_methods(class_type):
        methods = inspect.getmembers(class_type, predicate=inspect.isfunction)
        # print("ITERATING METHODS: ", methods)
        methods_child = []
        for index, (gc_f_name, f) in enumerate(methods):
            # print(index, gc_f_name, f)
            # print(gc_f_name.startswith('_'))
            if gc_f_name.startswith('_'):
                continue
            methods_child.append((gc_f_name, f))
        # print("FINISHED GETTING ALL CHILD====================")
        return methods_child

    def __generic_register_function(self, f, hz=-1, *args, gc_f_name=None):
        """
        Regitsters a function
        :param f: function to call with args
        :param hz: -1 is every call, >0 for any specified rate
        :return:
        """
        if not (hz == -1 or hz > 0):
            raise Exception("specified hz invalid: ", hz)
        # print("REGISTERING A FUNCTION: ", f)
        # print("arguments: ", f, hz, args, gc_f_name)
        # print(self.__methods_registered)
        # print(gc_f_name)
        if hz not in self.__methods_registered[gc_f_name]:
            self.__methods_registered[gc_f_name][hz] = [f]
            self.__start_call_thread(hz, gc_f_name)
        else:
            self.__methods_registered[gc_f_name][hz].append(f)

    def __generic_callback(self, *args, gc_f_name=None, **kwargs):
        """
        A generic callback function, each registered callback
        such as:
        sound_sensor_update(soundwave)
        will call each function registered to that one at -1hz (call on each update)
        after the function has executed.
        :param func_impl:
        :param args:
        :param kwargs:
        :return:
        """
        if gc_f_name is None:
            raise Exception("generic callback has no gc_f_name problem generating default methods: ", gc_f_name)
        # store the latest arguments/kwargs for the function.
        print('callback triggered')
        print(gc_f_name, args, kwargs)
        self.__methods_registered[gc_f_name]['args'] = args
        self.__methods_registered[gc_f_name]['kwargs'] = kwargs
        print("REGISTERED KWARGS")
        # execute every function that was registered to be executed at each call
        for f in self.__methods_registered[gc_f_name][-1]:
            f(*args, **kwargs)

    def __register_hooks(self, methods):
        """
        register every method (at the moment)
        with a register_"method_name" function
        so the user can register their callbacks to be called at specific rates
        or on each update
        :param methods:
        :return:
        """
        print(methods)
        for gc_f_name, method in methods:
            new_method_name = 'register_' + gc_f_name
            f = GenericCard.__generic_register_function
            f.__kwdefaults__ = {'hz': -1, 'gc_f_name': gc_f_name}
            f = self.__bind(self, f, new_method_name)
            # add the gc_f_name to the current list of methods registered
            self.__methods_registered[gc_f_name] = {'args': (), 'kwargs': {}, -1: []}
            # overwrite registered function by user so we can perform calls to all hooked functions
            f = GenericCard.__generic_callback
            # f.__defaults__.__setattr__('gc_f_name', gc_f_name)
            f.__kwdefaults__ = {'gc_f_name': gc_f_name}
            self.__bind(self, f, gc_f_name)

    def __call_functions(self, hz, gc_f_name):
        """
        Calls list of functions with latest arguments
        :param f_list:
        :return:
        """
        f_list = self.__methods_registered[gc_f_name][hz]
        args = self.__methods_registered[gc_f_name]['args']
        kwargs = self.__methods_registered[gc_f_name]['kwargs']
        for f in f_list:
            f(*args, **kwargs)

    def __call(self, hz, gc_f_name):
        while True:
            self.__call_functions(hz, gc_f_name)
            time.sleep(hz)

    def __start_call_thread(self, hz, gc_f_name):
        """
        Calls the relevant list of functions at a specified interval
        :param hz: interval to call functions (>0
        :return:
        """

        t = threading.Thread(target=self.__call,
                             args=(hz, gc_f_name))
        t.daemon = True
        t.start()
