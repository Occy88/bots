import inspect
import logging
import sys
import threading
import time

logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(asctime)s.%(msecs)03d %(levelname)s:\t%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


def GenericCardTemplate():
    class GenericCard:
        """
        A function calls a set of functions with latest args at a set time interval
        to create a bind_on function:
        create a function who's name starts with: do_
        the functions generated for you will be: bind_on_...

        signature

        """
        #  functions to call is a dictionary hz:[functions]
        # list of methods bound with their functions to call at the relevant intervals
        # method gc_f_name: {args:most recent,functions_to_call: { hz: [functions]}
        __methods_bound = {}

        def __init__(self, *args, **kwargs):
            # get all class methods
            # logging.info('========= CREATING GENERIC CARD ===================')
            # logging.info(self.__class__)
            # logging.info(dir(self.__class__))
            # logging.info(args)
            # logging.info(kwargs)
            # print('----------- ARGUMENTS DONE NOW GENERATING NEW METHODS ------------------')
            self.__bind_hooks(self.__get_child_methods(self.__class__))

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
            # logging.info("ITERATING METHODS: ", methods)
            methods_child = []
            for index, (gc_f_name, f) in enumerate(methods):
                # logging.info(index, gc_f_name, f)
                # logging.info(gc_f_name.startswith('_'))
                if not gc_f_name.startswith('do_'):
                    continue
                methods_child.append((gc_f_name, f))
            # logging.info("FINISHED GETTING ALL CHILD====================")
            return methods_child

        def __generic_bind_function_template(*args, **kwargs):
            def __generic_bind_function(self, f, hz=-1, *args, gc_f_name=None, **kwargs):
                """
                Regitsters a function
                :param f: function to call with args
                :param hz: -1 is every call, >0 for any specified rate
                :return:
                """
                # print("+========== GENERIC BIND FUNCTION ==================")
                if not (hz == -1 or hz > 0):
                    raise Exception("specified hz invalid: ", hz)
                # logging.info("bindING A FUNCTION: ", f)
                # logging.info("arguments: ", f, hz, gc_f_name)
                # logging.info(self.__methods_bound)
                # print('1: ', self.__methods_bound)
                # print('2: ', f, hz, gc_f_name)
                if hz not in self.__methods_bound[gc_f_name]:
                    self.__methods_bound[gc_f_name][hz] = [f]
                    # print('3: ', self.__methods_bound)
                    self.__start_call_thread(hz, gc_f_name)
                    # print('threads called')
                else:
                    self.__methods_bound[gc_f_name][hz].append(f)
                    # print("3.2: ", self.__methods_bound)
                # print("+========== ==================")

            return __generic_bind_function

        def __generic_callback_template(self, *args, **kwargs):
            def __generic_callback(self, *args, gc_f_name=None, original_function=None, **kwargs):

                """
                A generic callback function, each bound callback
                such as:
                sound_sensor_update(soundwave)
                will call each function bound to that one at -1hz (call on each update)
                after the function has executed.
                :param func_impl:
                :param args:
                :param kwargs:
                :return:
                """
                if gc_f_name is None or original_function is None:
                    raise Exception(
                        "generic callback has no gc_f_name or original_methods problem generating default methods: ",
                        gc_f_name)
                # store the latest arguments/kwargs fbind_on_frame_updateor the function.
                # print("recieved a callback from", gc_f_name)
                # print("updating arguments.")
                self.__methods_bound[gc_f_name]['args'] = args
                self.__methods_bound[gc_f_name]['kwargs'] = kwargs
                returned_args = [original_function(self, *args, **kwargs)]
                self.__methods_bound[gc_f_name]['returned_args'] = returned_args
                # print(self.__methods_bound)
                # execute every function that was bound to be executed at each call
                for f in self.__methods_bound[gc_f_name][-1]:
                    # print("CALLING FUNCTION: ", args, kwargs)
                    if len(returned_args) == 1 and returned_args[0] is None:
                        f(*args, **kwargs)
                    else:
                        f(*returned_args)

            return __generic_callback

        def __bind_hooks(self, methods):
            """
            bind every method (at the moment)
            with a bind_"method_name" function
            so the user can bind their callbacks to be called at specific rates
            or on each update
            :param methods:
            :return:
            """
            # print("METHODS IDENTIFIED: ", methods)
            for gc_f_name, method in methods:
                new_method_name = gc_f_name + '_complete'
                # print("method generated: ", new_method_name)
                f = self.__generic_bind_function_template()
                f.__annotations__ = method.__annotations__
                f.__kwdefaults__ = {'hz': -1, 'gc_f_name': gc_f_name}
                f = self.__bind(self, f, new_method_name)

                # print('_complete method signature: ', inspect.signature(f))
                # add the gc_f_name to the current list of methods bound
                # print("overwriting do_ method: ", gc_f_name)
                self.__methods_bound[gc_f_name] = {'args': (), 'kwargs': {}, 'returned_args': [None], -1: []}
                # print("dictionary updated: ", self.__methods_bound[gc_f_name])
                # overwrite bound function by user so we can perform calls to all hooked functions
                f = self.__generic_callback_template()
                # f.__defaults__.__setattr__('gc_f_name', gc_f_name)
                f.__kwdefaults__ = {'gc_f_name': gc_f_name, 'original_function': method}
                # print("set default args: ", f.__kwdefaults__)
                f.__annotations__ = method.__annotations__
                # print("set default annotations: ", f.__annotations__)
                self.__bind(self, f, gc_f_name)
                # print("method bound to self.", )
            # print("METHODS GENERATED DICT NEW DICT STRUCTURE FOR:", self.__class__)
            # print(self.__methods_bound)
            # print("==================")

        def __call_functions(self, hz, gc_f_name):
            """
            Calls list of functions with latest arguments
            if returned args are not none (function is executed before calling the bound methods with arguments)
            then we call the bound methods with the returned arguments (processed)
            otherwise we call the bound methods with args and kwargs (unprocessed)
            :param f_list:
            :return:
            """
            f_list = self.__methods_bound[gc_f_name][hz]
            # print(gc_f_name)
            # print(self.__methods_bound)
            original_f_args = self.__methods_bound[gc_f_name]['returned_args']
            args = self.__methods_bound[gc_f_name]['args']
            kwargs = self.__methods_bound[gc_f_name]['kwargs']
            for f in f_list:
                if len(original_f_args) == 1 and original_f_args[0] is None:
                    t = threading.Thread(target=f, args=args, kwargs=kwargs, daemon=True).start()
                else:
                    t = threading.Thread(target=f, args=original_f_args, daemon=True).start()

        def __call(self, hz, gc_f_name):
            """
            sends a call signal to all bound methods under the parent function.
            :param hz: call frequency
            :param gc_f_name: parent function name to which many methods are bound
            :return:
            """
            while True:
                self.__call_functions(hz, gc_f_name)
                time.sleep(hz)

        def __start_call_thread(self, hz, gc_f_name):
            """
            Starts the call thread for the relevant frequency of registered functions.
            each frequency has it's own thread where a sleep sleeps for that amount of time
            and calls all  bound functions on wake.
            :param hz: interval to call functions (>0
            :return:
            """
            t = threading.Thread(target=self.__call, args=(hz, gc_f_name), daemon=True).start()

    return GenericCard
