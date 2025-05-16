class main:
    def __init__(self,arg1,arg2):
        self.arg1 = arg1
        self.arg2 = arg2

    def one(self):
        print(self.arg1 + self.arg2)
    def two(self):
        print(self.arg1 * self.arg2)
    def three(self):
        print(self.arg1 // self.arg2)


main = main(1,2)
main.one()
main.two()
main.three()