import array
import time
import rp2pio
import board
import microcontroller
import adafruit_pioasm
from rp2pio import StateMachine
from passphrases import TreasurePassphrases



beginBitTransmissionAssembled = adafruit_pioasm.assemble("""
.program beginBitTransmission

    set x, 5 ; 6 full cycles
    wait 1 irq 1
pulse_cycle:
    set pins, 1 [6]
    set pins, 0 [5]
    jmp x-- pulse_cycle

; one less half-cycle loop (19 rather than 20) to incorporate the cost of the 'set' instruction
    set x 18 [2] ; 4 less instruction-cycles to allow transiton to next transmit-bit
blank_cycle:
    jmp x-- blank_cycle [6] ; half-38kHz cycle lasts 7 instructions - 'jmp' is 1, other 6 are pause
    irq 2
""")

controllerLoopAssembled = adafruit_pioasm.assemble("""
.program controllerLoop

    pull block
    set pins,1
    out isr, 16 ; LPF message is only 16 bits
    irq 1 ; write out SS bit
    wait 1 irq 2
    ; perform ss-bit pause (for start-bit of message)
    set x, 27 [13] ; one less loop (28 rather than 29) to incorporate the cost of the 'set' instruction
additional_start_bit_pause:
    jmp x--, additional_start_bit_pause [13] ; 38kHz cycle lasts 14 instructions - 'jmp' is 1, other 13 are pause

transmit_bit:
    out x, 1
    irq 1 ; write out bit start
    wait 1 irq 2
    jmp !x, bit_transmit_finished

    set x, 9 [13] ; one less loop (10 rather than 11) to incorporate the cost of the 'set' instruction
additional_high_bit_pause:
    jmp x--, additional_high_bit_pause [13] ; 38kHz cycle lasts 14 instructions - 'jmp' is 1, other 13 are pause

bit_transmit_finished:
    jmp !osre, transmit_bit

    irq 1 ; write out SS bit
    wait 1 irq 2
    ; perform ss-bit pause (for stop-bit of message)
    set x, 27 [13] ; one less loop (28 rather than 29) to incorporate the cost of the 'set' instruction
additional_stop_bit_pause:
    jmp x--, additional_stop_bit_pause [13] ; 38kHz cycle lasts 14 instructions - 'jmp' is 1, other 13 are pause
    set pins,0
""")

class LPFMessage:
    def __init__(self, toggleBit, escapeBit, channel, mode, data):
        self.toggleBit = toggleBit
        self.escapeBit = escapeBit
        self.channel = channel
        self.mode = mode
        self.data = data

    def asBinary(self):
        payloadNibbles = [
            (self.toggleBit << 3) + (self.escapeBit << 2) + self.channel, # TECC
            self.mode,                                                    # aMMM - 'a' was never used
            self.data
        ]
        # LRC LLLL xxxx = 0xF xor Nibble 1 xor Nibble 2 xor Nibble 3 
        lrc = 0xF ^ payloadNibbles[0] ^ payloadNibbles[1] ^ payloadNibbles[2] # functools.reduce not currently available
        return array.array('H', [(payloadNibbles[0] << 12) + (payloadNibbles[1] << 8) + (payloadNibbles[2] << 4) + lrc])


class LPFTransmitter:

    def __init__(self, pin):
        fre = round(125000000/(1645/7))
        StateMachine(beginBitTransmissionAssembled, frequency=fre, first_set_pin=pin)
        self._sm = StateMachine(controllerLoopAssembled, frequency=fre, first_set_pin=board.GP1)
        print("real frequency", self._sm.frequency)
        # self._sm.active(1)

    def transmit(self, lpfMessage):
        self._sm.write(lpfMessage.asBinary())


class LPFController:
    def __init__(self, transmitter):
        self.toggleBit = 0
        self.transmitter = transmitter

    def send(self, channel, command):
        message = LPFMessage(self.toggleBit,command.escapeBit,channel,command.mode,command.data)
        transmitter.transmit(message)

class PFOutput:
  Red = 0
  Blue = 1
  
class PWM:
    Float = 0
    BrakeThenFloat = 8
    Forward = list(range(0, 8)) # Value at index 0 not used
    Backward = list(range(16, 8, -1)) # Value at index 0 not used

    modeBit = 0

    def __init__(self, data):
        self.data = data

class SingleOutputCommand:
    escapeBit = 0

    def __init__(self, output, singleModeData):
        self.output = output
        self.data = singleModeData.data
        self.mode = (1 << 2) + (singleModeData.modeBit << 1) + output


transmitter = LPFTransmitter(board.GP0)
# transmitter.transmit(LPFMessage(0,0,0,0,0))
controller = LPFController(transmitter)

controller.send(channel = 0, command = SingleOutputCommand(PFOutput.Red, PWM(PWM.Forward[7])))



treasurePassphrases = TreasurePassphrases([None,"I guess you had to be there..."])

fakeTime = time.time()
while True:
    print(f'passphrase = {treasurePassphrases.passphraseFor(fakeTime)}')
    fakeTime += 1
    time.sleep(0.1)