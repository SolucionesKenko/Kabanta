from itertools import cycle
list = [1,2,3,4,5,6,7,8,9]
coun = 0
SequenceEnd = len(list)
SequenceStart = 0
SequenceRepeation = 0

while(1):
    
    coun = coun + 1
    listbuffer =cycle(list)
    for output in listbuffer:
        print(output)
        if(SequenceStart == SequenceEnd-1):
         
            if(SequenceRepeation>= 2):
                break
            else:
                SequenceRepeation+= 1
                SequenceStart = 0
                print("\n")
        else:
            SequenceStart+= 1
    if coun == 100:
        break