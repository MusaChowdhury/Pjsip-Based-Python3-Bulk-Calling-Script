import csv
import threading
import wave
from time import sleep
from sys import exit
import pjsua as pj

account_username = "_"                  # User Name
account_password = "_"                  # User Password
account_server = "_"                    # Server Domain
csv_file_location = './call_list.csv'   # Numbers To Call
audio_file_location = './play.wav'      # Recording To Play

# Global variable, will be used later
distinct_number = set()
audio_length = None
index = []
unanswered_user = []
answered_user = []
wait_between_calls = 45
maximum_retry = 3
# Global variable, will be used later


class Track:
    def __init__(self, caller_number, attempt_left=3):
        self.caller_number = caller_number
        self.attempt_left = attempt_left


def start_up():
    global wait_between_calls
    global maximum_retry
    global index
    try:
        print("\nBulk Calling System. Written By Musa Chowdhury\n")
        print(
            f"Current Configuration For This File is, User Name = {account_username}, Account Password = {account_password}",
            f"Account Server = {account_server}")
        print(f"Rename the CSV file to 'call_list.csv. Also Rename WAV file to 'play.wav'. Both files need to be "
              f"inside the same folder where this script exists.")

        # wait_between_calls = int(input("Maximum Wait Between Calls (in seconds ) = "))
        maximum_retry = int(input("Maximum Retry For Each Call = "))

        print("Press Enter To Continue\n")
        input()
    except:
        print("Try Again With Valid Input")
        exit()

    try:
        step_ok = True
        print("Reading CSV File, Only Selecting First Column Of Each Row, AND Delimiter is '\\n' or New Line")
        print("Only Unique Number Will Be Selected, Duplicate Number Will BE IGNORED")
        numbers_csv = open(csv_file_location)
        numbers_temp = csv.reader(numbers_csv, delimiter='\n')
        for x in numbers_temp:
            subject = str(x[0])
            if subject.isdigit():
                distinct_number.add(subject)


    except:
        print("Caught Error While Reading CSV File")
        step_ok = False

    if not step_ok:
        exit()

    print("Unique Number Found :", len(distinct_number))

    print("\nLooking for Audio File . . . ")

    try:
        global audio_length
        audio = wave.open(audio_file_location)
        audio_length = (1.0 * audio.getnframes()) / audio.getframerate()
        print("WAV File Length", str(audio_length) + " Second(s)")
        audio.close()
    except:
        print("Caught Error While Reading WAV File")

    print("\nCreating Call List .....")

    for x in distinct_number:
        index.append(Track(x, maximum_retry))

    print(f"Maximum Number of Retry if Any Caller Does Not Pick UP Phone : {maximum_retry} times\n")

    print("#" * 30)
    print("\nNow Wait ....\n\n")


class MyCallCallback(pj.CallCallback):

    def __init__(self, caller_object_this, current):
        self.caller_object_this = caller_object_this
        self.current = current
        super(MyCallCallback, self).__init__()

    def on_state(self):
        # print(self.call.info().state)
        # global answered_user
        global index
        if self.call.info().state == pj.CallState.DISCONNECTED:
            self.current.release()

        elif self.call.info().state == pj.CallState.CONFIRMED:
            # Call is Answered
            print("Call Answered", self.caller_object_this.caller_number, "#")

            call_slot = self.call.info().conf_slot
            self.wav_player_id = pj.Lib.instance().create_player(audio_file_location, loop=False)
            self.wav_slot = pj.Lib.instance().player_get_slot(self.wav_player_id)
            pj.Lib.instance().conf_connect(self.wav_slot, call_slot)
            sleep(audio_length)
            pj.Lib.instance().player_destroy(self.wav_player_id)
            self.call.hangup()
            answered_user.append(self.caller_object_this)
            index.remove(self.caller_object_this)
            # self.current.release()


class MyAccountCallback(pj.AccountCallback):
    sem = None

    def __init__(self, account):
        pj.AccountCallback.__init__(self, account)
        self.wav_slot = None
        self.wav_player_id = None

    def wait(self):
        self.sem = threading.Semaphore(0)
        self.sem.acquire()

    def on_reg_state(self):
        if self.sem:
            if self.account.info().reg_status >= 200:
                self.sem.release()


lib = pj.Lib()


def create_call(acc):
    while True:
        global unanswered_user
        global index
        global wait_between_calls
        # print(">>>" * 10, len(index))
        if len(index) == 0:
            return
        for i in index:

            if i.attempt_left >= 1:
                print("Call Trying For :", i.caller_number, "Attempt left : ", i.attempt_left)
                current = threading.Semaphore(0)
                acc.make_call(f"sip:{i.caller_number}@{account_server}", cb=MyCallCallback(i, current))
                current.acquire()
                # print(x)
                # print("Waiting For :", wait_between_calls, "seconds")
                # sleep(wait_between_calls)
            else:
                unanswered_user.append(i)
                index.remove(i)
            i.attempt_left -= 1


try:

    lib.init()
    lib.create_transport(pj.TransportType.UDP, pj.TransportConfig(5896))
    lib.start()
    acc = lib.create_account(pj.AccountConfig(account_server, account_username, account_password))
    acc_cb = MyAccountCallback(acc)
    acc.set_callback(acc_cb)
    acc_cb.wait()
    reg_status = acc.info().reg_status
    # os.system('clear')
    start_up()
    sleep(10)
    print(f"Registration complete, status={acc.info().reg_status}({acc.info().reg_reason})\n")
    create_call(acc)
    lib.destroy()
    lib = None

except pj.Error as e:
    print("Exception: " + str(e))
    lib.destroy()
    exit()

print("+" * 30)
print("\nAnswered Phone\n")
if len(answered_user):
    for i in answered_user:
        print(i.caller_number)
else:
    print("NO USER ANSWERED PHONE")

print("\n")
print("+" * 30)
print("\n\n\n")
print("-" * 30)
print("\nUnanswered Phone\n")
if len(unanswered_user):
    for i in unanswered_user:
        print(i.caller_number)
else:
    print("EVERY USER ANSWERED PHONE")
print("\n")
print("-" * 30)

