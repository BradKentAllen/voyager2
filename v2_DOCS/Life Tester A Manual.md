# Life Tester A Manual

These instructions augment:

1. Voyager2 guide
2. Voyager_setup guide



### UI

flashing green:  normal operation

flashing red:  fault, all gpio should be stopped

two blue:  keyboard interrupt has stopped function



### SSH interface

```
ssh tester@192.168.1.6
password:  hawk

# view the log:
tail ./data/log	  # this shows last 10 lines
cat ./data/log	  # this shows the entire file

# modify the stored cycles (modify then save with ctl-X and "Y")
nano ./data/life_cycles

```

