'''
Registers from the TMC2209 datasheet:
'''
# ===== TMC2209 register set =====


REGISTORS = {

    # GENERAL CONFIGURATION REGISTERS

    "GCONF" : 0x00,     # RW
    "GSTAT" : 0x01,      # R+WC
    "IFCNT" : 0x02,      # R
    "NODECONF" : 0x03,   # W
    "OTP_PROG" : 0x04,    # W
    "OTP_READ" : 0x05,   # W
    "IOIN"  :  0x06,     # R
    "FACTORY_CONF"  : 0x07,    # RW


    # Velocity Dependent Control

    "IHOLD_IRUN" : 0x10,    # W
    "TPOWERDOWN" : 0x11,    # W
    "TSTEP" : 0x12,         # R
    "TPWMTHRS" : 0x13,      # R
    "VACTUAL" : 0x22,       # W

    #  StallGuard Control

    "TCOOLTHRS": 0x14,   # W
    "SGTHRS":  0x40,     # W
    "SG_RESULT": 0x12,   # R
    "COOLCONF": 0x22,    # W

    # Sequencer Registers

    "MSCNT": 0x6A,  # R
    "MSCURACT": 0x6B,  # R

    # Chopper Control Registers

    "CHOPCONF": 0x6C,  # RW
    "DRV_STATUS": 0x6F,  # R
    "PWMCONF": 0x70,  # RW
    "PWM_SCALE": 0x71,  # R
    "PWM_AUTO": 0x72,  # R

    }