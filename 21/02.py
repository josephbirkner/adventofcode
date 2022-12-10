x = 0
y = 0
aim = 0
with open("02.data", 'r') as f:
    for command_and_arg in f:
        command, arg = command_and_arg.strip().split(" ")
        arg_n = int(arg)
        if command == "up":
            aim -= arg_n
        elif command == "down":
            aim += arg_n
        elif command == "forward":
            x += arg_n
            y += aim * arg_n
            assert y >= 0
        else:
            print("ERROR: Command is", command, arg)
            exit(1)
print(x*y)
