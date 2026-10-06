from pymodbus import client as pymodbus_client

# EM530 modbus registers (see manual, table 4.1)
# format: [("KEY", ADDR, "UNIT", FACTOR, "TYPE")]
# byte order MSB, word order LSW

fields = [
    # voltages
    ("V_L1_N", 0x0000, "V", 10, "INT32"),
    ("V_L2_N", 0x0002, "V", 10, "INT32"),
    ("V_L3_N", 0x0004, "V", 10, "INT32"),
    ("V_L1_L2", 0x0006, "V", 10, "INT32"),
    ("V_L2_L3", 0x0008, "V", 10, "INT32"),
    ("V_L3_L1", 0x000A, "V", 10, "INT32"),

    # currents
    ("A_L1", 0x000C, "A", 1000, "INT32"),
    ("A_L2", 0x000E, "A", 1000, "INT32"),
    ("A_L3", 0x0010, "A", 1000, "INT32"),

    # power
    ("W_L1", 0x0012, "W", 10, "INT32"),
    ("W_L2", 0x0014, "W", 10, "INT32"),
    ("W_L3", 0x0016, "W", 10, "INT32"),

    # VA
    ("VA_L1", 0x0018, "VA", 10, "INT32"),
    ("VA_L2", 0x001A, "VA", 10, "INT32"),
    ("VA_L3", 0x001C, "VA", 10, "INT32"),

    # VAR
    ("VAR_L1", 0x001E, "VAR", 10, "INT32"),
    ("VAR_L2", 0x0020, "VAR", 10, "INT32"),
    ("VAR_L3", 0x0022, "VAR", 10, "INT32"),

    # SYS
    ("V_L_N_SYS", 0x0024, "V", 10, "INT32"),
    ("V_L_L_SYS", 0x0026, "V", 10, "INT32"),
    ("W_SYS", 0x0028, "W", 10, "INT32"),
    ("VA_SYS", 0x002A, "VA", 10, "INT32"),
    ("VAR_SYS", 0x002C, "VAR", 10, "INT32"),

    # PF, phase, frequency
    ("PF_L1", 0x002E, "PF", 1000, "INT16"),
    ("PF_L2", 0x002F, "PF", 1000, "INT16"),
    ("PF_L3", 0x0030, "PF", 1000, "INT16"),
    ("PF_SYS", 0x0031, "PF", 1000, "INT16"),
    ("PHASE_SEQ", 0x0032, "SEQ", 1, "INT16"), # value -1 means "L1-L3-L2", value 1 means "L1-L2-L3"
    ("HZ", 0x0033, "Hz", 10, "INT16"),

    # kWh, kVarh
    ("KWH_TOT", 0x0034, "kWh", 10, "INT32"),
    ("KVARH_TOT", 0x0036, "kVarh", 10, "INT32"),
    ("W_SYS_DMD", 0x0038, "W", 10, "INT32"),
    ("W_SYS_DMD_MAX", 0x003A, "W", 10, "INT32"),
    ("KWH_PARTIAL", 0x003C, "kWh", 10, "INT32"),
    ("KVARH_PARTIAL", 0x003E, "kVarh", 10, "INT32"),
    ("KWH_L1", 0x0040, "kWh", 10, "INT32"),
    ("KWH_L2", 0x0042, "kWh", 10, "INT32"),
    ("KWH_L3", 0x0044, "kWh", 10, "INT32"),
    ("KWH_T1", 0x0046, "kWh", 10, "INT32"),
    ("KWH_T2", 0x0048, "kWh", 10, "INT32"),
    # note: 2 empty 32bit registers here
    ("KWH_TOT_EXPORT", 0x004E, "kWh", 10, "INT32"),
    ("KVARH_TOT_EXPORT", 0x0050, "kVarh", 10, "INT32"),
    ("KWH_PARTIAL_EXPORT", 0x0052, "kWh", 10, "INT32"),
    ("KVARH_PARTIAL_EXPORT", 0x0054, "kVarh", 10, "INT32"),
    ("KVAH_TOT", 0x0056, "kVAh", 10, "INT32"),
    ("KVAH_PARTIAL", 0x0058, "kVAh", 10, "INT32"),

    # run hour meter
    ("RUN_HOUR_METER", 0x005A, "h", 100, "INT32"),
    ("RUN_HOUR_METER_KWH_EXPORT", 0x005C, "h", 100, "INT32"),
    # note: 8 empty 32bit registers here
    ("RUN_HOUR_METER_PARTIAL", 0x006E, "h", 100, "INT32"),
    ("RUN_HOUR_METER_KWH_EXPORT_PARTIAL", 0x0070, "h", 100, "INT32"),

    # PF something
    ("PF_L1_LEAD_LAG", 0x0072, "PF", 1000, "INT16"), # negative values mean lead (C), positive values mean lag (L)
    ("PF_L2_LEAD_LAG", 0x0073, "PF", 1000, "INT16"),
    ("PF_L3_LEAD_LAG", 0x0074, "PF", 1000, "INT16"),
    ("PF_SYS_LEAD_LAG", 0x0075, "PF", 1000, "INT16"),

    # inductive/capacitive load
    ("L1_LOAD_LC", 0x0076, "LOAD_LC", 1, "INT16"), # value 1 means inductive (L), value -1 means capacitive (C)
    ("L2_LOAD_LC", 0x0077, "LOAD_LC", 1, "INT16"),
    ("L3_LOAD_LC", 0x0078, "LOAD_LC", 1, "INT16"),
    ("SYS_LOAD_LC", 0x0079, "LOAD_LC", 1, "INT16"),

    # note: 4 empty 32bit registers here

    # THD, DMD and whatnot (don't ask)
    ("THD_A_L1", 0x0082, "%", 100, "INT32"),
    ("THD_A_L2", 0x0084, "%", 100, "INT32"),
    ("THD_A_L3", 0x0086, "%", 100, "INT32"),
    # note: 1 empty 32bit register here
    ("THD_V_L1_N", 0x008A, "%", 100, "INT32"),
    ("THD_V_L2_N", 0x008C, "%", 100, "INT32"),
    ("THD_V_L3_N", 0x008E, "%", 100, "INT32"),
    # note: 1 empty 32bit register here
    ("THD_V_L1_L2", 0x0092, "%", 100, "INT32"),
    ("THD_V_L2_L3", 0x0094, "%", 100, "INT32"),
    ("THD_V_L3_L1", 0x0096, "%", 100, "INT32"),
    ("An", 0x0098, "A", 1000, "INT32"),
    ("DMD_L1", 0x009A, "A", 1000, "INT32"),
    ("DMD_L2", 0x009C, "A", 1000, "INT32"),
    ("DMD_L3", 0x009E, "A", 1000, "INT32"),
    ("DMD_MAX_L1", 0x00A0, "A", 1000, "INT32"),
    ("DMD_MAX_L2", 0x00A2, "A", 1000, "INT32"),
    ("DMD_MAX_L3", 0x00A4, "A", 1000, "INT32"),
    # note: 3 empty 32bit registers here
    ("DMD_W_L1", 0x00AC, "W", 10, "INT32"),
    ("DMD_W_L2", 0x00AE, "W", 10, "INT32"),
    ("DMD_W_L3", 0x00B0, "W", 10, "INT32"),
    ("DMD_W_MAX_L1", 0x00B2, "W", 10, "INT32"),
    ("DMD_W_MAX_L2", 0x00B4, "W", 10, "INT32"),
    ("DMD_W_MAX_L3", 0x00B6, "W", 10, "INT32"),
    # note: 3 empty 32bit registers here
    ("DMD_W_SYS", 0x00BE, "W", 10, "INT32"),
    ("DMD_W_MAX_SYS", 0x00C0, "W", 10, "INT32"),
    # note: 10 empty 32bit registers here
    ("DMD_VA", 0x00D6, "VA", 10, "INT32"),
    ("DMD_VA_MAX", 0x00D8, "VA", 10, "INT32")

]

