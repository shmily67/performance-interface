import subprocess

def main():
    p = subprocess.Popen(args=['ps', '-ef'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outdata, errdata = p.communicate()
    pid_pname_dict = {}
    pname_pid_dict = {} # pname -> [pid, pid]
    for line in outdata.split('\n'):
        if 'PrimaryServices' in line:
            words = line.split()
            #print words
            pid = words[1]
            pname = words[7].split('/')[-1]
            print pid, pname
            assert pid not in pid_pname_dict
            pid_pname_dict[pid] = pname
            if pname not in pname_pid_dict:
                pname_pid_dict[pname] = []
            pname_pid_dict[pname].append(pid)            

    p = subprocess.Popen(args=['lsof', '-i:5679', '-n', '-P'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outdata, errdata = p.communicate()
    print ''    
    connection_dict, name_dict = {}, {}
    for line in outdata.split('\n'):
        if 'beam.smp' != line[:8] and 'ESTABLISHED' in line:
            words = line.split()
            pid = words[1]
            addr = words[8].split('->')[0].split(':')
            pname = pid_pname_dict[pid] #
            print pid, addr, pname

            pid_list = pname_pid_dict[pname]
            i = 0
            for _pid in pid_list:
                if _pid == pid: break
                i += 1
            if 0 == i:
                connection_dict[tuple(addr)] = pname.replace('server_', '')
            else:
                connection_dict[tuple(addr)] = pname.replace('server_', '') + '%d'%i
    
    with open('connection_service_dict.txt', 'w') as f:
        for addr in connection_dict:
            ip, port = addr
            f.write("%s  %s  %s\n"%(ip, port, connection_dict[addr]))#print addr, ' -> ', connection_dict[addr]

    print ''
    for line in errdata.split('\n'):
        print line

if '__main__' == __name__:
    main()
