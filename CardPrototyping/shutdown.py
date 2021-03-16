import os
if os.name=='nt':
    import signal
import signal
# def shutdown(handler):
#     try:
#         signal.signal(signal.SIGINT, ._shutdown)
#         signal.signal(signal.SIGTERM, ._shutdown)
#         # signal.signal(signal.SIGKILL, ._shutdown)
#         signal.signal(signal.SIGQUIT, ._shutdown)
#         signal.signal(signal.SIGHUP, self._shutdown)
#     except Exception as e:
#         pass