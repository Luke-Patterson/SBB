import log_parser
import threading

queue = log_parser.Queue()

threading.Thread(target=log_parser.run,
                         args=(
                             queue,),
                         daemon=True).start()
update = queue.get()
state = update.state
import pdb; pdb.set_trace()