def read_data(opts={"mb_client":None}):
    
    mb_client:pymodbus_client.ModbusSerialClient = opts["mb_client"]

    if mb_client == None:
        print("read_data: client is None")
        return None

    print("modbus - read_data")

    # max 125 registers at a time, so two reads needed
    result1 = mb_client.read_holding_registers(address=0, count=120).registers
    result2 = mb_client.read_holding_registers(address=120, count=98).registers

    # combine
    result = result1 + result2

    # result should now have 218 registers (16bit)
    # parse values as per "fields" above
    data = {}
    for field in fields:
        tag = field[0]
        addr = field[1]
        unit = field[2]
        mult = field[3]
        type = field[4]

        if type == "INT16":
            val = float(int(result[addr]) / mult)

            # keys as "TAG(UNIT)"
            data[f"{tag}({unit})"] = val

        if type == "INT32":
            # LOGIK!
            # 1. shift lower word 16 bits to the left
            # 2. just handle the higher word as 32bit int
            # 3. OR them together
            # the EM530 manual states "LSW -> MSW", so lower is [addr + 1] (maybe)
            # (0xD8 (216 dec) is the last address, so [addr + 1] should be fine)
            lower = int(int(result[addr + 1]) << 16)
            higher = int(int(result[addr]))
            val = float(int(higher | lower) / mult)

            # keys as "TAG(UNIT)"
            data[f"{tag}({unit})"] = val

    return data
