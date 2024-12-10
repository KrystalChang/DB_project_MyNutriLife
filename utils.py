
def get_selection(conn, options):

    if isinstance(options, dict):
        option_idx = options.keys()
    else:
        option_idx = [x for x in range(1, len(options)+1)]
    recv_msg = conn.recv(100).decode("utf-8")
    while int(recv_msg) not in option_idx:
        msg = "[INPUT]Wrong input, please select "
        for idx in option_idx:
            msg = msg + f'[{idx}] '
        msg += ': '
        conn.send(msg.encode('utf-8'))
        
        recv_msg = conn.recv(100).decode("utf-8")
    print("Select option:", recv_msg)
    
    if isinstance(options, dict):
        return options[recv_msg]
    else:
        return options[int(recv_msg)-1]
    


def list_option(options):
    msg = ''
    if isinstance(options, dict):
        for idx, option in options.items():
            msg = msg + f'[{idx}] {option.get_name()}\n'
    elif isinstance(options, list):
        for idx, option in enumerate(options, 1):
            if hasattr(option, 'get_name'): # Action class
                msg += f'[{idx}] {option.get_name()}\n'
            else: # User info item
                msg += f'[{idx}] {option}\n'      

    return msg