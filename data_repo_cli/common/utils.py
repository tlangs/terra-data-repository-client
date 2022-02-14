

def dispatch_single_id_arg(func):
    return lambda clients, args: func(clients, args.id[0])
