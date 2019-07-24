#!/usr/bin/python3.6

# docker inspect info
import os
import json
import sys

# conname = sys.argv[1]


def dState(conname):
    Inspect_state = os.popen("docker inspect --format='{{json .State}}' %s" % conname)
    Statejs = json.loads(Inspect_state.read())
    print('容器运行状态 :', Statejs['Status'])
    print('容器启动时间 :', Statejs['StartedAt'])
    print('容器进程Pid :', Statejs['Pid'])


def dmount(conname):
    Inspect_mount = os.popen("docker inspect --format='{{json .Mounts}}' %s" % conname)
    Mountjs = json.loads(Inspect_mount.read())
    if len(Mountjs) == 0:
        print('此容器未挂载卷')
    else:
        for i in Mountjs:
            print('mount挂载类型:', i['Type'])
            print('挂载源目录[外]:', i['Source'])
            print('挂载目标目录[内]:', i['Destination'])
            print('挂载目录允许权限:', i['Mode'])


def dnetwork(conname):
    Inspect_net = os.popen("docker inspect --format='{{json .NetworkSettings}}' %s" % conname)
    Net_data = json.loads(Inspect_net.read())
    Net_port = Net_data['Ports']
    Net_ip = Net_data['IPAddress']
    Net_type = list(Net_data['Networks'])[0]
    print('运行的网络段名为:', Net_type)
    # print('当前容器IP:',Net_ip)
    # print(Net_port)

    Expose_port = list(Net_port)
    for p in Expose_port:
        myport=str(Net_port[p])
        if myport == "None" :
            Hport = 'None'
        else:
            Hport = str(Net_port[p][0]['HostPort'])

        # print(p,myport)
        print('容器内部运行工作端口为:%s,外部映射到容器内部的端口为:%s' % (p, Hport))


def dconfig(conname):
    Inspect_config = Inspect_state = os.popen("docker inspect --format='{{json .Config}}' %s" % conname)
    Config_data = json.loads(Inspect_config.read())
    image_name = Config_data['Image']
    image_cmd = Config_data['Cmd']
    print('容器运行的Cmd是:', image_cmd)
    print('容器运行镜像是:', image_name)


def info(conname):
    name = '当前查询容器为: %s' % conname
    print('+' + '-' * 37 + '+')
    print('|' + name.center(30) + '|')
    print('+' + '-' * 37 + '+')
    print(' 1)查询容器运行状态         ')
    print(' 2)查询容器目录挂载状态      ')
    print(' 3)查询容器镜像和CMD        ')
    print(' 4)查询容器网络情况        ')
    print(' n)退出当前容器查询        ')
    print(' q)退出所有                   ')


while True:
    os.system('clear')
    data = os.popen('''docker ps | awk 'NR>1{print "容器ID: "$1,"容器端口映射: "$(NF-1),"容器名: "$NF}'|rev|column -t |rev''').read()
    print('当前运行容器有\n%s' % data)
    conname = str(input('请输入你要查询的容器ID或容器名(退出请输入n):'))
    if conname == 'n' :
        break
    elif not conname :
        print('未输入,请重新输入。')
    elif conname not in data :
        print('容器不存在,请重新输入。')
    else:
        while True:
            info(conname)
            num = str(input('请输入你的选择:'))
            if num == '1':
                os.system('clear')
                print("容器运行状态查询结果:\n")
                dState(conname)
            elif num == '2':
                os.system('clear')
                print("容器目录挂载状态查询结果:\n")
                dmount(conname)
            elif num == '3':
                os.system('clear')
                print("容器镜像和CMD查询结果为:\n")
                dconfig(conname)
            elif num == '4':
                os.system('clear')
                print("容器网络情况查询结果为:\n")
                dnetwork(conname)
            elif num == 'q' or num == 'n':
                break
            else:
                print('\n输入有误,请重新输入\n')
    if num == 'q':
        break
