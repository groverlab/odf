import sys, datetime, time, platform, json

try:
    import serial
    from serial.tools.list_ports import comports
except ImportError as err:
    sys.exit("❌ Can't find pyserial module - install it by running 'pip install pyserial'")


def run(comments=""):
    r = {}
    if len(comments) > 0:
        comments = comments.replace(' ', '_')
    else:
        comments = input("Sample?  ").replace(' ', '_')
    r["filename"] = datetime.datetime.now().strftime("%Y%m%dT%H%M%S") + "_" + comments + ".json"

    ports = 0
    port = ""
    for p in comports():
        print(str(p))
        if "USB" in str(p) or "usb" in str(p):
            port = p.name
            ports += 1
    if ports == 0:
        sys.exit("❌ No port found - is the Arduino plugged in?")
    if ports >= 2:
        sys.exit("❌ Too many ports found - unplug everything but the Arduino and try again")
    if platform.system() == "Darwin":  # if MacOS...
        port = "/dev/" + port   # ...prepend /dev/
    print("✅ Found an Arduino at " + port)

    r["data"] = []
    ser = serial.Serial(port, 115200, timeout=5)

    start_time = time.time()
    r["start_time"] = str(start_time)

    t1 = 300  # 5 minutes  300
    t2 = 30*60 + t1  # 30 minutes of dissolution

    ser.flush()
    ser.read_all()
    while True:
        try:
            et = time.time() - start_time
            if 0 <= et < t1-5:  # baseline phase
                print(f"{str(datetime.timedelta(seconds=t1-et))}", end="\t")
            elif t1-5 <= et < t1:  # alarm phase
                print(f"{str(datetime.timedelta(seconds=t1-et))}\a", end="\t")
            elif t1 <= et < t2:  # dissolution phase
                print(f"{str(datetime.timedelta(seconds=t2-et))}", end="\t")
            elif et >= t2:  # experiment over
                break
            s = ser.readline().decode("utf-8", "ignore")
            print(f"{ser.inWaiting()}\t{s}", end="")
            r["data"].append(int(s))
        except:
            break
    r["stop_time"] = str(time.time())
    f = open(r["filename"], "w")
    json.dump(r, f)
    f.close()
    print("\n\aDONE")





