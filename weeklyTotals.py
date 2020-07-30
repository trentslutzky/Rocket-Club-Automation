import datetime

def main():
    t = datetime.datetime.now()
    print(t.strftime("%Y")+t.strftime("%W"))




if __name__ == '__main__':
    main()