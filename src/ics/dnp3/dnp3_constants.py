#!/usr/bin/env python3
"""
ShadowForge Toolkit - ICS/OT Edition
DNP3 Constants

Protocol constants for DNP3 link layer, function codes, and object groups.
"""

# DNP3 Link Layer Start Bytes
DNP3_START_BYTES = b"\x05\x64"

# Common DNP3 Function Codes
class FunctionCode:
    CONFIRM = 0x00
    READ = 0x01
    WRITE = 0x02
    SELECT = 0x03
    OPERATE = 0x04
    DIRECT_OPERATE = 0x05
    DIRECT_OPERATE_NR = 0x06
    RESPONSE = 0x81
    UNSOLICITED_RESPONSE = 0x82

# Common DNP3 Object Groups
class ObjectGroup:
    BINARY_INPUT = 1
    BINARY_INPUT_EVENT = 2
    DOUBLE_BIT_BINARY_INPUT = 3
    DOUBLE_BIT_BINARY_INPUT_EVENT = 4
    BINARY_OUTPUT = 10
    BINARY_OUTPUT_EVENT = 11
    BINARY_COMMAND = 12
    BINARY_OUTPUT_COMMAND_EVENT = 13
    COUNTER = 20
    COUNTER_EVENT = 22
    FROZEN_COUNTER = 21
    FROZEN_COUNTER_EVENT = 23
    ANALOG_INPUT = 30
    ANALOG_INPUT_EVENT = 32
    ANALOG_OUTPUT_STATUS = 40
    ANALOG_OUTPUT_COMMAND_EVENT = 43
    ANALOG_OUTPUT = 41
    TIME_AND_DATE = 50
    CLASS_0_DATA = 60
    CLASS_1_DATA = 61
    CLASS_2_DATA = 62
    CLASS_3_DATA = 63
    DEVICE_IDENTIFICATION = 80

# Common DNP3 Object Variations (examples)
class Variation:
    # Group 1 (Binary Input)
    BIN_PACKED_FORMAT = 1
    BIN_WITH_FLAGS = 2

    # Group 30 (Analog Input)
    ANALOG_32BIT = 1
    ANALOG_16BIT = 2
    ANALOG_FLOAT = 5

    # Group 40 (Analog Output Status)
    ANALOG_OUTPUT_32BIT = 1
    ANALOG_OUTPUT_16BIT = 2


# Common Internal Indications (IIN) bits
class InternalIndication:
    BROADCAST = 0x0001
    CLASS_1_EVENTS = 0x0002
    CLASS_2_EVENTS = 0x0004
    CLASS_3_EVENTS = 0x0008
    NEED_TIME = 0x0010
    LOCAL_CONTROL = 0x0020
    DEVICE_TROUBLE = 0x0040
    DEVICE_RESTART = 0x0080
    FUNCTION_NOT_SUPPORTED = 0x0100
    OBJECT_UNKNOWN = 0x0200
    PARAMETER_ERROR = 0x0400
    EVENT_BUFFER_OVERFLOW = 0x0800
    ALREADY_EXECUTING = 0x1000
    CONFIG_CORRUPT = 0x2000
    RESERVED_1 = 0x4000
    RESERVED_2 = 0x8000


if __name__ == "__main__":
    print("DNP3 Constants loaded")
    print(f"Example: Read Function Code = {FunctionCode.READ}")
    print(f"Example: Analog Input Group = {ObjectGroup.ANALOG_INPUT}")