import storage
storage.remount('/', readonly=False)



with open("boot_out.txt", "w") as bootlog:
    bootlog.write("booted")