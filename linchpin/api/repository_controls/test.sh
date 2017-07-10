#!/bin/bash

echo "Test 1: linchpin fetch <type> https://github.com/agharibi/SampleLinchpinDirectory ."
linchpin fetch workspace https://github.com/agharibi/SampleLinchpinDirectory .
linchpin fetch layout https://github.com/agharibi/SampleLinchpinDirectory .
linchpin fetch topology https://github.com/agharibi/SampleLinchpinDirectory .
linchpin fetch hooks https://github.com/agharibi/SampleLinchpinDirectory .
linchpin fetch credentials https://github.com/agharibi/SampleLinchpinDirectory .
linchpin fetch PinFile https://github.com/agharibi/SampleLinchpinDirectory .

echo -e "\nTest 2: linchpin fetch <type> 
        https://github.com/agharibi/SampleLinchpinDirectory/hello/bob/coolthings/stuff ."
linchpin fetch workspace \
    https://github.com/agharibi/SampleLinchpinDirectory/hello/bob/coolthings/stuff .
linchpin fetch layout \
    https://github.com/agharibi/SampleLinchpinDirectory/hello/bob/coolthings/stuff .
linchpin fetch topology \
    https://github.com/agharibi/SampleLinchpinDirectory/hello/bob/coolthings/stuff .
linchpin fetch hooks \
    https://github.com/agharibi/SampleLinchpinDirectory/hello/bob/coolthings/stuff .
linchpin fetch credentials \
    https://github.com/agharibi/SampleLinchpinDirectory/hello/bob/coolthings/stuff .
linchpin fetch PinFile \
    https://github.com/agharibi/SampleLinchpinDirectory/hello/bob/coolthings/stuff .

echo -e "\nTest 3: linchpin fetch <type> 
        https://github.com/agharibi/SampleLinchpinDirectory/hello/bob/coolthings/stuff/ ."
echo -e "\nPeep the slash\n"
linchpin fetch workspace \
    https://github.com/agharibi/SampleLinchpinDirectory/hello/bob/coolthings/stuff/ .
linchpin fetch layout \
    https://github.com/agharibi/SampleLinchpinDirectory/hello/bob/coolthings/stuff/ .
linchpin fetch topology \
    https://github.com/agharibi/SampleLinchpinDirectory/hello/bob/coolthings/stuff/ .
linchpin fetch hooks \
    https://github.com/agharibi/SampleLinchpinDirectory/hello/bob/coolthings/stuff/ .
linchpin fetch credentials \
    https://github.com/agharibi/SampleLinchpinDirectory/hello/bob/coolthings/stuff/ .
linchpin fetch PinFile \
    https://github.com/agharibi/SampleLinchpinDirectory/hello/bob/coolthings/stuff/ .

echo -e "\nTest 3: linchpin fetch <type> 
        github.com/agharibi/SampleLinchpinDirectory/hello/bob/coolthings/stuff/ ."
linchpin fetch workspace \
    github.com/agharibi/SampleLinchpinDirectory/hello/bob/coolthings/stuff/ .
linchpin fetch layout \
    github.com/agharibi/SampleLinchpinDirectory/hello/bob/coolthings/stuff/ .
linchpin fetch topology \
    github.com/agharibi/SampleLinchpinDirectory/hello/bob/coolthings/stuff/ .
linchpin fetch hooks \
    github.com/agharibi/SampleLinchpinDirectory/hello/bob/coolthings/stuff/ .
linchpin fetch credentials\
    github.com/agharibi/SampleLinchpinDirectory/hello/bob/coolthings/stuff/ .
linchpin fetch PinFile \
    github.com/agharibi/SampleLinchpinDirectory/hello/bob/coolthings/stuff/ .
