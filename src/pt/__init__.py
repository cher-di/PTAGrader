import os
import platform

PT_HOME = os.getenv('PT7HOME')
if not PT_HOME:
    raise Exception(f'Can not find Packet Tracer binaries')

PT_BIN_ROOT = os.path.join(PT_HOME, 'bin')

if platform.system() == 'Windows':
    PT_EXECUTABLE = os.path.join(PT_BIN_ROOT, 'PacketTracer7.exe')
elif platform.system() == 'Linux':
    PT_EXECUTABLE = os.path.join(PT_BIN_ROOT, 'PacketTracer7')
else:
    raise Exception(f'Unsupported OS: {platform.system()}')

PT_EXTENSIONS_ROOT = os.path.join(PT_HOME, 'extensions')
PTA_GRADER_ROOT = os.path.join(PT_EXTENSIONS_ROOT, 'PTAGrader')
PT_GRADER = os.path.join(PTA_GRADER_ROOT, 'Grader.jar')
