
nz_sent = [rd.uniform(-5, 5) for i in range(10)]
for i in nz_sent:
    IvySendMsg("APNzCommand nz={0}".format(i))

nz_received = []

def on_cx_proc(agent, connected):
    pass
def on_die_proc(agent, _id):
    pass
def on_msg(agent, data):
    global nz_received
    nz_received.append(data)

app_name = "MyIvyApplication" ivy_bus= "127.255.255.255:2010"
IvyInit(app_name, "[%s ready]" % app_name, 0, on_cx_proc, on_die_proc)
IvyStart(ivy_bus)
IvyBindMsg(on_msg, "^APNzControl nz=(.*)")
IvyMainLoop()

