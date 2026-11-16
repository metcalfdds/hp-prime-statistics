#!/usr/bin/env python3
"""patch_hpprime.py IN.exe OUT.exe -- make the HP Prime Virtual Calculator 2.4.2 (build 2026-09-09) start under Wine.

At start the emulator looks for a Connectivity Kit through Windows' device enumeration (WinRT DeviceInformation.CreateWatcher)
with a filter on System.Devices.Dnssd.* and nine requested properties.  Wine's property system (propsys, Wine 11.21 and
11.22) knows none of the Dnssd names, CreateWatcher fails, and the emulator's C++ exception ends it (exit code 3) before a
window opens.  This changes ONLY the names used by that search, each in place and at its own length:
  - the filter's text becomes  System.ItemNameDisplay:="  (padded in front with spaces), so the search asks for a device
    named _hpconnkit._tcp and finds none;
  - each of the nine requested property names becomes System.ItemNameDisplay, padded with NULs (Wine reads the name as a
    NUL-terminated string).
Nothing else in the file changes.  The search for a Connectivity Kit then finds nothing, which is all the cloud needs: files
go in and out through the calculator's own folder.  The patched file is HP's program and is never committed.
"""
import sys
src, dst = sys.argv[1], sys.argv[2]
d = bytearray(open(src, 'rb').read())
FILT = (b'System.Devices.AepService.ProtocolId:={4526e8c1-8aac-4153-9b16-55e86ada0e54} AND '
        b'System.Devices.Dnssd.Domain:="local" AND System.Devices.Dnssd.ServiceName:="')
assert d.count(FILT) == 1, 'the filter was not found exactly once: another build?'
new = b'System.ItemNameDisplay:="'
i = d.index(FILT)
d[i:i + len(FILT)] = b' ' * (len(FILT) - len(new)) + new
NAMES = ['System.Devices.Dnssd.ServiceName', 'System.Devices.Dnssd.HostName', 'System.Devices.IpAddress',
         'System.Devices.Dnssd.PortNumber', 'System.Devices.Dnssd.InstanceName', 'System.Devices.Dnssd.Domain',
         'System.Devices.Dnssd.FullName', 'System.Devices.Dnssd.NetworkAdapterId', 'System.Devices.Dnssd.TextAttributes']
rep = 'System.ItemNameDisplay'
for nm in NAMES:
    old = nm.encode('utf-16-le') + b'\0\0'
    assert d.count(old) == 1, nm + ' was not found exactly once'
    j = d.index(old)
    new = (rep + '\0' * (len(nm) - len(rep))).encode('utf-16-le') + b'\0\0'
    assert len(new) == len(old)
    d[j:j + len(old)] = new
open(dst, 'wb').write(d)
print('patched: the filter and %d property names; %d bytes' % (len(NAMES), len(d)))
